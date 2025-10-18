from django.urls import path
from .views import (
    AttendanceReportListView,
    AttendanceReportDetailView,
    GenerateReportView,
    DailySummaryView,
    MonthlySummaryView,
)

app_name = 'reports'

urlpatterns = [
    path('reports/', AttendanceReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', AttendanceReportDetailView.as_view(), name='report_detail'),
    path('reports/generate/', GenerateReportView.as_view(), name='generate_report'),
    path('reports/daily-summary/', DailySummaryView.as_view(), name='daily_summary'),
    path('reports/monthly-summary/', MonthlySummaryView.as_view(), name='monthly_summary'),
]