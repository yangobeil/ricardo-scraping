# Ricardo scraper

Code to find new recipes on Ricardo and send an email with the new ones. This is used to check weekly with the cron on a rasberry pi.

Don't forget to do
```
pip install requirements.txt
```

Need to have a .env file with the following variables:
- SENDER_EMAIL_ADDRESS
- SENDER_EMAIL_PASSWORD
- RECEIVER_EMAIL_ADDRESS

To set a cron task on the raspberry pi, follow these steps:
1. 