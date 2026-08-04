from django.urls import path
from .views import CSVUploadView, CSVUploadStatusView, CSVUploadStartImportView, CSVUploadDryRunView, PasswordChangeView

urlpatterns = [
    path('upload/csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('upload/csv/dry-run/', CSVUploadDryRunView.as_view(), name='upload-csv-dry-run'),
    path('upload/csv/<int:upload_id>/', CSVUploadStatusView.as_view(), name='upload-csv-status'),
    path('upload/csv/<int:upload_id>/start/', CSVUploadStartImportView.as_view(), name='upload-csv-start'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
]
