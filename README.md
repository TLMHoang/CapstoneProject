# Capstone project : Product Management API

This API allows you to manage products and their associated serial numbers (IMEIs). It provides endpoints for creating, reading, updating, and deleting products, as well as managing the serial numbers linked to each product.

## Motivation

The primary goal of this project is to provide a robust and scalable solution for managing product inventory and tracking individual items using unique serial numbers. This is crucial for businesses that need to maintain accurate records of their products, track warranty information, and manage returns or repairs.

## Hosted API

This API is not currently hosted on a public URL. However, it can be easily deployed to various cloud platforms or run locally for development and testing purposes.

<a href="cc090525ffc94e209d93439794de053-962124918.us-east-1.elb.amazonaws.com" target="_blank">Final URL</a>: cc090525ffc94e209d93439794de053-962124918.us-east-1.elb.amazonaws.com

## Prerequisites

- `Docker Desktop` - Installation instructions for all OSes can be found <a href="https://docs.docker.com/install/" target="_blank">here</a>.
- `Git`: <a href="https://git-scm.com/downloads" target="_blank">Download and install Git</a> for your system. 
- `Code editor`: You can <a href="https://code.visualstudio.com/download" target="_blank">download and install VS code</a> here.
- `AWS Account`
- `Python version 3.9` Check the current version using:
```bash
#  Mac/Linux/Windows 
python --version
```
You can download a specific release version from <a href="https://www.python.org/downloads/" target="_blank">here</a>.

- Python package manager - PIP `24.1.1`. PIP is already installed in Python `3.9.6` downloaded from python.org.
```bash
#  Mac/Linux/Windows Check the current version
pip --version
# Mac/Linux
pip install --upgrade pip==24.1.1
# Windows
python -m pip install --upgrade pip==24.1.1
```
- `AWS-CLI 2.17.0`: you can read docment install AWS-CLI from <a href="https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html" target="_blank">here</a>.
- `PostgreSQL 16`: The database used to store product and serial data.
- `Auth0`: For authentication and authorization (JWT-based).


## Project Dependencies

The project relies on the following key dependencies:

- `Flask`: A lightweight and flexible web framework for building APIs.
- `Flask-Migrate`: An extension for handling database migrations.
- `Flask-SQLAlchemy`: An ORM for interacting with the database.
- `python-dotenv`: For loading environment variables from a .env file.

## Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/TLMHoang/CapstoneProject/
cd ./<youpath>/CapstoneProject
```
#### These are the files relevant for the current project:
```bash

