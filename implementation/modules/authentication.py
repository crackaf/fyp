from typing import NamedTuple
import numpy as np
import time
from recoverybits import make as recoverybits_make, embed as recoverybits_embed, extract as recoverybits_extract
from authbits import make as authbits_make, embed as authbits_embed, extract as authbits_extract


class AuthenticationResult(NamedTuple):
    tempred: np.ndarray  # tempred array
    time: float


def watermark_authentication(imarr: np.ndarray) -> AuthenticationResult:

    start_t = time.time()

    # make hashes
    hashes = authbits_make.make(imarr)

    # extract hashes
    exhashes = authbits_extract.extract(imarr)

    tempred = np.zeros((exhashes.shape[0], exhashes.shape[1]), dtype=bool)

    for i in range(exhashes.shape[0]):
        for j in range(exhashes.shape[1]):
            tempred[i, j] = np.array_equal(hashes[i, j], exhashes[i, j])
    tempred = ~tempred
    return AuthenticationResult(tempred, time.time() - start_t)
