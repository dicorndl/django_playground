import logging
import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def form(request):
    return render(request, 'files/form.html', {})


@csrf_exempt
def upload(request):
    logger.info('upload called')

    if request.method == 'POST':
        prefix = request.POST.get('prefix')

        logger.info(len(request.FILES.getlist('files')))
        upload_list = request.FILES.getlist('files')

        for uploaded in upload_list:
            logger.info('uploaded')
            file_name = uploaded._name

            handle_uploaded_file(uploaded, file_name, prefix)
    return HttpResponse('hello')


def handle_uploaded_file(uploaded, file_name, prefix):
    extension = file_name.split('.')[-1]
    rename = '%s%s.%s' % (prefix, datetime.now().strftime('%Y%m%d%H%M%S%f'), extension)
    with open(os.path.join(settings.MEDIA_ROOT, rename), mode='wb') as fp:
        for chunk in uploaded.chunks():
            fp.write(chunk)
