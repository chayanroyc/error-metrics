import glob
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib

import numpy as np

from matplotlib import font_manager

font_dirs = ['/glade/u/home/chayan/myutils/extras/ttf/']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

# set font
plt.rcParams['font.family'] = 'Inter'


import sys

sys.path.append('/glade/u/home/chayan/myutils/')

import errormetrics as em

import sys

sys.path.append('/glade/u/home/chayan/myutils/')

import errormetrics as em

import numpy as np
from numpy.linalg import inv, det

alldata = pd.read_feather('./alldata_new.feather')

cols = ['BC_3D_AR1',
 'BC_3D_AR2',
 'BC_3D_AR3',
 'BC_3D_AR4',
 'BC_3D_AR5',
 'BC_3D_AR6',
 'BC_3D_AR7',
 'BC_3D_AR8',
 'BC_3D_AR9',
 'BC_3D_AR10',
 'BC_3D_BB',
 'BC_3D_BDRES',
       ]

len(cols)

alldata['BC_3D_BDRES'] = alldata['BC_3D_BDY'] + alldata['BC_3D_RES']

data_sources = ['C14', 'RS','G20'] #APCC

def return_Gd(df, sources = data_sources):

    df = df.query('SOURCE == @sources')
    G1 = df[
  cols
    ].values
    d = df['BC_OBS'].values.reshape(-1,1)
    G = G1.copy()

    assert d.shape[0] == G.shape[0]

    return G,d

import numpy as np
from numpy.linalg import inv, det

def calculate_nrss(y, yhat, sigma):
    """
    Normalized Residual Sum-of-Squares (NRSS)
    y     : observed data (vector)
    yhat  : model predictions (vector)
    sigma : data uncertainties (vector)
    """
    return np.sum((y - yhat)**2) / np.sum(sigma**2)

def calculate_reduced_chi2(y, yhat, sigma, num_params):
    """
    Reduced Chi-Squared Statistic.
    num_params : number of fitted parameters
    """
    N = len(y)
    chi2 = np.sum(((y - yhat) / sigma)**2)
    return chi2 / (N - num_params)

def calculate_posterior_covariance(K, Se, Sa):
    """
    Posterior error covariance matrix:
    S_posterior = (K^T Se^-1 K + Sa^-1)^-1
    K  : Jacobian matrix
    Se : Observation error covariance matrix
    Sa : Prior error covariance matrix
    """
    return inv(K.T @ inv(Se) @ K + inv(Sa))

def calculate_averaging_kernel(K, Se, Sa):
    """
    Averaging Kernel (Resolution Matrix):
    A = (K^T Se^-1 K + Sa^-1)^-1 K^T Se^-1 K
    """
    posterior = calculate_posterior_covariance(K, Se, Sa)
    return posterior @ (K.T @ inv(Se) @ K)

def calculate_dfs(A):
    """
    Degrees of Freedom for Signal (DFS):
    DFS = trace(A)
    """
    return np.trace(A)

def calculate_shannon_info(Sa, S_posterior):
    """
    Shannon Information Content:
    H = 0.5 * ln(|Sa| / |S_posterior|)
    """
    return 0.5 * np.log(det(Sa) / det(S_posterior))

def student_t_cost_and_grad(m, G, d_obs, sigma, nu, Cm_inv, m_prior):
    """
    Returns cost J_obs (Student-t), gradient, and residuals.
    """
    m = m.reshape(-1, 1)
    r = (d_obs - G @ m).ravel()                # residual vector
    s2 = sigma.ravel() ** 2                    # variance per obs

    # ----- Student-t negative log-likelihood ------------------
    one_plus = 1 + (r**2) / (nu * s2)
    J_obs = 0.5 * (nu + 1) * np.log(one_plus).sum()

    # weights for gradient (w_i * r_i)
    w = (nu + 1) / (nu * s2 + r**2)
    grad_obs = -G.T @ (w * r).reshape(-1, 1)   # minus sign → descent dir

    return J_obs, grad_obs, r

