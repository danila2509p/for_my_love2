from gc import enable

from django.db import models

class ImageModel(models.Model):
    image = models.BinaryField(editable=True)  # Путь для сохранения изображений
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата загрузки