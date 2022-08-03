import time
import numpy as np
from PIL import Image
from authentication import watermark_authentication
import cv2
import multiprocessing as mp
# import threading as th

class VideoAuthentication:
    ArrayOfFrames: np.ndarray
    is_Authentic: bool = True
    
    def wrapper(self,itr,return_dict):
        return_dict[itr]=watermark_authentication(self.ArrayOfFrames[itr]).tempred

    def VideoWatermarkAuthentication(self,path: str=None):
        if __name__ == "__main__":
            #loading video
            vidcap=cv2.VideoCapture(path)
            
            
            # Converting video to frames
            success,image=vidcap.read()
            count=0
            frames=[]
            while success:
                frames.append(image)
                success,image=vidcap.read()
                count+=1
            
            self.ArrayOfFrames=np.array(frames)
            

            manager = mp.Manager()
            return_dict = manager.dict()
            processes=[]
            for i in range (0,len(self.ArrayOfFrames),10):
                processes.append(mp.Process(target=self.wrapper,args=(i,return_dict)))
            print("appending")
            for i in range(0,len(processes)):  
                processes[i].start()
            print("started")
            for i in range(0,len(processes)):
                print(i,i)
                processes[i].join()
                print(i,i)
            print("joined")
            
            if np.any(return_dict.values()):
                print(return_dict.values())
                self.is_Authentic=False
            
            if self.is_Authentic:
                print("Video is authentic")
            else:
                print("Video is not authentic")
            
v=VideoAuthentication()
v.VideoWatermarkAuthentication(path="video.mp4")

            
            
        