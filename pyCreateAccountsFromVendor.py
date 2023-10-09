def Invoke_SyncAccounts(GRADIENTTOKEN: str, VENDORSESSIONAPITOKEN: str) -> dict:
    import pyImports
    vendorAccounts: list = pyImports.Get_AllAccountsFromVendor(VENDORSESSIONAPITOKEN)
    return pyImports.Invoke_CreateAccounts(GRADIENTTOKEN, vendorAccounts)
 