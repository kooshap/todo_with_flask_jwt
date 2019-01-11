from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

TODOLIST = [
    {
        "id": "1",
        "name": "grocery",
        "timestamp": str(get_timestamp())
    },
    {
        "id": "2",
        "name": "read",
        "timestamp": str(get_timestamp())
    },
    {
        "id": "3",
        "name": "gym",
        "timestamp": str(get_timestamp())
    }
]

class List(Resource):
    @jwt_required
    def get(self):
        """
        This function responds to a request for /todo
        with the complete lists of todo items

        :return:        sorted list of todo items
        """
        current_user = get_jwt_identity()
        return {"list": TODOLIST, "message":"logged in as {}".format(current_user)}

class Add(Resource):
    @jwt_required
    def post(self):
        """
        This function responds to a request for /todo
        by adding to todo items

        :return:        the new item
        """
        from uuid import uuid4

        parser = reqparse.RequestParser()
        parser.add_argument('name' ,required=True, help="name cannot be blank!")
        data = parser.parse_args()
        name = data['name']

        data = {}
        data["id"] = str(uuid4())
        data["name"] = name
        data["timestamp"] = get_timestamp()
        TODOLIST.append(data)
        return data

class Update(Resource):
    @jwt_required
    def post(self):
        """
        This function responds to a request for /todo
        by updating a todo item

        :return:        the updated item
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id' ,required=True, help="id cannot be blank!")
        parser.add_argument('name' ,required=True, help="name cannot be blank!")
        data = parser.parse_args()
        _id = data['id']
        name = data['name']
        for item in TODOLIST:
            if (_id == item["id"]):
                item["name"] = name
                item["timestamp"] = get_timestamp()
                return item

class Delete(Resource):
    @jwt_required
    def post(self):
        """
        This function responds to a request for /todo
        by removing a todo item

        :return:        the removed item
        """

        parser = reqparse.RequestParser()
        parser.add_argument('id' ,required=True, help="id cannot be blank!")
        data = parser.parse_args()
        _id = data['id']

        del_index=-1
        for idx, item in enumerate(TODOLIST):
            if (_id == item["id"]):
                del_index = idx

        return TODOLIST.pop(del_index) if del_index > -1 else ""

class Login(Resource):
    def post(self):
        """
        This function is for logging in the user

        :return:        access_token and refresh_token
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username' ,required=True, help="username cannot be blank!")
        parser.add_argument('password' ,required=True, help="password cannot be blank!")
        data = parser.parse_args()

        if data['username'] == "test" and data['password'] == "secret":
            access_token = create_access_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token
                }
        else:
            return {
                'message': 'Access denied'
                }, 401