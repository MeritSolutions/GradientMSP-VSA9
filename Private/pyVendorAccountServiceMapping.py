def Sort_VendorAccountServiceMappings(vendorServices: list, vendorAssets: list) -> dict:
    '''The VSA doesn't have a way to determime service mappings natively.
    We use a naming convention, the MachineID either starts with _supp
    or it doesn't. This splits the Machine IDs into the respective Account
    Service mappings and returns totals for all service mappings'''
    import pyImports
    SerivceUsage: dict = {service: 0 for service in vendorServices}

    for asset in vendorAssets:
        if '_supp' in asset['AgentName']:
            SerivceUsage['MSA_SUPPLEMENTAL_SERVICE'] += 1
        else:
            SerivceUsage['MSA_SERVICE'] += 1
            
    return SerivceUsage