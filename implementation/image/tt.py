# %%
from PIL import Image
import numpy as np


# %%
import time
start = time.time()


# %% [markdown]
# FLAGS
# 

# %%
filename="arbabcat"
ext="jpg"

# %% [markdown]
# blocks getting function
# 

# %%
def getblocks(image: np.ndarray, blockshape: tuple, moveAxis: bool = True, info: bool = False, addChannel: bool = True) -> np.ndarray:
    '''
    takes the array of image in grey= 2D and in RGB = 3D
    takes the numpy array and converts it the the blocks in the fastest way
    '''
    if(info):
        print("Image Shape:", image.shape)
        print("Block Shape:", blockshape)

    oldshape = list(image.shape)
    if addChannel and len(image.shape) == 2:
        mode = "grey"
        image = image.reshape((*image.shape, 1))
    else:
        mode = "color"

    if addChannel:
        img_height, img_width, channels = image.shape
    else:
        img_height, img_width = image.shape

    tile_height, tile_width = blockshape

    if addChannel:
        shp = img_height//tile_height, tile_height, img_width//tile_width, tile_width, channels
    else:
        shp = img_height//tile_height, tile_height, img_width//tile_width, tile_width

    def printinfo():
        print("Old Shape:", oldshape)
        print("Image Shape:", image.shape)
        print("Block Shape:", blockshape)
        print("New Shape Initial:", shp)
        print("img_height % tile_height != 0 :", img_height % tile_height != 0)
        print("img_width % tile_width != 0 :", img_width % tile_width != 0)

    if img_height % tile_height != 0 or img_width % tile_width != 0:
        print("warning: Block size is not fit for the image!")
        printinfo()

    if(info):
        printinfo()

    tiled_array = image.reshape(shp)
    tiled_array = tiled_array.swapaxes(1, 2)

    if moveAxis:
        if(addChannel):
            tiled_array = tiled_array.reshape(-1,
                                              *(tile_height, tile_width, channels))
            tiled_array = np.moveaxis(tiled_array, source=len(
                tiled_array.shape)-1, destination=1)
        else:
            tiled_array = tiled_array.reshape(-1, *(tile_height, tile_width))

    return tiled_array


