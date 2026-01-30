from flask import Flask, render_template, request, make_response, session
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado=None
    if request.method == 'POST':
        Ancho=float(request.form['Ancho'])
        Alto=float(request.form['Alto'])
        m2=500
        total=Ancho*Alto*m2
        resultado=total

        pass
    return render_template('index.html', resultado_cotizacion=resultado)


@app.route('/enviar', methods=['POST'])
def enviar_cotizacion():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        email = request.form.get('E-mail')
        ancho = request.form.get('ancho_envio')
        alto = request.form.get('alto_envio')
        precio = request.form.get('precio_envio')

        contenido = f"""
Datos de la Cotización:

Cliente: {nombre}
Teléfono: {telefono}
Email: {email}

Medidas:
Ancho: {ancho} metros
Alto: {alto} metros

Precio Final: ${precio}
        """

        mi_correo = os.getenv('EMAIL_USER')
        mi_contraseña = os.getenv('EMAIL_PASSWORD')
        
        mensaje = MIMEText(contenido)
        mensaje['Subject'] = "Nueva Cotización de Cliente"
        mensaje['From'] = mi_correo
        mensaje['To'] = mi_correo  # Cambiado: ahora te llega a ti

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mi_correo, mi_contraseña)
        server.send_message(mensaje)
        server.quit()

        # Guardar datos en session
        session['nombre'] = nombre
        session['telefono'] = telefono
        session['email'] = email
        session['ancho'] = ancho
        session['alto'] = alto
        session['precio'] = precio

        return render_template('exito.html', nombre=nombre, telefono=telefono, email=email, ancho=ancho, alto=alto, precio=precio)

    except Exception as e:
        return f"Error al enviar: {str(e)}", 500


@app.route('/descargar_cotizacion')
def descargar_cotizacion():
    nombre = session.get('nombre', '')
    telefono = session.get('telefono', '')
    email = session.get('email', '')
    ancho = session.get('ancho', '')
    alto = session.get('alto', '')
    precio = session.get('precio', '')

    contenido = f"""COTIZACIÓN DE PERSIANAS
{'='*50}

Datos del Cliente:
Nombre: {nombre}
Teléfono: {telefono}
Email: {email}

Medidas:
Ancho: {ancho} metros
Alto: {alto} metros

Precio Final: ${precio}
{'='*50}

Gracias por su preferencia.
"""

    response = make_response(contenido)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=cotizacion_{nombre.replace(" ", "_")}.txt'
    return response

if __name__ == '__main__':
    app.run(debug=True)