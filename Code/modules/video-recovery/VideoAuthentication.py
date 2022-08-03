import numpy as np
from triplerecovery import authenticate
import cv2
import multiprocessing as mp
# import threading as th


class videoAuthentication:
    ArrayOfFrames: np.ndarray
    is_Authentic: bool = True

    def wrapper(self, itr, return_dict):
        return_dict[itr] = authenticate(
            self.ArrayOfFrames[itr]).maskarr

    def VideoWatermarkAuthentication(self, path: str = None):
        if __name__ == "VideoAuthentication":
            # loading video
            vidcap = cv2.VideoCapture(path)

            # Converting video to frames
            success, image = vidcap.read()
            count = 0
            frames = []
            while success:
                frames.append(image)
                success, image = vidcap.read()
                count += 1

            self.ArrayOfFrames = np.array(frames)

            manager = mp.Manager()
            return_dict = manager.dict()
            processes = []
            for i in range(0, len(self.ArrayOfFrames), 10):
                processes.append(mp.Process(
                    target=self.wrapper, args=(i, return_dict)))
            print("appending")
            for i in range(0, len(processes)):
                processes[i].start()
            print("started")
            for i in range(0, len(processes)):
                processes[i].join()

            print("joined")

            if np.any(return_dict.values()):
                print(return_dict.values())
                self.is_Authentic = False

            if self.is_Authentic:
                print("Video is authentic")
            else:
                print("Video is not authentic")

    def SimpleAuthentication(self):
        if __name__ == "VideoAuthentication":
            manager = mp.Manager()
            return_dict = manager.dict()
            processes = []
            for i in range(0, len(self.ArrayOfFrames)):
                processes.append(mp.Process(
                    target=self.wrapper, args=(i, return_dict)))
            print("appending")
            for i in range(0, len(processes)):
                processes[i].start()
            print("started")
            for i in range(0, len(processes)):
                processes[i].join()
            print("joined")
            count = 0
            for i in return_dict.values():
                if np.any(i):
                    count += 1
            if np.any(return_dict.values()):
                self.is_Authentic = False

            # for i in range(0, len(self.ArrayOfFrames)):
            #     self.EmbedebFrames[i] = return_dict[i]
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter("authinticmask.mp4", fourcc, 30, (512, 512))
            for i in range(len(return_dict[i])):
                video.write(return_dict[i])
            video.release()
            if self.is_Authentic:
                print("Video is authentic")
            else:
                print("Video is not authentic",
                      "\n number of tampered frames :", count)
            return True
