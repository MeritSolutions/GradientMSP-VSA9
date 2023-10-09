import pyImports
# Globals
config_envs: dict = pyImports.loadENVs()
Uri = config_envs['GRADIENT_API_BASE_URI']
MaxRetries: int = 4
BackOffFactor: int = 2
StatusForceList: list = [429, 500, 502, 503, 504]

def New_PSAccount(GRADIENTTOKEN: str, accounts: list):
#region
    'Add a new Account to the Service Integration in Gradient'
    localUri: str = Uri + '/vendor-api/organization/accounts'
    headers: dict = {
        "accept": "application/json",
        "content-type": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: list = []
    for account in accounts:
        accountPayload: dict = {
            'name': account['OrgName'],
            'description': account['OrgRef'],
            'id': account['OrgId']
        }
        payload.append(accountPayload)

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Inserting New Account into Service Integration in Gradient")
        response: object = session.post(localUri, headers=headers, json=payload)
        pyImports.logger.success(f"{len(payload)} Accounts created")

    except:
        pyImports.logger.critical("Gradient Application API New_Accounts failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def New_PSVendorService(GRADIENTTOKEN: str, service: dict):
#region
    'Add a new Account to the Service Integration in Gradient'
    localUri: str = Uri + '/vendor-api/service'
    headers: dict = {
        "accept": "application/json",
        "content-type": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = service

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Inserting New Vendor Service into Service Integration in Gradient")
        response: object = session.post(localUri, headers=headers, json=payload)
        pyImports.logger.success(f"{service['name']}: Service created")

    except:
        pyImports.logger.critical("Gradient Application API New_VendorService failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def New_PSBilling(GRADIENTTOKEN: str, serviceIds: dict, vendorBillingUsage: list):
#region 
    '''Adds Billing usage to Billing UI'''
    usagePayload: list = []
    for usage in vendorBillingUsage:
        if usage['serviceName'] in serviceIds.keys():
            usage['serviceId'] = serviceIds[usage['serviceName']]
            usagePayload.append(usage)

    for service in serviceIds:
        orgServiceUsage: list = []
        for usage in usagePayload:
            if service == usage['serviceName']:
                serviceId = usage['serviceId']
                usageDict: dict = {
                    'clientName': usage['clientName']
                    ,'accountId': usage['clientId']
                    ,'unitCount': usage['unitCount']
                }
                orgServiceUsage.append(usageDict)

        UriUsage: str = Uri + f"/vendor-api/service/{serviceId}/count"
        headers: dict = {
            "accept": "application/json",
            "content-type": "application/json",
            "GRADIENT-TOKEN": GRADIENTTOKEN
        }

        session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

        try:
            for payload in orgServiceUsage:
                clientName: str = payload['clientName']
                del payload['clientName']
                pyImports.sleep(0.5)
                pyImports.logger.info("Inserting Usage Count into Billing Integration in Gradient")
                response: object = session.post(UriUsage, headers=headers, json=payload)
                if response.status_code == 404:
                    pyImports.logger.warning(f"Catching 404 error: {clientName} {service} Usage Count: {payload['unitCount']}")
                    continue
                pyImports.logger.success(f"{clientName} {service} Usage Count {payload['unitCount']} updated successfully.")

        except:
            pyImports.logger.critical("Gradient Service Usage Count Update failed. Exiting!")
            pyImports.sys.exit(0)

#endregion

def Get_PSAccounts(GRADIENTTOKEN: str) -> object:
#region
    '''Returns all accounts from Gradient'''
    localUri: str = Uri + '/vendor-api/organization/accounts'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = {}

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Getting Accounts already in Gradient")
        response: object = session.get(localUri, headers=headers, data=payload)
        sessionResponse: object = response.json()
        return sessionResponse

    except:
        pyImports.logger.critical("Gradient Application API Get_Accounts failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def Get_PSIntegration(GRADIENTTOKEN: str) -> object:
#region
    '''Returns the Integration Vendor Information from Gradient'''
    localUri: str = Uri + '/vendor-api/organization'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = {}

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Getting Partner Integration Information in Gradient")
        response: object = session.get(localUri, headers=headers, data=payload)
        sessionResponse: object = response.json()
        return sessionResponse

    except:
        pyImports.logger.critical("Gradient Partner Integration Information API Get_Integration failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def Get_PSVendor(GRADIENTTOKEN: str) -> object:
#region
    '''Returns the Integration Vendor Information from Gradient'''
    localUri: str = Uri + '/vendor-api'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = {}

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Getting Vendor Information in Gradient")
        response: object = session.get(localUri, headers=headers, data=payload)
        sessionResponse: object = response.json()
        sessionResponseResults: object = sessionResponse['data']
        return sessionResponseResults

    except:
        pyImports.logger.critical("Gradient Application API Get_Vendor failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def Get_PSVendorService(GRADIENTTOKEN: str, serviceId: str) -> object:
#region
    '''Returns the Integration Vendor Information from Gradient'''

    if not serviceId:
        pyImports.logger.critical("Error! The required parameter `ServiceId` missing when calling getVendorService. Exiting.")
        pyImports.sys.exit(0)

    localUri: str = Uri + '/vendor-api/service' + f'/{str(serviceId)}'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = {}

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Getting Vendor Information in Gradient")
        response: object = session.get(localUri, headers=headers, data=payload)
        sessionResponse: object = response.json()
        sessionResponseResults: object = sessionResponse['data']
        return sessionResponseResults

    except:
        pyImports.logger.critical("Gradient Application API Get_VendorService failed. Exiting!")
        pyImports.sys.exit(0)
#endregion

def Update_PSAccount(GRADIENTTOKEN:str, account: dict):
#region
    '''Updates Account information in Gradient'''
    if not account['id']:
        pyImports.logger.critical("Error! The required parameter `AccountId` missing when calling updateAccount. Exiting.")
        pyImports.sys.exit(0)

    localUri: str = Uri + '/vendor-api/organization/accounts' + f'/{str(account["id"])}'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = account

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Inserting New Account into Service Integration in Gradient")
        response: object = session.patch(localUri, headers=headers, data=payload)
        pyImports.logger.success(f"{account['name']}: Account created")

    except:
        pyImports.logger.critical("Gradient Application API Update Accounts failed. Exiting!")
        pyImports.sys.exit(0)

#endregion

def Update_PSIntegrationStatus(GRADIENTTOKEN: str, status: str = 'pending'):
#region
    '''Updating the Gradient Integration Status. Setting it to pending'''

    localUri: str = Uri + '/vendor-api/organization/status' + f'/{status}'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = {}

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Updating Integration Status in Gradient")
        response: object = session.patch(localUri, headers=headers, json=payload)
        sessionResponse: object = response.json()
        pyImports.logger.success(f"{sessionResponse['message']}")

    except:
        pyImports.logger.critical("Failed updating Gradient Integration Status to PENDING. Exiting!")
        pyImports.sys.exit(0)
    
#endregion

def Update_PSVendorService(GRADIENTTOKEN: str, service: dict):
#region
    '''Updates Vendor Service information in Gradient'''
    if not service['id']:
        pyImports.logger.critical("Error! The required parameter `ServiceId` missing when calling UpdateVendorService. Exiting.")
        pyImports.sys.exit(0)

    localUri: str = Uri + '/vendor-api/service' + f'/{str(service["id"])}'
    headers: dict = {
        "accept": "application/json",
        "GRADIENT-TOKEN": GRADIENTTOKEN
    }
    payload: dict = service

    session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

    try:
        pyImports.logger.info("Updating Service Info in Gradient")
        response: object = session.patch(localUri, headers=headers, data=payload)
        pyImports.logger.success(f"{service['name']}: Service updated")

    except:
        pyImports.logger.critical("Gradient Application API Update_VendorService failed. Exiting!")
        pyImports.sys.exit(0)
        
#endregion