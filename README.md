# azdevopsaction-pbi-docu
# PowerBI Documenter

## Introduction
The PowerBI Documenter project automates the documentation of Power BI workspaces, datasets, reports, users, and data sources. This process is designed to run daily, collecting data and transforming it into a format suitable for the DevOps wiki, ensuring that the documentation is always up-to-date and easily accessible.

## Getting Started
Follow these steps to set up and configure the PowerBI Documenter on your own system.

### Installation Process
1. **Create an App Registration in Azure Portal**: 
   - In the Azure portal, create an app registration. A service user will be automatically created as part of this process.

2. **Create a Security Group**:
   - In the Azure portal, navigate to the 'Groups' section and create a new security group named 'your customers devops organization'. Add the service user as a member and assign the necessary owner.

3. **Setup Billing**:
   - Navigate to `devopsorganization/settings/billing` and set up a normal subscription for the service. Ensure that "paid parallel jobs" is set to 1 for Microsoft-hosted agents.

4. **Obtain OpenAI License (Optional)**:
   - After setting up billing, you may optionally obtain an OpenAI license for translation services. Register for an OpenAI license and obtain the necessary API keys.

5. **Create a New Pipeline and Add YAML Configuration**:
   - Create a new pipeline in your Azure DevOps project. Obtain the YAML file from Thomas or another project that has a similar configuration. This file will define the build and deployment process. You will need to create the following variables within this file:
     - `APP_ID` (Azure app registration)
     - `APP_SECRET` (Azure app registration / Certificates & secrets)
     - `OPENAI_KEY` (Azure OpenAI subscription)
     - `PAT` (DevOps PAT)
     - `TENANT_ID` (Azure app registration)

### Software Dependencies
- Azure DevOps
- Azure Portal
- Power BI
- Optional: OpenAI

### Latest Releases
-

### API References
Refer to the official documentation of Azure DevOps and Power BI for detailed API references.

## Build and Test
To test the installation, run the main pipeline. The wiki should be created and visible in the overview.
Use to compile TypeScript into JavaScript: 
```bash
tsc
```
Use to create Package:
```bash
tfx extension create --manifest-globs vss-extension.json
```