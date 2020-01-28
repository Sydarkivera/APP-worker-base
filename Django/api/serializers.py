__author__ = "Simon Nilsson"
__copyright__ = "Copyright 2017, Axenu"
__license__ = "GNU"
__version__ = "0.1"
__maintainer__ = "Simon Nilsson"
__email__ = "simon@axenu.com"
__status__ = "Development"

from rest_framework import serializers
from api.models import *
import json
from django.contrib.auth.models import Permission

class BigintSerializer(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data

class TypeSerializer(serializers.Field):

    def to_representation(self, obj):
        for var in Module.MODULE_TYPES:
            if var[0] == obj:
                return var[1]
        # return Module.MODULE_TYPES[obj][1]
        return "Not found"

    def to_internal_value(self, data):
        for var in Module.MODULE_TYPES:
            if var[1] == data:
                return var[0]
        return 0
        # return {k:v for v,k in Module.MODULE_TYPES.items()}[data]

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

class ProcessSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='module.name', read_only=True)
    hidden = serializers.BooleanField(source='module.hidden', read_only=True)
    type = TypeSerializer(source='module.type', read_only=True)
    form = JSONSerializerField(source='module.form', read_only=True)
    value = JSONSerializerField(required=False)
    errors = JSONSerializerField(required=False)
    logs = JSONSerializerField(required=False)
    status = serializers.SerializerMethodField()
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False)
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(), required=False)
    filter = serializers.CharField(source='module.filter', read_only=True)

    class Meta:
        model = Process
        fields = ('process_id', 'order', 'name', 'type', 'form', 'value', 'status', 'log_path', 'err_path', 'module', 'package', 'hidden', 'filter', 'progress', 'template', 'errors', 'logs')

    def get_status(self,obj):
        return obj.get_status_display()

class PackageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    template_name = serializers.CharField(source='active_template.name', read_only=True)

    class Meta:
        model = Package
        fields = ('package_id', 'name', 'path', 'file_name', 'status', 'active_template', 'template_name')

    def get_status(self,obj):
        return obj.get_status_display()

class PackageDetailSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True)
    statistics = JSONSerializerField(required=True)
    template_name = serializers.CharField(source='active_template.name', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = ('package_id', 'name', 'file_name', 'status', 'processes', 'statistics', 'active_template', 'template_name')


    def get_status(self,obj):
        return obj.get_status_display()


class ModuleSerializer(serializers.ModelSerializer):
    form = JSONSerializerField()
    command = JSONSerializerField()
    type = TypeSerializer()
    resultFilter = JSONSerializerField()

    class Meta:
        model = Module
        fields = ('module_id', 'name', 'type', 'form', 'python_module', 'command', 'hidden', 'filter', 'resultFilter', 'dockerImage', 'description')

    def get_type(self,obj):
        return obj.get_type_display()

class TemplateListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Template
        fields = ('name', 'template_id')

class TemplateDetailSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True)

    class Meta:
        model = Template
        fields = ('name', 'template_id', 'processes')


# statistis serialisers

class FileTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = ('name', 'errors', 'total', 'size')


class GraphDataSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    size = BigintSerializer()
    count = BigintSerializer()
    class Meta:
        model = GraphData
        fields = ('date', 'size', 'count')

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('id', 'name', 'data')

class DockerImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DockerImage
        fields = ('id', 'name', 'mountpoint', 'label')

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('name', 'codename', 'content_type')
