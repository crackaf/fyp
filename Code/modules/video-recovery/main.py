import cv2
from VideoEmbedding import videoEmbedding
# from VideoEmbedding import videoEmbedding
from VideoAuthentication import videoAuthentication
from VideoRecovery import videoRecovery
from tampervideo import videoTampering
import multiprocessing as mp

# # Video Watermark Embedding
if __name__ == "__main__":
    videoE = videoEmbedding()
    outputfile = "videoEmbeded.mp4"
    videoE.VideoWatermarkEmbedding(path="jerry.mp4", output_path=outputfile)
    if videoE.is_embeded:
        vidcap = cv2.VideoCapture(outputfile)
        success, image = vidcap.read()
        height, width, layers = image.shape
        fps = vidcap.get(cv2.CAP_PROP_FPS)

        # # Video Tampering
        bt = False
        tampered, bt = videoTampering(videoE.EmbedebFrames)
        if bt:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter("videoTampered.mp4",
                                    fourcc, fps, (width, height))
            for i in range(len(tampered)):
                video.write(tampered[i])
            video.release()

            # # Video Authentication
            videoA = videoAuthentication()
            videoA.ArrayOfFrames = tampered
            ans = videoA.SimpleAuthentication()

            if ans:

                # # Video Recovery
                videoR = videoRecovery()
                videoR.ArrayOfFrames = tampered
                videoR.SimpleRecovery()
                if videoR.is_recovered:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video2 = cv2.VideoWriter(
                        'videoRecovered.mp4', fourcc, fps, (width, height))
                    for i in range(len(videoR.RecoveredFrames)):
                        video2.write(videoR.RecoveredFrames[i])
                    video2.release()
