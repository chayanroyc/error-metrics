import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from inversion.inversion_core import BayesianInversion
from inversion.inversion_optimizer import OptunaOptimizer
import errormetrics as em

def load_data(filepath='./alldata_new.feather'):
    """Load and prepare the data"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    # Load data
    alldata = pd.read_feather(filepath)
    
    # Define columns
    cols = [
        'BC_3D_AR1', 'BC_3D_AR2', 'BC_3D_AR3', 'BC_3D_AR4',
        'BC_3D_AR5', 'BC_3D_AR6', 'BC_3D_AR7', 'BC_3D_AR8',
        'BC_3D_AR9', 'BC_3D_AR10', 'BC_3D_BB', 'BC_3D_BDRES'
    ]
    
    # Calculate BC_3D_BDRES
    alldata['BC_3D_BDRES'] = alldata['BC_3D_BDY'] + alldata['BC_3D_RES']
    
    return alldata, cols

def prepare_inversion_data(alldata, cols, data_sources=['C14', 'RS', 'G20']):
    """Prepare matrices for inversion"""
    # Filter data for specified sources
    df = alldata.query('SOURCE == @data_sources')
    
    # Prepare observation matrix and data vector
    G = df[cols].values
    d = df['BC_OBS'].values.reshape(-1, 1)
    
    assert d.shape[0] == G.shape[0], "Mismatch in dimensions"
    
    return G, d

def plot_results(results, cols, save_path='inversion_results.png'):
    """Plot and save inversion results"""
    plt.figure(figsize=(12, 6))
    
    # Plot posterior means
    plt.subplot(121)
    plt.bar(range(len(cols)), results['posterior_mean'].flatten())
    plt.xticks(range(len(cols)), cols, rotation=45)
    plt.title('Posterior Mean Values')
    
    # Plot averaging kernel
    plt.subplot(122)
    plt.imshow(results['averaging_kernel'], cmap='viridis')
    plt.colorbar(label='Resolution')
    plt.title('Averaging Kernel')
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_optimization_history(study, save_path='optimization_history.png'):
    """Plot optimization history"""
    plt.figure(figsize=(10, 6))
    
    # Plot optimization history
    plt.plot(study.trials_dataframe()['value'], 'b-', label='Objective Value')
    plt.plot(study.trials_dataframe()['value'].cummax(), 'r--', label='Best Value')
    
    plt.xlabel('Trial')
    plt.ylabel('Objective Value')
    plt.title('Optimization History')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    try:
        # Load and prepare data
        print("Loading data...")
        alldata, cols = load_data()
        
        print("Preparing inversion data...")
        G, d = prepare_inversion_data(alldata, cols)
        
        # Initialize Optuna optimizer
        print("Initializing hyperparameter optimization...")
        optimizer = OptunaOptimizer(n_trials=50)  # Adjust number of trials as needed
        
        # Run optimization
        print("Running hyperparameter optimization...")
        optimization_results = optimizer.optimize(
            G=G,
            d_obs=d,
            m_prior=np.ones(len(cols)),
            Cd=np.eye(len(d)),
            Cm=np.eye(len(cols))
        )
        
        # Print optimization results
        print("\nOptimization Results:")
        print(f"Best parameters: {optimization_results['best_parameters']}")
        print(f"Best objective value: {optimization_results['best_value']:.4f}")
        
        # Get final results
        results = optimization_results['final_results']
        
        # Print inversion results
        print("\nInversion Results:")
        print(f"Number of observations: {results['num_observations']}")
        print(f"Number of parameters: {results['num_state_parameters']}")
        print(f"Reduced chi-squared: {results['chi2_red']:.2f}")
        print(f"NRSS: {results['nrss']:.2f}")
        print(f"Effective number of parameters: {results['effective_num_params']:.2f}")
        print(f"Shannon information: {results['shannon_information']:.2f}")
        print(f"Data resolution: {results['data_resolution']:.2f}")
        
        # Plot results
        print("\nPlotting results...")
        plot_results(results, cols)
        plot_optimization_history(optimization_results['study'])
        print("Results plots saved as 'inversion_results.png' and 'optimization_history.png'")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 