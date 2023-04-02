
=====

install all requirements

>>> pip install -r requirements.txt


In order to ocr pasted images in docx file and to create
a new docx file with ocred text pasted along the images

>>> python3 ocr_docx.py file.docx

Flags

* -df

give destination folder for images extracted from docx, default 'images'.

* -d

give name of a docx file you want to create, default 'ocred.docx'

* -l

give language tag for ocr, default is ancient greek 'grc', but you can use whichever you prefer

In order to work correctly you have to install pytesseract language pack on your machine, for Ancient Greek it will be:

* -cr

if files in docx are of format wmf or emf, the images size is equal to the size of page, with actual image
taking a small part of it, and so it needs to be cropped and prepared to ocr. The logic included in this
program works best for images works best if the foreground of the text has some yellowish
tint to it. If you work with different types of images in your docx, you should probably modify
logic in function ``get_text_field`` in get_text_images.py file. If images are not of mf
format, they are probably already png files that do not need cropping and that would suffer
from this procedure, then you should use -cr flag with 'No' value in order to prevent
this behaviour.


You have to install tesseract language pack for your language on your machine, for Ancient Greek
it would be:

>>> sudo apt install tesseract-ocr-grc

