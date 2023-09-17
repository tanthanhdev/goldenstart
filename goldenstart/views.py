import logging
import sesame.utils
from sesame.decorators import authenticate
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from http import HTTPStatus
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import io
from django.core.files import File
from zipfile import ZipFile, is_zipfile
from datetime import datetime
# 
from goldenstart.models import User, Document, Tracking
# services
from goldenstart.services.file import convert_pdf_to_excel

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def subscribe(request):
    try:
        if request.method == 'POST':
            data = request.POST
            # here we want to email the user the magic link.
            # first check user exists w/ that email
            email = data['email']
            access_code = data['access_code']
            user = User.objects.filter(email=email).first()
            
            if user is None:
                user = User(email=email, password=access_code)
                user.save()
            
            return JsonResponse({'success': True}, status=HTTPStatus.OK)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return JsonResponse({'success': False, }, status=HTTPStatus.BAD_REQUEST)

def upload_file(request):
    try:
        if request.method == 'POST' and request.FILES['file']:
            filename = request.FILES['file'].name
            file = request.FILES['file']
            email = request.POST['email']
            
            user = User.objects.filter(email=email).first()
            
            # upzip a zip files
            if is_zipfile(file):
                with ZipFile(file, 'r') as zip:
                    for target_file in zip.namelist():
                        with zip.open(target_file) as myfile:
                            with io.BytesIO() as buf:
                                buf.write(myfile.read())
                                buf.seek(0)
                                file_unziped = File(buf, target_file) # convert to the file from django
                                
                                # Save pdf file to DB
                                newDoc = Document(user=user, document = file_unziped, type="PDF")
                                newDoc.save()
                                
                                # Save CSV file to DB
                                file_excel = convert_pdf_to_excel(newDoc.document.path, email=email, filename_pdf=target_file)
                                newDoc = Document(user=user, document = file_excel, type="EXCEL")
                                newDoc.save()
            else:
                # Save pdf file to DB
                newDoc = Document(user=user, document = file, type="PDF")
                newDoc.save()
                
                # Save CSV file to DB
                file_excel = convert_pdf_to_excel(newDoc.document.path, email=email, filename_pdf=filename)
                newDoc = Document(user=user, document = file_excel, type="EXCEL")
                newDoc.save()
            
            # send email magic link
            link = request.build_absolute_uri(reverse('retrieval-page'))
            link += sesame.utils.get_query_string(user)
            html_message = render_to_string('emails/subscribe_successful.html', {'link': link})
            plain_message = strip_tags(html_message)

            
            send_mail(
                subject="Workpaper Complete",
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=True
            )
            
            user.mail_submitted_at = datetime.now()
            
            return JsonResponse({'success': True, 'filename': filename}, status=HTTPStatus.OK)
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return JsonResponse({'success': False, }, status=HTTPStatus.BAD_REQUEST)
    
def post_downloaded(request):
    tracking = Tracking.objects.all()[0]
    tracking.download_count += 1
    tracking.save()
    return JsonResponse({'success': True}, status=HTTPStatus.OK)

def post_visited(request):
    tracking = Tracking.objects.all()[0]
    tracking.visits += 1
    tracking.save()
    return JsonResponse({'success': True}, status=HTTPStatus.OK)

@authenticate
def retrieval_page(request):
    context = {"documents": Document.objects.filter(user=request.user, type="EXCEL")}
    return render(request, 'dashboard/retrieval_page.html', context)