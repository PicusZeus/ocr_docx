#!/usr/bin/python3

import argparse
import logging
from pathlib import Path
from get_text_images import emf_to_png_all, extract_images
from ocr_image import ocr_text_to_docx

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format_log = logging.Formatter('%(levelname)s:%(name)s%(message)s')
logpath = Path(Path.cwd() / 'ocr.log')
fileHandler = logging.FileHandler(logpath)
fileHandler.setFormatter(format_log)
logger.addHandler(fileHandler)
stream = logging.StreamHandler()
stream.setFormatter(format_log)
logger.addHandler(stream)


def main():
    parser = argparse.ArgumentParser(prog='ocr_docx.py', description='Extract images from docx, ocr them and paste ocr text into docx file')
    parser.add_argument('filepath')
    parser.add_argument('-df', '--destination_folder', default='images')
    parser.add_argument('-d', '--destination', default='ocred.docx')
    parser.add_argument('-l', '--language', default='grc')

    args = parser.parse_args()

    if args.destination_folder == 'images':

        if not Path(Path.cwd() / 'images').is_dir():

            Path.mkdir(Path.cwd() / 'images')
            logger.info("directory 'images' created")

    if args.destination:
        print(args.filepath, args.filepath.endswith('docx'))
        if args.filepath.endswith('docx') and Path(args.destination_folder).is_dir():
            process = extract_images(Path(args.filepath), Path(args.destination_folder))
            if len(process) == 2:
                print('Operation completed successfully. {} images were extracted ({:,.2f}KB total)'.format(process[0],
                                                                                                            process[1]/1024))
                logger.info(f'{process[0]} files extracted')
                logger.info('Converting to png')
                emf_to_png_all(args.destination_folder)

                ocr_text_to_docx(args.filepath, image_folder=args.destination_folder, output_file=args.destination, lang=args.language)
            else:
                print('Operation failed. File type {} not supported.'.format(process[0]))
                logger.info('Operation failed')
        else:

            logger.info('Filename or destination directory doesn\'t exist')
            logger.error(
                'File: {}; Directory: {}'.format(Path(args.filepath).exists(), Path(args.destination).exists()))


if __name__ == '__main__':
    main()

