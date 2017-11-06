import logging
import os
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def simple_upload(request):
    logger.info('simple_upload called')

    if request.method == 'POST':
        upload_list = request.FILES.getlist('files')

        uploaded_file_url = []
        for uploaded in upload_list:
            fs = FileSystemStorage()
            file_name = fs.save(_rename(uploaded.name), uploaded)
            uploaded_file_url.append(fs.url(file_name))

        return render(request, 'files/form.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'files/form.html')


def _rename(file_name):
    prefix = 'test'
    name, ext = os.path.splitext(file_name)

    return '{}_{}{}'.format(
        prefix,
        datetime.now().strftime('%Y%m%d%H%M%S%f'),
        ext
    )
