from django.urls import path
from .views import CSVUploadView, CSVUploadStatusView

urlpatterns = [
    path('upload/csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('upload/csv/<int:upload_id>/', CSVUploadStatusView.as_view(), name='upload-csv-status'),
]