import numpy as np
from scipy.optimize import minimize, NonlinearConstraint
import scipy.linalg as SLA


def constrained_bayesian_inversion(
        G, d_obs, m_prior, Cd, Cm,
        lambda_reg=1.0,        # keep, but you will not tune it any more
        optimizer='SLSQP',
        verbose=True,):
    """
    Solve linear Bayesian inversion and **diagnose χ² statistics**.
    The function now returns:
        J_obs   – observation misfit part
        J_prior – prior part
    so that the Optuna objective can push them toward their expected DOF.
    """
    # --- reshape & pre-compute inverses ------------------------------------
    m_prior = np.asarray(m_prior).reshape(-1, 1)
    Cd_inv  = SLA.pinv(Cd)
    Cm_inv  = SLA.pinv(Cm)

    num_obs = d_obs.size
    num_params = m_prior.size

    # --- cost, grad, hess ---------------------------------------------------
    def cost_function(m):
        m = m.reshape(-1, 1)
        innov = d_obs - G @ m
        reg   = m - m_prior
        return 0.5 * (innov.T @ Cd_inv @ innov
                      + lambda_reg * reg.T @ Cm_inv @ reg).squeeze()

    def jac(m):
        m = m.reshape(-1, 1)
        return (G.T @ Cd_inv @ (G @ m - d_obs)
                + Cm_inv @ (m - m_prior)).ravel()

    def hess(_):
        return G.T @ Cd_inv @ G + Cm_inv

    # --- Kalman gain & averaging kernel (unchanged) -------------------------
    gain = Cm @ G.T @ SLA.pinv(G @ Cm @ G.T + Cd)
    avgK = gain @ G
    effective_params = np.trace(avgK)

    # --- nonlinear constraint on diag(A) ------------------------------------
    def ak_constraint(m):
        return np.diag(avgK) - 0.2          # keep your 0.2 floor
    nonlinear_constraint = NonlinearConstraint(ak_constraint, 0, np.inf)

    # --- optimisation -------------------------------------------------------
    bounds = [(0.25, None)] * m_prior.size

    bounds[0] = (0.8, None)
    bounds[2] = (0.8, None)
        
    result = minimize(
        cost_function, m_prior.ravel(), method=optimizer,
        jac=jac, hess=hess if optimizer == 'trust-constr' else None,
        bounds=bounds, constraints=nonlinear_constraint
    )
    
    mhat = result.x.reshape(-1, 1)

    # --- posterior covariance & residuals -----------------------------------
    Cm_hat = Cm - gain @ G @ Cm
    resid  = d_obs - G @ mhat

    # ------------------------------------------------------------------------
    # χ² diagnostics you asked for
    J_obs   = float(resid.T @ Cd_inv @ resid)               # scalar
    J_prior = float((mhat - m_prior).T @ Cm_inv @ (mhat - m_prior))

    # everything below is unchanged bookkeeping ------------------------------
    sigma   = np.sqrt(np.diag(Cd)).reshape(-1, 1)
    nrss    = np.sum(resid**2) / np.sum(sigma**2)
    chi2_red = J_obs / max(d_obs.size - effective_params, 1)

    sign_prior, logdet_prior = np.linalg.slogdet(Cm)
    sign_post,  logdet_post  = np.linalg.slogdet(Cm_hat)
    shannon_info = 0.5 * (logdet_prior - logdet_post) if sign_prior > 0 and sign_post > 0 else np.nan

    # ------------------------------------------------------------------ OBJECTIVE
    # Push χ²_obs / N_obs  and χ²_prior / N_par toward 1; penalise their distance.
    loss = (abs(J_obs   / d.size         - 1.0) +
            abs(J_prior / m_prior.size   - 1.0))

    predictions_posterior = G @ mhat
    predictions_prior = G @ m_prior

    metrics_posterior = em.ErrorMetrics(predictions = predictions_posterior, observations = d).get_metrics(['RNP'])['RNP']
    metrics_prior = em.ErrorMetrics(predictions = predictions_prior, observations = d).get_metrics(['RNP'])['RNP']

    results = dict(
        num_observations = num_obs,
        num_state_parameters =  num_params,
        posterior_mean       = mhat,
        posterior_cov_diag   = np.diag(Cm_hat),
        J_obs                = J_obs,
        J_prior              = J_prior,
        chi2_red             = chi2_red,
        nrss                 = nrss,
        effective_num_params = effective_params,
        shannon_information  = shannon_info,
        averaging_kernel     = avgK,
        #gain_matrix          = gain,
        data_resolution = np.trace(gain @ G),
        KGE_prior  = metrics_prior,
        KGE_posterior = metrics_posterior,
        loss = loss
    )
    
    if verbose:
        print(f"χ²_obs / N_obs   = {J_obs   / d_obs.size :6.3f}")
        print(f"χ²_prior / N_par = {J_prior / m_prior.size:6.3f}")
        print(f"Reduced χ²       = {chi2_red:6.3f}")
        print(f"Loss              = {loss:6.3f}"),
    return results


