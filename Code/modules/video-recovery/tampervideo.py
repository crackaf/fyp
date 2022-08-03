import numpy as np
import multiprocessing as mp


def tamper(img):
    startx = 200
    starty = 200
    width = 50
    height = 50
    for i in range(width):
        for j in range(height):
            for k in range(3):
                img[startx+i][starty+j][k] = 0

    startx = 100
    starty = 100
    width = 50
    height = 50
    for i in range(width):
        for j in range(height):
            for k in range(3):
                img[startx+i][starty+j][k] = 0

    return img


def wrapper(itr, video, return_dict):
    return_dict[itr] = tamper(video[itr])


def videoTampering(video):
    if __name__ == "tampervideo":
        manager = mp.Manager()
        return_dict = manager.dict()
        processes = []
        for i in range(0, len(video)):
            p = mp.Process(target=wrapper, args=(i, video, return_dict))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        temp = video.copy()
        for i in range(0, len(video)):
            temp[i] = return_dict[i]
        return temp, True