# %%
def combineBlocks(tiled_array: np.ndarray, imageshape: tuple, blockshape: tuple, movedAxis: bool = True, channel: bool = True) -> np.ndarray:

    if channel:
        if len(imageshape) == 2:
            mode = "grey"
            imageshape = *imageshape, 1
        else:
            mode = "color"

    if channel:
        img_height, img_width, channels = imageshape
    else:
        img_height, img_width = imageshape

    tile_height, tile_width = blockshape

    if movedAxis:
        image = tiled_array.copy()
        if(channel):
            image = image.reshape(img_height//tile_height, tile_height,
                                  img_width//tile_width, tile_width, channels)
            swapaxisShape = list(image.shape)
            swapaxisShape[1], swapaxisShape[2] = swapaxisShape[2], swapaxisShape[1]
            image = image.reshape(swapaxisShape)
            image = image.swapaxes(1, 2)
        else:
            f = image.reshape(img_height//tile_height, tile_height,
                              img_width//tile_width, tile_width)
            swapaxisShape = list(f.shape)
            swapaxisShape[1], swapaxisShape[2] = swapaxisShape[2], swapaxisShape[1]
            tmp = f.reshape(swapaxisShape)
            image = tmp.swapaxes(1, 2)
    else:
        image = tiled_array
        # I haven't completed this else case. Btw we aren't using this case lol :)

    return image.reshape(imageshape)


# %%
def printnd(arr: np.ndarray):
    print("Shape:", arr.shape)
    print("Strides:", arr.strides)
    print(arr)


# %% [markdown]
# PSNR function
# 

# %%
from math import log10, sqrt


# %%
def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


# %% [markdown]
# importing image
# e.g lena which is 512x512
# importing as the grey image denoted by L flag
# 

# %%
lena = Image.open(f"{filename}.{ext}").convert("L")
lena
# lena = Image.open("fyp_image.JPG").convert("L")
# lena


# %% [markdown]
# converting to np array
# 

# %%
img = np.array(lena)
imgSize = img.shape
M, N = img.shape
img.shape, img.strides, img


# %%
if imgSize[0] % 64 != 0 or imgSize[1] % 64 != 0:
    raise Exception("Size not correct for embedding")


# %% [markdown]
# making 16 main blocks
# size of single main block S= M/sqrt(16) X T=N/sqrt(16)
# e.g for lena the 512x512 the partner blocks size would be 16 blocks each with size (512x512)/(4x4) = 128x128
# 

# %%
mainblockSize = (int(imgSize[0]/4), int(imgSize[1]/4))
mainblocks = getblocks(img.copy(), mainblockSize, info=True)
mainblocks.shape, mainblocks.strides, mainblocks


# %% [markdown]
# here the main blocks are like this index.
# 1st index is the block number.
# 2nd index is the channel (RGB) or 0 in Grey.
# 3rd and 4th are for indexing the block.
# 

# %% [markdown]
# converting back and checking
# 

# %% [markdown]
# lookup table
# 

# %%
lookup = np.array([[0, 7, 13, 10],
                  [1, 6, 12, 11],
                  [4, 2, 9, 15],
                  [5, 3, 8, 14]], dtype=np.uint8)
lookup


# %% [markdown]
# here the every row represents the partner blocks
# e.g
# A1 will be lookup[0][0].
# A2 will be lookup[0][2].
# D2 will be lookup[3][2].
# 

# %% [markdown]
# Step3
# Ab har main block ko divide karo k 4x4 k block ban jain
# numberOfBlocks=(SxT)/(4x4)
# e.g 128x128/4x4 = 1024
# 

# %%
avgblocksSize = (4, 4)
averages = np.zeros((16, int((mainblockSize[0]*mainblockSize[1]) /
                             (avgblocksSize[0]*avgblocksSize[1]))), dtype=np.uint8)
# 4 indicatior A,B,C,D, 4 blocks of A, then the 4x4 Blocks which have count = (SxT)/(4x4), e.g 1024


# %% [markdown]
# storing the averages of A, B, C, D
# 

# %%
for partner in lookup:  # A,B,C,D
    for id in partner:  # A1,A2,A3.....D4 etc
        averages[id] = getblocks(mainblocks[id][0].copy(), avgblocksSize,
                                 info=False, addChannel=False).mean((1, 2))


# %% [markdown]
# array([[162, 162, 162, 161],
#        [162, 162, 162, 161],
#        [162, 162, 162, 161],
#        [162, 162, 162, 161]], dtype=uint8)
# this will give you the avg 161. But it sould be 162 as it's dominant. Minor improvemnt reuqired
# 

# %% [markdown]
# now we have average of every mainblock according to 4x4. Which in total are 1024
# 

# %% [markdown]
# time to convert them into the binary
# 

# %%
averageBits = np.unpackbits(averages, axis=1)
# averageBits.shape, averageBits


# %% [markdown]
# merging partner blocks average to make the recovery bits
# 

# %%
recoveryBits = np.zeros(
    (averageBits.shape[0], averageBits.shape[1]*3), dtype=np.uint8)
for partner in lookup:  # A,B,C,D
    for id in partner:  # A1,A2,A3.....D4 etc
        recoveryBits[id] = np.concatenate(
            [averageBits[i] for i in partner if i != id])

# recoveryBits.shape, recoveryBits


# %% [markdown]
# password or key generation
# 

# %%
import hashlib


# %%
# password or key
password = "this is my password"
key = [x for x in hashlib.sha256(password.encode()).digest()]
# len(key)


# %% [markdown]
# permuttaion or shuffling
# 

# %%
for i in range(recoveryBits.shape[0]):
    np.random.RandomState(seed=key).shuffle(recoveryBits[i])

# recoveryBits.shape, recoveryBits


# %% [markdown]
# Recovery bits creation completed
# Now we need to make the space to put these recovery bits
# 

# %% [markdown]
# ### Making 16x16 for Step 8
# 
# Dividing the main blocks to 16x16 blocks
# Total blocks = SxT/16x16 = 128x128/16x16 = 64 Blocks
# 

# %%
mainblocks.shape


# %%
blocks16x16Size = (16, 16)
# reshaping because we needed that shape
blocks16x16 = mainblocks.copy().reshape(
    *mainblocks.shape[:-2],
    int((mainblockSize[0]*mainblockSize[1]) /
        (blocks16x16Size[0]*blocks16x16Size[1])),
    blocks16x16Size[0], blocks16x16Size[1]).copy()

# blocks16x16Size, blocks16x16.shape, blocks16x16.strides, blocks16x16


# %%
for i in range(mainblocks.shape[0]):
    blocks16x16[i][0] = getblocks(mainblocks[i][0].copy(), blocks16x16Size,
                                  info=False, addChannel=False)

# blocks16x16.shape, blocks16x16.strides, blocks16x16


# %% [markdown]
# combinign for checking
# 

# %% [markdown]
# ### Making 8x8 blocks of those 16x16 Step 9
# 

# %%
blocks8x8Size = (8, 8)
# reshaping because we needed that shape
blocks8x8 = blocks16x16.copy().reshape(
    *blocks16x16.shape[:-2],
    int((blocks16x16Size[0]*blocks16x16Size[1]) /
        (blocks8x8Size[0]*blocks8x8Size[1])),
    blocks8x8Size[0], blocks8x8Size[1])

# blocks8x8Size, blocks8x8.shape, blocks8x8.strides, blocks8x8


# %%
for i in range(blocks16x16.shape[0]):
    for j in range(blocks16x16.shape[2]):
        blocks8x8[i][0][j] = getblocks(blocks16x16[i][0][j].copy(), blocks8x8Size,
                                       info=False, addChannel=False)

# blocks8x8.shape, blocks8x8.strides, blocks8x8


# %% [markdown]
# combining and checking
# 

# %% [markdown]
# Now put the recovery bit in the first and second LSB of blocks4x4
# 

# %%
recoveryBits.reshape(recoveryBits.shape[0], int(
    recoveryBits.shape[1]//2), 2).shape


# %% [markdown]
# updating the lsb
# 

# %%
def set_bit(value, index, x):
    # """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    # mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    # # Clear the bit indicated by the mask (if x is False)
    # value &= ~mask
    # if x:
    #     # If x was True, set the bit indicated by the mask.
    #     value |= mask
    # return value            # Return the result, we're done.
    def set_bit2(value, bit):
        return value | (1 << bit)

    def clear_bit(value, bit):
        return value & ~(1 << bit)

    if x:
        return set_bit2(value, index)
    else:
        return clear_bit(value, index)


def get_bit(value, index):
    if value & (1 << index):
        return True
    else:
        return False


# %%
set_bit(2, 3, 0), set_bit(2, 2, 1)
#(0, 6)


# %%
bits = recoveryBits.reshape(
    recoveryBits.shape[0], int(recoveryBits.shape[1]//2), 2)
for i in range(blocks8x8[:, 0].shape[0]):
    for j in range(len(blocks8x8[i, 0, :, :3, :, :].flat)):
        number = blocks8x8[i, 0, :, :3, :, :].flat[j]
        blocks8x8[i, 0, :, :3, :, :].flat[j] = set_bit(
            set_bit(number, 0, bits[i][j][0]), 1, bits[i][j][1])

# for mainblock, blockbits in zip(blocks8x8[:, 0, :, :3, :, :], recoveryBits.reshape(recoveryBits.shape[0], int(recoveryBits.shape[1]//2), 2)):
#     for number, bits in zip(mainblock.flat, blockbits):
#         # print(number, bits)
#         number = set_bit(set_bit(number, 0, bits[0]), 1, bits[1])

# blocks8x8.shape, blocks8x8.strides, blocks8x8


# %% [markdown]
# ### get authenticaction bits
# 

# %% [markdown]
# getting hash of four blocks with lsb 0
# 

# %% [markdown]
# so we have the space of 128bit for hashing
# we want to add the size of image + the blocknumber of eachblock
# size will be multiple of 64
# 1byte of length, max length = 64*256=16384
# 1byte of width, max width = 64*256=16384
# the remaing length for hash is now 112
# for block number I'm excluding the 4 bits and 4bits will be reserved for the lookuptable
# the make the total bits=104, that make 104/8=13bytes
# we are using dynamic hasing algo (blake2b) with digest size 13bytes
# 

# %%
HASH_SIZE = 16


# %%
def set_lsb_zero(num: np.ndarray):
    '''
    Clearing the first two LSB of ndarray
    '''
    return set_bit(set_bit(num, 0, 0), 1, 0)


'''
Data is one 16x16 block converted into four 8x8 blocks
'''


def hash_block(data: np.ndarray, key: str = None, digest_size=HASH_SIZE, extras=[]):
    if data.shape != (4, 8, 8):
        print(f"Warning! given size {data.shape} instead of (4, 8, 8)")
    local = data.copy().astype(np.int8)  # copying to avoid overighting lsb
    local[-1] = set_lsb_zero(local[-1])  # setting last 8x8 blocks lsb zero
    if key is None:
        h = hashlib.blake2b(digest_size=digest_size)
    else:
        h = hashlib.blake2b(key=key.encode())
    h.update(local.data)
    for extra in extras:
        h.update(extra.encode())
    return h


def put_bits(data: np.ndarray, bits: np.ndarray):
    '''
    puts data in last two lsb of data
    '''
    if data.shape != (8, 8):
        print(f"Warning! given size {data.shape} instead of (8, 8)")
    if bits.shape != (64, 2):
        print(f"Warning! given size {bits.shape} instead of (64, 2)")
    localData = data.copy().reshape(-1)
    localBits = bits.copy()
    '''
    setting last two lsb of data to bits
    '''
    localData = np.fromiter((set_bit(set_bit(d, 0, b[0]), 1, b[1]) for d, b in zip(
        localData, localBits)), dtype=data.dtype)

    return localData.reshape(8, 8)


def get_bits(data: np.ndarray):
    '''
    gets data from last two lsb of data
    '''
    if data.shape != (8, 8):
        print(f"Warning! given size {data.shape} instead of (8, 8)")
    localData = data.copy()
    bits = np.zeros((64, 2), np.uint8)
    bits[:, 0] = np.fromiter((get_bit(d, 0)
                             for d in localData.flat), dtype=np.uint8)
    bits[:, 1] = np.fromiter((get_bit(d, 1)
                             for d in localData.flat), dtype=np.uint8)
    return bits


# %%
hashes = np.zeros((*blocks8x8[:, 0].shape[:2], HASH_SIZE*8), dtype=object)
# hashes.shape, hashes


# %%
def hexToDec(hexStr):
    return np.fromiter((int(x, 16) for x in hexStr), dtype=np.uint8)


def binToNp(binStr):
    return np.frombuffer(binStr, dtype=np.uint8)


# has = hash_block(blocks8x8[0, 0, 1])

# print(has, has.hexdigest(), len(has.digest()))
# dec = binToNp(has.digest())
# dec.shape, dec


# %%
# binToNp(b'\x')


# %%
# hashes[0]='ashdadka'
# hashes


# %%
# type(hashlib.sha256("basd".encode()).hexdigest())


# %%
# hash_block(blocks8x8[0, 0, 0], digest_size=32)


# %%
# temp=hash_block(
#             blocks8x8[0, 0, 0])
# x=temp.digest()
# temp.hexdigest(), binToNp(temp.digest()), x, type(x), x.hex(), x[0], x[1].to_bytes(8, byteorder='big').hex()


# %% [markdown]
# so there are four block of 8x8
# 8x8 block has (2bits) _ 8 _ 8=128bit space
# 

# %%
for i in range(blocks8x8[:, 0].shape[0]):
    for j in range(blocks8x8[:, 0].shape[1]):
        hashes[i][j] = np.unpackbits(binToNp(hash_block(
            blocks8x8[i, 0, j]).digest()))


# hashes.shape, hashes[0][0], hashes


# %% [markdown]
# #### now we have to put this hash in the 4th 8x8 block of eaxh 16x16block :)
# 

# %%
# reshaping it into 2bits in last for better placement
hashbits = hashes.reshape(
    hashes.shape[0], hashes.shape[1], hashes.shape[2]//2, 2)
# hashbits.shape


# %% [markdown]
# not the best approach
# will do it like we did with recoverybits

# %%
for i in range(blocks8x8[:, 0].shape[0]):
    for j in range(blocks8x8[:, 0].shape[1]):
        blocks8x8[i, 0, j, 3, :, :]=put_bits(blocks8x8[i, 0, j, 3, :, :], hashbits[i, j])

# blocks8x8.shape, blocks8x8.strides, blocks8x8


# %% [markdown]
# ### Now to combine the blocks back to Image
# 

# %% [markdown]
# first merge the 8x8
# 

# %%
combined16x16 = blocks16x16.copy()


# %%
for i in range(combined16x16.shape[0]):
    for j in range(combined16x16.shape[2]):
        combined16x16[i][0][j] = combineBlocks(blocks8x8[i][0][j].copy(), imageshape=(
            16, 16), blockshape=(8, 8), channel=False)
# combined16x16.shape, combined16x16.strides, combined16x16


# %% [markdown]
# merging 16x16 to 128x128
# 

# %%
combinedMainBlocks = mainblocks.copy()


# %%
for i in range(combinedMainBlocks.shape[0]):
    combinedMainBlocks[i][0] = combineBlocks(
        combined16x16[i][0], mainblockSize, blockshape=(16, 16), channel=False)

# combinedMainBlocks.shape, combinedMainBlocks


# %%
combinedImg = combineBlocks(combinedMainBlocks.copy(), imgSize, mainblockSize)
combinedImg.shape, combinedImg
combinedImg = combinedImg.reshape(imgSize)
combinedImg.shape, combinedImg


# %% [markdown]
# combining to the image
# 

# %%
Image.fromarray(combinedImg, 'L')


# %%
PSNR(img, combinedImg)


# %%
done = time.time()
elapsed = done - start


# %%
print(elapsed)

# %%
imgSize

# %%
raise Exception('stop')

# %%
print("This time includes all the unnessary outputs and checks")
elapsed


# %%
# saving to file
Image.fromarray(combinedImg, 'L').save(f"{filename}_watermarked.png")


# %%
# checking the saved file
lena = Image.open(f"{filename}_watermarked.png").convert("L")
img = np.array(lena)


# %%
(img == combinedImg).all()


# %% [markdown]
# # Auth

# %%
extractedHashes = np.zeros(hashbits.shape, dtype=hashbits.dtype)
extractedHashes.shape, extractedHashes


# %%
for i in range(blocks8x8[:, 0].shape[0]):
    for j in range(blocks8x8[:, 0].shape[1]):
        number = blocks8x8[i, 0, :, 3, :, :].flat[j]
        extractedHashes[i][j]=get_bits(blocks8x8[i, 0, j, 3, :, :])

blocks8x8.shape, blocks8x8.strides, blocks8x8


# %%
extractedHashes


# %%
extractedHashes.reshape(-1).shape, hashbits.reshape(-1).shape


# %%
extractedHashes.reshape(-1).shape, hashbits.reshape(-1).shape


# %%
ret=(extractedHashes.reshape(-1) == hashbits.reshape(-1))
unique, counts = np.unique(ret, return_counts=True)
dic=dict(zip(unique, counts))
dic

# %%
if False in dic:
  raise Exception("not all hashes are equal, embedding of auth bits are not correct")
else:
  print("all hashes are equal, embedding of auth bits are correct")

# %%
extractedHashes=extractedHashes.reshape(extractedHashes.shape[0], extractedHashes.shape[1], extractedHashes.shape[2]*2)
hashbits=hashbits.reshape(hashbits.shape[0], hashbits.shape[1], hashbits.shape[2]*2)
extractedHashes.shape, hashbits.shape


# %%
tempred=np.zeros((extractedHashes.shape[0],extractedHashes.shape[1]), dtype=np.uint8)
tempred.shape

# %%
for i in range(extractedHashes.shape[0]):
    for j in range(extractedHashes.shape[1]):
        tempred[i][j]=(extractedHashes[i][j]==hashbits[i][j]).all()

# %%
tempred

# %%
unique, counts = np.unique(tempred, return_counts=True)
dict(zip(unique, counts))

# %%
tempred = np.where(tempred == 1, 255, tempred)

# %%
tempred.shape

# %%
Image.fromarray(tempred, 'L')


# %%
Image.fromarray(tempred.reshape(imgSize[0]//16,imgSize[1]//16), 'L')


# %%
temp=tempred.copy()

# %%
temp=temp.reshape(temp.shape[0], imgSize[0]//64,imgSize[1]//64)
temp.shape

# %%
temp=combineBlocks(temp,(imgSize[0]//16,imgSize[1]//16),(imgSize[0]//64,imgSize[1]//64),channel=False)
temp.shape

# %%
Image.fromarray(temp.reshape(imgSize[0]//16,imgSize[1]//16), 'L')


# %%
imgSize

# %%
(imgSize[0]//16,imgSize[1]//16)

# %% [markdown]
# # Recovery

# %%
extractedRecvBits=np.zeros(bits.shape, dtype=bits.dtype)
extractedRecvBits

# %%
(blocks8x8==prev8x8).all()

# %%
for i in range(blocks8x8[:, 0].shape[0]):
  for j in range(len(blocks8x8[i, 0, :, :3, :, :].flat)):
    number= blocks8x8[i, 0, :, :3, :, :].flat[j]
    extractedRecvBits[i][j][0]=get_bit(number, 0)
    extractedRecvBits[i][j][1]=get_bit(number, 1)

# %%
extractedRecvBits

# %%
bits.shape

# %%
blocks8x8[:, 0].shape[0]

# %%
len(blocks8x8[i, 0, :, :3, :, :].flat)

# %%
bits

# %%
(extractedRecvBits==bits).all()


