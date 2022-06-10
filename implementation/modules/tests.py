import cv2
import numpy as np
from PIL import Image
import time
from recoverybits import make, embed, extract
from authbits import make as make_authbits, embed as embed_authbits, extract as extract_authbits
from recovery import watermark_recovery


def embedding(imagepath):
    start_t = time.time()

    imarr = np.array(Image.open(imagepath).convert('L'))
    imread_t = time.time()

    lookup = np.array([[0, 7, 13, 10],
                      [1, 6, 12, 11],
                      [4, 2, 9, 15],
                      [5, 3, 8, 14]], dtype=np.uint8)

    # make recoverybits
    recovery_bits = make.make(imarr, lookup)
    make_t = time.time()

    # embed recoverybits
    embededim = embed.embed(imarr, recovery_bits)
    embed_t = time.time()

    # make hashes
    hashes = make_authbits.make(imaembededimrr)
    make_t2 = time.time()

    # embed hashes
    embededim2 = embed_authbits. embed(embededim, hashes)
    embed_t2 = time.time()

    # extract recoverybits
    extracted_bits = extract.extract(embededim2)
    extract_t = time.time()
    # extract recoverybits
    extracted_bits2 = extract_authbits.extract(embededim2)
    extract_t2 = time.time()
    # extract
    # compare

    # print
    print("imagepath:", imagepath)
    print("recovery_bits:", recovery_bits.shape)
    print("hashes:", hashes.shape)
    print("embededim:", embededim.shape)
    print("embededim2:", embededim2.shape)
    print("psnr", cv2.PSNR(imarr, embededim))
    print("psnr2", cv2.PSNR(imarr, embededim2))
    print("extracted_bits:", extracted_bits.shape)
    print("extracted_bits2:", extracted_bits2.shape)
    print("imread_t:", imread_t-start_t)
    print("make_t:", make_t-imread_t)
    print("make_t2:", make_t2-make_t)
    print("embed_t:", embed_t-make_t)
    print("embed_t2:", embed_t2-embed_t)
    print("extract_t:", extract_t-embed_t)
    print("extract_t2:", extract_t2-extract_t)
    print("result embedding:", "CORRECT" if (
        recovery_bits != extracted_bits).sum() == 0 else "INCORRECT")
    print("result hashes:", "CORRECT" if (
        hashes != extracted_bits2).sum() == 0 else "INCORRECT")
    print("alltime: ", time.time()-start_t)

    # Image.fromarray(embededim).show("RecoveryTest")
    Image.fromarray(embededim2).show("EmbeddingTest")


def auth(imagepath):
    start_t = time.time()

    imarr = np.array(Image.open(imagepath).convert('L'))
    imread_t = time.time()

    lookup = np.array([[0, 7, 13, 10],
                      [1, 6, 12, 11],
                      [4, 2, 9, 15],
                      [5, 3, 8, 14]], dtype=np.uint8)

    # make recoverybits
    recovery_bits = make.make(imarr, lookup)
    make_t = time.time()

    # embed recoverybits
    embededim = embed.embed(imarr, recovery_bits)
    embed_t = time.time()

    # make hashes
    hashes = make_authbits.make(embededim)
    make_t2 = time.time()

    # embed hashes
    embededim2 = embed_authbits.embed(embededim, hashes)
    embed_t2 = time.time()

    # edit image
    startx = 1
    starty = 1
    width = 4
    height = 4

    for i in range(width):
        for j in range(height):
            embededim2[startx+i][starty+j] = 0

    # extract recoverybits
    extracted_bits = extract.extract(embededim2)
    extract_t = time.time()
    # extract recoverybits
    extracted_bits2 = extract_authbits.extract(embededim2.copy())
    extract_t2 = time.time()
    # extract
    # compare

    # print
    print("imagepath:", imagepath)
    print("recovery_bits:", recovery_bits.shape)
    print("hashes:", hashes.shape)
    print("embededim:", embededim.shape)
    print("embededim2:", embededim2.shape)
    print("psnr", cv2.PSNR(imarr, embededim))
    print("psnr2", cv2.PSNR(imarr, embededim2))
    print("extracted_bits:", extracted_bits.shape)
    print("extracted_bits2:", extracted_bits2.shape)
    print("imread_t:", imread_t-start_t)
    print("make_t:", make_t-imread_t)
    print("make_t2:", make_t2-make_t)
    print("embed_t:", embed_t-make_t)
    print("embed_t2:", embed_t2-embed_t)
    print("extract_t:", extract_t-embed_t)
    print("extract_t2:", extract_t2-extract_t)
    print("result embedding:", "CORRECT" if (
        recovery_bits != extracted_bits).sum() == 0 else "INCORRECT")
    print("result hashes:", "CORRECT" if (
        hashes != extracted_bits2).sum() == 0 else "INCORRECT")
    print("recv diff:", (recovery_bits != extracted_bits).sum())
    print("hashess diff:", np.array_equal(hashes, extracted_bits2))
    print("alltime: ", time.time()-start_t)

    # Image.fromarray(embededim).show("RecoveryTest")
    Image.fromarray(embededim2).show("EmbeddingTest")


