from skimage.transform import resize
from skimage.metrics import structural_similarity
import cv2
from os.path import dirname, join

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

def find_similarity(file1,file2):
    img00 = cv2.imread(file1, 0)
    img01 = cv2.imread(file2, 0)

    orb_similarity = orb_sim(img00, img01)
    imgx = resize(img01, (img00.shape[0], img00.shape[1]),anti_aliasing=True, preserve_range=True)
    ssim = structural_sim(img00, imgx)
    return orb_similarity, ssim

def start(filepath1, filepath2):
    orb,ssim = find_similarity(filepath1,filepath2)
    text1 = "ORB Sim : " + str(int(orb*10000)/100) + "%"
    text2 = "SSIM Sim : " + str(int(ssim*10000)/100) + "%"
    return text1+text2