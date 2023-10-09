def Invoke_CreateServices(GRADIENTTOKEN: str, vendorServices: list ):
    import pyImports

    try:
        GradientServices: dict = pyImports.Get_PSVendor(GRADIENTTOKEN)

        GradientServicesNames: set = set([skus['name'] for skus in GradientServices['skus']])
        vendorServicesNames: set = set([service['name'] for service in vendorServices])
        VendorExists: list = list(vendorServicesNames - GradientServicesNames)

        CreateVendorSkuDto = []
        if len(VendorExists) > 0:
            CreateVendorSkuDto = [row for row in vendorServices if row['name'] in VendorExists]

        if len(CreateVendorSkuDto) > 0:
            for sku in CreateVendorSkuDto:
                pyImports.New_PSVendorService(GRADIENTTOKEN, sku)

        else:
            pyImports.logger.info("No new services to sync...")

    except:
        pyImports.logger.critical("Gradient Application API Invoke_CreateServices failed. Exiting!")
        pyImports.sys.exit(0)
