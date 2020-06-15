import imageio
import numpy as np
#from skimage.color import rgb2lab, rgb2gray, lab2rgb
import matplotlib.pyplot as plt

def print_image_summary(image, labels):
    print('--------------')
    print('Image Details:')
    print('--------------')
    print(f'Image dimensions: {image.shape}')
    print('Channels:')

    if len(labels) == 1:
        image = image[..., np.newaxis]

    for i, lab in enumerate(labels):
        min_val = np.min(image[:,:,i])
        max_val = np.max(image[:,:,i])
        print(f'{lab} : min={min_val:.4f}, max={max_val:.4f}')





def histogram(A, no_levels):
    # gets the size of the input matrix
    N, M = A.shape

    # creates an empty histogram with size proportional to the number of graylevels
    hist = np.zeros(no_levels).astype(int)

    # computes for all levels in the range
    for i in range(no_levels):
        # the np.where() function returns the indices for all coordinates
        # in some array matching the condition. In this case, all pixels
        # that have value 'i'
        pixels_value_i = np.where(A == i)

        # by counting how many coordinates the np.where function returned,
        # we can assign it at the respective histogram bin
        # this is done by getting the size of the vector of coordinates
        hist[i] = pixels_value_i[0].shape[0]

    return(hist)




def global_histogram(img, bins, norm='sum', factor=512):
    # single color channel
    if (len(img.shape) == 2):
        hist,_ = np.histogram(img, bins=bins)
    
    # RGB
    if (len(img.shape) == 3):
        hist_R,_ = np.histogram(img[:,:,0], bins=bins)
        hist_G,_ = np.histogram(img[:,:,1], bins=bins)
        hist_B,_ = np.histogram(img[:,:,2], bins=bins)
        hist = np.concatenate([hist_R, hist_G, hist_B])

    # normalizes resulting histogram
    hist = hist.astype(float)

    if (norm == 'sum'):
        hist /= (hist.sum() + 0.0001)

    if (norm == 'value'):
        hist /= (hist.max() + 0.0001)
        hist *= factor
        hist = hist.astype(int)

    return hist


def thresholding(f, L):
    # create a new image with zeros
    g = np.ones(f.shape).astype(np.uint8)
    g = g*255
    # setting to 1 the pixels above the threshold
    g[np.where(f < L)] = 0
    return g

def main():
    image1 = imageio.imread('Images/Cancer/con_CNC_001.png', as_gray=True)
    image2 = imageio.imread('Images/photo2.jpg', as_gray=True)

    hist1,_ = np.histogram(image1, bins=256, range=(0,256))
    #hist1 = histogram(image1, 265)
    plt.bar(range(256), hist1)

    hist2,_ = np.histogram(image2, bins=256, range=(0,256))
    #hist2 = histogram(image2, 256)
    plt.bar(range(256), hist2)
    
    processed_img = thresholding(image1, 80)
    processed_img = thresholding(image2, 160)
    imageio.imwrite('output_photo1.jpg', processed_img)
    imageio.imwrite('output_photo2.jpg', processed_img)

if __name__ == '__main__':
    main()
