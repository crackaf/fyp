from typing import NamedTuple
import numpy as np
import scipy.ndimage
import time
from blocks import get_blocks, combine_blocks
from recoverybits import make as recoverybits_make, embed as recoverybits_embed, extract as recoverybits_extract
from authbits import make as authbits_make, embed as authbits_embed, extract as authbits_extract
from authentication import watermark_authentication


class RecoveryResult(NamedTuple):
    imarr: np.ndarray  # recovered array
    time: float


def _watermark_recovery(imarr: np.ndarray, recovery_bits: np.ndarray,
                        tempred: np.ndarray, lookup: np.ndarray) -> RecoveryResult:

    start_t = time.time()

    recoveredarr = imarr.copy()

    # only do if any of the blocks are tempred
    if np.any(tempred):

        # converting the image to 16x16 blocks
        # making 16 main blocks
        # size of single main block S= M/sqrt(16) X T=N/sqrt(16)
        # e.g for lena the 512x512 the partner blocks size would be 16 blocks each with size (512x512)/(4x4) = 128x128
        mainblock_shape = (int(imarr.shape[0]/4), int(imarr.shape[1]/4))
        mainblocks = get_blocks(imarr.copy(), mainblock_shape)

        # here the main blocks are like this index.
        # 1st index is the block number.
        # 2nd index is the channel (RGB) or 0 in Grey.
        # 3rd and 4th are for indexing the block.

        # Making 16x16 for Step 8
        # Dividing the main blocks to 16x16 blocks
        # Total blocks = SxT/16x16 = 128x128/16x16 = 64 Blocks

        b16x16_shape = (16, 16)
        # reshaping because we needed that shape
        b16x16 = mainblocks.reshape(
            *mainblocks.shape[:-2],
            int((mainblock_shape[0]*mainblock_shape[1]) /
                (b16x16_shape[0]*b16x16_shape[1])),
            b16x16_shape[0], b16x16_shape[1]).copy()

        for i in range(mainblocks.shape[0]):
            b16x16[i][0] = get_blocks(mainblocks[i][0], b16x16_shape,
                                      addChannel=False)

        for partner in range(lookup.shape[0]):  # A,B,C,D
            for id in range(lookup.shape[1]):  # A1,A2,A3.....D4 etc
                # check if this is tempred
                if np.any(tempred[lookup[partner, id]]):
                    # this mainblock is tempred, so we need to recover it
                    # but which 16x16 block is tempred?

                    # get the partner block of this id also the id it sits
                    partner_block = -1, -1
                    for i in range(lookup[partner].shape[0]):
                        # if this id isn't tempred, we can stop
                        if i != id and not np.any(tempred[lookup[partner, i]]):
                            partner_block = partner, i
                            break

                    if partner_block == (-1, -1):
                        print(
                            "Could not find partner block for id {}".format(id))
                        continue

                    # get recovery bits of this id
                    # get index of this id in the partner block
                    idx = id
                    if partner_block[1] < id:
                        idx -= 1

                    # now we have partner_block, so we can recover it
                    # get the recovery bits of this partner block
                    recovery_bits_partner = recovery_bits[lookup[partner_block],
                                                          idx*recovery_bits.shape[1]//3:idx*recovery_bits.shape[1]//3+recovery_bits.shape[1]//3]

                    # now we have recovrey bits the exact partner block
                    # but these are in binary, so we need to convert them to uint
                    recovery_decimals = np.packbits(recovery_bits_partner)

                    # these recovery bits are for all the main blocks 4x4
                    # but we are going to replace only the tempred 16x16

                    # shaping these recovery bits to the 16x16 blocks
                    r16x16 = get_blocks(scipy.ndimage.zoom(recovery_decimals.reshape(int(
                        imarr.shape[0]/(4*4)), int(imarr.shape[1]/(4*4))), 4, order=0), b16x16_shape, addChannel=False)

                    # now we repace which ever 16x16 block is tempred
                    for i in range(tempred[lookup[partner, id]].shape[0]):
                        if tempred[lookup[partner, id], i]:
                            # means this 16x16 block is tempred
                            b16x16[lookup[partner, id], 0, i] = r16x16[i]

        # combining the 16x16 blocks to the main blocks
        # merging 16x16
        cmainblocks = mainblocks.copy()
        for i in range(cmainblocks.shape[0]):
            cmainblocks[i][0] = combine_blocks(
                b16x16[i][0], mainblock_shape, blockshape=b16x16_shape, channel=False)

        # merging main blocks to main image
        recoveredarr = combine_blocks(cmainblocks.copy(), imarr.shape,
                                      mainblock_shape).reshape(imarr.shape)

    return RecoveryResult(recoveredarr, time.time() - start_t)


def watermark_recovery(imarr: np.ndarray, lookup: np.ndarray) -> RecoveryResult:
    # extracting the recovery bits
    recovery_bits = recoverybits_extract.extract(imarr)
    # extracting the auth bits
    auth_bits = watermark_authentication(imarr).tempred

    # calling the recovery function
    return _watermark_recovery(imarr, recovery_bits, auth_bits, lookup)