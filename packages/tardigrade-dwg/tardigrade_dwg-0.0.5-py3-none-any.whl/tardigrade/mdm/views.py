from django.shortcuts import render

# Create your views here.

from . import models

from rest_framework import viewsets, permissions
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

class ProjectApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to manage projects.
    """
    queryset = models.Project.objects.all().order_by('-name')
    serializer_class = serializers.ProjectSerializer
    permission_classes = []
    #
    # def details(self):

class EnvironmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to manage environments.
    """
    queryset = models.Environment.objects.all().order_by('-name')
    serializer_class = serializers.EnvironmentSerializer
    permission_classes = []

class EntityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to manage entities.
    """
    queryset = models.Entity.objects.all().order_by('-name')
    serializer_class = serializers.EntitySerializer
    permission_classes = []

class ConnectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to manage connections.
    """
    queryset = models.Connection.objects.all().order_by('-name')
    serializer_class = serializers.ConnectionSerializer
    permission_classes = []