# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from crm.models import ProductRental
from .Serializer import RentalServiceSerializer, ClaimGoodSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

import datetime
import logging


class RentalServiceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ProductRental.objects.all()
    serializer_class = RentalServiceSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)

    filter_fields = ('serviceNo', 'deliveryStore', 'name', 'phone')

    def list(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        createDate = request.GET.getlist('createDate[]', None)
        finishDate = request.GET.getlist('finishDate[]', None)
        leaseholdStatus = request.GET.getlist('leaseholdStatus[]', None)
        creditStatus = request.GET.getlist('creditStatus[]', None)

        if not createDate and not finishDate and not leaseholdStatus and not creditStatus:
            return super(RentalServiceViewset, self).list(self.request, *args, **kwargs)
        else:
            filterargs = request.GET.copy().dict()
            cdlist = filterargs.pop('createDate[]', None)
            fdlist = filterargs.pop('finishDate[]', None)
            lhlist = filterargs.pop('leaseholdStatus[]', None)
            cslist = filterargs.pop('creditStatus[]', None)
            timeformat = "%Y-%m-%d %H:%M:%S"

            if cdlist and isinstance(cdlist, list):
                if cdlist[0] == cdlist[1]:
                    dt = datetime.datetime.strptime(cdlist[0], timeformat)
                    filterargs['gmt_create__date'] = dt#.date()
                else:
                    dtstart = datetime.datetime.strptime(cdlist[0], timeformat)#.date()
                    dtend = datetime.datetime.strptime(cdlist[1], timeformat)#.date()
                    filterargs['gmt_create__date__gte'] = dtstart
                    filterargs['gmt_create__date__lte'] = dtend

            if fdlist and isinstance(fdlist, list):
                if fdlist[0] == fdlist[1]:
                    dt = datetime.datetime.strptime(cdlist[0], timeformat)
                    filterargs['finishDate'] = dt#.date()
                else:
                    dtstart = datetime.datetime.strptime(fdlist[0], timeformat)#.date()
                    dtend = datetime.datetime.strptime(fdlist[1], timeformat)#.date()
                    filterargs['finishDate__gte'] = dtstart
                    filterargs['finishDate__lte'] = dtend

            if lhlist and isinstance(lhlist, list):
                if len(lhlist) == 1:
                    filterargs['leaseholdStatus'] = lhlist[0]
                else:
                    filterargs['leaseholdStatus__in'] = lhlist

            if cslist and isinstance(cslist, list):
                if len(cslist) == 1:
                    filterargs['creditStatus'] = cslist[0]
                else:
                    filterargs['creditStatus__in'] = cslist

            filterargs.pop('limit', None)
            filterargs.pop('offset', None)

            try:
                queryset = ProductRental.objects.filter(**filterargs)
            except Exception, e:
                logger.error(e)
                return Response({"detail": e.message}, HTTP_400_BAD_REQUEST)
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
            serializer = RentalServiceSerializer(queryset, many=True)
            return Response(serializer.data)

        pass


# 取货接口
class ClaimGoodsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClaimGoodSerializer

    # _ignore_model_permissions = True

    def post(self, request, *args, **kwargs):
        serializer = ClaimGoodSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            try:
                serializer.save()
                serializer.data['claimResult'] = '0'
            except Exception, e:
                print e
                logger = logging.getLogger('django')
                logger.error(e)
                return Response({"detail": e.detail[0]}, HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

