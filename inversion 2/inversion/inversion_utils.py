import numpy as np
from numpy.linalg import inv, det
import scipy.linalg as SLA

def calculate_nrss(y, yhat, sigma):
    """Normalized Residual Sum-of-Squares (NRSS)"""
    return np.sum((y - yhat)**2) / np.sum(sigma**2)

def calculate_reduced_chi2(y, yhat, sigma, num_params):
    """Reduced Chi-Squared Statistic"""
    N = len(y)
    chi2 = np.sum(((y - yhat) / sigma)**2)
    return chi2 / (N - num_params)

def calculate_posterior_covariance(K, Se, Sa):
    """Posterior error covariance matrix"""
    return inv(K.T @ inv(Se) @ K + inv(Sa))

def calculate_averaging_kernel(K, Se, Sa):
    """Averaging Kernel (Resolution Matrix)"""
    posterior = calculate_posterior_covariance(K, Se, Sa)
    return posterior @ (K.T @ inv(Se) @ K)

def calculate_dfs(A):
    """Degrees of Freedom for Signal (DFS)"""
    return np.trace(A)

def calculate_shannon_info(Sa, S_posterior):
    """Shannon Information Content"""
    return 0.5 * np.log(det(Sa) / det(S_posterior))

def student_t_cost_and_grad(m, G, d_obs, sigma, nu, Cm_inv, m_prior):
    """Student-t cost function and gradient"""
    m = m.reshape(-1, 1)
    r = (d_obs - G @ m).ravel()
    s2 = sigma.ravel() ** 2

    one_plus = 1 + (r**2) / (nu * s2)
    J_obs = 0.5 * (nu + 1) * np.log(one_plus).sum()

    w = (nu + 1) / (nu * s2 + r**2)
    grad_obs = -G.T @ (w * r).reshape(-1, 1)

    return J_obs, grad_obs, r 