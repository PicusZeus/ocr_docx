

Usage
=====

install all requirements

>>> pip install -r requirements.txt

In order to ocr pasted images in docx file and to create
a new docx file with ocred text pasted along the images

>>> python3 ocr_docx.py file.docx

Flags

* -df

give destinateion folder for images extracted from docx, default 'images'.

* -d

give name of a docx file you want to create, default 'ocred.docx'

* -l

give language tag for ocr, default is ancient greek 'grc', but you can use whichever you prefer

In order to work correctly you have to install pytesseract language pack on your machine

>>> sudo apt install tesseract-ocr-grc

