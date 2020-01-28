__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

from django.db import models
from django.contrib.auth.models import AbstractUser
from jsonfield import JSONField

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    process_id = models.IntegerField(default=0)
    # order = models.IntegerField(default=10000)
    # package = models.ForeignKey(Package, related_name='processes', on_delete=models.CASCADE, blank = True, null=True)
    # template = models.ForeignKey(Template, related_name='processes', on_delete=models.CASCADE, blank = True, null=True)
