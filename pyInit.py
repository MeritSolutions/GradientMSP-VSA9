def InitGradientConnection(invokeAction: str):
    import pyImports

    actions: list = set(['sync-accounts', 'sync-services', 'update-status', 'sync-usage'])
    if invokeAction not in actions:
        pyImports.logger.critical(f"{invokeAction} is not a valid action! Please use sync-accounts, sync-services, update-status, or sync-usage")
        pyImports.sys.exit(0)

    
    pyImports.logger.info("Loading ENVs from file.")
    config_envs: dict = pyImports.loadENVs()

    pyImports.logger.info("Validating ENVs")
#region Checking ENVs to make sure they are not empty strings
    if len(config_envs['VENDOR_API_KEY']) == 0 or len(config_envs['PARTNER_API_KEY']) == 0:
        pyImports.logger.critical("Gradient API keys are required in ENV. Exiting!")
        pyImports.sys.exit(0)
    
    if len(config_envs['API_KEY']) == 0 or len(config_envs['API_SECRET_KEY']) == 0 or len(config_envs['API_URL']) == 0:
        pyImports.logger.critical("Application API keys are required in ENV. Exiting!")
        pyImports.sys.exit(0)
#endregion

    pyImports.logger.info("Generating GRADIENTTOKEN")
#region Checks, Generates, and returns GRADIENTTOKEN
    authorizationToken: str = pyImports.BuildGradientToken(config_envs['VENDOR_API_KEY'], config_envs['PARTNER_API_KEY'])
    pyImports.logger.info("GRADIENTTOKEN Built & Received.")
    return authorizationToken
#endregion



