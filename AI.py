import sys
import os
import json
import time
import io
import argparse
import pybase64 as base64
import google.cloud
from google.cloud import vision, storage
from google.cloud.vision import types
from watchdog.observers import Observer
from apiclient import discovery
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageDraw

#export GOOGLE_APPLICATION_CREDENTIALS=/Users/samfinton/Documents/Yukon\ College\ Work/GarbageBot/kidscamp-88df0e22019d.json

fullfolderpath = '/Users/samfinton/Documents/Yukon College Work/GarbageBot/garbagebotbucket1/'
foldername = 'garbagebotbucket1/'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'kidscamp-88df0e22019d.json'


class Watcher:
    DIRECTORY_TO_WATCH = fullfolderpath

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
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @classmethod
    def vision_image_manager(latest_file):
     # Instantiates a client

        service = discovery.build('vision', 'v1')
     # text.png is the image file.
        with open(latest_file, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
              "requests":[
                {
                  "image":{
                    "content": image_content.decode('UTF-8')
                  },
                  "features":[
                    {
                      "type":"LABEL_DETECTION",
                      "maxResults":3,
                      "latLongRect" : {
                      object(LatLongRect)
                      }
                    }
                  ]
                }
              ]
            })




            response = service_request.execute()
            print(response['responses'])
            res_dict = dict(response)
            return res_dict



    @classmethod
    def detect_crop_hints(latest_file, image_file):
        #Detect crop hints on a single image and return the first result.
        client = vision.ImageAnnotatorClient()

        with io.open(image_file, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
        image_context = types.ImageContext(crop_hints_params=crop_hints_params)

        response = client.crop_hints(image=image, image_context=image_context)
        hints = response.crop_hints_annotation.crop_hints

        # Get bounds for the first crop hint using an aspect ratio of 1.77.
        vertices = hints[0].bounding_poly.vertices

        return vertices


    def draw_hint(image_file):
        #Draw a border around the image using the hints in the vector list.
        vects = Handler.detect_crop_hints(image_file)
        im = Image.open(image_file)
        draw = ImageDraw.Draw(im)
        draw.polygon([
            vects[0].x, vects[0].y,
            vects[1].x, vects[1].y,
            vects[2].x, vects[2].y,
            vects[3].x, vects[3].y], None, 'red')
        im.save('output-hint.jpg', 'JPEG')
        print('Saved image with bounding box.')

    @staticmethod
    def on_any_event(event):
        if event.event_type == 'created':
            latest_file = event.src_path
            print(latest_file)
            Handler.detect_crop_hints(latest_file)
            Handler.draw_hint(latest_file)
            #Handler.vision_image_manager(latest_file)

w = Watcher()
w.run()
