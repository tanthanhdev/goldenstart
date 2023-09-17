from zipfile import ZipFile
import base64
import tabula
import pandas as pd
import io
import time
import os
from django.core.files import File
from django.core.files.base import ContentFile

def get_filenames(path_to_zip):
    """ return list of filenames inside of the zip folder"""
    with ZipFile(path_to_zip, 'r') as zip:
        return zip.namelist()
    
def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

def convert_pdf_to_excel(file_path_pdf, email, filename_pdf):
    folder_path_output = f"media/temp/{email}/output/"
    filename_xlsx = filename_pdf.replace('.pdf', '.xlsx')
    
    # create dynamic directory, if it does not exist
    if not os.path.exists(folder_path_output):
        os.makedirs(folder_path_output)
    
    file_path_output_csv = folder_path_output + str(int(time.time())) + ".csv" 
    # file_path_output_xlsx = folder_path_output + str(time.time()) + ".xlsx" 
    
    
    # Read pdf into list of DataFrame
    dfs = tabula.read_pdf(file_path_pdf, pages=1)
    # convert PDF into CSV file
    tabula.convert_into(file_path_pdf, file_path_output_csv, output_format="csv", pages=1)
    
    # Convert to excel file
    data = pd.read_csv(file_path_output_csv)
    # data.to_excel(file_path_output_xlsx, index=False)
    
    # return excel file
    buffer = io.BytesIO()
    # df = pd.read_excel(file_path_output_xlsx, header=0)
    data.to_excel(buffer, index=False)
    
    buffer.write(buffer.getvalue())
    buffer.seek(0)
    
    file = File(buffer, filename_xlsx)
    
    return file
