from flask import render_template, request, Blueprint, url_for, jsonify
from flask_restplus import Api, Resource
from app import app
from app.queueMaker import queue_service
import logging, os
from moviepy.editor import VideoFileClip
from sherpa_editor import create_caption


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


@app.route('/caption/<int:proj_id>/<int:vid_id>')
def caption_generator(proj_id, vid_id):
    frame_file = 'img/{}/{}_frame.jpg'.format(str(proj_id), str(vid_id))
    print(frame_file)
    return render_template('caption_pos.html', frame_loc = frame_file)

@app.route('/_render_caption')
def render_caption():
    x = request.args.get('x', 0, type=int)
    y = request.args.get('y', 0, type=int)
    loc = (x, y)
    clip = create_caption.generate_caption()
    pass


api = Api(app)

@api.route('/chunk/<int:proj_id>')
class RenderChunk(Resource):
    def get(self, proj_id):
        logging.debug("Creating render request for project '{}' ".format(proj_id))
        queue_service.create_chunk(proj_id)
        return "We are rendering the project now. This may take some time depending on your project."


def get_frame_from_id(proj_id, vid_id):
    vid = os.path.join(app.config['BASE_DIR'], app.config['VIDS_LOCATION'], str(proj_id), str(vid_id)+".mp4")
    vid = VideoFileClip(vid)
    if not os.path.isdir('app/' + 'img/' + str(proj_id)):
        os.mkdir('app/' + 'img/' + str(proj_id))
    vid.save_frame(
        'app/' + 'img/' + str(proj_id) + '/{}_frame.jpg'.format(str(vid_id)),
        t=1
    )

    print('app/' + 'img/' + str(proj_id) + '/{}_frame.jpg'.format(str(vid_id)))
    return 'app/' + 'img/' + str(proj_id) + '/{}_frame.jpg'.format(str(vid_id))

