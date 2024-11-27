from flask import Flask, request, jsonify
import json
import requests
from app_targets.telegram import send_telegram_notification
from app_targets.matrix import send_matrix_message
from utils import get_list_name


app = Flask(__name__)

# Load config from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

planka_config = config['planka']

if config['telegram']['enable'] == True:
    print('[ ✅ ] Telegram Notification')
    telegram_config = config['telegram']
    enableTelegram = True
else:
    print('[ ❌ ] Telegram Notification')
    enableTelegram = False

if config['matrix']['enable'] == True:
    print('[ ✅ ] Matrix Notification')
    matrix_config = config['matrix']
    enableMatrix = True
else:
    print('[ ❌ ] Matrix Notification')
    enableMatrix = False

routPath = config['bot']['route']
@app.route("/"+routPath, methods=["POST"])
def webhook():
    print("Webhook called")
    print("Headers:", request.headers)

    token = request.headers.get("Authorization")
    if token != f"Bearer {planka_config['access_token']}":
        print("Invalid token:", token)
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        print("Invalid payload")
        return jsonify({"error": "Invalid payload"}), 400

    # print("Received payload:", data)

    # Extract main info
    event_type = data.get("event")
    if event_type == 'cardCreate':
        eventInfo = "Kartu Baru"
    if event_type == 'cardUpdate':
        eventInfo = "Update kartu"
    if event_type == 'cardDelete':
        eventInfo = "Hapus kartu"

        
    item = data.get("data", {}).get("item", {})
    prev_item = data.get("prevData", {}).get("item", {})
    included = data.get("data", {}).get("included", {})
    user = data.get("user", {})

    # Project information
    project = next(iter(included.get("projects", [])), {})
    project_name = project.get("name")
    lists = included.get("lists", [])
    board_id = item.get("boardId")
    project_url = f"{planka_config['base_url']}/boards/{board_id}"

    # Update information
    current_list_id = item.get("listId")
    previous_list_id = prev_item.get("listId")

    # Get Before After
    previous_list_name = get_list_name(lists, previous_list_id)
    current_list_name = get_list_name(lists, current_list_id)

    updated_at = item.get("updatedAt")
    username = user.get("name")
    item_name = item.get("name", "Unknown Item")

    # Message Format
    format_message = (
        f"{eventInfo} by {username} \n"
        f"{item_name} in {project_name} updated to {current_list_name}\n\n"
        f"Details: ({project_url})"
    )

    if enableTelegram:
        # Send notif to Telegram
        telegram_sent = send_telegram_notification(format_message, config["telegram"]["bot_token"], config["telegram"]["chat_id"])
        if telegram_sent:
            print("Update sent successfully to Telegram.")
        else:
            print("Failed to send notification to Telegram.")
        return jsonify({"status": "success"}), 200

    if enableMatrix:
        # Send notif to Matrix
        matrix_sent = send_matrix_message(format_message, matrix_config)
        if matrix_sent:
            print("Update sent successfully to Matrix.")
        else:
            print("Failed to send notification to Telegram.")

        return jsonify({"status": "success"}), 200



if __name__ == "__main__":
    print("Starting webhook server...")
    app.run(debug=False, host='0.0.0.0', port=config['bot']['port'])
