from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import datetime
import traceback
import json
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from rest_framework.response import Response
from rest_framework.decorators import api_view
import queue
import csv
from .models import PdfData
from threading import Thread
from uuid import uuid4
from django.conf import settings
import io
from django.utils.decorators import decorator_from_middleware
from .Middleware import Middleware

load_balance = decorator_from_middleware(Middleware)

def IndexPage(request):
    return render(request, 'index.html')

# method to parse upload pdf

@api_view(['POST'])
@load_balance
def uploadpdf(request):
    try:
        print("in")
        filename = generate_ref_id()
        fs = FileSystemStorage(location=settings.STATIC_ROOT+"/media")
        filesave = fs.save(filename+'.pdf', request.FILES['filedata'])
        filepath = fs.path(filesave)
        pdf_text = extract_text_from_pdf(filepath,filename)
        pdf_data = PdfData()
        pdf_data.data = pdf_text
        pdf_data.save()
        return Response({"status": "SUCCESS", "message": "file Uploaded Sucessfully","refId":filename}, content_type='application/json', status=200)
    except:
        traceback.print_exc()
        return Response({"status": "FAILURE", "message": "Invalid Request"}, content_type='application/json', status=500)

@api_view(['GET'])
@load_balance
def fetchdata(request):
    try:
        content = request.data
        ref_id = request.GET['refid']
        with open(settings.STATIC_ROOT+'/media/'+ref_id+'.txt','r') as file:
            file_text = file.read()
        return Response({"status": "SUCCESS", "message": "Invalid Request","data":file_text}, content_type='application/json', status=200)
    except:
        traceback.print_exc()
        return Response({"status": "FAILURE", "message": "Invalid Request"}, content_type='application/json', status=500)

def extract_text_from_pdf(pdf_path,filename):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        with open(settings.STATIC_ROOT+'/media/'+filename+'.txt','w') as file:
            file.write(text)
    return text

def generate_ref_id():
    now = datetime.datetime.now()
    return "ID" + str(now.year) + '%02d' % now.month + '%02d' % now.day + str(uuid4().int)[:5]
