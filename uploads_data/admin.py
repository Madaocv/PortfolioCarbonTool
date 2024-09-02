# uploads_data/admin.py
import pandas as pd
from django.contrib import admin
from .models import CompanyFile, PortfolioFile, FileDataFrame
from .forms import UploadFileForm
from django.utils.html import format_html
from django.urls import reverse
import io

@admin.register(CompanyFile)
class CompanyFileAdmin(admin.ModelAdmin):
    form = UploadFileForm
    list_display = ['file_name', 'uploaded_at', 'uploaded_by']
    readonly_fields = ['uploaded_at', 'uploaded_by']
    actions = ['delete_selected']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            obj.file_name = obj.file.name
        super().save_model(request, obj, form, change)
        if hasattr(obj, 'data_frame'):
            df = pd.read_parquet(io.BytesIO(obj.data_frame.data_frame))
        else:
            obj.data_frame = FileDataFrame.objects.create(company_file=obj)
            df = pd.read_excel(obj.file.path, skiprows=1)
        column_names = [f"{chr(65 + i)}" for i in range(len(df.columns))]
        df.columns = column_names
        last_valid_index = df['A'].last_valid_index()
        if last_valid_index is not None:
            df = df.loc[:last_valid_index].reset_index(drop=True)
        if hasattr(obj, 'data_frame'):
            obj.data_frame.save_data_frame(df)
        else:
            FileDataFrame.objects.create(company_file=obj, data_frame=df)
            
    def delete_model(self, request, obj):
        # obj.data_frame_rows.all().delete()
        if hasattr(obj, 'data_frame'):
            obj.data_frame.delete()
        super().delete_model(request, obj)


@admin.register(PortfolioFile)
class PortfolioFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'uploaded_at', 'uploaded_by','file_link']
    readonly_fields = ['uploaded_at', 'uploaded_by','file_link']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            obj.file_name = obj.file.name
        super().save_model(request, obj, form, change)
        if hasattr(obj, 'data_frame'):
            df = pd.read_parquet(io.BytesIO(obj.data_frame.data_frame))
        else:
            obj.data_frame = FileDataFrame.objects.create(portfolio_file=obj)
            df = pd.read_excel(obj.file.path)
        # Завантажуємо файл як DataFrame
        df = pd.read_excel(obj.file.path)

        # Видалення порожніх рядків на початку
        df.dropna(how='all', inplace=True)

        # Перевірка, чи перший рядок містить текстові заголовки
        if isinstance(df.iloc[0, 0], str) and isinstance(df.iloc[0, 1], str):
            df.columns = df.iloc[0]  # Використовуємо перший рядок як заголовок, якщо це текст
            df = df[1:]  # Видаляємо перший рядок, який тепер є заголовками
        else:
            # Якщо перший рядок містить дані, а не заголовки, встановлюємо заголовки вручну
            df.columns = ['ISIN', 'Weight']

        # Збереження DataFrame в базу даних
        if hasattr(obj, 'data_frame'):
            obj.data_frame.save_data_frame(df)
        else:
            FileDataFrame.objects.create(portfolio_file=obj, data_frame=df)
            
    def delete_model(self, request, obj):
        if hasattr(obj, 'data_frame'):
            obj.data_frame.delete()
        super().delete_model(request, obj)

    def file_link(self, obj):
        if obj.file:
            preview_url = reverse('file_preview', args=['portfoliofile', obj.pk])
            return format_html(f'<a href="{preview_url}" target="_blank">Transform file to dataframe {obj.name}</a>')
        return "No file uploaded"
    file_link.short_description = "File preview"
