import numpy as np
import scipy.linalg as SLA
from scipy.optimize import minimize, NonlinearConstraint
from .inversion_utils import (
    calculate_posterior_covariance,
    calculate_averaging_kernel,
    calculate_dfs,
    calculate_shannon_info
)

class BayesianInversion:
    """Main class for performing Bayesian inversion"""
    
    def __init__(self, G, d_obs, m_prior, Cd, Cm, lambda_reg=1.0):
        """
        Initialize the inversion problem
        
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
        lambda_reg : float
            Regularization parameter
        """
        self.G = G
        self.d_obs = d_obs
        self.m_prior = np.asarray(m_prior).reshape(-1, 1)
        self.Cd = Cd
        self.Cm = Cm
        self.lambda_reg = lambda_reg
        
        # Pre-compute inverses
        self.Cd_inv = SLA.pinv(Cd)
        self.Cm_inv = SLA.pinv(Cm)
        
        # Dimensions
        self.num_obs = d_obs.size
        self.num_params = m_prior.size
        
        # Initialize results
        self.results = None

    def _cost_function(self, m):
        """Cost function for optimization"""
        m = m.reshape(-1, 1)
        innov = self.d_obs - self.G @ m
        reg = m - self.m_prior
        return 0.5 * (innov.T @ self.Cd_inv @ innov + 
                     self.lambda_reg * reg.T @ self.Cm_inv @ reg).squeeze()

    def _jacobian(self, m):
        """Jacobian of the cost function"""
        m = m.reshape(-1, 1)
        return (self.G.T @ self.Cd_inv @ (self.G @ m - self.d_obs) +
                self.Cm_inv @ (m - self.m_prior)).ravel()

    def _hessian(self, _):
        """Hessian of the cost function"""
        return self.G.T @ self.Cd_inv @ self.G + self.Cm_inv

    def _setup_constraints(self):
        """Setup optimization constraints"""
        # Calculate Kalman gain and averaging kernel
        gain = self.Cm @ self.G.T @ SLA.pinv(self.G @ self.Cm @ self.G.T + self.Cd)
        self.avgK = gain @ self.G
        
        # Nonlinear constraint on averaging kernel
        def ak_constraint(m):
            return np.diag(self.avgK) - 0.2
        return NonlinearConstraint(ak_constraint, 0, np.inf)

    def solve(self, optimizer='SLSQP', verbose=True):
        """
        Solve the inversion problem
        
        Parameters:
        -----------
        optimizer : str
            Optimization method to use
        verbose : bool
            Whether to print progress information
            
        Returns:
        --------
        dict
            Dictionary containing inversion results
        """
        # Setup constraints
        constraints = self._setup_constraints()
        
        # Setup bounds
        bounds = [(0.25, None)] * self.num_params
        bounds[0] = (0.8, None)  # Special bounds for first parameter
        bounds[2] = (0.8, None)  # Special bounds for third parameter
        
        # Run optimization
        result = minimize(
            self._cost_function,
            self.m_prior.ravel(),
            method=optimizer,
            jac=self._jacobian,
            hess=self._hessian if optimizer == 'trust-constr' else None,
            bounds=bounds,
            constraints=constraints
        )
        
        # Calculate posterior statistics
        mhat = result.x.reshape(-1, 1)
        Cm_hat = self.Cm - self.avgK @ self.G @ self.Cm
        resid = self.d_obs - self.G @ mhat
        
        # Calculate metrics
        J_obs = float(resid.T @ self.Cd_inv @ resid)
        J_prior = float((mhat - self.m_prior).T @ self.Cm_inv @ (mhat - self.m_prior))
        effective_params = np.trace(self.avgK)
        
        # Store results
        self.results = {
            'num_observations': self.num_obs,
            'num_state_parameters': self.num_params,
            'posterior_mean': mhat,
            'posterior_cov_diag': np.diag(Cm_hat),
            'J_obs': J_obs,
            'J_prior': J_prior,
            'chi2_red': J_obs / max(self.num_obs - effective_params, 1),
            'nrss': np.sum(resid**2) / np.sum(np.diag(self.Cd)),
            'effective_num_params': effective_params,
            'shannon_information': calculate_shannon_info(self.Cm, Cm_hat),
            'averaging_kernel': self.avgK,
            'data_resolution': np.trace(self.avgK),
            'optimization_success': result.success,
            'optimization_message': result.message
        }
        
        return self.results

    def get_results(self):
        """Return the inversion results"""
        if self.results is None:
            raise ValueError("Inversion has not been solved yet. Call solve() first.")
        return self.results 