.
├── AWS
│   ├── aws-auth-patch.yml
│   ├── buildspec.yml
│   ├── ci-cd-codepipeline.cfn.yml 
│   ├── iam-role-policy.json 
│   ├── param.txt 
│   ├── simple_jwt_api.yml 
│   └── trust.json
│   └──
├── BE
│   ├── __init__.py 
│   ├── .env 
│   ├── app.py 
│   ├── auth.py 
│   ├── config.py 
│   ├── Dockerfile 
│   ├── model.py 
│   ├── requirements.txt 
│   ├── test_main.py 
│   └── testapi.py 
├── FE #Optional
│   ├── src
│   │   ├── app 
│   │   │   ├── pages 
│   │   │   │   ├── product-menu 
│   │   │   │   │   ├── product-form 
│   │   │   │   │   │   ├── product-form.component.html 
│   │   │   │   │   │   ├── product-form.component.scss 
│   │   │   │   │   │   └── product-form.component.ts
│   │   │   │   │   ├── product-menu.module.ts 
│   │   │   │   │   ├── product-menu.page.html 
│   │   │   │   │   ├── product-menu.page.scss 
│   │   │   │   │   └── product-menu.page.ts
│   │   │   │   ├── tabs 
│   │   │   │   │   ├── tabs.module.ts 
│   │   │   │   │   ├── tabs.page.html 
│   │   │   │   │   ├── tabs.page.scss 
│   │   │   │   │   ├── tabs.page.spec.ts 
│   │   │   │   │   ├── tabs.page.ts 
│   │   │   │   │   └── tabs.router.module.ts
│   │   │   │   ├── user-page
│   │   │   │   │   ├── user-page.module.ts 
│   │   │   │   │   ├── user-page.page.html 
│   │   │   │   │   ├── user-page.page.scss 
│   │   │   │   │   ├── user-page.page.spec.ts 
│   │   │   │   │   └── user-page.page.ts
│   │   │   ├── services 
│   │   │   │   ├── auth.service.ts 
│   │   │   │   └──  products.service.ts
│   │   │   ├── app-routing.module.ts 
│   │   │   ├── app.component.html 
│   │   │   ├── app.component.spec.ts 
│   │   │   ├── app.component.ts 
│   │   │   └── app.module.ts
│   │   ├── assets 
│   │   │   ├── icon
│   │   │   │   └── favicon.png
│   │   │   └── shapes.svg
│   │   ├── environments 
│   │   │   ├── environment.prod.ts 
│   │   │   └── environment.ts
│   │   ├── theme
│   │   │   └── variables.scss
│   │   ├── global.scss 
│   │   ├── index.html 
│   │   ├── karma.conf.js 
│   │   ├── main.ts 
│   │   ├── polyfills.ts 
│   │   ├── test.ts 
│   │   ├── tsconfig.app.json 
│   │   ├── tsconfig.spec.json 
│   │   ├── tslint.json 
│   │   └── zone-flags.ts
│   ├── angular.json 
│   ├── ionic.config.json 
│   ├── package-lock.json 
│   ├── package.json 
│   ├── README.md 
│   ├── tsconfig.json 
│   └── tslint.json
├── buildspec.yml 
├── Dockerfile 
├── phone-store.yml 
├── README.md 
└── requirements.txt
```

### 2. Create and activate a virtual environment:

```bash
cd ./BE
python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables:

- Create a .env file in the project root directory.
- Add the following variables, replacing placeholders with your actual values:


Add the following variables, replacing placeholders with your actual values:
```bash
DATABASE_URI=your_URI_Database_PostgreSQL
AUTH0_DOMAIN=your_auth0_domain
API_AUDIENCE=your_api_audience
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
```


### 5. Run database migrations:
You can skip this step because the code currently only has 1 new migration. there is no migration to update the database, so there is no need to run the command. When you run for the first time, it will automatically create a database for you.

Commend if Need
```bash
flask init
flask db upgrade
```

### 6. Start the development server:
```bash
python app.py
```

### 7. Run FE (optional)

- Install package for FE
```bash
npm install
```
- Run : node version lastest can run with command
```bash
npm start
```

## Deployment

Have Account AWS and setting configuare account in AWS-CLI

### 1. Create Cluster 
```bash
# ARM 
eksctl create cluster --name <cluster-name> --nodes=2 --version=1.3—0 instance-types=t4g.medium --region=us-east-1
#x86/x64
eksctl create cluster --name <cluster-name> --nodes=2 --version=1.3—0 instance-types=t2.medium --region=us-east-1
```
### 2. Create Role
```base
aws iam create-role --role-name <role-name> --assume-role-policy-document file://trust.json --output text --query 'Role.Arn'
```

### 3. Authorize the CodeBuild using EKS RBAC

#### 3.1. Fetch - Get the current configmap and save it to a file
```bash
# Mac/Linux - The file will be created at `/System/Volumes/Data/private/tmp/aws-auth-patch.yml` path
kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
# Windows - The file will be created in the current working directory
kubectl get -n kube-system configmap/aws-auth -o yaml > aws-auth-patch.yml
```

#### 3.2. Edit - Open the aws-auth-patch.yml file using any editor, such as VS code editor
```bash
# Mac/Linux
code /System/Volumes/Data/private/tmp/aws-auth-patch.yml
# Windows
code aws-auth-patch.yml
```

#### 3.3 Edit  aws-auth-patch.yml
Add the following group in the data → mapRoles section of this file. YAML is indentation-sensitive, therefore refer to the snapshot below for a correct indentation:
```bash
   - groups:
       - system:masters
     rolearn: arn:aws:iam::<ACCOUNT_ID>:role/UdacityFlaskDeployCBKubectlRole
     username: build 
```

