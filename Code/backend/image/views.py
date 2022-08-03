from django.http import HttpResponse
import cv2
import os
import numpy as np
import triplerecovery as tr

from backend.settings import BASE_DIR
import json
import io
from PIL import Image
from binascii import a2b_base64
import uuid

# Create your views here.
def index(request):
    return HttpResponse("No.")

def watermark(request):
    if request.method=="POST":
        print("POST RECEIVED -> WATERMARK")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        img_data = body['image']
        key = body['key']

        binary_data = a2b_base64(img_data)

        received_image_name = str(uuid.uuid4()) + ".png"

        fd = open('received_images/' + received_image_name, 'wb')
        fd.write(binary_data)
        fd.close()
        img_arr = cv2.imread("received_images/" + received_image_name)
        print("EMBEDDING STARTED")
        print(key)
        if len(key)>0:
            idx=ord(key[0])%5
            output = tr.embed(img_arr, key=key,lookupidx=idx)
        else:
            output = tr.embed(img_arr)
        # output = tr.embed(img_arr)
        watermarked_img_arr = output.imarr
        print("Time: ", output.time)

        watermared_image_name = str(uuid.uuid4()) + ".png"

        cv2.imwrite("watermarked_images/" + watermared_image_name, watermarked_img_arr)
        
        
        return HttpResponse(os.path.join(BASE_DIR,"watermarked_images\\" + watermared_image_name))
    else:
        return HttpResponse("GET, world. You're at the watermarked index.")

def authenticate(request):
    #get body from request
    if request.method=="POST":
        print("POST RECEIVED -> AUTHENTICATE")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        img_data = body['image']
        binary_data = a2b_base64(img_data)
        received_image_name = str(uuid.uuid4()) + ".png"

        fd = open('received_images/' + received_image_name, 'wb')
        fd.write(binary_data)
        fd.close()
        
        img_arr = cv2.imread("received_images/" + received_image_name)
        print("AUTHENTICATION STARTED")
        print(img_arr)
        output_arr = tr.authenticate(img_arr)
        authenticated_arr = output_arr.maskarr
        print("AUTHENTICATION COMPLETED")
        print("Time: ", output_arr.time)

        authenticated_image_name = str(uuid.uuid4()) + ".png"

        cv2.imwrite("authenticated_images/" + authenticated_image_name, authenticated_arr)

        return HttpResponse(os.path.join(BASE_DIR,"authenticated_images\\" + authenticated_image_name))
    else:
        return HttpResponse("GET, world. You're at the authenticated index.")

def recover(request):
    #get body from request
    if request.method=="POST":
        print("POST RECEIVED -> RECOVER")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        img_data = body['image']
        key = body['key']
        binary_data = a2b_base64(img_data)
        received_image_name = str(uuid.uuid4()) + ".png"

        fd = open('received_images/' + received_image_name, 'wb')
        fd.write(binary_data)
        fd.close()

        img_arr = cv2.imread("received_images/" + received_image_name)
        print("RECOVERY STARTED")
        print(key)
        if len(key)>0:
            idx=ord(key[0])%5
            output = tr.recover(img_arr, key=key,lookupidx=idx)
        else:
            output = tr.recover(img_arr)
        recovered_arr = output.imarr
        print("RECOVERY COMPLETED")
        print("Time: ", output.time)

        recovered_image_name = str(uuid.uuid4()) + ".png"

        cv2.imwrite("recovered_images/" + recovered_image_name, recovered_arr)


        return HttpResponse(os.path.join(BASE_DIR,"recovered_images\\" + recovered_image_name))
    else:
        return HttpResponse("GET, world. You're at the recovered index.")
