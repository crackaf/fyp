from typing import Literal
import numpy as np
import cv2
from flags import DEBUG
from embedding import watermark_embedding

DEBUG_IMAGE = True


class Image:

    # image numpy array
    imarr: np.ndarray = None

    # is embedding successful?
    is_embedded: bool = False

    # Constructors

    def __init__(self, _imarr: np.ndarray) -> None:

        if _imarr.shape[0] % 64 != 0 or _imarr.shape[1] % 64 != 0:
            # raise error if the shape isn't correct
            raise ValueError(
                "Image shape is not correct! It should be a multiple of 64!")

        self.imarr = _imarr.copy()

        self.debug_image("Loaded Image", self.imarr)

    @classmethod
    def imread(cls, impath: str, mode: 0 | 1 = 0) -> None:
        '''
        Call the constructor with the path to the image and the mode of the image.\n
        impath: path to image\n
        flags: mode of image (L, RGB, etc.) default: 0
        grayscale = 0
        color = 1
        '''
        # converting file to numpy array
        return cls(cv2.imread(impath, mode))

    # Getters
    def show_imarr(self) -> None:
        '''
        Shows the image in the window
        '''
        cv2.imshow("Image", self.imarr)
        cv2.waitKey(0)

    # Debug Image
    @staticmethod
    def debug_image(winname: str, imarr: np.ndarray) -> None:
        if DEBUG and DEBUG_IMAGE:
            cv2.imshow("Debug Image", imarr)

    def embedding(self) -> bool:
        data = watermark_embedding(self.imarr)
        self.imarr = data.imarr
        self.is_embedded = True
        return True
