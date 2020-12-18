
from flask import Flask
app=Flask(__name__)

app.secret_key = 'mi-super-duper-llave-secreta-jeje :)'

import portal.rutas