G,d = return_Gd(alldata, sources = ['C14', 'RS', 'G20'])

m_prior = np.ones(G.shape[1]).reshape(-1,1)

# Example data and parameters
Cd = (np.eye(d.size))  # Inverse data covariance matrix, replace with real matrix

Cm = (np.eye(m_prior.size))  # Inverse model covariance matrix, replace with real matrix

print(G.shape, d.shape, m_prior.shape, Cd.shape, Cm.shape)

import sys

sys.path.append('/glade/u/home/chayan/myutils/')

import errormetrics as em

def prepare_inversion(G,d):
    m_prior = np.ones(G.shape[1]).reshape(-1,1)

    # Example data and parameters
    Cd = (np.eye(d.size))  # Inverse data covariance matrix, replace with real matrix
    
    Cm = (np.eye(m_prior.size))  # Inverse model covariance matrix, replace with real matrix

    return m_prior, Cd, Cm

import optuna
import numpy as np
import sqlite3
from optuna.samplers import TPESampler, CmaEsSampler, BaseSampler
from optuna.trial import Trial
from optuna.pruners import BasePruner
import typing
import sqlite3
import time
from joblib import Parallel,delayed

class DuplicateIterationPruner(BasePruner):
    def prune(self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial") -> bool:
        completed_trials = study.get_trials(states=[optuna.trial.TrialState.COMPLETE])
        for completed_trial in completed_trials:
            if completed_trial.params == trial.params:
                return True
        return False

class SwitchingSampler(optuna.samplers.BaseSampler):
    def __init__(self, switch_trial=30, seed=None):
        """
        Custom sampler that switches from TPE to CMA-ES
        
        Args:
            switch_trial (int): Trial number to switch from TPE to CMA-ES
            seed (int): Random seed for reproducibility
        """
        self._tpe = TPESampler(seed=seed, multivariate=True, group=True)
        self._cmaes = CmaEsSampler(seed=seed, consider_pruned_trials=True)
        self._switch_trial = switch_trial
        
    def infer_relative_search_space(self, study, trial):
        """Defines the search space for the trial."""
        if trial.number <= self._switch_trial:
            return self._tpe.infer_relative_search_space(study, trial)
        return self._cmaes.infer_relative_search_space(study, trial)
    
    def sample_relative(self, study, trial, search_space):
        """Samples parameters for the trial."""
        if trial.number <= self._switch_trial:
            return self._tpe.sample_relative(study, trial, search_space)
        return self._cmaes.sample_relative(study, trial, search_space)
    
    def sample_independent(self, study, trial, param_name, param_distribution):
        """Samples independent parameters."""
        if trial.number <= self._switch_trial:
            return self._tpe.sample_independent(study, trial, param_name, param_distribution)
        return self._cmaes.sample_independent(study, trial, param_name, param_distribution)



class MultiplePruners(optuna.pruners.BasePruner):

    def __init__(
        self,
        pruners: typing.Iterable[optuna.pruners.BasePruner],
        pruning_condition: str = "any",
    ) -> None:

        self._pruners = tuple(pruners)

        self._pruning_condition_check_fn = None
        if pruning_condition == "any":
            self._pruning_condition_check_fn = any
        elif pruning_condition == "all":
            self._pruning_condition_check_fn = all
        else:
            raise ValueError(f"Invalid pruning ({pruning_condition}) condition passed!")
        assert self._pruning_condition_check_fn is not None

    def prune(
        self,
        study: optuna.study.Study,
        trial: optuna.trial.FrozenTrial,
    ) -> bool:

         return self._pruning_condition_check_fn(pruner.prune(study, trial) for pruner in self._pruners)



def make_serializable(obj):
    if isinstance(obj, dict):
        return {key: make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, np.bool_):  # <-- Add this line
        return bool(obj)
    return obj


def objective(trial):
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning) 

    #print(f"PID {os.getpid()} running trial {trial.number}")
    
    obs_error = np.round(trial.suggest_float('obs_error', 0.05, 0.9, step=0.05),4)

    prior_error_dict = {}
    for i in range(1, N_PARAMS+1):
        prior_error_dict[f'prior_m_{i}'] = np.round(trial.suggest_float(
            f'prior_m_{i}', 0.05, 3, step=0.05), 4)

    G, d = return_Gd(alldata,  ['C14', 'RS','G20'])

    m_prior, Cd, Cm = prepare_inversion(G, d)

    #########################

    # Multiply all other diagonal elements by c_rest
    for i in range(1, N_PARAMS+1):
        Cm[i-1, i-1] *= (prior_error_dict[f'prior_m_{i}'] * m_prior[i-1]) ** 2

    floor = 0.1 * np.nanmedian(
    np.where(d < np.nanpercentile(d,100), d, np.nan)
    )
    sigmad = np.maximum(obs_error * d.squeeze(), floor)
    #cap = 3*np.nanmedian(d)
    
    #sigmad = np.minimum(sigmad,cap)

    Cd = np.diag(sigmad ** 2)

    inversion_results = constrained_bayesian_inversion(
        G=G, d_obs=d, m_prior=m_prior, Cd=Cd, Cm=Cm, lambda_reg=1, verbose=False)

    # Convert your results dictionary to JSON serializable format
    serialization_results = make_serializable(inversion_results)

    predictions_posterior = G @ inversion_results['posterior_mean']
    predictions_prior = G @ m_prior

    metrics_posterior = em.ErrorMetrics(predictions = predictions_posterior, observations = d).get_metrics(['KGE'])['KGE']
    trial.set_user_attr("KGE_posterior", metrics_posterior)
    
    metrics_prior = em.ErrorMetrics(predictions = predictions_prior, observations = d).get_metrics(['KGE'])['KGE']
    trial.set_user_attr("KGE_prior", metrics_prior)

    if metrics_posterior <= metrics_prior:
        raise optuna.TrialPruned()

    loss = (abs(inversion_results['J_obs']   / d.size         - 1.0) +
            abs(inversion_results['J_prior'] / m_prior.size   - 1.0))

    trial.set_user_attr("results", serialization_results)

    # 2. Soft bias penalty in objective
    mean_resid = float((d - G @ inversion_results['posterior_mean']).mean())
    
    loss += 0.3 * abs(mean_resid) / np.nanstd(d)   # ← new term
    
    return loss


from optuna.storages import RDBStorage

storage = RDBStorage(
    url="postgresql+psycopg2://localhost/optuna",
    engine_kwargs=dict(pool_size=30, max_overflow=0, pool_pre_ping=True),
)

study = optuna.create_study(
    study_name      = "tpe_cmaes_seasonal_cost",
    direction       = "minimize",
    storage         = storage,
    load_if_exists  = True,
    sampler         = SwitchingSampler(switch_trial=1000, seed=5),
    pruner          = MultiplePruners(
        (DuplicateIterationPruner(), optuna.pruners.HyperbandPruner())
    ),
)

study.optimize(objective, n_trials=2000, n_jobs=15, show_progress_bar=True, gc_after_trial=True)



