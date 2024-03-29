import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import driveClip
from config import Config
import os.path
import json
from multiprocessing import Process, Pipe
from datetime import datetime
import logging
import sys

class Watcher:
    DIRECTORY_TO_WATCH = os.path.join(Config.BASE_DIR, Config.QUEUE_LOCATION)

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
                logging.debug("Watcher: Sleeping")
                print("Watcher: Sleeping")
        except:
            self.observer.stop()
            logging.error("-1 - Error")
            print("-1 - Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        print("Watcher: Event found: {}".format(event.event_type))
        logging.debug("Watcher: Event found: {}".format(event.event_type))
        logging.debug("Directory: {}".format(os.path.basename(event.src_path)))
        if event.is_directory:
            return None

        # Windows is created
        # Linux is modified
        elif event.event_type == 'modified':
            time.sleep(1)
            recv_end, send_end = Pipe(False)
            # Take any action here when a file is first created.
            print("Received event {} for file {} - Beginning render job." .format(event.event_type, event.src_path))
            logging.debug("Received event {} for file {} - Beginning render job." .format(event.event_type, event.src_path))
            # Testing print
            f = os.path.relpath(event.src_path, Watcher.DIRECTORY_TO_WATCH)
            pid, rend_type, other = f.split("_", 2)
            print(pid)
            print(rend_type)
            print(other)
            logging.debug("File found: {}".format(f))
            logging.debug("Source path: {}".format(event.src_path))
            logging.debug("Render type: {}".format(rend_type))

            # Open the file for reading
            json_file = open(event.src_path, 'r')
            json_data = json.load(json_file)
            # If job hasn't been done
            if json_data['status'] == False:
                # Get the ID and run the render on it
                proj_id = json_data["id"]

                print("Project ID is {}".format(proj_id))
                logging.debug("Project ID is {}".format(proj_id))  

                compress = True if rend_type == "preview" else False
                chunk = True if rend_type == "chunk" else False    
                logging.debug("Compress status: {}, Chunk status: {}".format(compress, chunk))

                logging.debug("Starting render serivce...")
                p = Process(target=driveClip.render_video, args=(proj_id, send_end, compress, chunk))
                p.start()
                p.join()
                render_return =  recv_end.recv()
                render_status = render_return[1]
                info = render_return[0]
                # Update the complete time at the end and dump it to file 
                logging.debug("Updating JSON status file")
                json_data['dateCompleted'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                json_data['status'] = True
                json_data['correctlyRendered'] = render_status
                json_data['otherInfo'] = info
                logging.debug("JSON Data for {}:".format(proj_id))
                logging.debug(json_data)
                with open(event.src_path, "w") as json_write:
                    json.dump(json_data, json_write)
                if render_status == 1:
                    logging.debug("File written successfully.")
                    print("File written successfully")
                    return
                else:
                    logging.debug("Job completed, but an error may have occured during render service")
                    return
            else:
                logging.debug("File already rendered")
                print("File already rendered")
                return


if __name__ == '__main__':

    log_file_name = os.path.join(
        Config.BASE_DIR,
        Config.LOGS_LOCATION,
        Config.WATCHER_LOGS, 
        datetime.now().strftime("%Y.%m.%d-%H-%M-%S") + "_render_watcher_instance.log"
    )

    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file_name
    )

    logging.debug("Beginning watcher service")

    w = Watcher()
    w.run()