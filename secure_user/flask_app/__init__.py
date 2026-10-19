import os
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-fallback")
bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios, entradas
