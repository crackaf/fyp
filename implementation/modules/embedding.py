from typing import NamedTuple
import numpy as np
import time
from recoverybits import make as recoverybits_make, embed as recoverybits_embed, extract as recoverybits_extract
from authbits import make as authbits_make, embed as authbits_embed, extract as authbits_extract

CHECK_EMBEDDING = False


class EmbeddingResult(NamedTuple):
    imarr: np.ndarray
    time: float
    is_checked: bool = False
    is_correct: bool = False


def watermark_embedding(imarr: np.ndarray, lookup: np.ndarray | None = None) -> EmbeddingResult:
    """
    Embed watermark into image.
    @Returns: dict[np.ndarray, int]
    embedded image, time taken to embed
    """

    if lookup is None:
        lookup = np.array([
            [0, 7, 13, 10],
            [1, 6, 12, 11],
            [4, 2, 9, 15],
            [5, 3, 8, 14]], dtype=np.uint8)

    if not CHECK_EMBEDDING:
        # make embedding and just return
        start_t = time.time()
        recvim = recoverybits_embed.embed(
            imarr, recoverybits_make.make(imarr, lookup))
        return EmbeddingResult(authbits_embed.embed(
            recvim,
            authbits_make.make(recvim)
        ),  time.time() - start_t)

    # make embedding and also check if it's correct
    start_t = time.time()
    # make recoverybits
    recovery_bits = recoverybits_make.make(imarr, lookup)
    recvim = recoverybits_embed.embed(imarr, recovery_bits)

    # make hashes
    hashes = authbits_make.make(recvim)

    embeddedim = authbits_embed.embed(
        recvim,
        hashes
    )

    # extract recoverybits
    exrecovery = recoverybits_extract.extract(embeddedim)

    # extract hashes
    exhashes = authbits_extract.extract(embeddedim)

    return EmbeddingResult(embeddedim, time.time() - start_t, True, np.array_equal(recovery_bits, exrecovery) and np.array_equal(hashes, exhashes))
