from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Base(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        verbose_name=_('Name'),
        max_length = 500
    )

    def __str__(self):
        return str(name);

class Project(Base, models.Model):

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

class Entity(Base, models.Model):

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='entities'
    )

class Environment(Base, models.Model):

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='environments'
    )
    production = models.BooleanField()

class Connection(models.Model):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='connections'
    )