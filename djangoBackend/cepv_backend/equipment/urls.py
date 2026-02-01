from django.urls import path
from .views import uploadCSVAPIView, DatasetHistoryAPIView,DatasetPDFReportAPIView,SignupAPIView,DatasetAnalyzeAPIView

urlpatterns = [
    path('upload/', uploadCSVAPIView.as_view()), # POST
    path('history/', DatasetHistoryAPIView.as_view()), # GET
    path('report/<int:dataset_id>/', DatasetPDFReportAPIView.as_view(), name='dataset-report'),
    path('auth/signup/',SignupAPIView.as_view()),
    path('dataset/<int:dataset_id>/analyze/', DatasetAnalyzeAPIView.as_view(), name='dataset-analyze'),
]