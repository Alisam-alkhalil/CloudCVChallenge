# [VIEW IT HERE](https://alisamalkhalil.online) <sub>*(Test view counter at the bottom of the screen by refreshing the page.)*</sub>


# My Cloud CV Challenge

## Introduction / Overview

This project is a dynamic online CV hosted on AWS. It uses a serverless architecture to ensure fast loading, security, and real-time updates. The frontend, built with HTML and JavaScript, is hosted on **Amazon S3** and distributed globally via **CloudFront** for fast loading and enhanced security (HTTPS and DDoS protection). The backend leverages **AWS Lambda**, **API Gateway**, and **DynamoDB** to power a live visitor counter, which updates dynamically with each page load. **Amazon Cognito** is used for secure user authentication and authorization. The project also includes a CI/CD pipeline using **GitHub Actions** to automate deployments whenever changes are pushed to the repository after completing tests.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [How It Works](#how-it-works)
   - [Frontend](#frontend)
   - [API Gateway](#api-gateway)
   - [Lambda](#lambda)
   - [DynamoDB](#dynamodb)
   - [Cognito](#cognito)
   - [CI/CD Pipeline](#ci/cd-pipeline)
3. [How to Deploy](#how-to-deploy)

---

## System Architecture

The architecture consists of the following key components:

- **Amazon S3**: Hosts the static frontend of the website.
- **CloudFront**: Reduces load time and enhances security with HTTPS and DDoS protection.
- **API Gateway**: Handles incoming HTTP requests, routes them to the Lambda function to update the view count.
- **AWS Lambda**: Executes python functions triggered by API Gateway requests, interacting with DynamoDB to update the view count.
- **Amazon DynamoDB**: A NoSQL database that stores the view count.
- **Amazon Cognito**: Provides user authentication and authorisation limited to only query the view count on DynamoDB.
- **GitHub Actions**: Automates deployments whenever changes are pushed to the repository after completing tests.

![System Architecture](./images/architecture.jpg)
---

## How It Works

### Frontend

1. **User Interaction**: A user triggers an HTTP request by refreshing the page or taking any action that requires interaction with the backend.
2. **API Request**: The frontend sends an HTTP request to the **API Gateway**.

### API Gateway

1. **Request Handling**: The **API Gateway** receives the request from the frontend and forwards it to the corresponding **Lambda** function for processing.


### Lambda

1. **Backend Processing**: After authentication, **Lambda** is triggered to execute, which queries the current view count from **DynamoDB** .
2. **Data Handling**: Lambda increases the view count by 1 and updates in the database.

### DynamoDB

1. **Data Storage**: **DynamoDB** stores the viewcount in a table.
2. **Read/Write Operations**: Each page refresh or API request will trigger an update to DynamoDB.

### Cognito

1. **User Authentication**: A guest user on cognito with permissions to only query the view count on DynamoDB is used to access the database through the Javascript file and to update the view count on the html website.

### CI/CD Pipeline

1. **GitHub Actions**: GitHub Actions is used to automate deployments whenever changes are pushed to the repository.
2. **Testing**: The pipeline includes tests to ensure the pipeline functions as expected.
3. **Build and Deploy**: After tests are passed, the pipeline deploys the frontend and backend to the S3 bucket and updates the CloudFront distribution.
4. **Lambda Function**: The Lambda function is updated with any new code changes.

**Example:**
![System Architecture](./images/githubactions.jpg)
---


### How to Deploy

1. **Clone the Repository**: Clone the repository to your local machine.
2. **Set up AWS Credentials**: Set up your AWS credentials using the AWS CLI or through the AWS Management Console by using:

```bash
aws configure
```
3. **Change Directory**: Navigate to the cloudformation folder in the cloned directory using:

```bash
cd cloudformation
```

4. **IMPORTANT! Change Bucket Name**: Edit the **S3_BUCKET** parameter in the **deploy.sh** file to your desired UNIQUE S3 bucket name. If you wish you can also edit the **STACK_NAME** and **S3_STACK_NAME** parameter to your desired UNIQUE stack name.

5. **Create Stack**: Run the following command to create the CloudFormation stack on a bash terminal:

```bash
./deploy.sh
```

6. **View the Site**: Once the stack is deployed, go to CloudFront and view the website at the provided Distribution domain name of the created distribution.

7. **Refresh the Page**: Refresh the page to see the updated view count.


## How to set up CI/CD Pipeline

1. Create an IAM user with these permissions for the Lambda function and S3 bucket.

```bash
"lambda:UpdateFunctionCode",
"lambda:GetFunction",
"lambda:InvokeFunction,
"s3:PutObject",
"s3:DeleteObject",
"s3:GetObject"
```

2. Retrieve the user Access key and Secret key.
On your repository, go to Settings -> Secrets and variables -> Actions -> Add a new secret -> Name: "**ACCESSKEY**" -> Value: "Add your access key" -> Name: "**SECRETKEY**" -> Value: " Add your secret key".

3. Update the S3 bucket name in the **deploy.yml** file located in the .github/workflows folder to your bucket name.

4. Now, you can push to the main branch and the pipeline will deploy the changes to the S3 bucket and update the CloudFront distribution as well as test and deploy the backend code.
