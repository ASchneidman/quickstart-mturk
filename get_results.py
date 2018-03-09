import boto3
import time
import os
from dotenv import load_dotenv
import sys

def get_res(hit_id):
    # load dotenv in the base root
    APP_ROOT = os.path.join(os.path.dirname(__file__), '')   # refers to application_top
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    #Start Configuration Variables
    AWS_ACCESS_KEY_ID = os.getenv('KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('SECRET_KEY')

    MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    MTURK_PROD = 'https://mturk-requester.us-east-1.amazonaws.com'
    mturk = boto3.client('mturk',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        region_name = 'us-east-1',
        endpoint_url = MTURK_SANDBOX,
    )

    # You will need the following library
    # to help parse the XML answers supplied from MTurk
    # Install it in your local environment with
    # pip install xmltodict
    import xmltodict
    # Use the hit_id previously created
    #hit_id = '306W7JMRYZ47I0WXQL8LU7LRI3AB8A'
    # We are only publishing this task to one Worker
    # So we will get back an array with one item if it has been completed
    worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])
    while (worker_results['NumResults'] <= 0):
        print("No results found, waiting 1 min then checking results")
        time.sleep(60)
        worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])
        print("Checking results")

    if worker_results['NumResults'] > 0:
       for assignment in worker_results['Assignments']:
          xml_doc = xmltodict.parse(assignment['Answer'])

          print ("Worker's answer was:")
          if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
             # Multiple fields in HIT layout
             for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                print ("For input field: " + answer_field['QuestionIdentifier'])
                print ("Submitted answer: " + answer_field['FreeText'])
          else:
             # One field found in HIT layout
             print ("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
             print ("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
    else:
       print ("No results ready yet")

if __name__ == "__main__":
    input = sys.argv[1]
    id = str(input)
    get_res(id)
