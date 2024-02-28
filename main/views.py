import os
import datetime
import uuid
import zipfile
import shutil
import logging
from bs4 import BeautifulSoup
import re
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadForm
from cloudinary.uploader import upload
from cloudinary import config
from django.conf import settings


def config_cloudinary(cloud_name, api_key, api_secret):
    try:
        config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
    except Exception as e:
        logging.error("Error configuring Cloudinary: %s", e)
        return False, "Error configuring Cloudinary"
    return True, None


def handle_uploaded_file(zip_file, temp_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)


def handle_image_upload(root, src):
    image_path = os.path.join(root, src)
    if os.path.exists(image_path):
        response = upload(image_path, format="webp")
        secure_url = response['secure_url'].replace('/upload/', '/upload/f_auto,q_auto/w_auto/')
        return secure_url
    return src


def modify_files(temp_dir):
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.html'):
                modify_html_file(file_path, root)
            elif file.endswith('.css'):
                modify_css_file(file_path, root)


def modify_html_file(file_path, root):
    with open(file_path, 'r+', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

        for img in soup.find_all('img'):
            src = img.get('src', '')
            img['src'] = handle_image_upload(root, src)
        
        f.seek(0)
        f.write(str(soup))
        f.truncate()


def modify_css_file(file_path, root):
    modified = False
    with open(file_path, 'r+', encoding='utf-8') as f:
        contents = f.read()
        style_pattern = r"background-image\s*:\s*url\(['\"]?(.*?)['\"]?\)"
        matches = re.findall(style_pattern, contents, re.IGNORECASE)
        for match in matches:
            secure_url = handle_image_upload(root, match.strip('\'"'))
            contents = contents.replace(match, secure_url)
            modified = True
        if modified:
            f.seek(0)
            f.write(contents)
            f.truncate()


def create_and_send_zip(temp_dir):
    zip_path = os.path.join(temp_dir, "optimized.zip")
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != zip_path:
                    zip_ref.write(file_path, os.path.relpath(file_path, temp_dir))

    with open(zip_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="optimized.zip"'
        return response


def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if 'zip_file' not in request.FILES:
            return HttpResponse("No zip file provided.", status=400)
        if form.is_valid():
            cloud_name = form.cleaned_data.get('cloud_name')
            api_key = form.cleaned_data.get('api_key')
            api_secret = form.cleaned_data.get('api_secret')

            config_success, error_message = config_cloudinary(cloud_name, api_key, api_secret)
            if not config_success:
                return render(request, 'main/index.html', {'form': form, 'messages': [error_message]})

            base_temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
            os.makedirs(base_temp_dir, exist_ok=True)
            temp_dir = os.path.join(base_temp_dir, datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(uuid.uuid4()))
            os.makedirs(temp_dir)

            try:
                handle_uploaded_file(form.cleaned_data['zip_file'], temp_dir)
                modify_files(temp_dir)
                return create_and_send_zip(temp_dir)
            except Exception as e:
                logging.error("Error optimizing images: %s", e)
                return render(request, 'main/index.html', {'form': form, 'messages': [f"Error optimizing images: {e}. Please try again."]})
            finally:
                shutil.rmtree(temp_dir)
        else:
            logging.error("Error validating form: %s", form.errors)
            return render(request, 'main/index.html', {'form': form, 'messages': [form.errors]})
    else:
        form = UploadForm()
    return render(request, 'main/index.html', {'form': form})
