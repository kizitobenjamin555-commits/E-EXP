from django.urls import path
from .views import CSVUploadView, CSVUploadStatusView, CSVUploadStartImportView, CSVUploadDryRunView

urlpatterns = [
    path('upload/csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('upload/csv/dry-run/', CSVUploadDryRunView.as_view(), name='upload-csv-dry-run'),
    path('upload/csv/<int:upload_id>/', CSVUploadStatusView.as_view(), name='upload-csv-status'),
    path('upload/csv/<int:upload_id>/start/', CSVUploadStartImportView.as_view(), name='upload-csv-start'),
]
