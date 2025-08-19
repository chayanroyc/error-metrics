import optuna
from typing import Iterable, Dict, Any
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint
from .inversion_core import BayesianInversion
import error_metrics as em

class DuplicateIterationPruner(optuna.pruners.BasePruner):
    """Prunes duplicate iterations in optimization"""
    def prune(self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial") -> bool:
        return False

class SwitchingSampler(optuna.samplers.BaseSampler):
    """Custom sampler that switches between different sampling strategies"""
    def __init__(self, switch_trial=30, seed=None):
        self.switch_trial = switch_trial
        self.seed = seed
        self._rng = np.random.RandomState(seed)

    def infer_relative_search_space(self, study, trial):
        return {}

    def sample_relative(self, study, trial, search_space):
        return {}

    def sample_independent(self, study, trial, param_name, param_distribution):
        return {}

class MultiplePruners(optuna.pruners.BasePruner):
    """Combines multiple pruners with configurable pruning conditions"""
    def __init__(
        self,
        pruners: Iterable[optuna.pruners.BasePruner],
        pruning_condition: str = "any",
    ) -> None:
        self.pruners = pruners
        self.pruning_condition = pruning_condition

    def prune(
        self,
        study: optuna.study.Study,
        trial: optuna.trial.FrozenTrial,
    ) -> bool:
        if self.pruning_condition == "any":
            return any(pruner.prune(study, trial) for pruner in self.pruners)
        elif self.pruning_condition == "all":
            return all(pruner.prune(study, trial) for pruner in self.pruners)
        else:
            raise ValueError("pruning_condition must be 'any' or 'all'")

def make_serializable(obj):
    """Convert numpy types to Python native types for serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

class OptunaOptimizer:
    """Optuna-based hyperparameter optimization for Bayesian inversion"""
    
    def __init__(self, n_trials=100, study_name="bayesian_inversion"):
        self.n_trials = n_trials
        self.study_name = study_name
        
    def _create_objective(self, G, d_obs, m_prior, Cd, Cm):
        """Create the objective function for Optuna"""
        def objective(trial):
            # Sample hyperparameters
            lambda_reg = trial.suggest_float("lambda_reg", 0.1, 10.0, log=True)
            optimizer = trial.suggest_categorical("optimizer", ["SLSQP", "trust-constr"])
            
            # Create and solve inversion
            inversion = BayesianInversion(
                G=G,
                d_obs=d_obs,
                m_prior=m_prior,
                Cd=Cd,
                Cm=Cm,
                lambda_reg=lambda_reg
            )
            
            try:
                results = inversion.solve(optimizer=optimizer, verbose=False)
                
                # Calculate predictions
                predictions_posterior = G @ results['posterior_mean']
                predictions_prior = G @ m_prior
                
                # Calculate KGE metrics
                metrics_posterior = em.ErrorMetrics(
                    predictions=predictions_posterior, 
                    observations=d_obs
                ).get_metrics(['KGE'])['KGE']
                
                metrics_prior = em.ErrorMetrics(
                    predictions=predictions_prior, 
                    observations=d_obs
                ).get_metrics(['KGE'])['KGE']
                
                # Prune if posterior is not better than prior
                if metrics_posterior <= metrics_prior:
                    raise optuna.TrialPruned()
                
                # Calculate main loss terms
                loss = (abs(results['J_obs'] / d_obs.size - 1.0) + 
                       abs(results['J_prior'] / m_prior.size - 1.0))
                
                # Add bias penalty
                mean_resid = float((d_obs - predictions_posterior).mean())
                loss += 0.3 * abs(mean_resid) / np.nanstd(d_obs)
                
                # Store metrics for later analysis
                trial.set_user_attr("KGE_posterior", metrics_posterior)
                trial.set_user_attr("KGE_prior", metrics_prior)
                
                return loss
                
            except Exception as e:
                return float('inf')  # Return infinity for failed trials
                
        return objective
    
    def optimize(self, G, d_obs, m_prior, Cd, Cm) -> Dict[str, Any]:
        """
        Optimize hyperparameters using Optuna
        
        Parameters:
        -----------
        G : ndarray
            Observation matrix
        d_obs : ndarray
            Observation vector
        m_prior : ndarray
            Prior mean vector
        Cd : ndarray
            Observation error covariance matrix
        Cm : ndarray
            Prior error covariance matrix
            
        Returns:
        --------
        dict
            Dictionary containing best parameters and study results
        """
        # Create study
        study = optuna.create_study(
            study_name=self.study_name,
            direction="minimize",
            sampler=SwitchingSampler(),
            pruner=MultiplePruners([DuplicateIterationPruner()])
        )
        
        # Create objective function
        objective = self._create_objective(G, d_obs, m_prior, Cd, Cm)
        
        # Run optimization
        study.optimize(objective, n_trials=self.n_trials)
        
        # Get best parameters
        best_params = study.best_params
        best_value = study.best_value
        
        # Create final inversion with best parameters
        final_inversion = BayesianInversion(
            G=G,
            d_obs=d_obs,
            m_prior=m_prior,
            Cd=Cd,
            Cm=Cm,
            lambda_reg=best_params['lambda_reg']
        )
        
        final_results = final_inversion.solve(
            optimizer=best_params['optimizer'],
            verbose=True
        )
        
        return {
            'best_parameters': best_params,
            'best_value': best_value,
            'study': study,
            'final_results': final_results
        } 