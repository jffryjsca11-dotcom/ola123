from flask import Flask, render_template
import socket

app = Flask(__name__)
HOST = "192.168.100.19"  ## Ip de tu servidor en la VM
PORT = 12345            ## Puerto de la APK

def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            s.connect((HOST, PORT))
            data = s.recv(1024).decode().strip()
            print("RECIBIDO:", data)
            
            ejeX, ejeY = data.split(',')
            ejeX = float(ejeX.replace('X:', ''))
            ejeY = float(ejeY.replace('Y:', ''))
            return ejeX, ejeY
    except Exception as e:
        print("ERROR:", e)
        return 0.0, 0.0

def mapear_a_matriz(valor, min_val=-10.0, max_val=10.0):
    if valor < min_val: valor = min_val
    if valor > max_val: valor = max_val
    proporcion = (valor - min_val) / (max_val - min_val)
    # Mapea a un índice de 0 a 4 (Matriz 5x5)
    return int(proporcion * 4)

@app.route('/')
def index():
    ejeX, ejeY = leer_sensor() 
    
    celda_x = mapear_a_matriz(ejeX)
    celda_y = 4 - mapear_a_matriz(ejeY) # Invertimos Y para que el positivo apunte hacia arriba
    
    return render_template(
        'index.html',
        ejeX=ejeX,
        ejeY=ejeY,
        celda_x=celda_x,
        celda_y=celda_y
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
