# Reddit Alerts
The end goal of this project is to push out alerts to an android app when a new post is posted in a specific subreddit
(buildapcsales) because I don't trust the ones on the market and I want more options to filter by (like flairs)

It could potentially turn into a [cloudwatch lambda project](https://medium.com/better-programming/cron-job-patterns-in-aws-126fbf54a276)

## Development
This is a python project, create your virual environment and 

    pip install requirements.txt
    
Then run

    pre-commit install
    
To install the following three pre-commit hooks

 - black
 - code coverage
 - code coverage report
 
This will ensure no broken code is submitted, make sure to write tests!

