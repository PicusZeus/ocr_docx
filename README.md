# ocr-docx

A simple Python 3 app for extracting and ocring text images pasted into docx files.
The application reads text that exists on an images and pastes it into the main text, in the paragraph the image was placed. You
should check and correct the results, because there will certainly be some mistakes, the amount of which will depend on the
quality of images. In order to work correctly the images must be pasted into the doc file as paragraphs (this is
very important), as otherwise the app will be confused and will be unable to guess were to paste the ocred text.

The app was created for Ancient Greek texts, but works fine with other languages as well. In current state
it runs only on Linux and requires OpenOffice to be installed in order to work correctly with xml files.

All the info as to how you can run the app, you can find in teh docs.rst.

It uses google tesseract. You have to install your language of choice on the machine before proceeding, for the Ancient Greek language it would be:
>sudo apt install tesseract-ocr-grc

## Change Log

    * 0.21 added TIFF to the image formats that can be processed.
    * 0.2 minor fixes, now not only Ancient Greek supported, updated dependencies, added -cr flag for docx files
    with images in different format then emf/wmf (To Do: add to extracted images flag of what original format they were
    so that it automatically chooses if images should be cropped or not)
    * 0.1 initial release
