def loadENVs():
    import pyImports
    '''Called to load the ENVs from a .env file.
    Returns a dictionary of ENVs. DOES NOT perform ENV validation.'''

    pyImports.logger.info("Loading ENVs")
#region Loads ENVs from .env config file
    config: dict = pyImports.dotenv_values(".env")

    return config
#endregion
