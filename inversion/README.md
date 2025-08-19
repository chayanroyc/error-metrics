# Bayesian Inversion Framework

This repository contains a modular implementation of a Bayesian inversion framework, originally developed in a Jupyter notebook. The code has been organized into separate modules for better maintainability and reusability.

## Project Structure

```
.
├── data_utils.py      # Data loading and preprocessing utilities
├── matrix_utils.py    # Forward model matrix construction
├── inversion.py       # Core Bayesian inversion logic
├── metrics_utils.py   # Error metrics computation
└── optuna_utils.py    # Custom Optuna samplers and pruners
```

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install numpy scipy pandas optuna
```

## Usage Guide

### 1. Data Loading and Preparation

```python
from data_utils import load_data
from matrix_utils import return_Gd

# Load your data
df = load_data('path_to_your_data.csv')

# Build forward model matrix and observation vector
sources = ['C14', 'RS']  # Specify your source names
G, d = return_Gd(df, sources)
```

### 2. Running the Inversion

```python
from inversion import prepare_inversion, constrained_bayesian_inversion

# Prepare inversion parameters
m_prior, Cd, Cm = prepare_inversion(G, d)

# Run the inversion
results = constrained_bayesian_inversion(
    G, d, m_prior, Cd, Cm,
    lambda_reg=1.0,  # Regularization parameter
    optimizer='SLSQP',  # Optimization method
    verbose=True
)
```

The inversion results include:
- Posterior mean and covariance
- Chi-square statistics
- Effective parameters
- Shannon information
- Averaging kernel
- Data resolution

### 3. Computing Error Metrics

```python
from metrics_utils import compute_metrics

# Compute predictions
predictions = G @ results['posterior_mean']

# Calculate error metrics
metrics = compute_metrics(predictions, d)
```

### 4. Hyperparameter Optimization with Optuna

The `optuna_utils.py` module provides custom samplers and pruners for hyperparameter optimization:

- `SwitchingSampler`: Switches between TPE and CMA-ES samplers
- `DuplicateIterationPruner`: Prunes duplicate trials
- `MultiplePruners`: Combines multiple pruners
- `EarlyStoppingPruner`: Implements early stopping

Example usage:
```python
import optuna
from optuna_utils import SwitchingSampler, EarlyStoppingPruner

# Create a study with custom sampler and pruner
study = optuna.create_study(
    sampler=SwitchingSampler(switch_trial=30),
    pruner=EarlyStoppingPruner(min_trials=10, patience=5)
)

# Define your objective function
def objective(trial):
    lambda_reg = trial.suggest_float('lambda_reg', 0.1, 10.0)
    # ... rest of your optimization logic
    return loss

# Run optimization
study.optimize(objective, n_trials=100)
```

## Key Features

1. **Modular Design**: Each component is isolated in its own module for easy maintenance and testing
2. **Flexible Data Handling**: Customize data loading and preprocessing in `data_utils.py`
3. **Robust Inversion**: Implements constrained Bayesian inversion with various optimization methods
4. **Comprehensive Metrics**: Wrapper for error metrics computation
5. **Advanced Optimization**: Custom Optuna utilities for hyperparameter tuning

## Notes

- The code assumes specific column names in your data (e.g., 'BC_3D_', 'BC_OBS', 'SOURCE'). Adjust these in `matrix_utils.py` if needed.
- The inversion includes constraints on the averaging kernel and parameter bounds.
- Error metrics are computed using a custom `errormetrics` module.

## Contributing

Feel free to submit issues and enhancement requests! 