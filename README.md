# Planka Webhook Notification

Simple webhook to send notification from [Planka](https://github.com/plankanban/planka) to Telegram and Matrix bot with custom notification. 

## Item Requirements
- API Token of Telegram bot account
- Matrix account with credential token and password

## Usage
```bash
# Install dependencies 
pip install -r requirements.txt

# copy config file
cp sample-config.json config.json

```

Update the config.json base your account information. To run the webhook; 

```bash
python plankabot.py
```

By default this script will run in `localhost:3003/webhook`. Just set the webhook URL and secret key in planka env you should get notification both in Telegram or Matrix if the config set as true.

