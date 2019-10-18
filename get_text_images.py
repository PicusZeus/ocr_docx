#!/usr/bin/python3

import os
import shutil
import logging
import argparse
import tempfile
import concurrent.futures
from multiprocessing import Lock
import cv2
from pathlib import Path
from zipfile import ZipFile


IMAGE_EXT = ('png', 'jpeg', 'jpg', 'emf')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format_log = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
logpath = Path(Path.cwd() / 'image.log')
fileHandler = logging.FileHandler(logpath)
fileHandler.setFormatter(format_log)
logger.addHandler(fileHandler)
stream = logging.StreamHandler()
stream.setFormatter(format_log)
logger.addHandler(stream)
lock = Lock()

def is_image(filename):
    # a utility function
    return any(filename.endswith(ext) for ext in IMAGE_EXT)


def extract_images(filepath, destination_folder='images'):
    '''Function to extract images from a given docx file'''

    overall_size = 0
    data = []
    destination = Path.cwd() / destination_folder
    try:
        # Creates a temporary directory
        with tempfile.TemporaryDirectory() as working_dir:
            logger.info('Created temporal working directory {}'.format(working_dir))

            # Unzips the images
            with ZipFile(filepath) as working_zip:
                image_list = [name for name in working_zip.namelist() if is_image(name)]
                for x in image_list:
                    overall_size = overall_size + working_zip.getinfo(x).file_size
                file_count = len(image_list)
                working_zip.extractall(working_dir, image_list)

                data.append(file_count)
                data.append(overall_size)
            logger.info('Extracted {} images'.format(file_count))

            # Copies the extracted images to destination directory
            for x in image_list:

                shutil.copy(Path(working_dir).resolve() / x, destination.resolve())
                logger.info('Copied {}'.format(x))
            logger.info('Copied all image files to {}'.format(destination))

        return data

    except Exception as e:
        logger.info('File is a {}'.format(filepath.suffix))
        logger.error(
            'There was an error unzipping the file, make sure it\'s a zipped file (.zip, .docx, .xlsx, .pptx)')
        logger.exception(e)

        data.append(filepath.suffix)

        return data

def emf_to_png_all(folder='images'):
    """
    in docx some images are stored as emf files,
    this format need to be converted first into sth readable, and the easiest way is to use openoffice.
    there are also cropped and thresholded, in order to be make it easier to ocr
    """

    p = Path(Path.cwd() / folder)
    if not p.is_dir():
        logger.error('no images folder')
    emf_files = [x for x in p.glob('*.emf')]
    if len(emf_files) > 0:
        os.chdir(str(Path(Path.cwd() / folder)))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            [executor.submit(emf_to_png, file) for file in emf_files]

        img_files = [x for x in os.listdir('.') if is_image(x)]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            [executor.submit(prepare_img_to_ocr, path) for path in img_files]
        os.chdir('..')

def emf_to_png(file_path):
    with lock:
        os.system("libreoffice --headless --convert-to png {}". format(str(file_path)))
        file_path.unlink()



def prepare_img_to_ocr(path):
    with lock:
        cropped = get_text_field(path)
        cv2.imwrite(path, cropped)

def get_text_field(img_path):
    """
    in docx images are stored in files, that have white background and on it
    the picture that was pasted into doc. This inhibits ocr, and
    so text field has to be extracted first
    :param img: an img file path from docx, if emf, it has to be firstyly convverted
     to png.
    :return: a cropped and thresholded np object that can be used by pytesseract
    """
    img = cv2.imread(str(img_path), 0)
    try:
        logger.info('processing {}'.format(img_path))
    except:
        logger.error('incorrect img path')
        return None
    img_inv = cv2.bitwise_not(img)

    contours,hierarchy = cv2.findContours(img_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # there should be only one text field
    dst = contours[0]
    cropped = img[dst[0][0][1]:dst[2][0][1],dst[0][0][0]:dst[2][0][0]]

    medium = (int(cropped[2].max()) + int(cropped[2].min())) // 2
    if medium > 155:
        medium = medium - (medium // 6)
        # if the img is too dark medium variable must be modified

    ret, thresh = cv2.threshold(cropped,medium,255, cv2.THRESH_BINARY)
    return thresh



def main():
    parser = argparse.ArgumentParser(prog='get_image_text.py',
                                     description='Extracts images from docx, convert them to png and prepare to ocr')
    parser.add_argument('filepath')
    parser.add_argument('-d', '--destination', default='images')
    args = parser.parse_args()

    if args.destination == 'images':
        if not Path(Path.cwd() / 'images').is_dir():
            Path.mkdir(Path.cwd() / 'images')
            logger.info("directory 'images' created")

    if args.destination:
        if Path(args.filepath).is_file() and Path(args.destination).is_dir():
            process = extract_images(Path(args.filepath), Path(args.destination))
            if len(process) == 2:
                print('Operation completed successfully. {} images were extracted ({:,.2f}KB total)'.format(process[0],
                                                                                                            process[1]/1024))
                logger.info('Operation successful')
                logger.info('Converting to png')
                emf_to_png_all(args.destination)
            else:
                print('Operation failed. File type {} not supported.'.format(process[0]))
                logger.info('Operation failed')
        else:

            logger.info('Filename or destination directory doesn\'t exist')
            logger.error(
                'File: {}; Directory: {}'.format(Path(args.filepath).exists(), Path(args.destination).exists()))


if __name__ == "__main__":
    main()
