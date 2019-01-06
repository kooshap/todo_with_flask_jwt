from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import todo

app = Flask(__name__)
api = Api(app)

api.add_resource(todo.List, '/list')
api.add_resource(todo.Add, '/add')
api.add_resource(todo.Update, '/update')
api.add_resource(todo.Delete, '/delete')
api.add_resource(todo.Login, '/login')

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)