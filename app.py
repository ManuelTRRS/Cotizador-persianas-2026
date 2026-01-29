from flask import Flask,render_template, request

app = Flask(__name__)

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

if (__name__ == '__main__'):
    app.run(debug=True)