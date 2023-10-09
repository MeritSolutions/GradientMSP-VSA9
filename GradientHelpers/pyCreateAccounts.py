def Invoke_CreateAccounts(GRADIENTTOKEN: str, vendorAccounts: list):
    import pyImports
    try:
        GradientAccounts: list = pyImports.Get_PSAccounts(GRADIENTTOKEN)
        GradientAccountNames: set = set([account['id'] for account in GradientAccounts])
        vendorAccountNames: set = set([account['OrgId'] for account in vendorAccounts])
        AccountExists: list = list(vendorAccountNames - GradientAccountNames)

        CreateAccountMappingDto: list = []
        if len(AccountExists) > 0:
            CreateAccountMappingDto = [row for row in vendorAccounts if row['OrgId'] in AccountExists]
            pyImports.New_PSAccount(GRADIENTTOKEN, CreateAccountMappingDto)
            
        else:
            pyImports.logger.info("No new accounts to sync...")

    except:
        pyImports.logger.critical("Gradient Application API Invoke_CreateAccount failed. Exiting!")
        pyImports.sys.exit(0)
