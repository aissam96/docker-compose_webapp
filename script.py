import pymongo
from pymongo import MongoClient
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# connection to mongodb Container
client=MongoClient("mongo",27017)

class Watcher:
    DIRECTORY_TO_WATCH = "/var/access_logs"

    def __init__(self):
        self.observer = Observer()

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


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "Received created event - %s." % event.src_path

        elif event.event_type == 'modified':

            file=open("/var/access_logs/access.log","r")
            last_log=file.readlines()[-1]
            last_log_json=last_log.replace('"','\"')
            d=json.loads(last_log_json)
            client.ebot7db.access.insert_one(d).inserted_id

            print "Received modified event - %s." % event.src_path


if __name__ == '__main__':
    w = Watcher()
    w.run()
