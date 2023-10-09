
def main():
    import pyImports
    # pyImports.logger.add("GradientVSA_1.log", rotation="5 MB", retention="10 days" )    # Automatically rotate too big file
    pyImports.logger.add("GradientVSA_1.log", mode='w')    # Automatically rotate too big file
    pyImports.logger.info("Starting Logging...")


    try:
        invokeAction: str = pyImports.sys.argv[1]
    except: 
        pyImports.logger.critical("No action supplied! Please use sync-accounts, sync-services, update-status, or sync-usage")
        pyImports.sys.exit(0)

#region Checks for missing API keys, generates the GRADIENT Token and return the Target Vendor Authorization Tokens.
    pyImports.logger.info("Getting Gradient API Tokens and Vendor REST API Tokens")
    GRADIENTTOKEN: str = pyImports.InitGradientConnection(invokeAction)
    VENDORSESSIONAPITOKEN: str = pyImports.Invoke_KaseyaVSA9API()

    match invokeAction:
        case 'sync-accounts':
            pyImports.Invoke_SyncAccounts(GRADIENTTOKEN, VENDORSESSIONAPITOKEN)
        
        case 'sync-services':
            pyImports.Invoke_SyncServices(GRADIENTTOKEN)

        case 'update-status':
            pyImports.Invoke_UpdateStatus(GRADIENTTOKEN)

        case 'sync-usage':
            pyImports.Invoke_SyncUsage(GRADIENTTOKEN, VENDORSESSIONAPITOKEN)

    pyImports.logger.info(f"Finished {invokeAction}.")

#endregion



if __name__ == "__main__":
    main()
