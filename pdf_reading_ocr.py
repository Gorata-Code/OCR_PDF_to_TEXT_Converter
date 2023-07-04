import os
import sys
import platform
import pytesseract
from pathlib import Path
from conversion_engine.reader import convert_pdf_to_images


def script_summary() -> None:
    print('''
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     \t***------------------------------------------------------------------------***\n

        \t"OCR PDF READER" Version 1.0.0\n

        This bot will help you read content from a PDF file (including images)
        and convert it to a text file. All you need to do is provide the name
        of the PDF file you want to read.

        Cheers!!
    ''')


def ocr_pdf_reader_bot(file_name: str, poppler_path) -> None:
    try:
        convert_pdf_to_images(file_name, poppler_path)

    except Exception and FileNotFoundError:
        if FileNotFoundError:
            print(
                '\n\t*** Unable to locate your file. Please make sure you provide a valid file name & '
                'file extension within this folder. ***')
        else:
            raise

    input('\nPress Enter to Exit.')
    sys.exit(0)


def main() -> None:
    script_summary()
    file_name: str = input('\nPlease type the name of the file (including the extension) you would like to convert '
                           'and Press Enter: ')

    if len(file_name.strip()) >= 5:
        if not os.path.splitext(file_name)[-1].casefold() == '.pdf':
            input('\n\tPlease provide a valid pdf file name.')
        else:
            if os.path.exists(file_name):
                ocr_pdf_reader_bot(file_name, poppler_binaries)
            elif FileNotFoundError:
                print(
                    '\n\t*** Unable to locate your file. Please make sure you provide a valid file name & '
                    'file extension within this folder. ***')
                input('\nPress Enter to Exit: ')
                sys.exit(1)

    elif len(file_name.strip()) < 5 or os.path.splitext(file_name.strip()[-1]) == '':
        print('\n\tPlease provide a valid file name.')
        input('\nPress Enter to Exit: ')
        sys.exit(1)


if __name__ == '__main__':
    #  Setting up a few utilities for Windows OS
    if platform.system() == "Windows":

        # For reading text from images
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

        # For converting PDF pages to images
        poppler_binaries: Path = Path("C:\\Program Files\\poppler-0.68.0_x86\\bin")

    main()
