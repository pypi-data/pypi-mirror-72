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
    API végpont a cégformák törzs lekérdezésére.
    """
    queryset = models.Project.objects.all().order_by('-name')
    serializer_class = serializers.ProjectSerializer
    permission_classes = []
