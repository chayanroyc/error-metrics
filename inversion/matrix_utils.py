def return_Gd(df, sources):
    """
    Build the forward model matrix G and observation vector d from the dataframe.
    sources: list of source names to filter.
    """
    # You may need to adjust 'cols' and 'BC_OBS' column names as per your data
    df = df.query('SOURCE == @sources')
    cols = [col for col in df.columns if col.startswith('BC_3D_')]
    G1 = df[cols].values
    d = df['BC_OBS'].values.reshape(-1,1)
    G = G1.copy()
    assert d.shape[0] == G.shape[0]
    return G, d 