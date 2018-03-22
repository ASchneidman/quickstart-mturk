import os
#import setup
from flask import Flask, render_template, url_for, request, make_response
import boto3
from dotenv import load_dotenv
import psycopg2
import secrets
import xml.etree.cElementTree as ET

from oauth2client.tools import argparser


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
conn = None
try:
    conn = psycopg2.connect(
            dbname="sqa_data",
            user="sqa_downloader",
            host="localhost",
            password=secrets.DB_PW)
except psycopg2.OperationalError as e:
        print('Unable to connect!\n{0}').format(e)
        sys.exit(1)
cur = conn.cursor()
conn.autocommit = True
cur.execute("SELECT video_id FROM youtube_data LIMIT 10;")
ids = [e[0] for e in cur.fetchall()]

#5 cents per HIT
amount = 0.05

#frame_height in pixels
frame_height = 800

for id in ids:

    #This url will be the url of your application, with appropriate GET parameters
    url = ("https://salty-journey-20160.herokuapp.com/?video=" + str(id))
    #Generate xml file
    root = ET.Element("ExternalQuestion", xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd")
    ET.SubElement(root, "ExternalURL").text = url
    ET.SubElement(root, "FrameHeight").text = str(frame_height)

    tree = ET.ElementTree(root)
    tree.write("question.xml")
    #Here, I create two sample qualifications
    #qualifications = Qualifications()
    #qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="90"))
    #qualifications.add(NumberHitsApprovedRequirement(comparator="GreaterThan", integer_value="100"))

    questionform = open(file='question.xml',mode='r').read()

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
