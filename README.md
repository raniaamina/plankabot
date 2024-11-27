# Planka Webhook Notification

Simple webhook to send notification from [Planka](https://github.com/plankanban/planka) to Telegram and Matrix bot with custom notification (maybe will add more if needed). 

## Item Requirements
- API Token of Telegram bot account
- Matrix account with credential token and password
- Planka service ofc :")

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

You can customize the message by editting this part in `plankabot.py`

```python
# Message Format
    format_message = (
        f"{eventInfo} by {username} \n"
        f"{item_name} in {project_name} updated to {current_list_name}\n\n"
        f"Details: ({project_url})"
    )
```

