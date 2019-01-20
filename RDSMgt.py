import json
import boto3
import os

rds = boto3.client('rds')
aws_region = os.environ['AWS_REGION']
sts = boto3.client("sts")
aws_account = sts.get_caller_identity()["Account"]

def lambda_handler(event, context):
	if event['action'] == "start" :
		startRDSInstances()
	elif event['action'] == "stop" :
		stopRDSInstances()
	else:
		print(event['action'] + ' is not valid action.')

def skipRDSInstance(rdsDBInstance):
	rdsInstanceARN = 'arn:aws:rds:' + aws_region + ':' + aws_account + ':db:' + rdsDBInstance['DBInstanceIdentifier']
	rdsInstanceTags = rds.list_tags_for_resource(ResourceName=rdsInstanceARN)
	for tag in rdsInstanceTags['TagList'] :
		if tag['Key'] == "opt-in" and tag['Value'] == "auto-restart" :
			return False
	return True

def stopRDSInstances():
	rdsInstances = rds.describe_db_instances()
	for rdsInstance in rdsInstances['DBInstances'] :
		if skipRDSInstance(rdsInstance) == False :
			stopRDSInstance(rdsInstance)
		
def startRDSInstances():
	rdsInstances = rds.describe_db_instances()
	for rdsInstance in rdsInstances['DBInstances'] :
		if skipRDSInstance(rdsInstance) == False :
			startRDSInstance(rdsInstance)
		
def stopRDSInstance(rdsDBInstance):
	if rdsDBInstance['DBInstanceStatus'] == "available" :
		print('Stop=' + rdsDBInstance['DBInstanceIdentifier'])
		rds.stop_db_instance(DBInstanceIdentifier=rdsDBInstance['DBInstanceIdentifier'])

def startRDSInstance(rdsDBInstance):
	if rdsDBInstance['DBInstanceStatus'] == 'stopped' :
		print('Start=' + rdsDBInstance['DBInstanceIdentifier'])
		rds.start_db_instance(DBInstanceIdentifier=rdsDBInstance['DBInstanceIdentifier'])
