AWS.config.update({
    region: "eu-west-1",
    credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: awsConfig.cognito.identityPoolId,
    }),
});

const docClient = new AWS.DynamoDB.DocumentClient();

/**
 * Retrieve the current view count from DynamoDB and update the HTML element with the count.
 * If there is an error or no count is found, display an error message.
 */
function getViewCount() {
    const params = {
        TableName: "VisitorCountTable",  
        Key: {
            "id": "viewcount"  
        }
    };

    docClient.get(params, function(err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
            document.getElementById("view-count").innerText = "Error loading view count";
        } else {
            console.log("DynamoDB Get Item Result:", JSON.stringify(data, null, 2));

            if (data.Item && data.Item.count) {  
                const viewCount = parseInt(data.Item.count, 10); 
                if (!isNaN(viewCount)) {
                    document.getElementById("view-count").innerText = viewCount || "View count not found";
                } else {
                    console.error("Invalid view count value.");
                    document.getElementById("view-count").innerText = "View count not found";
                }
            } else {
                console.error("Count not found in the item.");
                document.getElementById("view-count").innerText = "View count not found";
            }
        }
    });
}

window.onload = getViewCount;



fetch(awsConfig.apiGateway.endpoint, {
    method: 'GET', 
})
.then(response => response.json())
.then(data => {
    console.log('Lambda function invoked:', data);  
})
.catch(error => {
    console.error('Error invoking Lambda:', error);  
});

