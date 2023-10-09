def Invoke_GetServiceIds(GRADIENTTOKEN: str) -> dict:
    '''Gets serviceIds created in Gradient'''
    import pyImports
    
    try:
        vendorData: object = pyImports.Get_PSVendor(GRADIENTTOKEN)
        skus: object = vendorData['skus']
        skuServiceIds = {sku['name']: sku['id'] for sku in skus}
        return skuServiceIds

    except:
        pyImports.logger.critical("An error occurred while getting service IDs. Exiting!")
        pyImports.sys.exit(0)
