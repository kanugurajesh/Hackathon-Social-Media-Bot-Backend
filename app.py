import os
from email.message import EmailMessage
import ssl
import smtplib
import cohere
from twilio.rest import Client
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)
gmate_sender = "ge49@gmail.com"
gmate_password = "flcvfsvpaeno"
account_sid = 'Aa26c88efdb819e4b0065e'
auth_token = 'bdcd466878bf8f12d7b1c'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name=name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/respond', methods=['POST'])
def respond():
    client = cohere.Client('S3tQc1i346N45O5A85eNzhh8o0qLb4FLdIA9')
    data = request.get_json()
    prompt = data.get('message')
    generated_text = client.generate(prompt)
    return {"message": str(generated_text[0])}

@app.route('/send_email', methods=['POST'])
def send_email():
    client = cohere.Client('S3tQc1i6m6N9022O5A85e5678hh8oLb4dIA9Fu')
    data = request.get_json()
    prompt = data.get('message')
    generated_text = client.generate(prompt)
    gmate_receiver = data.get('gmail')
    subject = "Email from Gmate"
    em = EmailMessage()
    em['Subject'] = subject
    em['From'] = gmate_sender
    em['To'] = gmate_receiver
    em.set_content(str(generated_text[0]))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(gmate_sender, gmate_password)
        server.send_message(em)
        print("Email sent successfully")
    return {"message": str(generated_text[0])}

@app.route('/send_whatsapp', methods=['POST'])
def send_whatapp():
    cohere_client = cohere.Client('S3tQc1i6m5AA85eNzhh0qLb4FIA9Fu')
    data = request.get_json()
    number = data.get('whatsapp')
    client = Client(account_sid, auth_token)
    body = cohere_client.generate(data.get('message'))[0]
    message = client.messages.create(
    from_='whatsapp:+147532386883',
    body=body,
    to=f'whatsapp:{number}'
    )
    return {"message": str(body)}
@app.route('/send_sms', methods=['POST'])
def send_sms():
    cohere_client = cohere.Client('S3tQc1m6N905AO5A85eNh8o0b4dIFu')
    data = request.get_json()
    number = data.get('sms')
    client = Client(account_sid, auth_token)
    body = cohere_client.generate(data.get('message'))[0]
    message = client.messages.create(
    from_='+15739203473',
    body=body,
    to=f'{number}'
    )
    return {"message": str(body)}

if __name__ == '__main__':
   app.run()
