from pdf20 import page_16_17, page_1_2
from extract_images import extract_images
import os
import time
from multiprocessing import Pool


def main():
    ts = time.time()
    pdfs_path = os.getcwd() + '/data/'
    # p = multiprocessing.Pool()
    # q = multiprocessing.Pool()
    # r = multiprocessing.Pool(processes=4
    pdfs = list()
    for pdf in os.listdir(pdfs_path):
        pdfs.append(pdfs_path+pdf)

    with Pool(20) as p:
        p.map(extract_images, pdfs)
    
    with Pool(20) as p:
        p.map(page_1_2, pdfs)

    with Pool(20) as p:
        p.map(page_16_17, pdfs)

    # for _ in range(100):
        # print("processing {}".format(pdf))
        # p = map(extract_images, file)
        # q = map(page_1_2, file)
        # r = map(page_16_17, file)
        # extract_images(file)
        # page_1_2(file)
        # page_16_17(pdfs_path + pdf)
    print("Time is {}".format(time.time() - ts))


if __name__ == '__main__':
    main()
    # ts = time.time()
