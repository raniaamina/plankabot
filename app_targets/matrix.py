import requests
import json

def send_matrix_message(message, config):
    send_message_url = f"{config['host']}/_matrix/client/r0/rooms/{config['room_id']}/send/m.room.message"
    
    message_payload = {
        "msgtype": "m.text",  
        "body": message 
    }

    headers = {
        "Authorization": f"Bearer {config['token']}",  
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(send_message_url, json=message_payload, headers=headers)
        

        if response.status_code == 200:
            return True
        else:
            logging.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error while sending message: {str(e)}")
        return False
