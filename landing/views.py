import os
from datetime import datetime
import logging
from celery import current_app
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import imghdr

from landing.forms import FileImageForm
from .tasks import resize_image

logger = logging.getLogger('func_image_resizer')


def home(request):
    form_upload = FileImageForm()
    return render(request, 'landing/home.html', locals())


# func for POST request from /upload_file url
def upload_file(request):
    if request.method == 'POST':
        context = {}
        form = FileImageForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info('submit is correct')
            paths_to_files = []
            name_for_zip = str(datetime.now())
            width, height = int(request.POST['width']), int(request.POST['height'])
            for item in request.FILES.getlist('file'):
                print(imghdr.what(item))
                path_to_file = os.path.join(settings.MEDIA_ROOT, 'documents', item.name)
                paths_to_files.append(path_to_file)
                with open(path_to_file, 'wb+') as fp:
                    for chunk in item.chunks():
                        fp.write(chunk)
                logger.debug('file saved correctly')
            logger.debug('files saved correctly')
            task = resize_image.delay(paths_to_files, width, height, name_for_zip)
            logger.debug('task started')
            context['task_id'] = task.id
            context['task_status'] = task.status
            # context['form'] = form
            return JsonResponse(context)
        return render(request, 'landing/home.html', context)
    return render(request, 'landing/home.html')


# func for GET request from /task/task_id url
def check_result(request, task_id):
    task = current_app.AsyncResult(task_id)
    response_data = {'task_status': task.status, 'task_id': task.id}
    if task.status == 'SUCCESS':
        response_data['results'] = task.get()
        # print(type(response_data['results']['archive_path']))
    return JsonResponse(response_data)
