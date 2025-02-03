import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Teste - Topaz',
    'description': 'Desenvolvido por Lucas Pereira, 2025',
    'termsOfService': 'https://github.com/spereiralucas/TesteTopaz'
}
swagger = Swagger(app)

app.app_context().push
CORS(app)

app.config.from_object('config')

os.environ['WERKZEUG_TIMEOUT'] = '60'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


# Import Models
from app.models import __init__

# Import Routes
from app.routes import __init__
