# uploads_data/models.py
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from openpyxl import load_workbook
from django.urls import reverse
from pprint import pformat
import pandas as pd
import json
import io
from io import StringIO
from django_pandas.managers import DataFrameManager
import fastparquet
import tempfile
def validate_excel_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

    # Further validation using pandas or openpyxl can be added here if needed
    try:
        load_workbook(value)
    except Exception:
        raise ValidationError('Invalid Excel file.')

class CompanyFile(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_excel_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Upload company data'
        verbose_name_plural = 'Upload company data'

    def __str__(self):
        return self.file_name
    
    def get_preview_url(self):
        return reverse('file_preview', args=[self.pk])

class PortfolioFile(models.Model):
    name = models.CharField(max_length=255, help_text="Введіть назву портфоліо")
    file = models.FileField(upload_to='portfolio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Create new portfolio'
        verbose_name_plural = 'Create new portfolios'

    def __str__(self):
        return self.name


class FileDataFrame(models.Model):
    company_file = models.OneToOneField(CompanyFile, on_delete=models.CASCADE, related_name='data_frame', null=True, blank=True)
    portfolio_file = models.OneToOneField(PortfolioFile, on_delete=models.CASCADE, related_name='data_frame', null=True, blank=True)
    data_frame = models.BinaryField()
    def save_data_frame(self, df):
        # Створюємо тимчасовий файл для збереження Parquet даних
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            # Записуємо DataFrame у Parquet формат у тимчасовий файл
            fastparquet.write(tmp_file.name, df, compression='GZIP')

            # Зчитуємо дані з тимчасового файлу
            tmp_file.seek(0)  # Повертаємо курсор на початок файлу
            parquet_data = tmp_file.read()

        # Збереження Parquet даних у поле data_frame
        self.data_frame = parquet_data

        # Зберігаємо об'єкт
        self.save()
    def get_data_frame(self):
        # Завантаження Parquet даних з поля data_frame
        parquet_buffer = io.BytesIO(self.data_frame)
        return pd.read_parquet(parquet_buffer, engine='fastparquet')
