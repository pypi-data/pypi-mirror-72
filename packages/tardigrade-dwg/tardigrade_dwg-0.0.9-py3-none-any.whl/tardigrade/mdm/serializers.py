from rest_framework import serializers
from . import models

class EntitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Entity
        fields = ['pk', 'name']

class EnvironmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Environment
        fields = ['pk', 'name']

class ConnectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Connection
        fields = ['pk', 'name']



class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Project
        fields = [
            'pk',
            'name',
            'entities',
            # 'environments',
            # 'connections',
        ]

    # id = serializers.HyperlinkedIdentityField(view_name='project-details')
    entities = serializers.HyperlinkedRelatedField(many=True, view_name='project_detail', read_only=True)
    # environments = serializers.HyperlinkedRelatedField(many=True, read_only=True)
    # connections = serializers.HyperlinkedRelatedField(many=True, read_only=True)