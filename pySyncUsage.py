def Invoke_SyncUsage(GRADIENTTOKEN: str, VENDORSESSIONAPITOKEN: str): 
    import pyImports

    try:
        pyImports.logger.info("Starting SyncUsage call")
        VendorAccounts: object = pyImports.Get_AllAccountsFromVendor(VENDORSESSIONAPITOKEN)
        serviceIds: dict = pyImports.Invoke_GetServiceIds(GRADIENTTOKEN)
        vendorUsageBilling: dict = []

        for org in VendorAccounts:
            pyImports.logger.info(f"Getting Vendor active license count for: {org['OrgName']}")
            assets: list = pyImports.Get_AccountUsage(VENDORSESSIONAPITOKEN, org, serviceIds)
            UsageCount: list = pyImports.Sort_VendorAccountServiceMappings(serviceIds, assets)

            for usage, usageValue in UsageCount.items():
                if int(usageValue) > 0: 
                    vendorBilling: dict = {
                    'clientId': org['OrgId']
                    ,'clientName': org['OrgName']
                    ,'serviceName': usage
                    ,'unitCount': usageValue
                    }
                    vendorUsageBilling.append(vendorBilling)

        response: object = pyImports.New_PSBilling(GRADIENTTOKEN, serviceIds, vendorUsageBilling)

    except:
        pyImports.logger.critical("Failed syncing usage. Exiting!")
        pyImports.sys.exit(0)


