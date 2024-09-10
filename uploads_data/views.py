from django.shortcuts import render, get_object_or_404
from .models import CompanyFile, PortfolioFile
from django.contrib.auth.decorators import login_required


@login_required
def file_preview(request, pk, model):
    if model == 'companyfile':
        file_instance = get_object_or_404(CompanyFile, pk=pk)
        df_instance = file_instance.data_frame
    elif model == 'portfoliofile':
        file_instance = get_object_or_404(PortfolioFile, pk=pk)
        df_instance = file_instance.data_frame

    # Завантажуємо DataFrame із бази даних
    if df_instance:
        df = df_instance.get_data_frame()

        # Конвертуємо DataFrame у HTML для перегляду
        preview_html = df.to_html()
    else:
        preview_html = "<p>No data available for this file.</p>"

    return render(request, 'uploads_data/preview.html', {'preview_html': preview_html})