def recovery(imagepath):
    start_t = time.time()

    imarr = np.array(Image.open(imagepath).convert('L'))
    imread_t = time.time()

    lookup = np.array([[0, 7, 13, 10],
                      [1, 6, 12, 11],
                      [4, 2, 9, 15],
                      [5, 3, 8, 14]], dtype=np.uint8)

    # make recoverybits
    recovery_bits = make.make(imarr, lookup)
    make_t = time.time()

    # embed recoverybits
    embededim = embed.embed(imarr, recovery_bits)
    embed_t = time.time()

    # make hashes
    hashes = make_authbits.make(embededim)
    make_t2 = time.time()

    # embed hashes
    embededim2 = embed_authbits.embed(embededim, hashes)
    embed_t2 = time.time()

    # edit image
    startx = 200
    starty = 200
    width = 200
    height = 200

    for i in range(width):
        for j in range(height):
            embededim2[startx+i][starty+j] = 0
            
    startx = 100
    starty = 100
    width = 100
    height = 100

    for i in range(width):
        for j in range(height):
            embededim2[startx+i][starty+j] = 0

    # extract recoverybits
    extracted_bits = extract.extract(embededim2)
    extract_t = time.time()
    # extract recoverybits
    extracted_bits2 = extract_authbits.extract(embededim2.copy())
    extract_t2 = time.time()

    # recover image
    val = watermark_recovery(embededim2, lookup)

    # print
    print("imagepath:", imagepath)
    print("recovery_bits:", recovery_bits.shape)
    print("hashes:", hashes.shape)
    print("embededim:", embededim.shape)
    print("embededim2:", embededim2.shape)
    print("psnr", cv2.PSNR(imarr, embededim))
    print("psnr2", cv2.PSNR(imarr, embededim2))
    print("extracted_bits:", extracted_bits.shape)
    print("extracted_bits2:", extracted_bits2.shape)
    print("imread_t:", imread_t-start_t)
    print("make_t:", make_t-imread_t)
    print("make_t2:", make_t2-make_t)
    print("embed_t:", embed_t-make_t)
    print("embed_t2:", embed_t2-embed_t)
    print("extract_t:", extract_t-embed_t)
    print("extract_t2:", extract_t2-extract_t)
    print("result embedding:", "CORRECT" if (
        recovery_bits != extracted_bits).sum() == 0 else "INCORRECT")
    print("result hashes:", "CORRECT" if (
        hashes != extracted_bits2).sum() == 0 else "INCORRECT")
    print("recv diff:", (recovery_bits != extracted_bits).sum())
    print("hashess diff:", np.array_equal(hashes, extracted_bits2))
    print("alltime: ", time.time()-start_t)
    print("recovertime:", val.time)

    Image.fromarray(embededim2).show("EmbeddingTest")
    Image.fromarray(val.imarr).show("RecoveryTest")


imagepath = "/media/crackaf/44edb061-17db-4bf8-89a9-ad14bbb373b5/code/github/fyp/implementation/raw/lena.gif"
recovery(imagepath)
