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
from api.models import Job
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

@api_view(['GET'])
def default(request):
    if request.method == 'GET':
        add.now(3, 7)
        return HttpResponse("A simple get request. started add task", status=200)

@api_view(['PUT', 'GET'])
def start(request):
    if request.method == 'PUT':
        logger.info("%s recieved start request with id: %s" % (os.environ['HOSTNAME'], request.data['job_id']))
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
        job = Job(job_id=request.data['job_id'], process_id=request.data['process_id'])
        job.save()

        #start task...
        if 'command' not in request.data:
            logger.error("missing command in request")
            return HttpResponse("Command not present in data", status=400)

        # execute command
        execute_command(request.data['command'], job.job_id)

        return HttpResponse(status=200)

    # elif request.method == 'GET':
    #     add.now(3, 7)
    #     return HttpResponse("A simple get request. started add task", status=200)

# @api_view(['GET', 'PUT', 'DELETE'])
# def process_detail(request, process_id):
#     """
#     Display specific process.
#     """
#     process = get_object_or_404(Process, pk=process_id)
#     if request.method == 'GET':
#         serializer = ProcessSerializer(process)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProcessSerializer(
#             process, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             process.status = Process.PROCESS_STATUS_EDITED
#             process.save()
#             if process.package != None:
#                 process.package.status = Package.PACKAGE_STATUS_EDITED
#                 process.package.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         if process.package != None:
#             process.package.status = Package.PACKAGE_STATUS_EDITED
#             process.package.save()
#             # delet old logfiles
#             if os.path.exists(process.log_path):
#                 os.remove(process.log_path)
#             if os.path.exists(process.err_path):
#                 os.remove(process.err_path)
#         process.delete()
#         return HttpResponse(status=204)
#
#
# @api_view(['GET', 'POST'])
# def process_add(request):
#     """
#     Add new process.
#     """
#     if request.method == 'POST':
#         serializer = ProcessSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             if 'package' in request.data:
#                 package = get_object_or_404(Package, pk=request.data['package'])
#                 package.status = Package.PACKAGE_STATUS_EDITED
#                 package.save()
#                 serializer = ProcessSerializer(package.processes, many=True)
#                 return Response(serializer.data)
#             elif 'template' in request.data:
#                 template = get_object_or_404(Template, pk=request.data['template'])
#                 serializer = ProcessSerializer(template.processes, many=True)
#                 return Response(serializer.data)
#             else:
#                 return Response('A call to add process requires either package or template to be defined', status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         processes = Process.objects.all()
#         serializer = ProcessSerializer(processes, many=True)
#         return Response(serializer.data)
#
#
# @api_view(['GET', 'POST'])
# def template_list(request):
#     """
#     list templates.
#     """
#     if request.method == 'GET':
#         templates = Template.objects.all().order_by('template_id')
#         serializer = TemplateListSerializer(templates, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # create a new template
#         if 'package_id' not in request.data:
#             # check if it can be created as a completely new template
#             if 'template_id' in request.data:
#                 # update template_id with the data from package_id.
#                 template = get_object_or_404(Template, pk=request.data['template_id'])
#                 template.name = request.data['templateName']
#                 template.save()
#                 serializer = TemplateDetailSerializer(template)
#                 return Response(serializer.data)
#             else:
#                 if 'templateName' in request.data:
#                     template = Template(name=request.data['templateName'])
#                     template.save()
#                     serializer = TemplateDetailSerializer(template)
#                     return Response(serializer.data)
#                 return Response('package_id or templateName is required to save a new template', status=status.HTTP_400_BAD_REQUEST)
#         package = get_object_or_404(Package, pk=request.data['package_id'])
#         if 'template_id' in request.data:
#             # update template_id with the data from package_id.
#             template = get_object_or_404(Template, pk=request.data['template_id'])
#             # if templateName exists, update the name of template
#             if 'templateName' in request.data:
#                 template.name = request.data['templateName']
#                 template.save()
#             # delete old processes
#             template.processes.all().delete()
#             # save the new updated processes
#             for process in package.processes.all():
#                 if not process.module.hidden:
#                     process.pk = None
#                     process.template = template
#                     process.package = None
#                     process.save()
#             package.active_template = template
#             package.save()
#             return HttpResponse(status=204)
#         elif 'templateName' in request.data:
#             # save as a new template.
#             logger.info('template from name only')
#             logger.info(request.data['templateName'])
#             template = Template(name=request.data['templateName'])
#             template.save()
#             for process in package.processes.all():
#                 if not process.module.hidden:
#                     process.pk = None
#                     process.template = template
#                     process.package = None
#                     process.save()
#             package.active_template = template
#             package.save()
#             return HttpResponse(status=204)
#         else:
#             return Response('package_id is required to save a new template', status=status.HTTP_400_BAD_REQUEST)
#
#
#
# @api_view(['GET', 'DELETE'])
# def template_detail(request, template_id):
#     """
#     display a single template.
#     """
#     template = get_object_or_404(Template, pk=template_id)
#     if request.method == 'GET':
#         serializer = TemplateDetailSerializer(template)
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if not template.packages.all().exists():
#             template.delete()
#             return HttpResponse(status=200)
#         else:
#             return HttpResponse(status=409)
#
# @api_view(['GET', 'PUT'])
# def template_process_list(request, template_id):
#     """
#     List all processes of selected Tempalte.
#     """
#     template = get_object_or_404(Template, pk=template_id)
#     if request.method == 'GET':
#         serializer = ProcessSerializer(template.processes, many=True)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         logger.info(request.data)
#         for process in request.data:
#             p = Process.objects.get(pk=process['process_id'])
#             p.order = process['order']
#             # p.status = Process.PROCESS_STATUS_EDITED
#             p.save()
#         return HttpResponse(status=204)
#
# @api_view(['PUT'])
# def template_package_detail(request, template_id, package_id):
#     """
#     Set a template to a package
#     """
#     template = get_object_or_404(Template, pk=template_id)
#     package = get_object_or_404(Package, pk=package_id)
#     if request.method == 'PUT':
#         # delete old processes from package
#         if package.active_template != None:
#             for process in package.processes.all():
#                 if not process.module.hidden:
#                     process.delete()
#
#         package.active_template = template
#         order = package.processes.all().order_by('order').reverse()[0].order + 1
#         for process in template.processes.all().order_by('order'):
#             if not process.module.hidden:
#                 process.pk = None
#                 process.template = None
#                 process.package = package
#                 process.order = order
#                 order += 1
#                 process.save()
#         package.status = package.PACKAGE_STATUS_EDITED
#         package.save()
#     return HttpResponse(status=204)
#
# @api_view(['GET'])
# @permission_classes((AllowAny, ))
# def dashboardStats(request):
#     """
#     Get the data required for the global dashboard in one json response
#     """
#     if request.method == 'GET':
#         #filetypes:
#         fileTypes = FileType.objects.all().order_by('total').reverse()
#         data = {}
#         data['fileTypes'] = FileTypesSerializer(fileTypes, many=True).data
#         # variables
#         var = Variable.objects.get(name="total_number_of_files")
#         data['total_number_of_files'] = var.data
#         var = Variable.objects.get(name="total_size")
#         data['total_size'] = var.data
#         var = Variable.objects.get(name="total_number_of_packages")
#         data['total_number_of_packages'] = var.data
#         var = Variable.objects.get(name="total_number_of_errors")
#         data['total_number_of_errors'] = var.data
#
#         #graphdata
#         graph = GraphData.objects.order_by('date')[:52]
#         data['graphData'] = GraphDataSerializer(graph, many=True).data
#         # graph = GraphData(date=datetime.date.today(), size=300000000, count=3452)
#
#         return Response(data)
#
# @api_view(['GET', 'POST'])
# def variables_global(request):
#     """
#     Get a list of system variables or (POST) set the variables
#     """
#
#     if request.method == 'GET':
#         global_variables = ['work_dir_path', 'packages_path', 'premis_file_name', 'tools_path', 'work_dir_path_host', 'premis_template_path', 'premis_event_template_path']
#         res = {}
#         for vname in global_variables:
#             v = get_object_or_404(Variable, name=vname)
#             res[vname] = v.data
#         return JsonResponse(res)
#     elif request.method == 'POST':
#         for key, value in request.data.items():
#             v = get_object_or_404(Variable, name=key)
#             v.data = value
#             v.save()
#
#         # for var in request.data:
#         #     v = get_object_or_404(Variable, pk=var.id)
#         #     serialzer = VariableSerializer(v, request.data)
#         #     if serialzer.is_valid():
#         #         serialzer.save()
#         #     else:
#         #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return HttpResponse(status=200)
#
#
# @api_view(['GET'])
# @permission_classes((AllowAny, ))
# def permissions(request):
#     # logger.info(request.user)
#     if request.user.is_authenticated:
#         # username = request.user.username
#         # permissions = Permission.objects.filter(user=request.user)
#         #
#         # serializer = PermissionSerializer(permissions, many=True)
#         if (request.user.is_superuser):
#             return JsonResponse({"admin":True})
#         else:
#             return JsonResponse({"admin":False})
#     return HttpResponse(status=200)
