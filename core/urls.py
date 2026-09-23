from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv_file, name='upload_csv_file'),
    path('map/', views.map_columns_view, name='map_columns_view'),
    path('results/', views.analysis_results_view, name='analysis_results_view'),
    path('download-pdf/', views.download_pdf_view, name='download_pdf_view'),
]