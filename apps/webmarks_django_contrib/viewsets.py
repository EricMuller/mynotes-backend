from abc import ABCMeta

from rest_framework import viewsets


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class RetrieveUpdateModelViewSet(viewsets.mixins.RetrieveModelMixin,
                                 viewsets.mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):
    __metaclass__ = ABCMeta

    pass
