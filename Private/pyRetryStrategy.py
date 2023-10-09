def sessionRetry(MaxRetries: int = 4, BackOffFactor: int = 2, StatusForceList: list = [429, 500, 502, 503, 504]):
    '''Builds urllib session retry adapter and returns the object'''
    import pyImports
#region
    Retry_Strategy: object = pyImports.Retry(total=MaxRetries, backoff_factor=BackOffFactor, status_forcelist=StatusForceList)
    
    # Create an HTTP adapter with the retry strategy and mount it to session
    HttpAdapter: object = pyImports.HTTPAdapter(max_retries=Retry_Strategy)

    # Create a new session object
    session: object = pyImports.requests.Session()
    session.mount('http://', HttpAdapter)
    session.mount('https://', HttpAdapter)

    return session
#endregion

