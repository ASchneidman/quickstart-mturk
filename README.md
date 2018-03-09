# quickstart-mturk
The easiest way to start developing with Amazon Mechanical Turk (mturk), using Flask and boto3.
# Purpose
To easily start developing crowdsourcing tasks without going from blogpost to blogpost. Note that the entire assignment is yours to create via HTML/CSS/JS, so the possibilities are endless.  
# General flow
* Register on mturk.com and https://requester.mturk.com/developer/sandbox
* Create your HIT in page.html
* Deploy to heroku (or your choice of hosting service)
* Set heroku environment variables KEY and SECRET_KEY to your amazon key and secrety key
* Create .env file in project directory, define KEY=<your key> and SECRET_KEY=<your secret key> on seperate lines (make sure to add .env to .gitignore)
* Edit and execute python post_hits.py. This will give you a link to your HIT in sandbox mode where you can complete it and a key to access the results
* Run python get_results.py <HIT ID> to get the results of the hit (can be automated)

# To deploy via Heroku
Download the heroku toolbelt, login, run 'heroku create' in the directory, and add, commit and push the code to the heroku repository created via 'git push heroku master'.
# To make HITs
Update the url variable in post_hits.py to correctly point to your application and then execute post_hits.py
