from skimage.transform import resize
from skimage.metrics import structural_similarity
import cv2
import PIL.Image as Image
import io
import base64
import numpy

def orb_sim(img1, img2):
    orb = cv2.ORB_create()

    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(desc_a, desc_b)
    similar_regions = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)


def structural_sim(img1, img2):

    sim, diff = structural_similarity(img1, img2, full=True)
    return sim

def find_similarity(pimg00,pimg01):
    cimg00 = cv2.cvtColor(numpy.array(pimg00), cv2.COLOR_RGB2BGR)
    cimg01 = cv2.cvtColor(numpy.array(pimg01), cv2.COLOR_RGB2BGR)
    orb_similarity = orb_sim(cimg00, cimg01)
    # imgx = resize(cimg01, (cimg00.shape[0], cimg00.shape[1]),anti_aliasing=True, preserve_range=True)
    # ssim = structural_sim(cimg00, imgx)
    return orb_similarity

def start(data1, data2):
    byteData1 = base64.b64decode(data1)
    byteData2 = base64.b64decode(data2)
    img1 = Image.open(io.BytesIO(byteData1))
    img2 = Image.open(io.BytesIO(byteData2))
    orb = find_similarity(img1,img2)
    text1 = "ORB Sim : " + str(int(orb*10000)/100) + "%"
    # text2 = "SSIM Sim : " + str(int(ssim*10000)/100) + "%"
    return text1