import json
import boto3
import os

ec2 = boto3.client('ec2')
autoScalingClient = boto3.client('autoscaling')
aws_region = os.environ['AWS_REGION']
sts = boto3.client("sts")
aws_account = sts.get_caller_identity()["Account"]
autoSaclingGrpPro = ['Launch',
                'Terminate',
                'HealthCheck',
                'ReplaceUnhealthy',
                'ScheduledActions',
                'AddToLoadBalancer',
                'AlarmNotification',
                'AZRebalance']
tagKey = 'tag:opt-in'
tagVal = 'auto-restart'

def lambda_handler(event, context):
	handleAction(event['action'])
	
def handleAction(action):
    ec2Instances = getEc2InstancesByTag(tagVal)
    autoScalingGrpToResume = set()
    for reservation in ec2Instances['Reservations'] :
        for ec2Instance in reservation['Instances'] :
            autoScalingGroupName=getAutoScalingGroupName(ec2Instance['InstanceId'])
            if action == "stop" :
                suspendProcesses(autoScalingGroupName)
                stopEC2Instance(ec2Instance)
            elif action == "start" :
                autoScalingGrpToResume.add(autoScalingGroupName)
                startEC2Instance(ec2Instance)
    resumeAutoSclGrpProc(autoScalingGrpToResume)
    
def resumeAutoSclGrpProc(autoScalingGrpToResume):
    for autoScalingGrp in autoScalingGrpToResume :
        resumeProcesses(autoScalingGrp)

def suspendProcesses(autoScalingGroupName):
    if autoScalingGroupName != None :
        autoScalingClient.suspend_processes(
        AutoScalingGroupName=autoScalingGroupName,
        ScalingProcesses=autoSaclingGrpPro
        )
        
def getEc2InstancesByTag(tagValue):
    ec2Instances = ec2.describe_instances(
        Filters=[{
            'Name': tagKey,
            'Values': [
                tagValue
                ]
        }]
        )
    return ec2Instances 

def getAutoScalingGroupName(ec2InstanceId):
    autoScalingGrp=autoScalingClient.describe_auto_scaling_instances(
        InstanceIds=[
            ec2InstanceId
            ]
        )
    for autoScalingInstance in autoScalingGrp['AutoScalingInstances'] :
        return autoScalingInstance['AutoScalingGroupName']
    return None

def stopEC2Instance(ec2Instance):
    if ec2Instance['State']['Name'] == 'running' :
        ec2.stop_instances(InstanceIds=[ec2Instance['InstanceId']])

def startEC2Instance(ec2Instance):
    if ec2Instance['State']['Name'] == 'stopped' :
        ec2.start_instances(InstanceIds=[ec2Instance['InstanceId']])

def resumeProcesses(autoScalingGroupName):
    if autoScalingGroupName != None :
        autoScalingClient.resume_processes(
            AutoScalingGroupName=autoScalingGroupName,
            ScalingProcesses=autoSaclingGrpPro
        )