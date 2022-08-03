# import time
import numpy as np
# from PIL import Image
from embedding import watermark_embedding
from authentication import watermark_authentication
import cv2
import multiprocessing as mp
# from moviepy.editor import VideoFileClip,ImageClip,concatenate_videoclips
# import threading as th


class VideoEmbedding:
    ArrayOfFrames: np.ndarray
    is_embeded: bool = False
    EmbedebFrames: np.ndarray = None

    def wrapper(self, itr, lookup, return_dict):
        return_dict[itr] = watermark_embedding(
            self.ArrayOfFrames[itr], lookup).imarr
        print(itr)

    def VideoWatermarkEmbedding(self, lookup: np.ndarray = None, path: str = None):

        if __name__ == "__main__":
            # loading video
            # clip=VideoFileClip(path)
            vidcap = cv2.VideoCapture(path)

            # getting the number of frames in the video and also the fps of the video
            # fps=clip.fps
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Converting video to frames

            success, image = vidcap.read()
            height, width, layers = image.shape
            size = (width, height)
            count = 0
            fourcc = cv2.VideoWriter_fourcc(*"H264")
            video = cv2.VideoWriter('video.mkv', fourcc, fps, (width, height))
            # height, width= clip.size
            frames = []

            while success:
                frames.append(image)
                # return_list.append(image)
                success, image = vidcap.read()
                count += 1

            self.ArrayOfFrames = np.array(frames)

            lookup = np.array([
                [0, 7, 13, 10],
                [1, 6, 12, 11],
                [4, 2, 9, 15],
                [5, 3, 8, 14]], dtype=np.uint8)

            self.EmbedebFrames = np.ones(
                self.ArrayOfFrames.shape, dtype=np.uint8)

            manager = mp.Manager()
            return_dict = manager.dict()
            processes = []
            for i in range(0, len(self.ArrayOfFrames)):
                processes.append(mp.Process(
                    target=self.wrapper, args=(i, lookup, return_dict)))
                processes[i].start()
            print("appending")
            # for i in range(0,len(self.ArrayOfFrames)):
            #     processes[i].start()
            print("started")
            for i in range(0, len(self.ArrayOfFrames)):
                processes[i].join()
            print("joined")
            for i in range(0, len(self.ArrayOfFrames)):
                self.EmbedebFrames[i] = return_dict[i]

            # clips=[ImageClip(self.EmbedebFrames[i]).set_duration(clip.duration) for i in range(0,len(self.EmbedebFrames))]
            # concat_clip = concatenate_videoclips(clips, method="compose")
            # concat_clip.write_videofile("test.mkv",fps=fps,codec='libx264')

            for i in range(len(self.EmbedebFrames)):
                video.write(self.EmbedebFrames[i])
            video.release()
            self.is_embeded = True


v = VideoEmbedding()
v.VideoWatermarkEmbedding(path="yy.mp4")
