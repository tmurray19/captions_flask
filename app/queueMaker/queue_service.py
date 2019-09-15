from datetime import datetime
from json import dump, load
from os.path import join, exists
from app import app
import logging


def create_chunk(proj_id):

    # Define data points
    """
    ID: int --> Project ID
    dateRequested: String --> Exact time requested at
    dateCompleted: String --> Time video was written to file
    status: Bool --> True for completed, False for not
    otherInfo: String --> Any error messages
    """
    # Create json info
    queue_info = {
        "id": proj_id,
        "dateRequested": datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"),
        "dateCompleted": "TBA",
        "status": False,
        "firstTime": True,
        "otherInfo": "None"
    }
    try:
        render_type = "_chunk_"
        if exists(join(app.config['BASE_DIR'], app.config['CHUNK_QUEUE_FOLDER'], proj_id + render_type + "queue_status.json")):
            queue_info['firstTime'] = False
        logging.debug(queue_info)
        print(queue_info)
        with open(join(app.config['BASE_DIR'], app.config['CHUNK_QUEUE_FOLDER'], proj_id + render_type + "queue_status.json"), 'w') as outfile:
            dump(queue_info, outfile)
    
        logging.debug("Queue file written to {}".format(join(app.config['BASE_DIR'], app.config['CHUNK_QUEUE_FOLDER'], proj_id + "_queue_status.json")))
        
        return 1
    except Exception as e:
        logging.error("An Exception has occured:")
        logging.error(e)
        return 0



def get_queue_status(proj_id, compressed_render, chunk_render):
    compress_bool = True if compressed_render==1 else False
    chunk_book = True if chunk_render==1 else False        
    render_type = "_full_"
    if compress_bool:
        render_type = "_preview_"
    if chunk_book:
        render_type = "_chunk_"
    try:
        # Call JSON File and check for render status
        queue_loc = join(app.config['BASE_DIR'], app.config['QUEUE_FOLDER'], proj_id + render_type + "queue_status.json")
        with open(queue_loc) as json_file:
            json_data = load(json_file)
            logging.debug("File render status: {}".format(json_data['correctlyRendered']))
            logging.debug("Info: {}".format(json_data['otherInfo']))
            return json_data['correctlyRendered']

    
    except Exception as e:
        logging.debug(e)
        return -1
