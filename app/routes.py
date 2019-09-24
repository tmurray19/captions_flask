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
    get_frame_from_id(proj_id, vid_id)
    frame_file = 'img/{}/{}_frame.png'.format(str(proj_id), str(vid_id))
    print(frame_file)
    return render_template('caption_pos.html', frame_loc = frame_file, proj_id=proj_id, vid_id=vid_id)

@app.route('/_render_caption')
def render_caption():
    x = request.args.get('x', 0, type=str)
    y = request.args.get('y', 0, type=str)
    proj_id = request.args.get('proj_id', 0, type=str)
    vid_id = request.args.get('vid_id', 0, type=str)
    print(x)
    print(y)
    print(proj_id)
    print(vid_id)
    loc = (x, y)
    img = create_caption.generate_caption(loc, proj_id, vid_id)    
    print(img)
    return jsonify(image_status = img)
    


api = Api(app)

@api.route('/chunk/<int:proj_id>')
class RenderChunk(Resource):
    def get(self, proj_id):
        logging.debug("Creating render request for project '{}' ".format(proj_id))
        queue_service.create_chunk(proj_id)
        return "We are rendering the project now. This may take some time depending on your project."


def get_frame_from_id(proj_id, vid_id):
    if os.path.isfile(os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame.png'.format(str(vid_id))):
        print("File exists")
        return os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame.png'.format(str(vid_id))
    vid = os.path.join(app.config['BASE_DIR'], app.config['VIDS_LOCATION'], str(proj_id), str(vid_id)+".mp4")
    print("At file {}".format(vid))
    vid = VideoFileClip(vid)
    print(vid)
    if not os.path.isdir(os.getcwd() + '/app/static/img/' + str(proj_id)):
        print("Making dir: ")
        print(os.mkdir(os.getcwd() + '/app/static/img/' + str(proj_id)))
        os.mkdir(os.getcwd() + '/app/static/img/' + str(proj_id))
    vid.save_frame(
        os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame.png'.format(str(vid_id)),
        t=1
    )

    print(os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame.png'.format(str(vid_id)))
    return os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame.png'.format(str(vid_id))

