import os


# Config file
class Config(object):
    # Secret key used for verification
    # This Secret Key is depreciated, an d
    SECRET_KEY = os.environ.get('SECRET_KEY') or "WgnYVzwgwF7Alu1B3DehuO-C-QoKcBitsHqpiFi1cRE"
    
    # Directories
    BASE_DIR = os.environ.get('BASE_DIR') or "/mnt/csae48d5df47deax41bcxbaa"

    # Windows
    BASE_DIR = os.environ.get('BASE_DIR') or "N:/project"

    # Mac
    BASE_DIR = os.environ.get('BASE_DIR') or '/Users/Taidghmurray'
    VIDS_LOCATION = os.environ.get('VIDS_LOCATION') or 'Downloads'

    #VIDS_LOCATION = os.environ.get('VIDS_LOCATION') or "videos"
    QUEUE_LOCATION = os.environ.get('QUEUE_LOCATION') or 'renderQueue'
    LOGS_LOCATION = os.environ.get('LOGS_LOCATION') or "logs" 
    RESOURCE_PATH = os.environ.get('RESOURCE_PATH') or 'resource'
    WATCHER_LOGS = os.environ.get('WATCHER_LOG') or 'renderWatcher'
    RENDER_LOGS = os.environ.get('RENDER_LOG') or 'renderService'
    FLASK_LOGS = os.environ.get('FLASK_LOG') or 'renderFlask'
    QUEUE_FOLDER = os.environ.get('QUEUE_FOLDER') or 'renderQueue'
    CHUNK_QUEUE_FOLDER = os.environ.get('CHUNK_QUEUE_FOLDER') or 'chunkQueue'

    # Defining storage name and key
    STORAGE_ACCOUNT_NAME = os.environ.get('STORAGE_ACCOUNT_NAME') or 'csae48d5df47deax41bcxbaa'
    STORAGE_ACCOUNT_KEY = os.environ.get('STORAGE_ACCOUNT_KEY') or \
        ''

    SHARE_NAME = os.environ.get('SHARE_NAME') or 'cs-william-squarev-media-10037ffe909d3982' 
    # Defining name of json file containing edits
    PROJECT_NAME = os.environ.get('PROJECT_NAME') or 'FinalSubclipJson.json'
