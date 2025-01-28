#!/bin/bash
STACK_NAME="Test-CV-Challenge"
S3_STACK_NAME="Test-CV-Bucket"
S3_BUCKET="alisam-test-cv-bucket" #<--- ADD YOUR OWN UNIQUE NAME

# Step 1: Deploy S3 bucket first
aws cloudformation deploy \
    --template-file s3-bucket.yaml \
    --stack-name $S3_STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides S3BucketName=$S3_BUCKET

# Step 2: Wait for the S3 bucket stack to be created
echo "Waiting for S3 stack to be created..."
aws cloudformation wait stack-create-complete --stack-name $S3_STACK_NAME
echo "S3 stack created successfully!"

# Step 3: Upload necessary files to S3
aws s3 cp ../index.html s3://$S3_BUCKET/
aws s3 cp ../viewCounter.js s3://$S3_BUCKET/
aws s3 cp ../lambda_function.zip s3://$S3_BUCKET/

# Step 4: Deploy the rest of the infrastructure
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides S3BucketName=$S3_BUCKET

# Step 5: Wait for the main stack to be created
echo "Waiting for main CloudFormation stack to be created..."
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
echo "Main stack created successfully!"

# Step 6: Get output values
IDENTITY_POOL_ID=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='CognitoIdentityPoolId'].OutputValue" --output text)
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='APIGatewayEndpoint'].OutputValue" --output text)
DYNAMO_TABLE=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='DynamoDBTableName'].OutputValue" --output text)

# Step 7: Generate config.js
cat <<EOF > ../config.js
window.awsConfig = {
    region: "eu-west-1",
    cognito: {
        identityPoolId: "$IDENTITY_POOL_ID"
    },
    dynamoDB: {
        tableName: "$DYNAMO_TABLE",
        partitionKey: "id"
    },
    apiGateway: {
        endpoint: "$API_ENDPOINT"
    }
};
EOF

# Step 8: Upload the updated config.js
aws s3 cp ../config.js s3://$S3_BUCKET/

echo "Deployment complete!"
