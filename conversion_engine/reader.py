import os
import sys
import platform
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory


def convert_pdf_to_images(file_name, poppler_path) -> None:

    """
    Save each pdf page as an image file and call the converter function on it
    :param file_name: The PDF document file name, will also be used as the final text document file name
    :param poppler_path: Path to Poppler binaries for windows, pdf2image is a wrapper for Poppler
    :return:  None
    """

    # We create a reference / path to our final text file which will reside in the same directory as the script
    final_txt_file: [str, bytes] = resource_path(f"../{os.path.splitext(file_name)[0]}.txt")

    # We create a temporary directory for saving our images before we convert them to text
    with TemporaryDirectory() as tmpdir:

        # We convert our PDF document pages to images at 300 DPI. Windows needs access to the poppler binary path
        if platform.system() == "Windows":
            pdf_document_pages: [Image] = convert_from_path(pdf_path=file_name, dpi=300, poppler_path=poppler_path)
        else:
            pdf_document_pages: [Image] = convert_from_path(pdf_path=file_name, dpi=300)

        # Iterate through all the PDF document pages & save them to our temporary folder and convert each image to text
        for page_num, page_content in enumerate(pdf_document_pages, 1):
            image_name: str = f"{tmpdir}/Page {page_num}.jpg"
            page_content.save(image_name, "JPEG")

            print(f'\n\tConverting image {page_num} to text...')

            # We call the reader / converter function on the current page
            read_images_write_text(final_txt_file, image_name)

            print(f'\n\t\tImage {page_num} successfully converted!')

        print(f'\nYour PDF "{file_name}" has been successfully converted to a text file named "{file_name[:-4]}.txt"!')


def read_images_write_text(final_txt_file, image_file: str) -> None:

    """
    We read each saved image of the pdf document and convert its contents to strings & write them to our txt file
    :param final_txt_file: The resulting text file that will contain all our strings (text)
    :param image_file: The current image / page we have captured from the pdf document for reading
    :return: None
    """

    with open(final_txt_file, mode='a') as converted_file:

        # Convert the text image to string
        document_text: str = str((pytesseract.image_to_string(Image.open(image_file)))).replace("-\n", "")

        # Write our text to file
        converted_file.write(document_text)


def resource_path(relative_path) -> [str, bytes]:

    """
    For managing file resources.
    :param: relative_path: The relative path (relative to the script file) of the target file as a string
    :return: A list of bytes (file content) and string (file path)
    """

    base_path: [] = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
