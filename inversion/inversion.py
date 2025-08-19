import numpy as np
from scipy.optimize import minimize, NonlinearConstraint
import scipy.linalg as SLA

def prepare_inversion(G, d):
    m_prior = np.ones(G.shape[1]).reshape(-1,1)
    Cd = np.eye(d.size)
    prior_error = 1e6
    Cm = np.eye(G.shape[1]) * (prior_error ** 2)
    return m_prior, Cd, Cm

def constrained_bayesian_inversion(G, d_obs, m_prior, Cd, Cm, lambda_reg=1.0, optimizer='SLSQP', verbose=True):
    m_prior = np.asarray(m_prior).reshape(-1, 1)
    Cd_inv  = SLA.pinv(Cd)
    Cm_inv  = SLA.pinv(Cm)
    num_obs = d_obs.size
    num_params = m_prior.size
    def cost_function(m):
        m = m.reshape(-1, 1)
        innov = d_obs - G @ m
        reg   = m - m_prior
        return 0.5 * (innov.T @ Cd_inv @ innov + lambda_reg * reg.T @ Cm_inv @ reg).squeeze()
    def jac(m):
        m = m.reshape(-1, 1)
        return (G.T @ Cd_inv @ (G @ m - d_obs) + Cm_inv @ (m - m_prior)).ravel()
    def hess(_):
        return G.T @ Cd_inv @ G + Cm_inv
    gain = Cm @ G.T @ SLA.pinv(G @ Cm @ G.T + Cd)
    avgK = gain @ G
    effective_params = np.trace(avgK)
    def ak_constraint(m):
        return np.diag(avgK) - 0.2
    nonlinear_constraint = NonlinearConstraint(ak_constraint, 0, np.inf)
    bounds = [(0.1, 5)] * m_prior.size
    bounds[0] = (0.75, 5)
    bounds[2] = (0.75, 5)
    result = minimize(cost_function, m_prior.ravel(), method=optimizer, jac=jac, hess=hess if optimizer == 'trust-constr' else None, bounds=bounds, constraints=nonlinear_constraint)
    mhat = result.x.reshape(-1, 1)
    Cm_hat = Cm - gain @ G @ Cm
    resid  = d_obs - G @ mhat
    J_obs   = float(resid.T @ Cd_inv @ resid)
    J_prior = float((mhat - m_prior).T @ Cm_inv @ (mhat - m_prior))
    sigma   = np.sqrt(np.diag(Cd)).reshape(-1, 1)
    nrss    = np.sum(resid**2) / np.sum(sigma**2)
    chi2_red = J_obs / max(d_obs.size - effective_params, 1)
    sign_prior, logdet_prior = np.linalg.slogdet(Cm)
    sign_post,  logdet_post  = np.linalg.slogdet(Cm_hat)
    shannon_info = 0.5 * (logdet_prior - logdet_post) if sign_prior > 0 and sign_post > 0 else np.nan
    loss = (abs(J_obs   / (d_obs.size - effective_params)         - 1.0) + abs(J_prior / (effective_params)   - 1.0))
    results = dict(
        num_observations = num_obs,
        num_state_parameters =  num_params,
        posterior_mean       = mhat,
        posterior_cov_diag   = np.diag(Cm_hat),
        J_obs                = J_obs,
        J_prior              = J_prior,
        chi2_red             = chi2_red,
        nrss                 = nrss,
        effective_params = effective_params,
        shannon_information  = shannon_info,
        averaging_kernel     = avgK,
        data_resolution = np.diagonal(G @ gain),
        loss = loss
    )
    if verbose:
        print(f"χ²_obs / N_obs   = {J_obs   / d_obs.size :6.3f}")
        print(f"χ²_prior / N_par = {J_prior / m_prior.size:6.3f}")
        print(f"Reduced χ²       = {chi2_red:6.3f}")
        print(f"Loss             = {loss:6.3f}")
    return results 