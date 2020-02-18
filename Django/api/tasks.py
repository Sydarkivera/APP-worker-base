__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

from background_task import background
from django.core.exceptions import ObjectDoesNotExist
# from api.models import Module, Package, Process, Template, Variable, FileType
from api.models import Job
from logging import getLogger
import importlib
import time
import traceback
import logging
import os
import subprocess
import pwd
import re
import docker
from docker.types import Mount
import uuid
import shutil
import requests
from django.http import HttpResponse
import tempfile
from time import sleep

logger = getLogger('background_task')

@background(schedule=60)
def add(a, b):
    logger.info(a+b)
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')

@background()
def execute_command(data):
    # logger.info("execute command")
    # logger.info(command)
    # logger.info(pwd.getpwuid( os.getuid() )[ 0 ])

    command = data['command']

    log = ""
    error = ""

    logger.info("%s executing command: %s with id: %s" % (os.environ['HOSTNAME'], command, data['container_id']))

    try:
        tempLOG = tempfile.TemporaryFile()
        tempERR = tempfile.TemporaryFile()
        p = subprocess.Popen(command, stdout=tempLOG, stderr=tempERR, shell=True)
        
        # p = subprocess.check_output(command, shell=True)

        stdout, stderr = p.communicate()
        # logger.info(stdout)
        # logger.info(stderr)
        p.wait()

        tempLOG.seek(0)
        # print(tempLOG.read())
        stdout = tempLOG.read()

        tempERR.seek(0)
        # print(tempERR.read())
        stderr = tempERR.read()

        tempLOG.close()
        tempERR.close()
        logger.info("Command finished")
        # logger.info(p.returncode)
        logger.info(stdout)
        logger.info(stderr)
        p.kill()
        if stdout and stdout != None:
            log = stdout.decode('utf-8')
            # logger.info(log)
            # logger.info(stdout.decode('utf-8'))
            # retval = (1, log)
        if stderr and stderr != None:
            error = stdout.decode('utf-8')
            # logger.error(error)
            # retval = (-1, stderr.decode('utf-8'))
    except e:
        logging.error(traceback.format_exc())
        error = traceback.format_exc()

    logger.info(error)

    # communicate result back to server...(Environment variable or settings varaible for APP server name) TODO: container_name
    container_name = "django"
    newData = {}
    newData['stdout'] = log
    newData['stderr'] = stderr
    # data['file'] = first_file
    # job = Job.objects.get(pk=job_id)
    newData['process_id'] = data['process_id']
    newData['file_name'] = data['file_name']
    newData['file_id'] = data['file_id']
    newData['container_id'] = data['container_id']
    # data['job_id'] = job_id
    # data['job_id'] = job_id#...
    # figure out name of new container in network
    url = "http://" + container_name + "/api/worker/result/"
    logger.info("%s returning result from job: %s to url: %s" % (os.environ['HOSTNAME'], data['container_id'], url))
    # logger.info(url)
    returnResult(url, newData)


def returnResult(url, data, numberOfTries=0):
    try:
        r = requests.put(url, data=data)
        # logger.info("status code: " + str(r.status_code))
        if r.status_code != requests.codes.ok:
            logger.info("Got non 200 status code when returning process result to APP")
            r.raise_for_status()
            # self.try_again(url, data)
            logger.info("Got non 200 from APP")
        else:
            #status is ok and a new package should have been recieved.
            # logger.info("Got 200 from APP")
            # logger.info("Put request to start work. edit")
            response_data = r.json()
            # logger.info(response_data)

            if 'done' in response_data:
                logger.info("job completed")
                return HttpResponse("Job done", status=200)

            if 'process_id' not in response_data:
                logger.error("missing process_id in response")
                return HttpResponse(status=400)

            #start task...
            if 'command' not in response_data:
                logger.error("missing command in response")
                return HttpResponse("Command not present in data", status=400)

            # execute command
            execute_command(response_data)
            pass
    except requests.exceptions.RequestException as e:
        # self.try_again(url, data)
        logger.info(e)
        logger.info("failed to return result")
        if numberOfTries < 3:
            sleep(numberOfTries)
            logger.info("retrying")
            returnResult(url, data, numberOfTries+1)
    except:
        logger.info("unknown error")
        if numberOfTries < 3:
            sleep(numberOfTries)
            logger.info("retrying")
            returnResult(url, data, numberOfTries+1)