import mimetypes
import uuid

import boto3
from django.conf import settings
from django.urls import get_resolver, reverse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from base.helpers.decorators import exception_handler

# Create your views here.


class DocumentUploadS3ApiView(views.APIView):
    permission_classes = (IsAuthenticated,)
    swagger_tags = ["S3 File Upload"]

    @method_decorator(exception_handler)
    def post(self, request, *args, **kwargs):
        document = request.FILES['document']
        folder = request.POST['folder']

        filename = document.name
        filename = f'{uuid.uuid4().hex}-{filename}'
        file_type = mimetypes.guess_type(filename)[0]
        key = f'{folder}/{filename}'
        content = document.read()

        client = boto3.client("s3", endpoint_url=settings.S3_ENDPOINT)

        client.put_object(
            Body=content,
            Bucket=settings.S3_BUCKET,
            Key=key,
            ContentType=file_type
        )
        host = settings.S3_ENDPOINT
        res = {
            'url': f'{host}/{key}'
        }
        return Response(data=res, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    data = {
        'message': 'Api service',
        'method': request.method
    }
    return Response(data={'message': data}, status=status.HTTP_200_OK)



def get_urls(request, url_patterns, namespace=""):
    urls = []
    for pattern in url_patterns:
        url_name = f"{namespace}:{pattern.name}"
        urls.append(request.build_absolute_uri(reverse(url_name)))
    return urls


class RootAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        app_names = ["accounts", "organizations"]
        endpoints = {}
        for app in app_names:
            resolver = get_resolver(app)
            endpoints[app] = {}
            for url in ["admin", "user", "public"]:
                resolver = get_resolver(f"{app}.urls.{url}")
                url_patterns = resolver.url_patterns
                print(url_patterns)
                endpoints[app][url] = get_urls(
                    request, url_patterns, f"{app}.apis:{url}"
                )
        return Response(endpoints)
