import numpy as np
import imageio
import matplotlib.pyplot as plt
from skimage import morphology, measure
from math import *
import math

def thresholding(f, L):
    # create a new image with zeros
    f_tr = np.ones(f.shape).astype(np.uint8)
    # setting to 1 the pixels above the threshold
    f_tr[np.where(f < L)] = 0
    return f_tr


def draw_line(mat, x0, y0, x1, y1, inplace=False):
    
    if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
            0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
        raise ValueError('Invalid coordinates.')
        
    if not inplace:
        mat = mat.copy()
        
    if (x0, y0) == (x1, y1):
        mat[x0, y0] = 1
        return mat if not inplace else None
    
    # Swap axes if Y slope is smaller than X slope
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
        
    # Swap line direction to go left-to-right if necessary
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
        
    # Write line ends
    mat[x0, y0] = 1
    mat[x1, y1] = 1
    
    # Compute intermediate coordinates using line equation
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    
    # Write intermediate coordinates
    mat[x, y] = 255
    mat[x+1, y] = 255
    mat[x-1, y] = 255
    mat[x, y+1] = 255
    mat[x, y-1] = 255
    mat[x+1, y+1] = 255
    mat[x-1, y-1] = 255
    
    if not inplace:
        return mat if not transpose else mat.T


def getAndRemoveNeighboors(curPixelPos, whitePixels, pixelsToBeProcessed, pixelCluster):          
    neighboors = {(curPixelPos[0]-1, curPixelPos[1]-1), (curPixelPos[0]-1, curPixelPos[1]), (curPixelPos[0]-1, curPixelPos[1]+1),
                  (curPixelPos[0], curPixelPos[1]-1),   (curPixelPos[0], curPixelPos[1]),   (curPixelPos[0], curPixelPos[1]+1),
                  (curPixelPos[0]+1, curPixelPos[1]-1), (curPixelPos[0]+1, curPixelPos[1]), (curPixelPos[0]+1, curPixelPos[1]+1)
                 }
    
    if (pixelCluster.count(curPixelPos) == 0):
        pixelCluster.append(curPixelPos)
        
    for p in neighboors:
        if p in whitePixels:
            pixelsToBeProcessed.append(p)
            pixelCluster.append(p)
            whitePixels.remove(p)
    
    return whitePixels, pixelsToBeProcessed, pixelCluster

# Return the group of white adjascent pixels, i.e. the pixels of the stars 
def clustering(img):
    whitePixels = set()
    recognizedClusters = []
    
    n, m = img.shape
    for x in range(n):
        for y in range(m):
            if (img[x,y] == 1):
                whitePixels.add(tuple([x,y]))
                
    while (len(whitePixels) != 0):
        pixelCluster = []
        pixelsToBeProcessed = []
        
        p = whitePixels.pop()
        pixelsToBeProcessed.append(p)
        
        while (len(pixelsToBeProcessed) != 0):
            curPixel = pixelsToBeProcessed[0]
            whitePixels, pixelsToBeProcessed, pixelCluster = getAndRemoveNeighboors(curPixel, whitePixels, pixelsToBeProcessed, pixelCluster)
            pixelsToBeProcessed.remove(curPixel)
    
        recognizedClusters.append(pixelCluster)
    
    return recognizedClusters


def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
    
    
def slope(x1, y1, x2, y2): # Line slope given two points:
    return (y2-y1)/(x2-x1)

def angle(s1, s2): 
    return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))

# Calculate the angles between the lines that connect the 3 brightest stars (making a triangle)  
def triangle_angles(stars):
    lineA = ((stars[0][0][0], stars[0][0][1]), (stars[1][0][0], stars[1][0][1]))
    lineB = ((stars[0][0][0], stars[0][0][1]), (stars[2][0][0], stars[2][0][1]))
    lineC = ((stars[1][0][0], stars[1][0][1]), (stars[2][0][0], stars[2][0][1]))

    slope1 = slope(lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1])
    slope2 = slope(lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1])
    slope3 = slope(lineC[0][0], lineC[0][1], lineC[1][0], lineC[1][1])

    a1 = abs(angle(slope1, slope2))
    a2 = abs(angle(slope1, slope3))
    a3 = abs(angle(slope3, slope2))

    triangle = []
    triangle.append(a1)
    triangle.append(a2)
    triangle.append(a3)
    triangle.sort()
    
    return triangle

def calculaErro(triangle, expected):
    erro = abs(triangle[0] - expected[0])
    erro += abs(triangle[1] - expected[1])
    erro += abs(triangle[2] - expected[2])
    return erro/3


if __name__ == __"main"__:
    main()

def main():
    filename = str(input()).rstrip()
    image1 = imageio.imread(filename, as_gray = True)
    colored_image = imageio.imread(filename)
    
    img_o1 = thresholding(image1,80)

    S = clustering(img_o1)
    # Order the stars to get the brightest ones
    stars = sorted(S, key=len)
    stars.reverse()

    # Drow the lines between the 3 brightest spots forming a triangle
    img_line = draw_line(img_o1, stars[0][0][0], stars[0][0][1], stars[1][0][0], stars[1][0][1])
    img_line = draw_line(img_line, stars[0][0][0], stars[0][0][1], stars[2][0][0], stars[2][0][1])
    img_line = draw_line(img_line, stars[1][0][0], stars[1][0][1], stars[2][0][0], stars[2][0][1])

    output_img[:,:,2] = img_line

    # Find the angles
    triangle = triangle_angles(stars)

    # Data to compare the angles of the constallations based on the angles between the brightest stars
    Constellations = {
    "Orion": [11, 25.4 ,36.45],
    "UrsaMinor": [21.2, 26.71, 47.84],
    "UrsaMajor": [14.97, 25.03, 40],
    "Gemini": [13.12, 75.9, 86.6],
    "Scorpius": [16.87, 27.4, 44.3]
    }

    menorErro = 99999

    # Compare the angle and find one of the constallations
    for const in Constellations:
        x = Constellations[const]
        erro = calculaErro(triangle, x)
        if (erro < menorErro):
            aux = const
            menorErro = erro

    print("Your Constellation is... " + aux)

    plt.imshow(img_line, cmap="gray")

    