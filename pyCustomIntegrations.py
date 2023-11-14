import pyImports
# Globals
config_envs: dict = pyImports.loadENVs()
MaxRetries: int = 4
BackOffFactor: int = 2
StatusForceList: list = [429, 500, 502, 503, 504]


def Invoke_KaseyaVSA9API() -> str:
#region Initial VSA Session Authorization
    '''Gets and returns temporary API session access token by using the API username and API user secret. 
    The temporary API session token is good for 24 hours but will refresh the timestamp of the temporary session
    token if this is called before the temporary session token expiration'''

    Uri: str = config_envs['API_URL'] + '/auth'
    API_KEY: str = config_envs['API_KEY']
    API_SECRET_KEY: str = config_envs['API_SECRET_KEY']
    
# Initial Credentials for authorization
    pyImports.logger.info("Building initial VSA authorization Token (Same as Gradient Token base64 encoded)")
    authorizationToken: str = pyImports.BuildGradientToken(API_KEY, API_SECRET_KEY) 
    
    session = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)

#Authorize against Kaseya API to get Session Expiration and Session API Token
    InitialAuth_Payload: dict = {}
    InitialAuth_Header: dict = {}
    InitialAuth_Header['Authorization'] = 'Basic ' + authorizationToken
    
    try: 
        PostAuth_Response: object = session.get(Uri, headers=InitialAuth_Header, data=InitialAuth_Payload)
        pyImports.logger.info("Success: Received VSA Session API Token and Session Expiration")

        PostAuth_Response = PostAuth_Response.json()
    except:
        pyImports.logger.critical("Cannot connect to the VSA API to get the Auth Key. Exiting!")
        pyImports.sys.exit(0)

#Post VSA Session Authorization
    PostAuth_SessionAPIToken: str = PostAuth_Response['Result']['ApiToken']

    return PostAuth_SessionAPIToken
#endregion

def Get_AllAccountsFromVendor(VENDORSESSIONAPITOKEN: str) -> list:
#region Get Organizations
    '''Gets all organizations from the VSA API. 
    The temporary API session token needs to be provided.'''

    Uri: str = config_envs['API_URL'] + '/system/orgs'
    actionExpression: str = '?'
    actionMultiple: str = '&'
    actionA: str = '$orderby=OrgName' # Optional
    actionB: str = '$skip=' # Mandatory
    skipCounter: int = 0
    totalOrganizations: int = 0
    Organizations: list = []


    try:
        session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)
        sessionPayload: dict = {}
        sessionHeaders: dict = {}
        sessionHeaders['Authorization'] = 'Bearer ' + VENDORSESSIONAPITOKEN 

        response: object = session.get(Uri, headers=sessionHeaders, data=sessionPayload)
        pyImports.logger.info("Success: Received VSA All Organizations")
        sessionResponse: object = response.json()
        
        totalOrganizations = int(sessionResponse['TotalRecords']) #Getting Total Organization Count

        #Looping through API until all Orgs are parsed. The Maximun number of records returned by the API is 100. 
        #A LoopExit of 10 would allow 10000 Organizations to be parsed.
        loopExit = 0

        while totalOrganizations > len(Organizations) and loopExit <= 10:  
            UriOrganizations = f"{Uri}{actionExpression}{actionA}{actionMultiple}{actionB}{skipCounter}"
            
            response: object = session.get(UriOrganizations, headers=sessionHeaders, data=sessionPayload)
            sessionResponse: object = response.json()
            sessionResponseResults: list = sessionResponse['Result']

            for org in sessionResponseResults:
                organization: dict = {
                'OrgId': org['OrgId']
                ,'OrgName': org['OrgName']
                ,'OrgRef': org['OrgRef']
                }
                Organizations.append(organization)

            skipCounter = skipCounter + 100

            loopExit = loopExit + 1

        pyImports.logger.info(f"Organizations feteched: {len(Organizations)}")
        return Organizations

    except:
        pyImports.logger.critical("Cannot connect to the VSA API for Organizations. Exiting!")
        pyImports.sys.exit(0)
