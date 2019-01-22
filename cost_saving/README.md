Serverless-python based Lambda to save usage cost of RDS DB Instances as well as EC2 Instances.

These Lambda functions are using AWS SDK for python, provided by AWS itself.

If you want to opt-in selected EC2 and RDS DB instances for cost saving, you just need to add following tag to EC2 and/ RDS DB instance. 
Then, the scheduled execution of Lambda will take care of the rest.

To schedule execution of Lambda, you can user AWS cloud watch event rules feature. 

1) EC2Management - Takes of changing EC2 state as well as change in auto-scaling groups, if applicable.
2) RDSManagement - Takes of changing RDSDB Instance state.

To test these Lambda's you can use following input json;

1) To start instances.
{
  "action": "start"
}

2) To stop instances.
{
  "action": "stop"
}

There are other solutions available provided by AWS itself, but those are requires more AWS resource usage such as DynamoDB as well as less control over the Lambda function code.
