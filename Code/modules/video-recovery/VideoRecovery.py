import numpy as np
from recover import recover
import cv2
import multiprocessing as mp


class videoRecovery:
    ArrayOfFrames: np.ndarray
    is_recovered: bool = False
    RecoveredFrames: np.ndarray = None

    def wrapper(self, itr, lookup, return_dict):
        return_dict[itr] = recover(
            self.ArrayOfFrames[itr], lookup).imarr

    def VideoRecovery(self, lookup: np.ndarray = None, path: str = None):

        if __name__ == "VideoRecovery":
            # loading video
            vidcap = cv2.VideoCapture(path)

            # getting the number of frames in the video and also the fps of the video
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Converting video to frames
            success, image = vidcap.read()
            height, width, layers = image.shape
            size = (width, height)
            count = 0
            frames = []

            while success:
                frames.append(image)
                success, image = vidcap.read()
                count += 1

            self.ArrayOfFrames = np.array(frames)

            lookup = np.array([[0, 7, 13, 10],
                               [1, 6, 12, 11],
                               [4, 2, 9, 15],
                               [5, 3, 8, 14]], dtype=np.uint8)

            self.RecoveredFrames = np.ones(
                self.ArrayOfFrames.shape, dtype=np.uint8)

            manager = mp.Manager()
            return_dict = manager.dict()
            processes = []
            for i in range(0, len(self.ArrayOfFrames)):
                processes.append(mp.Process(
                    target=self.wrapper, args=(i, lookup, return_dict)))
            print("appending")
            for i in range(0, len(self.ArrayOfFrames)):
                processes[i].start()
            print("started")
            for i in range(0, len(self.ArrayOfFrames)):
                processes[i].join()
            print("joined")
            for i in range(0, len(self.ArrayOfFrames)):
                self.RecoveredFrames[i] = return_dict[i]

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(
                'recovered.mp4', fourcc, fps, (width, height))
            for i in range(len(self.RecoveredFrames)):
                video.write(self.RecoveredFrames[i])
            video.release()
            self.is_recovered = True

    def SimpleRecovery(self):
        if __name__ == "VideoRecovery":

            lookup = np.array([[0, 7, 13, 10],
                               [1, 6, 12, 11],
                               [4, 2, 9, 15],
                               [5, 3, 8, 14]], dtype=np.uint8)

            self.RecoveredFrames = np.ones(
                self.ArrayOfFrames.shape, dtype=np.uint8)

            manager = mp.Manager()
            return_dict = manager.dict()
            processes = []
            for i in range(0, len(self.ArrayOfFrames)):
                processes.append(mp.Process(
                    target=self.wrapper, args=(i, lookup, return_dict)))
            print("appending")
            for i in range(0, len(self.ArrayOfFrames)):
                processes[i].start()
            print("started")
            for i in range(0, len(self.ArrayOfFrames)):
                processes[i].join()
            print("joined")
            for i in range(0, len(self.ArrayOfFrames)):
                self.RecoveredFrames[i] = return_dict[i]

            self.is_recovered = True


# v = VideoRecovery()
# v.VideoRecovery(path="video.mp4")
