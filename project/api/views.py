from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response

from project import db
from project.models import Task
from flask_restful import Api, Resource, url_for


################
#### config ####
################

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


class TasksList(Resource):
    def get(self):
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
            }
            json_results.append(data)
        return jsonify(json_results)


class Tasks(Resource):
    def get(self, task_id):
        result = db.session.query(Task).filter_by(task_id=task_id).first()
        if result:
            result = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
            }
            code = 200
        else:
            result = {"error": "Element does not exist"}
            code = 404
        return make_response(jsonify(result), code)


api.add_resource(Tasks, '/api/v1/tasks/<int:task_id>')
api.add_resource(TasksList, '/api/v1/tasks/')
