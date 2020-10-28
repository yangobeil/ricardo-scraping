# Ricardo scraper

Code to find new recipes on Ricardo and send an email with the new ones. This is used to check weekly with heroku's scheduler.

Need to have a .env file with the following variables:
- SENDER_EMAIL_ADDRESS
- SENDER_EMAIL_PASSWORD
- RECEIVER_EMAIL_ADDRESS
- MONGO_USERNAME
- MONGO_PASSWORD