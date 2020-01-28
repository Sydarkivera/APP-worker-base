__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"
from django.conf.urls import url, include
from django.contrib import admin
import rest_framework.urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

admin.autodiscover()

urlpatterns = [
    # url(r'^sysadmin/', admin.site.urls),
    # # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api/', include('api.urls')),
    # url(r'^auth/api-token-auth/', obtain_jwt_token),
    # url(r'^auth/api-token-refresh/', refresh_jwt_token),
    # url(r'^auth/api-token-verify/', verify_jwt_token),
    url(r'^', include('api.urls')),
]
