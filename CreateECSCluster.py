import logging
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    return dispatch(event)

def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'CreateCluster':
        return create_cluster(intent_request)
        
    raise Exception('Intent with name ' + intent_name + ' not supported')

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def create_cluster(intent_request):
    clusterName = get_slots(intent_request)["clusterName"]
    noOfInstances = get_slots(intent_request)["numberOfInstances"]
    return trigger_pipeline(cluster_name,noOfInstances, intent_request)
    
def trigger_pipeline(clusterName, noOfInstances, intent_request):
    result = subprocess.call("curl -k -X POST -F token=xxxxxxxxxxxxxxxx -F variables[ECS_CLUSTER_NAME]="+ clusterName +" -F variables[NO_OF_ECS_INSTANCES]=" + noOfInstances +  " -F ref=master https://xxx.aws.xxx/api/v4/projects/xxx/trigger/pipeline", shell=True)
    return close({'contentType': 'PlainText','content': result}, intent_request)

def close(message, intent_request):
    response = {
        'sessionAttributes': intent_request['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': message
        }
    }
    return response
