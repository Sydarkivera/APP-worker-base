__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'start/', views.start),
    url(r'', views.default)
]

# APP starts worker process: needs id of job, details of specific job (command, file and other needs)
# APP send message to worker to start a task.
# When first task is complete, worker sends POST to APP asking for next file.
