from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import File
from .serializers import FileSerializer
from .tasks import process_file


@api_view(['POST'])
def upload_file(request):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
        file_serializer.save()
        process_file.delay(file_serializer.data['id'])
        return Response(file_serializer.data,status=status.HTTP_201_CREATED)
    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def file_list(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)

