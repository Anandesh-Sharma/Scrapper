from pdf20 import page_16_17, page_1_2
from extract_images import extract_images
import os
import time
import multiprocessing


def main():
    ts = time.time()
    count = 1
    pdfs_path = os.getcwd() + '/data/'
    p = multiprocessing.Pool()
    q = multiprocessing.Pool()
    # r = multiprocessing.Pool(processes=4)

    for pdf in os.listdir(pdfs_path):
        file = pdfs_path + pdf
        print("processing {}".format(pdf))
        p = map(extract_images, file)
        q = map(page_1_2, file)
        # r = map(page_16_17, file)
        # extract_images(file)
        # page_1_2(file)
        # page_16_17(pdfs_path + pdf)
        if count > 5:
            break
        count += 1
    print("Time is {}".format(time.time() - ts))


if __name__ == '__main__':
    main()
    # ts = time.time()