#endregion

def Get_AllServicesFromVendor() -> list:
#region Get all services from vendor
    '''Gets all Services from Vendor. BUT this is the Kaseya VSA so we will force the service types since there are not any configured in the VSA'''

    services: list = [
        {'name': "MSA_SERVICE", 'description': "MERIT Service Plan Per Device Price", 'category': 'service delivery', 'subcategory': 'desktop management and support'}
        ,{'name': "MSA_SUPPLEMENTAL_SERVICE", 'description': "MERIT Service Plan for Supplemental Devices, Per Device Price", 'category': 'service delivery', 'subcategory': 'desktop management and support'}
    ]

    return services
#endregion

def Get_AccountUsage(VENDORSESSIONAPITOKEN: str, account: dict, vendorServices: list) -> list:
#region Gets account license usage
    '''This get the account usage from the Kaseya VSA.
    The temporary API session token needs to be provided.
    Account expects a dictionary {'OrgId':'OrgName'}'''
    LastCheckInTime: str = pyImports.datetime.datetime.strftime((pyImports.datetime.datetime.now() - pyImports.datetime.timedelta(days=45)), '%Y-%m-%dT%H:%M:%S')
    Uri: str = config_envs['API_URL'] + '/assetmgmt/agents'
    actionExpression: str = '?'
    actionMultiple: str = '&'
    actionA: str = '$filter=' + 'OrgId eq ' + f'{account["OrgId"]}' + 'M' # Mandatory an M must be added to the end of the number to denote a decimal data type instead of the default double data type
    actionB: str = '$skip=' # Mandatory
    actionC: str = f" and LastCheckInTime ge DATETIME'{LastCheckInTime}'" # Filtering for assets that have checked in w/in the past 45 days.
    skipCounter: int = 0
    totalAssets: int = 0
    Assets: list = []
    UriAssets = f"{Uri}{actionExpression}{actionB}{skipCounter}{actionMultiple}{actionA}{actionC}"


    try:
        session: object = pyImports.sessionRetry(MaxRetries=MaxRetries, BackOffFactor=BackOffFactor, StatusForceList=StatusForceList)
        sessionPayload: dict = {}
        sessionHeaders: dict = {}
        sessionHeaders['Authorization'] = 'Bearer ' + VENDORSESSIONAPITOKEN

        response: object = session.get(UriAssets, headers=sessionHeaders, json=sessionPayload)
        pyImports.logger.info("Success: Received VSA Total Assets for Organizations")
        sessionResponse: object = response.json()
        totalAssets = int(sessionResponse['TotalRecords']) #Getting Total Organization Count

        #Looping through API until all Assets are parsed. The Maximun number of records returned by the API is 100. 
        #A LoopExit of 10 would allow 10000 Organizations to be parsed.
        loopExit: int = 0

        while totalAssets > len(Assets) and loopExit <= 10:  
            UriAssets = f"{Uri}{actionExpression}{actionB}{skipCounter}{actionMultiple}{actionA}{actionC}"
            response: object = session.get(UriAssets, headers=sessionHeaders, json=sessionPayload)
            sessionResponse: object = response.json()

            sessionResponseResults: object = sessionResponse['Result']

            
            for asset in sessionResponseResults:
                assetDetails: dict = {
                'AgentName': asset['AgentName']
                ,'LastCheckInTime': pyImports.datetime.datetime.strptime((asset['LastCheckInTime'])[:19], '%Y-%m-%dT%H:%M:%S')
                }
                Assets.append(assetDetails)

            skipCounter = skipCounter + 100

            loopExit = loopExit + 1

        pyImports.logger.info(f"Assets feteched: {len(Assets)}")
        return Assets

    except:
        pyImports.logger.critical("Cannot connect to the VSA API for Assets. Exiting!")
        pyImports.sys.exit(0)
#endregion
