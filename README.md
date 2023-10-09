# GradientMSP: Hosted Kaseya VSA 9 Billing Integration

# Introduction
This is a Python version (>= 3.11) of the GradientMSP Synthesize-SDK-PS for a self-hosted Kaseya VSA version 9 integration. This follows Gradient's "template" structure and folder & file organization based on the public GitHub SDK. This could work with a hosted version of Kaseya VSA, but it has never been tested against the Hosted version. This repository was built against the "R95 version of the Kaseya REST API." 


# Disclaimer
My organization provides this repository for my organization, so this disclaims all implied warranties, and shall not be liable for damages arising out of the use of or inability to use these scripts. This is provided on an as-is basis.

## Requirements
- Python >= 3.11
- Synthesize API credentials
- Vendor API credentials
- Synthesize Account (GradientMSP)

## Files and Folders
You might consider this as a port of their PS SDK into Python for the point of integrating Kaseya VSA. File names and folder structures are mimicked as closely as possible to the GradientMSP PS SDK for clarity and ease of following their code. 

## NOTES - Here there be Dragons...
So, Kaseya VSA doesn't have a dedicated field to identify unique asset groups. First, my organization happens to use the "Agent Name" field to determine two asset types for our GradientMSP billing integrations. This is apparent in the "Get_AllServicesFromVendor" in the pyCustomIntegrations file where I statically populate the Vendor Services for Kaseya based on our service agreement billing. Second, the "Sort_VendorAccountServiceMappings" in the "private\pyVendorAccountServiceMapping" file builds the VSA service billing groups used in the GradientMSP integration. This is specific to my organization's environment and integration with GradientMSP, so this is all subject to change. 


## Getting Started
python main.py {action}
Possible actions are: sync-accounts, sync-services, update-status, or sync-usage

## Support
There isn't any support. 

## Related
https://www.meetgradient.com/