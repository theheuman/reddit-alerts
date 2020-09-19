# Reddit Alerts
The end goal of this project is to push out alerts to an android app when a new post is posted in a specific subreddit
(buildapcsales) because I don't trust the ones on the market and I want more options to filter by (like flairs)

It could potentially turn into a [cloudwatch lambda project](https://medium.com/better-programming/cron-job-patterns-in-aws-126fbf54a276)

## TODO
- move to database?
- add firebase
- create ionic app with android

## Development
This is a python project, create your virtual environment and 

    pip install requirements.txt
    
Then run

    pre-commit install
    
Which will install the following three pre-commit hooks

 - black
 - custom code tester and coverage checker
 
This will ensure no broken code is submitted, make sure to write tests for code you write!

