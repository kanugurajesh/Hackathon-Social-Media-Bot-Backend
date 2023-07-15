# import os
# import cohere
# from email.message import EmailMessage
# import ssl
# import smtplib
# import time

# from flask import (Flask, redirect, render_template, request,
#                    send_from_directory, url_for)

# app = Flask(__name__)
# gmate_sender = "gmate4869@gmail.com"
# gmate_password = "flytcvfsbivpaeno"

# @app.route('/')
# def index():
#    print('Request for index page received')
#    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/hello', methods=['POST'])
# def hello():
#    name = request.form.get('name')

#    if name:
#        print('Request for hello page received with name=%s' % name)
#        return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))

# @app.route('/send_email', methods=['POST'])
# def send_email(data):
#     data = request.json()
#     prompt = data.get('message')
#     client = cohere.Client('S3tQc1i6m6N905AO5A85eNzhh8o0qLb4FLdIA9Fu')
#     generated_text = client.generate(prompt)
#     gmate_receiver = "kanugurajesh3@gmail.com"
#     subject = "Email from Gmate"
#     em = EmailMessage()
#     em['Subject'] = subject
#     em['From'] = gmate_sender
#     em['To'] = gmate_receiver
#     em.set_content(str(generated_text[0]))

#     context = ssl.create_default_context()

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(gmate_sender, gmate_password)
#         server.send_message(em)
#         print("Email sent successfully")
#     return {"message": str(generated_text[0])}

# if __name__ == '__main__':
#    app.run()

import os
from email.message import EmailMessage
import ssl
import smtplib
import time
import cohere

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)
gmate_sender = "gmate4869@gmail.com"
gmate_password = "flytcvfsbivpaeno"

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
    client = cohere.Client('S3tQc1i6m6N905AO5A85eNzhh8o0qLb4FLdIA9Fu')
    data = request.get_json()
    prompt = data.get('message')
    generated_text = client.generate(prompt)
    return {"message": str(generated_text[0])}

@app.route('/send_email', methods=['POST'])
def send_email():
    client = cohere.Client('S3tQc1i6m6N905AO5A85eNzhh8o0qLb4FLdIA9Fu')
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

if __name__ == '__main__':
   app.run()
