import pymongo
from pymongo import MongoClient
import time
import json
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

# connection to mongodb Container
client=MongoClient("mongo",27017)

# watching the access log every time it is modified
class Watcher:
    DIRECTORY_TO_WATCH = "/var/access_logs"

    def __init__(self):
        self.observer = PollingObserver()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()

# collecting and saving the access logs
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        # every time the file is modified the current code runs
        elif event.event_type == 'modified':
            # openning the access log
            file=open("/var/access_logs/access.log","r")
            # extracting the last line of the file
            last_log=file.readlines()[-1]
            # converting the string line to json
            last_log_json=last_log.replace('"','\"')
            d=json.loads(last_log_json)
            # inserting the json file to the database
            client.myDB.access.insert_one(d).inserted_id

            print "Received modified event - %s." % event.src_path
            

# running the script
if __name__ == '__main__':
    w = Watcher()
    w.run()
