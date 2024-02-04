from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import File
from .serializers import FileSerializer
from .tasks import process_file


class FileUploadTests(APITestCase):
    def test_upload_file(self):
        url = reverse('upload_file')
        file_data = {'file': open('path/to/your/file.txt', 'rb')}
        response = self.client.post(url, file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['file'], 'http://testserver/uploads/your_file.txt')

    def test_get_file_list(self):
        url = reverse('file_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class FileModelTests(TestCase):
    def test_file_creation(self):
        file = File.objects.create(file=SimpleUploadedFile('file.txt', b'file_content'))
        self.assertEqual(file.file.url, 'uploads/file.txt')


class FileSerializerTests(TestCase):
    def test_file_serializer(self):
        file_data = {'file': SimpleUploadedFile('file.txt', b'file-content')}
        serializer = FileSerializer(data=file_data)
        self.assertTrue(serializer.is_valid())


class CeleryTaskTests(TestCase):
    def test_process_file_task(self):
        file = File.objects.create(file='file.txt', processed=False)
        process_file(file.id)
        file.refresh_from_db()
        self.assertTrue(file.processed)
