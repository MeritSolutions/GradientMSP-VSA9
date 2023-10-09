def BuildGradientToken(VENDOR_API_KEY: str, PARTNER_API_KEY: str):
    import pyImports
    '''Returns the Base64 Encoded authorization token.
    This function expects two strings to be provided.'''

    authorizationToken: str = f'{VENDOR_API_KEY}:{PARTNER_API_KEY}'
    authorizationTokenEncoded: str = pyImports.base64.b64encode(authorizationToken.encode()).decode()

    return authorizationTokenEncoded