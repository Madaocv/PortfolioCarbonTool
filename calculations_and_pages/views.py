from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .utils import mock_data, calculation
from uploads_data.models import FileDataFrame, PortfolioFile
from django.contrib.auth.decorators import login_required
import time
import pandas as pd
from django.http import HttpResponse
from pprint import pformat
@login_required
def createportfolio(request):
    is_in_development = True

    return render(request, 'createportfolio.html', {'is_in_development': is_in_development})


@login_required
def holdings(request):
    portfolios = PortfolioFile.objects.all().order_by('uploaded_at')
    
    custom_portfolios = [
        # {'name': 'Custom Portfolio 1', 'id': 'custom_1'},
        # {'name': 'Custom Portfolio 2', 'id': 'custom_2'},/
    ]
    combined_portfolios = list(custom_portfolios) + list(portfolios)
    return render(request, 'holdings.html', {'portfolios': combined_portfolios})

@login_required
def portfolio(request):
    portfolios = PortfolioFile.objects.all().order_by('uploaded_at')
    
    custom_portfolios = [
        # {'name': 'Custom Portfolio 1', 'id': 'custom_1'},
        # {'name': 'Custom Portfolio 2', 'id': 'custom_2'},/
    ]
    combined_portfolios = list(custom_portfolios) + list(portfolios)
    is_in_development = True
    return render(request, 'portfolio.html', {
        'portfolios': combined_portfolios,
        'is_in_development': is_in_development
    })


@require_POST
def calculate_chart_data(request):
    all_file_data_frames = FileDataFrame.objects.filter(company_file__isnull=False)
    data_frames = []
    for file_data_frame in all_file_data_frames:
        # print(f"Processing FileDataFrame ID: {file_data_frame.id}")
        try:
            # file_start_time = time.time()
            df = file_data_frame.get_data_frame()
            data_frames.append(df)
            # file_end_time = time.time()
            # print(f"Processed FileDataFrame ID: {file_data_frame.id} in {file_end_time - file_start_time:.2f} seconds")
            # print(df.shape)
        except Exception as e:
            print(f"Error processing FileDataFrame ID: {file_data_frame.id} - {e}")
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        # Видаляємо повторення значень по першій колонці
        # combined_df = combined_df.drop_duplicates(subset=['A'])
    data = json.loads(request.body)
    portfolio = data.get('portfolio')
    reference = data.get('reference')
    is_absolute = data.get('absoluteRelative')
    is_company = data.get('companyContribution')
    # print(f"portfolio: {portfolio}")
    # print(f"reference: {reference}")
    # print(f"is_absolute: {is_absolute}")
    # print(f"is_company: {is_company}")
    try:

        if not portfolio:
            raise ValueError("Portfolio ID is missing or invalid.")
        maintitle = "Contribution" if is_company else "Company"
        lefttitle = "" if is_company else "Carbon Intensivity"
        bottomtitle = "" if is_company else "Change trought 2030"
        portfolio_file = PortfolioFile.objects.get(id=portfolio)
        df_prtfolio = portfolio_file.data_frame.get_data_frame()
        reference_file = PortfolioFile.objects.get(id=reference)
        df_reference = reference_file.data_frame.get_data_frame()
        start = time.time()
        df = calculation(
            df=df,
            portfolio=df_prtfolio,
            portfolio_name=portfolio_file.name,
            reference=df_reference,
            reference_name=reference_file.name,
            is_absolute=is_absolute,
            is_company=is_company
        )
        # print(df[['AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO']].head(12))
        # print(df[['BV', 'BW', 'BX', 'BY', 'BZ']].head(12))
        end = time.time()
        # print("Calculation time: ", end - start)
        if is_company:
            df_filtered = df[[df.columns[1], "AV", "AY"]].dropna(subset=["AV", "AY"])
        else:
            df_filtered = df[[df.columns[1], "AQ", "AT"]].dropna(subset=["AQ", "AT"])
        data = [{"x": row.iloc[1], "y": row.iloc[2], "text": row.iloc[0]} for _, row in df_filtered.iterrows()]

        result = {
            "data": data,
            "maintitle": maintitle,
            "lefttitle": lefttitle,
            "bottomtitle": bottomtitle
        }
        return JsonResponse(result)
    except (ValueError, PortfolioFile.DoesNotExist) as e:
        return JsonResponse({
            "error": str(e)
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred: " + str(e)
        }, status=500)
        
        
@require_POST
def calculate_portfolio_data(request):
    data = json.loads(request.body)
    print(pformat(data))
    return JsonResponse({"data": []})