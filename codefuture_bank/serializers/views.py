from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from serializers import serializers


@api_view(['GET'])
def phone_serializer_view(request: Request) -> Response:

    phone = request.GET.get('phone')

    return Response({"phone": serializers.phone_serializer(phone)})


@api_view(['GET'])
def fcs_serializer_view(request: Request) -> Response:
    fcs = request.GET.get('fcs')

    return Response({"fcs": serializers.fcs_serializer(fcs)})
