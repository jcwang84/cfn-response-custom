
import json
import urllib3


SUCCESS = "SUCCESS"
FAILED = "FAILED"

def send(event, context, response_status, response_data, physical_resource_id=None, no_echo=False): #pylint: disable = R0913
    """code for cfnresponse module, unable to import if source code from s3 bucket

        Args:
            event, context, response_status, response_data, physical_resource_id=None, no_echo=False

        Returns:
            None

        Raises:
            None
    """
    response_url = event['ResponseURL']
    http = urllib3.PoolManager()
    print(response_url)

    response_body = {}
    response_body['Status'] = response_status
    response_body['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    response_body['PhysicalResourceId'] = physical_resource_id or context.log_stream_name
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['NoEcho'] = no_echo
    response_body['Data'] = response_data

    json_response_body = json.dumps(response_body)

    print("Response body:\n" + json_response_body)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_response_body))
    }

    try:
        response = http.request('PUT',
                                response_url,           # pylint: disable = E1101
                                body=json_response_body,
                                headers=headers)
        print(f'Status code: {response.status}')
    except Exception as e:  # pylint: disable = W0703 , C0103
        print(f'send(..) Fail: {e}')
