from scipy.stats import gumbel_r
from scipy.special import gamma
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math
import time

gumbel_min = gumbel_r.ppf(0.01)
gumbel_max = gumbel_r.ppf(0.99)

def getRandomTipettPPF():
    return np.random.randint(gumbel_min*100,gumbel_max*100)/100
    #return np.random.randint(0,100)/100

def fishertippett(s):
    L = 10
    fract1=(L**L)/gamma(L)
    exp1 = math.exp(L*s)
    exp2 = math.exp((-1) * L * math.exp(s))
    res = fract1 * exp1 * exp2
    return res

def normalizeNoise(noise):
    return noise

#Noise value between 0 and 1
def getNoiseValue():
    rand_tipett = getRandomTipettPPF()
    noise_val = fishertippett(rand_tipett)

    noise_val_normalized = normalizeNoise(noise_val)

    return noise_val_normalized

def generateNoise2D(resize,scale):

    width = int(resize[1]//scale)
    height = int(resize[0]//scale)

    noise2Darr = []

    for line in range(height):
        noisyLine = []
        for column in range(width):
            noisyLine.append(getNoiseValue())
        noise2Darr.append(noisyLine)


    img_resized = Image.fromarray(np.array(noise2Darr)).resize((resize[0],resize[1]))

    return np.array(img_resized)

def resizer(img,newsize):
    img_resized = Image.fromarray(img).resize(newsize)
    return img_resized

def convert2greyscale(img):
    np_cleaned_img = []

    for line in img:
        newline=[]
        
        for pix in line:
            newpix = pix[:3]
            sum = 0
            for c in newpix:
                sum+=c
            
            newline.append(sum/3)

        np_cleaned_img.append(newline)

    return np.array(np_cleaned_img)



def convert2log(img):
    np_cleaned_img = []

    for line in img:
        newline=[]
        
        for pix in line:

            if(pix<=0):
                print("negative value = ",pix)
                newline.append(0)
            else:         
                newline.append(math.log(pix))

        np_cleaned_img.append(newline)

    return np.array(np_cleaned_img)

def convert2exp(img):
    np_cleaned_img = []

    for line in img:
        newline=[]
        
        for pix in line:
                        
            newline.append(math.exp(pix))

        np_cleaned_img.append(newline)

    return np.array(np_cleaned_img)

def applyNoise(sar_img,noiseImg,scale=1):
    width = sar_img.shape[0]
    height = sar_img.shape[1] 

    noisy_res = []
        
    for line in range(height):
        newline=[]
        for pix in range(width):
            newpix = sar_img[line][pix]+noiseImg[line][pix]*scale
            newline.append(newpix)

        noisy_res.append(newline)
    
    return np.asarray(noisy_res)

def tipettNoiser_fromPNG(path,resize,noisepower, noisescale):

    time1 = time.time()
    #print(f"opening file")
    sar_file = Image.open(path)
    #print(f"opened file in : {(time.time()-time1):0.3f}")

    #print(sar_file)

    time2 = time.time()
    sar_file_resized = sar_file.resize(resize)
    #print(f"resized file in : {(time.time()-time2):0.3f}")

    np_sar_file_resized =  np.asarray(sar_file_resized)

    time3 = time.time()
    np_sar_cleaned = convert2log(np_sar_file_resized)
    #print(f"converted to greyscale array in : {(time.time()-time3):0.3f}")

    time4 = time.time()
    noiseImg = generateNoise2D(resize,noisescale)
    #print(f"generated noise array in : {(time.time()-time4):0.3f}")

    time5 = time.time()
    noisy_sar = applyNoise(np_sar_cleaned,noiseImg,noisepower)
    #print(f"applied noise in : {(time.time()-time5):0.3f}")

    time6 = time.time()
    noisy_sar = convert2exp(noisy_sar)
    #print(f"converted to exp in : {(time.time()-time6):0.3f}")

    #print(f"total computation time : {(time.time() - time1):0.3f}")

    return noisy_sar

def tipettNoiser_fromARRAY(array,noisepower, noisescale):

    sar_file = array

    # time2 = time.time()
    sar_file_resized = sar_file
    #print(f"resized file in : {(time.time()-time2):0.3f}")

    np_sar_file_resized =  sar_file_resized

    # time3 = time.time()
    np_sar_cleaned = convert2log(np_sar_file_resized)
    #print(f"converted to greyscale array in : {(time.time()-time3):0.3f}")

    # time4 = time.time()
    noiseImg = generateNoise2D(array.shape,noisescale)
    #print(f"generated noise array in : {(time.time()-time4):0.3f}")

    # time5 = time.time()
    noisy_sar = applyNoise(np_sar_cleaned,noiseImg,noisepower)
    #print(f"applied noise in : {(time.time()-time5):0.3f}")

    # time6 = time.time()
    noisy_sar = convert2exp(noisy_sar)
    #print(f"converted to exp in : {(time.time()-time6):0.3f}")

    #print(f"total computation time : {(time.time() - time2):0.3f}")

    return noisy_sar