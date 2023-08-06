from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Base(models.Model):
    """
    Base model entities.
    """

    class Meta:
        abstract = True

    name = models.CharField(
        verbose_name=_('Name'),
        max_length = 500
    )

    def __str__(self):
        return str(name);

class Project(Base, models.Model):
    """
    Project model.
    """

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

class Entity(Base, models.Model):
    """
    Entity model.
    """

    class Meta:
        verbose_name = _('entity')
        verbose_name_plural = _('entities')


    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='entities'
    )

class Environment(Base, models.Model):
    """
    Environment model.
    """

    class Meta:
        verbose_name = _('environment')
        verbose_name_plural = _('environments')

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='environments'
    )
    production = models.BooleanField()

class Connection(models.Model):

    class Meta:
        verbose_name = _('connection')
        verbose_name_plural = _('connections')

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='connections'
    )

