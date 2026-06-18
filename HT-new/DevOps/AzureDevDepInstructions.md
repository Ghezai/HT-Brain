# Azure Environments Deployment Instruction

## Easy Setup Main Points

### 1. Prepare infrastructure code

- Make sure these folders exist in the codebase:
  - `src/infrastructure`
  - `src/pipelines`
- These folders hold the Azure infrastructure setup and Azure DevOps pipeline definitions.

### 2. Choose environment name

- Decide the environment name before setup.
- Example:
  - `int` for integration
  - `test` for test
  - `prod` for production
- In the instructions, `<env>` means this environment name.

### 3. Create Azure DevOps variable group

- In Azure DevOps, create variable group:
  - `infrastructure-<env>`
- For the first infrastructure deployment, add:
  - `rebuildSecrets=true`
- After infrastructure works, change it to:
  - `rebuildSecrets=false`

### 4. Create Azure resource group manually

- Before running the first infrastructure pipeline, manually create:
  - `friio-<env>` resource group

### 5. Add infrastructure pipeline

- Add Azure DevOps pipeline:
  - `Friio <env> - deploy infrastructure`
- Run this pipeline first.
- The first run can fail when creating ACI because the fresh ACR has no image yet.

### 6. Push first Liquibase image to ACR

- If infrastructure pipeline fails because ACR has no image, push the Liquibase image manually:

```bash
az login --tenant <tenant_id>
az acr login --name friioacr<env>
cd liquibase
bash build.sh
docker tag friio-liquibase:1.0 friioacr<env>.azurecr.io/friio/liquibase:latest
docker push friioacr<env>.azurecr.io/friio/liquibase:latest
```

- Then rerun the infrastructure pipeline.

### 7. Create database login and Liquibase user

- After infrastructure deployment succeeds, connect to MSSQL `master` database and create login:

```sql
CREATE LOGIN [friio_login] WITH PASSWORD = 'changeme';
```

- Then connect to `friio-database-<env>` and run:

```sql
CREATE SCHEMA [polaris];
CREATE USER liquibase_user FOR LOGIN friio_login WITH DEFAULT_SCHEMA = polaris;
ALTER ROLE db_owner ADD MEMBER liquibase_user;
```

### 8. Create backup/commit storage

- Before build/release pipeline setup, manually create a Storage Account and Blob for:
  - database backups
  - last successful commit tracking
- Example:
  - Storage Account: `friioexport<env>`
  - Blob: `last-successful-commit`
- Give Azure Pipeline Service Principal this RBAC role:
  - `Storage Blob Data Contributor`

### 9. Add build and release pipeline

- Add Azure DevOps pipeline:
  - `Friio <env> - build and release docker images`
- Initial pipeline variables:
  - `azureServiceConnection=<AzurePipelineServiceConnectionName>`
  - `buildAll=true`
  - `lastSuccessfulCommitStorageAccountName=<storage account name>`
  - `lastSuccessfulCommitBlobName=<blob name>`
- After first successful run, change:
  - `buildAll=false`

### 10. Normal deployment flow

- Run infrastructure pipeline when Azure resources or infrastructure changes.
- Run build/release pipeline when application services or Docker images need deployment.
- Keep secrets in Azure DevOps variable groups and Key Vault, not in Git.

---

## Original Notes

Ihor Skrypnyk
Apr 23
Preapre codebase related to Infrastructure for deployment:

src/infrastructure
src/pipelines
Configure Azure DevOps Variables Groups for environment.

Add pipelines to Azure DevOps Pipelines:

Friio <env> - deploy infrastructure
Friio <env> - build and release docker images
Note. <env> should be replaces on the name of your environment, for example <env>=int for integration environment.

Adding Friio <env> - deploy infrastructure
In Azure DevOps Library Variable Group infrastructure-<env> define such variables for initial startup of Friio <env> - deploy infrastructure pipeline:
rebuildSecrets=true

Manually create friio-<env> resource group before intial pipeline start.

During the deployment of Friio <env> - deploy infrastructure you will face with failure of creation ACI rescource. It happends because there is no any image inside fresh created ACR can be fixed in two ways:

manually upload image to ACR and redeploy infrasturucture pipeline

az login --tenant <tenant_id>
az acr login --name friioacr<env>.azurecr.io
cd liquibase && bash build.sh
docker tag friio-liquibase:1.0 friioacr<env>.azurecr.io/friio/liquibase:latest
docker push friioacr<env>.azurecr.io/friio/liquibase:latest 
add images_build_and_push pipeline with only one step: liquibase build and push
For the third deployment of Friio <env> - deploy infrastructure define:
rebuildSecrets=false (to not rebuild Application secrets after each deployment and take it from Key Vault secrets)

When Infrastructure pipeline deployed successfuly execute such MSSQL databases scripts for liquibase ACI auth

Login to master on the MSSQL server:
CREATE LOGIN [friio_login] WITH PASSWORD = 'changeme'; (credentials will be used for login to database)

Login to friio-database-<env> db:


CREATE SCHEMA [polaris];
CREATE USER liquibase_user FOR LOGIN friio_login WITH DEFAULT_SCHEMA = polaris;
ALTER ROLE db_owner ADD MEMBER liquibase_user;
Adding Friio <env> - build and release docker images
Before adding Friio <env> - build and release docker images pipeline, manually create separate Storage Account and Blob inside to store backups from database and last-successful-commit. For example call Storage account - friioexport<env>, Blob - last-successful-commit. These names will be required during further pipeline creation. Attach
Storage Blob Data Contributor RBAC role for Azure Pipeline Service Principal to get last-successful-commit object.

In Azure DevOps Friio <env> - build and release docker images pipeline UI define such variables for initial startup pipeline:
azureServiceConnection=<AzurePipelineServiceConnectionName> (allow to Azure DevOps interact with Azure Cloud)
buildAll=true (rebuild all services even there is no changes)
lastSuccessfulCommitStorageAccountName=<lastSuccessfulCommitStorageAccountName> (Storage Account name where the last successful commit will store)
lastSuccessfulCommitBlobName=<lastSuccessfulCommitBlobName> (Blob name inside Storage Account where the last successful commit will store)

After pipeline execution redefine buildAll=false to not rebuild all services every time and just rely on changes and last-successful-commit approach.
