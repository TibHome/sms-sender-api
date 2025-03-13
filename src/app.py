from myfunctions import *
from flask import Flask, request, jsonify

ENDPOINT = "http://192.168.0.1"

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send_message():
    
    recipient = request.form.get("recipient")
    message = request.form.get("message")
    
    if not recipient:
        return jsonify({"response": "Error : Recipient missing"}), 400
    
    if not message:
        return jsonify({"response": "Error : Message missing"}), 400
    
    try:
        is_site_accessible()
        login()
        send_sms(recipient, message)
        logout()
        return jsonify({"response": "success"})
    except Exception as e:
        return jsonify({"response": f"Error : {e}"}), 400

if __name__ == '__main__':
    app.run(debug=False)