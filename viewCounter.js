
AWS.config.update({
    region: "eu-west-1", 
    credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: "eu-west-1:64f1cd95-58cf-4e40-b40a-0f6511a6d1c2",
    }),
});


const docClient = new AWS.DynamoDB.DocumentClient();


function getViewCount() {
    const params = {
        TableName: "CVViewCount",   
    };


    docClient.scan(params, function(err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
            document.getElementById("view-count").innerText = "Error loading view count";
        } else {
            console.log("DynamoDB Scan Result:", JSON.stringify(data, null, 2)); 

            if (data.Items && data.Items.length > 0) {
               
                const firstItem = data.Items[0]; 
                console.log("First item:", JSON.stringify(firstItem, null, 2)); 

                if (firstItem.views) {
                    const viewCount = parseInt(firstItem.views, 10);  
                    if (!isNaN(viewCount)) {
                        document.getElementById("view-count").innerText = viewCount || "View count not found";
                    } else {
                        console.error("Invalid view count value.");
                        document.getElementById("view-count").innerText = "View count not found";
                    }
                } else {
                    console.error("View count not found in the first item.");
                    document.getElementById("view-count").innerText = "View count not found";
                }
            } else {
                console.error("No items found in DynamoDB.");
                document.getElementById("view-count").innerText = "View count not found";
            }
        }
    });
}


window.onload = getViewCount;
