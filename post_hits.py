import os
#import setup
from flask import Flask, render_template, url_for, request, make_response
import boto3
from dotenv import load_dotenv
#from boto.mturk.connection import MTurkConnection
#from boto.mturk.question import ExternalQuestion
#from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
#from boto.mturk.price import Price

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

#Start Configuration Variables
AWS_ACCESS_KEY_ID = os.getenv('KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('SECRET_KEY')
DEV_ENVIROMENT_BOOLEAN = True
DEBUG = True
#End Configuration Variables

#This allows us to specify whether we are pushing to the sandbox or live site.
if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
else:
    AMAZON_HOST = "https://mturk-requester.us-east-1.amazonaws.com"

connection = boto3.client('mturk',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
        endpoint_url=AMAZON_HOST)

#5 cents per HIT
amount = 0.05

#frame_height in pixels
frame_height = 800

#Here, I create two sample qualifications
#qualifications = Qualifications()
#qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="90"))
#qualifications.add(NumberHitsApprovedRequirement(comparator="GreaterThan", integer_value="100"))

#This url will be the url of your application, with appropriate GET parameters
url = "https://salty-journey-20160.herokuapp.com/"
questionform = open(file='questions.xml',mode='r').read()

#questionform = boto3.question.ExternalQuestion(url, frame_height)
create_hit_result = connection.create_hit(
    Title="Annotate this monologue",
    Description="Annotate a monologue",
    Keywords="annotation, languages, ML",
    #duration is in seconds
    LifetimeInSeconds = 60*60,
    #max_assignments will set the amount of independent copies of the task (turkers can only see one)
    MaxAssignments=15,
    Question=questionform,
    Reward='0.15',
    AssignmentDurationInSeconds = 600,
    AutoApprovalDelayInSeconds = 14400,
     #Determines information returned by method in API, not super important
    #response_groups=('Minimal', 'HITDetail'),
    #qualifications=qualifications,
)
print ("A new HIT has been created. You can preview it here:")
print ("https://workersandbox.mturk.com/mturk/preview?groupId=" + create_hit_result['HIT']['HITGroupId'])
print ("HITID = " + create_hit_result['HIT']['HITId'] + " (Use to Get Results)")
