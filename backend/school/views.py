import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.files.storage import default_storage
from .models import CSVUpload
from .serializers import CSVUploadSerializer
from .tasks import process_csv_upload
import io

class CSVUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        path = default_storage.save(f'uploads/{file.name}', file)
        upload = CSVUpload.objects.create(uploader=request.user, filename=file.name, file=path, status='uploaded')
        # For now: do minimal validation: check header exists
        try:
            file.seek(0)
            decoded = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded)
            headers = reader.fieldnames
            if not headers:
                upload.status = 'error'
                upload.errors = {'file': 'No headers found'}
                upload.save()
                return Response({'detail': 'CSV has no headers'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            upload.status = 'error'
            upload.errors = {'exception': str(e)}
            upload.save()
            return Response({'detail': 'Error reading CSV file', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        upload.status = 'validated'
        upload.save()
        serializer = CSVUploadSerializer(upload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CSVUploadStartImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, upload_id):
        try:
            upload = CSVUpload.objects.get(id=upload_id)
        except CSVUpload.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        if upload.status not in ('validated', 'uploaded'):
            return Response({'detail': f'Cannot start import when status={upload.status}'}, status=status.HTTP_400_BAD_REQUEST)
        # enqueue celery task
        task = process_csv_upload.delay(upload.id)
        upload.status = 'queued'
        upload.save()
        return Response({'detail': 'Import queued', 'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class CSVUploadStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, upload_id):
        try:
            upload = CSVUpload.objects.get(id=upload_id)
        except CSVUpload.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CSVUploadSerializer(upload)
        return Response(serializer.data)

class CSVUploadDryRunView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            file.seek(0)
            text = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(text))
            errors = []
            create_count = 0
            update_count = 0
            for idx, row in enumerate(reader, start=1):
                if not row.get('first_name') or not row.get('last_name'):
                    errors.append({'row': idx, 'error': 'missing name'})
                if not row.get('class_code'):
                    errors.append({'row': idx, 'error': 'missing class_code'})
                # more validations could be added here
                create_count += 1
            return Response({'create_count': create_count, 'update_count': update_count, 'errors': errors})
        except Exception as e:
            return Response({'detail': 'Error reading CSV file', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
