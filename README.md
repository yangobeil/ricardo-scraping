# Ricardo scraper

Code to find new recipes on Ricardo and send an email with the new ones. This is used to check weekly with heroku's scheduler.

Need to have a .env file with the following variables:
- SENDER_EMAIL_ADDRESS
- SENDER_EMAIL_PASSWORD
- RECEIVER_EMAIL_ADDRESS
- MONGO_USERNAME
- MONGO_PASSWORD

The email part is inspired by [this](https://realpython.com/python-send-email/) and the heroku scheduler 
by [this](https://medium.com/analytics-vidhya/schedule-a-python-script-on-heroku-a978b2f91ca8).