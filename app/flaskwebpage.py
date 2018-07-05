# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, json
import sys, os, traceback
from flask_mail import Mail, Message

current_directory = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    try:
        return render_template('index.html')
    except:
        return get_exception()


@app.route("/sobre-nosotros")
def bussines():
    return render_template('empresa.html')

@app.route("/contactanos")
def contactus():
    return render_template('contactanos.html')

@app.route("/servicio-a-domicilio")
def delivery():
    return render_template('delivery.html')

@app.route("/alquiler-de-carros-economicos-pequenos")
def smallcars():
    return render_template('smallcars.html')

@app.route("/alquiler-de-carros-medianos-familiares")
def mediumcars():
    return render_template('mediumcars.html')

@app.route("/alquiler-de-camionetas-suv")
def suvcars():
    return render_template('suvcars.html')

# Route to send contact Email
@app.route("/enviarmensaje", methods=['POST'])
def sendmail():
    # #Read values from UI
    _name = request.form['name']
    _email = request.form['email']
    _phone =  request.form['phone']
    _cartype = request.form['cartype']
    _message = request.form['message']

    err_str='<span>Mensaje no enviado, completa correctamente los campos</span>'
    ok_str='1'

    if _name and _email and _phone and _message:
        # White email content
        body_email = """
        Datos de la persona interesada en el servicio de alquiler de carros
        Nombre: {tname}
        Email: {temail}
        Telefono: {tphone}
        Tipo de carro de interes: {tcartype}
        Mensaje: {tmessage}
        """.format(tname= _name, temail= _email, tphone=_phone, tcartype=_cartype, tmessage=_message)
        # Send email
        gomail(body_message=body_email)
        # Return email response
        return json.dumps({'html':ok_str})
    else:
        return json.dumps({'html':err_str})

def gomail(body_message):
    mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'rayther.rentacar@gmail.com',
    "MAIL_PASSWORD": 'Rentacar73'
    }
    app.config.update(mail_settings)
    mail = Mail(app)
    msg = Message(
        body=body_message,
        subject="Notificacion de la web",
        sender="rayther.rentacar@gmail.com",
        recipients=["rayther.rentacar@gmail.com", "info@rayther.com", "teresa_avella@hotmail.com", "javierriatiga@yahoo.com"])
    mail.send(msg)


#Shows the public IP and etho0 IP of the machine (good for validation, e.g. load balancing)
@app.route("/ip_address")
def ip_address():
    try:
        from urllib2 import urlopen
        public_ip = urlopen('http://ipv4.icanhazip.com').read().strip()
        container_ip = os.popen(''' ip addr show eth0 | grep "inet" | awk '{print $2}' | cut -d/ -f1 | cut -d$'\n' -f 1''').read().strip()
        return '''
Public IP: {public_ip} <br>
Container IP: {container_ip}
'''.format(public_ip=public_ip, container_ip=container_ip)
    except:
        return get_exception()


#Letsencrypt certbot
@app.route('/.well-known/acme-challenge/<token_value>')
def letsencrpyt(token_value):
    try:
        with open('{current_directory}/.well-known/acme-challenge/{token_value}'.format(current_directory=current_directory, token_value=token_value)) as f:
            answer = f.readline().strip()
        return str(answer)
    except:
        return get_exception()


#Displays the 500 error
@app.errorhandler(500)
def get_500_error(error):
    try:
        return "500 error - %s" % (error)
    except:
        return get_exception()


#Gets a client's IP address
def get_client_ip():
    'Gets client IP from xforward for or remote address if not proxied'
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def get_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return '''
Python Version: {version}
File: {file_name}
Error Type: {error_type}
Error Message: {error_message}
Traceback:
{traceback}
         '''.format(
                    version =sys.version.split("(")[0],
                    file_name = fname,
                    error_type = exc_type.__name__,
                    error_message = exc_obj,
                    traceback = traceback.format_exc().replace(", in ",", in \n"),
                    )
