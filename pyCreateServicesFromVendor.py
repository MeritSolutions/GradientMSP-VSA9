def Invoke_SyncServices(GRADIENTTOKEN: str):
    import pyImports
    RequiredServices: list = pyImports.Get_AllServicesFromVendor()
    return pyImports.Invoke_CreateServices(GRADIENTTOKEN, RequiredServices)


