from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import UploadForm
import os
import zipfile
import shutil
from bs4 import BeautifulSoup
from cloudinary import config, uploader
import logging
import datetime
import uuid
import re

def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if 'zip_file' not in request.FILES:
            return HttpResponse("No zip file provided.", status=400)
        if form.is_valid():
            zip_file = form.cleaned_data['zip_file']
            cloud_name = form.cleaned_data['cloud_name']
            api_key = form.cleaned_data['api_key']
            api_secret = form.cleaned_data['api_secret']
            try:
                config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
            except Exception as e:
                logging.error("Error configuring Cloudinary: %s", e)
                return render(request, 'static/index.html', {'form': form, 'messages': ['Error configuring Cloudinary']})

            # Create a base directory for temporary files if it doesn't exist
            base_temp_dir = os.path.join(settings.BASE_DIR, 'tmp')
            os.makedirs(base_temp_dir, exist_ok=True)

            # Create a unique temporary directory
            temp_dir_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(uuid.uuid4())
            temp_dir = os.path.join(base_temp_dir, temp_dir_name)
            os.makedirs(temp_dir)
            try:
                # Extract zip file
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Recursively traverse temp directory for HTML and CSS files
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file.endswith('.html'):
                            with open(file_path, 'r+', encoding='utf-8') as f:
                                contents = f.read()
                                soup = BeautifulSoup(contents, 'html.parser')

                                # Find and upload images, then replace their paths
                                images = soup.find_all('img')
                                for img in images:
                                    image_path = os.path.join(root, img['src'])
                                    if os.path.exists(image_path):
                                        response = uploader.upload(image_path, format="webp")
                                        secure_url = response['secure_url'].replace('/upload/', '/upload/f_auto,q_auto/w_auto/')
                                        img['src'] = response['secure_url']

                                # Write the modified contents back to the file
                                f.seek(0)
                                f.write(str(soup))
                                f.truncate()
                        elif file.endswith('.css'):
                            modified = False
                            with open(file_path, 'r+', encoding='utf-8') as f:
                                contents = f.read()
                                style_pattern = r"background-image\s*:\s*url\(['\"]?(.*?)['\"]?\)"
                                matches = re.findall(style_pattern, contents, re.IGNORECASE)
                                for match in matches:
                                    image_url = match.strip('\'"')
                                    if not image_url.startswith("http"):
                                        image_path = os.path.join(root, image_url)
                                        response = uploader.upload(image_path, format="webp")
                                        secure_url = response['secure_url'].replace('/upload/', '/upload/f_auto,q_auto/w_auto/')
                                        contents = contents.replace(match, secure_url)
                                        modified = True
                                if modified:
                                    # Write the modified contents back to the file
                                    f.seek(0)
                                    f.write(contents)
                                    f.truncate()

                # Zip the modified directory
                zip_path = os.path.join(temp_dir, "optimized.zip")
                with zipfile.ZipFile(zip_path, 'w') as zip_ref:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if file_path != zip_path:
                                zip_ref.write(file_path, os.path.relpath(file_path, temp_dir))

                # Send the zip file back to the client
                with open(zip_path, 'rb') as f:
                    response = HttpResponse(f, content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename="optimized.zip"'
                    return response
            except Exception as e:
                logging.error("Error optimizing images: %s", e)
                return render(request, 'static/index.html', {'form': form, 'messages': ['Error optimizing images, please try again.']})
            finally:
                shutil.rmtree(temp_dir)
    else:
        form = UploadForm()

    return render(request, 'static/index.html', {'form': form})

