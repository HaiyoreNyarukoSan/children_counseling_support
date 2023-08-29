from django.apps import AppConfig
from ultralytics import YOLO


class AnalyzerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "analyzer"
