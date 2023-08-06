from rest_framework import serializers
from . import models

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Project
        fields = ['pk', 'name']

