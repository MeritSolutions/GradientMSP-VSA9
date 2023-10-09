def Initialize_CreateServiceRequest(service: dict) -> dict:
    import pyImports
    
    pyImports.logger.info("Initializing Create Service Request")
    name: str = service['serviceName']
    description: str = service['serviceDescription']
    supportArticle: str = service['serviceSupportArticle']
    supportContact: str = service['serviceSupportContact']
    category: str = service['serviceCatagory']
    subcategory: str = service['serviceSubCatagory']

    if not name:
        pyImports.logger.critical("invalid value for 'Name', 'Name' cannot be null. Exiting.")
        pyImports.sys.exit(0)
    if not description:
        pyImports.logger.critical("invalid value for 'Description', 'Description' cannot be null. Exiting.")
        pyImports.sys.exit(0)
    if not category:
        pyImports.logger.critical("invalid value for 'Category', 'Category' cannot be null. Exiting.")
        pyImports.sys.exit(0)
    if not subcategory:
        pyImports.logger.critical("invalid value for 'Subcategory', 'Subcategory' cannot be null. Exiting")
        pyImports.sys.exit(0)

    service: dict = {
        'name': name,
        'description': description,
        'supportArticle': supportArticle,
        'supportContact': supportContact,
        'category': category,
        'subcategory': subcategory
    }

    return service