#### 3.4. Update - Update your cluster's configmap
```bash
# Mac/Linux
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
# Windows
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat aws-auth-patch.yml)"
```

#### 3.5. Check the health of your clusters nodes
```bash
kubectl get nodes
```

### 4. Create stack CodeBuild and CodePipeline

#### 4.1. Modify temple
- Open temple file `./AWS/ci-cd-codepipeline.cfn.yml`
- Modify:
```yaml
Parameters:
  EksClusterName:
    Default: <ClusterName>
  GitSourceRepo:
    Default: <Repo_Git_Name>
  GitBranch:
    Default: <Git_Branch>
  GitHubUser:
    Default: <Git_Name>
  CodeBuildDockerImage:
    Default: aws/codebuild/standard:4.0 #change if need
  KubectlRoleName:
    Default: <Role_Name> # role-name create in Step 2 of Deployment
```
#### 4.2. Create Stack
Use the AWS web-console to create a stack for CodePipeline using the CloudFormation template file ci-cd-codepipeline.cfn.yml. Go to the <a href="https://us-east-2.console.aws.amazon.com/cloudformation/" target="_blank">CloudFormation service</a> in the AWS console. Press the `Create Stack` button. It will make you go through the following three steps -

#### 4.3. Configuring `buildspec.yml`

## Authentication

This API uses Auth0 for authentication and authorization. You'll need to set up an Auth0 application and configure the appropriate environment variables ([see step 4 above](###-4.-Set-up-environment-variables:)).

You can you with .env in repo and login with account:
- `Admin`: Full permission
```yaml
Email: admin@dev.com
Password: Xopru6-xesquj-kaqgef
```
- `Viewer`: With permission View
```yaml
Email: viewer@dev.com
Password: bocmyk-9kYrki-zokqef
```

## API Endpoints and RBAC

Most endpoints require authentication using a JSON Web Token (JWT). You'll need to include a valid JWT in the Authorization header of your requests. The JWT should be in the format "Bearer <your_jwt>".

### Error Handling

The API returns standard HTTP status codes to indicate the success or failure of requests. Common error codes include:

- `400 Bad Request`: The request was invalid or malformed.
- `401 Unauthorized`: The request lacked valid authentication credentials.
- `404 Not Found`: The requested resource was not found.
- `405 Method Not Allowed`: The requested HTTP method is not supported for the endpoint.
- `422 Unprocessable Entity`: The request was well-formed but unable to be followed due to semantic errors.
- `500 Internal Server Error`: An unexpected error occurred on the server.

### Endpoints

#### GET /products
- Fetches a list of all products.
- For each product, it includes the product ID, name, and the number of associated serial numbers.
- Requires authentication: No

#### GET /products/<id>
- Retrieves details of a specific product by its ID.
- Includes the product name and a list of all associated serial numbers (IMEIs).
- Requires authentication: Yes (requires 'get:products-detail' permission)

#### POST /products
- Creates a new product.
- Requires a JSON body with the product name (e.g., {"name": "Product X"}).
- Returns the details of the newly created product.
- Requires authentication: Yes (requires 'post:products' permission)

#### PATCH /products/<id>
- Updates an existing product by its ID.
- Requires a JSON body with the fields to update (e.g., {"name": "New Product Name"}).
- Returns the details of the updated product.
- Requires authentication: Yes (requires 'patch:products' permission)

#### DELETE /products/<id>
- Deletes a product by its ID.
- Returns the ID of the deleted product.
- Requires authentication: Yes (requires 'delete:products' permission)

#### POST /CreateProducts
- Creates a new product and associated serial numbers (IMEIs).
- Requires a JSON body with the product name and an array of IMEIs (e.g., {"name": "Product Z", "imeis": ["123456789012345", "987654321098765"]}).
- Returns the details of the created product and the successfully created serial numbers.
- Requires authentication: Yes (requires 'post:products' permission)

