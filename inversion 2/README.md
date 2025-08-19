# Bayesian Inversion Package

A Python package for performing Bayesian inversion with various optimization strategies and statistical analysis tools.

## Features

- Bayesian inversion with customizable priors
- Multiple optimization strategies (SLSQP, trust-constr)
- Statistical analysis tools
- Visualization capabilities
- Error metrics calculation

## Installation

```bash
pip install -e .
```

## Usage

```python
from inversion.inversion_core import BayesianInversion
import numpy as np

# Initialize inversion
inversion = BayesianInversion(
    G=observation_matrix,
    d_obs=observations,
    m_prior=prior_mean,
    Cd=observation_covariance,
    Cm=prior_covariance
)

# Solve inversion
results = inversion.solve(optimizer='SLSQP')

# Get results
print(results['posterior_mean'])
```

## Components

- `inversion_core.py`: Main inversion class
- `inversion_utils.py`: Utility functions
- `inversion_optimizer.py`: Optimization tools
- `run_inversion.py`: Example script

## Dependencies

- numpy
- pandas
- matplotlib
- scipy
- optuna
- pyarrow 