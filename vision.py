import json
import sys
import os
import requests
import AI

def path_clear():
    print('Scan the area in front of the sensor - ensuring it is clear to drive ahead')
    time.sleep(3)

def JustDirt():
    print('Take picture of current block. Check block against NN. If just dirt, JustDirt = True.')
    time.sleep(3)

def GarbagePic():
    print('Take a picture of current block. Upload this block to Amazon. If trash, GarbageisThere = True')
    time.sleep(3)

def GarbageisThere():
    print(str(detect_labels()))
    #writeToJSONFile('./','jsonData',jsonData)


# def writeToJSONFile(path, fileName, data):
#     filePathNameWExt = './' + path + '/' + fileName + '.json'
#     with open(filePathNameWExt, 'w') as fp:
#         json.dump(data, fp)

    #Look through returned JSON - if answers are NOT - tree, grass, roots, etc - GarbageisThere = True
