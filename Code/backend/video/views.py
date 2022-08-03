from django.http import HttpResponse
import cv2
import os
import numpy as np
import triplerecovery as tr
import json
import io
from PIL import Image
from binascii import a2b_base64



# Create your views here.
def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")

def watermark(request):
    if request.method=="POST":
        video_obj = request.FILES['file']
        vid_path = video_obj.temporary_file_path()
        # call video embedding function
        return HttpResponse("POST, world. You're at the video watermark index.")
    else:
        return HttpResponse("GET, world. You're at the watermark index.")

def authenticate(request):
    #get body from request
    if request.method=="POST":
        video_obj = request.FILES['file']
        vid_path = video_obj.temporary_file_path()

        return HttpResponse("POST, world. You're at the authenticated index.")
    else:
        return HttpResponse("GET, world. You're at the authenticated index.")

def recover(request):

    if request.method=="POST":
        video_obj = request.FILES['file']
        vid_path = video_obj.temporary_file_path()

        return HttpResponse("POST, world. You're at the recovery index.")
    else:
        return HttpResponse("GET, world. You're at the recovery index.")
