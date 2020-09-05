from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ocr-docx",
    version="0.2",
    description="Python 3 library extracting and ocring images included in docx files",
    long_description=long_description,
    license="MIT",
    url="http://github.com/PicusZeus/modern-greek-accentuation",
    author="Krzysztof Hilman",
    author_email="krzysztof.hilman@gmail.com",
    packages=find_packages(),
    install_requires=['lxml==4.5.2', 'nltk==3.5', 'numpy==1.19.1', 'opencv-python==4.4.0.42', 'Pillow==7.2.0',
                      'pytesseract==0.3.6', 'python-docx==0.8.10', 'six==1.15.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux"],
    python_requires='>+3.6'
)
