import pandas as pd
import numpy as np

def load_data(filepath):
    """
    Load and preprocess data from the given filepath.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file containing the data
        
    Returns:
    --------
    pd.DataFrame
        Processed dataframe with the following columns:
        - SOURCE: Source identifier
        - BC_OBS: Observed black carbon values
        - BC_3D_*: Modeled black carbon values for different sources
    """
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Ensure required columns exist
    required_cols = ['SOURCE', 'BC_OBS']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Data must contain columns: {required_cols}")
    
    # Filter out any rows with missing values
    df = df.dropna(subset=required_cols)
    
    # Ensure BC_OBS is numeric
    df['BC_OBS'] = pd.to_numeric(df['BC_OBS'], errors='coerce')
    
    # Filter out any rows where BC_OBS is non-positive
    df = df[df['BC_OBS'] > 0]
    
    # Ensure all BC_3D_ columns are numeric
    bc_cols = [col for col in df.columns if col.startswith('BC_3D_')]
    for col in bc_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill any remaining NaN values in BC_3D_ columns with 0
    df[bc_cols] = df[bc_cols].fillna(0)
    
    return df

def preprocess_data(df, sources=None, min_obs=10):
    """
    Preprocess the data for inversion analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe from load_data()
    sources : list, optional
        List of sources to include in the analysis
    min_obs : int, optional
        Minimum number of observations required per source
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe ready for inversion
    """
    if sources is not None:
        df = df[df['SOURCE'].isin(sources)]
    
    # Count observations per source
    source_counts = df['SOURCE'].value_counts()
    valid_sources = source_counts[source_counts >= min_obs].index
    
    # Filter to only include sources with sufficient observations
    df = df[df['SOURCE'].isin(valid_sources)]
    
    # Sort by source and reset index
    df = df.sort_values('SOURCE').reset_index(drop=True)
    
    return df 