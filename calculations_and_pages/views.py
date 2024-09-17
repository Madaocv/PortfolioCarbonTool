from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .utils import mock_data, calculation, calculation_prtfolio, prepare_data_for_response, calculation_waterfall, transform_data_for_multiple_series
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
    is_in_development = False
    return render(request, 'portfolio.html', {
        'portfolios': combined_portfolios,
        'is_in_development': is_in_development
    })

# TODO rename to holdings
@require_POST
def calculate_chart_data(request):
    all_file_data_frames = FileDataFrame.objects.filter(company_file__isnull=False)
    data_frames = []
    for file_data_frame in all_file_data_frames:
        try:
            df = file_data_frame.get_data_frame()
            data_frames.append(df)
        except Exception as e:
            print(f"Error processing FileDataFrame ID: {file_data_frame.id} - {e}")
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
    data = json.loads(request.body)
    portfolio = data.get('portfolio')
    reference = data.get('reference')
    is_absolute = data.get('absoluteRelative')
    is_company = data.get('companyContribution')
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
        df = calculation(
            df=df,
            portfolio=df_prtfolio,
            portfolio_name=portfolio_file.name,
            reference=df_reference,
            reference_name=reference_file.name,
            is_absolute=is_absolute,
            is_company=is_company
        )
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
    output_file_format = {
        "chart1": {
            "maintitle": None,
            "lefttitle": None,
            "bottomtitle": None,
            "data": None,
            "render": True,
            "serieslen": None,
        },
        "chart2": {
            "maintitle": None,
            "lefttitle": None,
            "bottomtitle": None,
            "data": None,
            "render": False
        }
    }
    all_file_data_frames = FileDataFrame.objects.filter(company_file__isnull=False)
    data_frames = []
    for file_data_frame in all_file_data_frames:
        try:
            df = file_data_frame.get_data_frame()
            data_frames.append(df)
        except Exception as e:
            print(f"Error processing FileDataFrame ID: {file_data_frame.id} - {e}")
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
    data = json.loads(request.body)
    portfolio = data.get('portfolios', [])
    portfolio_filter = [obj for obj in portfolio if obj['checked']]
    portfolio_dfs = []
    portfolio_names = []
    if len(portfolio_filter) > 1:
        for obj in portfolio_filter:
            portfolio_file = PortfolioFile.objects.get(id=obj['id'])
            df_prtfolio = portfolio_file.data_frame.get_data_frame()
            portfolio_dfs.append(df_prtfolio)
            portfolio_names.append(portfolio_file.name)
        # Count Chart 2 Data
        coutn_result_df, df, columns = calculation_prtfolio(df=df, portfolios=portfolio_dfs)
        result = prepare_data_for_response(coutn_result_df, portfolio_names)
        # print(pformat(result))
        output_file_format['chart2']['data'] = result
        output_file_format['chart2']['lefttitle'] = "Weighted average carbon intensity (rel to ACWI)"
        output_file_format['chart2']['bottomtitle'] = "Implied % emissions change through 2030"
        output_file_format['chart2']['render'] = True
        # Count Waterfall Data
        print("X"*50)
        print(columns)
        print("X"*50)
        waterfall_result_df = calculation_waterfall(df=df, columns=columns)
        data_for_watrfal_chart = transform_data_for_multiple_series(waterfall_result_df)
        print('-'*50)
        print(pformat(waterfall_result_df))
        print('.'*50)
        print(pformat(data_for_watrfal_chart))
        print(len(waterfall_result_df))
        print('.'*50)
        output_file_format['chart1']['data'] = data_for_watrfal_chart
        output_file_format['chart1']['serieslen'] = len(waterfall_result_df)
        return JsonResponse(output_file_format)
    else:
        return JsonResponse(output_file_format)