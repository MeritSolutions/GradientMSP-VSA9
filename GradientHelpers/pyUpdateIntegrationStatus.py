def Invoke_UpdateStatus(GRADIENTTOKEN: str):
    '''Get the current Integration Status. If the integration status is set to inactive, this will
      set the status to pending.'''
    import pyImports

    try:
        pyImports.logger.info("Checking current vendor Integration Status.")
        integrationStatusResponse: dict = pyImports.Get_PSIntegration(GRADIENTTOKEN)

    except:
        pyImports.logger.critical("An error occurred while checking the Integration Status. Exiting!")
        pyImports.sys.exit(0)


    if integrationStatusResponse['status'] == 'inactive':
        try:
            pyImports.Update_PSIntegrationStatus(GRADIENTTOKEN, status='pending')

        except:
            pyImports.logger.critical("An error occurred while updating Integration Status. Exiting!")
            pyImports.sys.exit(0)

    else:
        pyImports.logger.info(f"No changes. Current Integration status: {integrationStatusResponse['status']}")