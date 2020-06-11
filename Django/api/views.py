__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
# from api.models import Job
# from api.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
# from api.tasks import executeProcessFlow, finishPackage
from django.core.files.base import ContentFile, File
from django.utils.six import b, BytesIO
import json
from config.settings import BASE_DIR

from api.tasks import add, execute_command
import os
# from django.contrib.sites.models import Site

# import os
# import pwd
# from os import listdir
# from os.path import isfile, join
# from django.conf import settings
# import subprocess
# import shutil
# import tarfile
# from io import UnsupportedOperation
# import time
# import tarfile

# api call order:
# wait for a request of first job. respond with OK.
# while have job:
#    when job is done, send POST to APP with status and request next job.
#if no further job is recieved prepare to close??

from logging import getLogger
logger = getLogger('django')

@api_view(['PUT', 'GET'])
def start(request):
    if request.method == 'PUT':
        logger.info("%s recieved start request with id: %s" % (os.environ['HOSTNAME'], request.data['container_id']))
        # start the job.
        # logger.info("Put request to start work. edit")
        # logger.info(request.data)
        # logger.info(request.build_absolute_uri())
        # current_site = Site.objects.get_current()
        # logger.info(current_site)
        # logger.info(current_site.domain)
        if 'process_id' not in request.data:
            logger.error("missing process_id in request")
            return HttpResponse(status=400)
        # create job.
        # job = Job(job_id=request.data['job_id'], process_id=request.data['process_id'])
        # job.save()

        #start task...
        if 'command' not in request.data:
            logger.error("missing command in request")
            return HttpResponse("Command not present in data", status=400)

        # execute command
        execute_command(request.data)

        return HttpResponse(status=200)

    # elif request.method == 'GET':
    #     add.now(3, 7)
    #     return HttpResponse("A simple get request. started add task", status=200)
