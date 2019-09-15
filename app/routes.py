from flask import render_template, request, Blueprint, url_for
from flask_restplus import Api, Resource
from app import app
from multiprocessing import Process
from app.queueMaker import queue_service
from datetime import datetime
import os
import logging


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-chunk', methods=['POST'])
def create_chunk():
    proj_id = request.form['proj_id']
    logging.debug("Creating render request for project '{}' ".format(proj_id))
    queue_service.create_chunk(proj_id)
    return "We are rendering the project now. This may take some time depending on your project."


@app.route('/view/<int:proj_id>', methods=['POST'])
def view(proj_id):
    pass


api = Api(app)

@api.route('/chunk/<int:proj_id>')
class RenderChunk(Resource):
    def get(self, proj_id):
        logging.debug("Creating render request for project '{}' ".format(proj_id))
        queue_service.create_chunk(proj_id)
        return "We are rendering the project now. This may take some time depending on your project."
