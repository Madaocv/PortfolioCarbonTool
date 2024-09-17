import pandas as pd
import numpy as np
import time
import string
from pprint import pformat

def sumproduct(df, col1, col2):
    df[col1] = pd.to_numeric(df[col1], errors='coerce')
    df[col2] = pd.to_numeric(df[col2], errors='coerce')
    result = (df[col1] * df[col2]).sum()
    return result


def custom_formula(bw_value, bz_value):
    result = bw_value - bz_value
    if result < -100:
        return -100
    elif result > 100:
        return 100
    else:
        return result


def calculate_formula_new_minus(df, column1, column2):
    df[column1] = pd.to_numeric(df[column1], errors='coerce')
    df[column2] = pd.to_numeric(df[column2], errors='coerce')
    filtered_df = df[(df[column1] < 99999999999999900000) & (df[column1].notna()) &
                    (df[column2] < 99999999999999900000) & (df[column2].notna())]
    filtered_df = filtered_df[(filtered_df[column1] != float('inf')) & 
                            (filtered_df[column1] != float('-inf')) & 
                            (filtered_df[column2] != float('inf')) & 
                            (filtered_df[column2] != float('-inf'))]
    numerator = -(filtered_df[column1] * filtered_df[column2]).sum()
    if numerator == float('inf') or numerator == float('-inf') or pd.isna(numerator):
        return float('nan')
    denominator = filtered_df[column2].sum()
    if denominator == 0 or pd.isna(denominator):
        return 0
    else:
        return numerator / denominator


def calculate_relative_difference(df, target_column, base_row, subtract_row):
    base_value = df.loc[df['AF'] == base_row, target_column].values[0]
    subtract_value = df.loc[df['AF'] == subtract_row, target_column].values[0]
    difference = base_value - subtract_value
    return difference


def calculate_formula(df, column1, column2):
    df[column1] = pd.to_numeric(df[column1], errors='coerce')
    df[column2] = pd.to_numeric(df[column2], errors='coerce')
    filtered_df = df[(df[column1] < 99999999999999900000) & (df[column2] < 99999999999999900000)]
    filtered_df = filtered_df.dropna(subset=[column1, column2])
    filtered_df = filtered_df[(filtered_df[column1] != float('inf')) & 
                              (filtered_df[column1] != float('-inf')) & 
                              (filtered_df[column2] != float('inf')) & 
                              (filtered_df[column2] != float('-inf'))]
    numerator = (filtered_df[column1] * filtered_df[column2]).sum()
    if numerator == float('inf') or numerator == float('-inf') or pd.isna(numerator):
        return float('nan')
    denominator = filtered_df[column2].sum()
    if denominator == 0 or pd.isna(denominator):
        return 0
    else:
        return numerator / denominator


def calculate_formula_new(df, column1, column2):
    df[column1] = pd.to_numeric(df[column1], errors='coerce')
    df[column2] = pd.to_numeric(df[column2], errors='coerce')
    filtered_df = df[(df[column1] < 99999999999999900000) & (df[column1] != 0) & (df[column1].notna()) &
                     (df[column2] < 99999999999999900000) & (df[column2] != 0) & (df[column2].notna())]
    filtered_df = filtered_df[(filtered_df[column1] != float('inf')) & 
                              (filtered_df[column1] != float('-inf')) & 
                              (filtered_df[column2] != float('inf')) & 
                              (filtered_df[column2] != float('-inf'))]
    numerator = (filtered_df[column1] * filtered_df[column2]).sum()
    if numerator == float('inf') or numerator == float('-inf') or pd.isna(numerator):
        return float('nan')
    denominator = filtered_df[column2].sum()
    if denominator == 0 or pd.isna(denominator):
        return 0
    else:
        return numerator / denominator
    
# def calculate_formula_newMove(df, column1, column2):
#     df[column1] = pd.to_numeric(df[column1], errors='coerce')
#     df[column2] = pd.to_numeric(df[column2], errors='coerce')
#     filtered_df = df[(df[column1] < 99999999999999900000) & (df[column1] != 0) & (df[column1].notna()) &
#                     (df[column2] < 99999999999999900000) & (df[column2] != 0) & (df[column2].notna())]
#     filtered_df = filtered_df[(filtered_df[column1] != float('inf')) & 
#                             (filtered_df[column1] != float('-inf')) & 
#                             (filtered_df[column2] != float('inf')) & 
#                             (filtered_df[column2] != float('-inf'))]
#     numerator = (filtered_df[column1] * filtered_df[column2]).sum()
#     if numerator == float('inf') or numerator == float('-inf') or pd.isna(numerator):
#         return float('nan')
#     denominator = filtered_df[column2].sum()
#     if denominator == 0 or pd.isna(denominator):
#         return 0
#     else:
#         return numerator / denominator

def mock_data(swichto=None):
    names = [
        "Nextracker Inc", "Solaria Energia y Medio Ambiente, S.A.", "OX2 AB (publ)", "ENPHASE ENERGY, INC.",
        "Alfen NV", "CORPORACION ACCIONA ENERGIAS RENOVABLES SA", "ARRAY TECHNOLOGIES, INC.",
        "EDP Renovaveis, S.A.", "Sungrow Power Supply Co., Ltd.", "NEOEN SA",
        "SOLAREDGE TECHNOLOGIES, INC.", "VESTAS WIND SYSTEMS A/S", "ITRON, INC.",
        "SCHNEIDER ELECTRIC SE", "Landis+Gyr Group AG", "Shoals Technologies Group Inc",
        "LEGRAND SA", "SMA Solar Technology AG", "INDUSTRIE DE NORA S.P.A.", "Nordex SE",
        "VOLTALIA SA", "HYDRO ONE LIMITED", "STEM, INC.", "JOHNSON CONTROLS INTERNATIONAL PLC",
        "Fluence Energy Inc", "SPIE SA", "FIRST SOLAR, INC.",
        "Contemporary Amperex Technology Co., Ltd.", "ORMAT TECHNOLOGIES, INC.",
        "MASTEC, INC.", "Ariston Holding N.V.", "FORVIA SE", "Signify N.V.",
        "REDEIA CORPORACION, S.A.", "NEXANS SA", "SAMSUNG SDI CO., LTD.", "ELIA GROUP SA",
        "JOHNSON MATTHEY PLC", "Gurit Holding AG", "UMICORE SA", "COMPAGNIE PLASTIC OMNIUM SE",
        "Sif Holding N.V.", "DEME GROUP NV", "LG CHEM LTD", "Wacker Chemie AG", "XINYI SOLAR HOLDINGS LIMITED"
    ]

    x_values_bc = [
        -76.13935698, -76.10528032, -76.08568612, -75.63419241, -75.57344927, -75.56337382,
        -75.45931492, -75.16829311, -74.18828859, -73.71505513, -73.65519195, -73.38539493,
        -72.70352611, -72.20611959, -72.2039764, -71.75121094, -71.58498334, -68.21317886,
        -67.67248096, -67.65396755, -66.414741, -65.78658197, -64.76345192, -60.59958488,
        -60.59759513, -59.89188398, -56.63005023, -51.78276439, -47.18726408, -46.84275609,
        -44.93369699, -37.50635314, -35.66736662, -27.71907875, -27.39848046, -21.00090598,
        -18.55819334, -9.347318763, -6.785252873, -5.481676292, 5.971138979, 76.99519941,
        80.54734943, 109.3048168, 248.5449476, 452.9421889
    ]
    
    x_values_bh = [
    -0.878576068, -1.403083771, -1.384949266, -1.722045512, -1.270360435, -2.283399105,
    -2.084805988, -2.997479153, -0.910529283, -1.745393837, -0.201348981, -3.254180081,
    -0.679980292, -1.345898199, -1.482874758, -0.460119263, -1.125626515, -0.952981836,
    -0.837965696, -1.321738095, -0.743262821, -1.70417418, -0.313544567, -0.721376348,
    -0.924205705, -0.748871845, -2.925873237, -1.440120586, -0.53016129, -0.636470487,
    -0.42036714, -0.630513913, -0.882372142, -0.973939511, -1.005608421, -0.695726009,
    -0.400868996, -0.457733683, -0.049532526, -0.2597032, 0.123897384, 0.744106648,
    0.724039514, 1.484144515, 5.297574694, 12.27987331
    ]

    y_values_bf = [
        8.255768293, 8.232982448, 8.263939185, 8.255768293, 8.255768293, 7.704648558, 8.255768293,
        7.965298216, 8.255768293, 8.255768293, 8.442520119, 7.745119061, 8.519348773, 8.146691203,
        6.226267928, 8.255768293, 7.344192048, 8.730979396, 8.255768293, 5.567882294, 8.255768293,
        8.255768293, 8.255768293, 8.563222623, 8.255768293, 9.449072845, 1.979046912, 8.255768293,
        8.255768293, 8.255768293, -0.885584034, -30.42281695, -15.28197427, -7.260995097,
        7.32496544, 11.45318168, -2.429323794, 4.370580535, 8.255768293, 9.648197616, 3.55225503,
        8.255768293, 8.255768293, 17.97542363, -87.6305008, 8.255768293
    ]
    y_values_bk = [
    0.095263747, 0.151784002, 0.150424306, 0.187968011, 0.13877627, 0.232821627,
    0.228092121, 0.317631469, 0.101324871, 0.195476583, 0.023079063, 0.343447251,
    0.079679619, 0.151851631, 0.127870735, 0.052941797, 0.115482562, 0.121977379,
    0.102228417, 0.108778279, 0.092392224, 0.213862261, 0.039969322, 0.101936445,
    0.125913052, 0.11814864, 0.102250314, 0.229599598, 0.092755722, 0.112174289,
    -0.008284883, -0.511433604, -0.378059544, -0.255122837, 0.268848739, 0.379425363,
    -0.052474967, 0.214025217, 0.060267327, 0.457098826, 0.073707061, 0.07978643,
    0.074211039, 0.244070913, -1.867787408, 0.223825007
    ]
    if swichto == "company":
        x_values = x_values_bc
        y_values = y_values_bf
        maintitle = "Company Main Title"
        lefttitle = "Company Left Axis Title"
        bottomtitle = "Company Bottom Axis Title"
    elif swichto == "contribution":
        x_values = x_values_bh
        y_values = y_values_bk
        maintitle = "Contribution Main Title"
        lefttitle = "Contribution Left Axis Title"
        bottomtitle = "Contribution Bottom Axis Title"
    # Формуємо список об'єктів для відправки у відповідь
    data = []
    for i in range(len(names)):
        data.append({
            "x": x_values[i],
            "y": y_values[i],
            "text": names[i]
        })

    # Повертаємо результати у форматі JSON
    result = {
        "data": data,
        "maintitle": maintitle,
        "lefttitle": lefttitle,
        "bottomtitle": bottomtitle
    }
    return result


def automated_calculation(df=None, portfolio_name=None, reference_name=None):
    # Список колонок для обчислення
    columns_to_calculate = ['AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
    base_columns = ['P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']

    for col_base, col_target in zip(base_columns, columns_to_calculate):
        df[col_target] = None
        df.loc[df['AF'] == portfolio_name, col_target] = calculate_formula(df, col_base, 'AA')
        df.loc[df['AF'] == reference_name, col_target] = calculate_formula(df, col_base, 'AD')

    return df


def calculation(df=None, portfolio=None, reference=None, is_absolute=None, is_company=None, portfolio_name=None, reference_name=None):
    df['A'] = df['A'].str.strip()
    # portfolio
    portfolio_df = portfolio.dropna(subset=['ISIN', 'Weight'], how='all')
    portfolio_df['ISIN'] = portfolio_df['ISIN'].str.strip()
    df['AA'] = df['A'].map(portfolio_df.set_index('ISIN')['Weight'])
    # TODO
    df['AB'] = None
    df['AC'] = None
    # reference
    reference_df = reference.dropna(subset=['ISIN', 'Weight'], how='all')
    reference_df['ISIN'] = reference_df['ISIN'].str.strip()
    df['AD'] = df['A'].map(reference_df.set_index('ISIN')['Weight'])
    # Filter df to keep only rows with ISINs in both portfolio_df and reference_df
    # valid_isins = set(portfolio_df['ISIN']).intersection(reference_df['ISIN'])
    # df = df[df['A'].isin(valid_isins)].copy()
    # print(df.shape)
    
    df['N'] = df['C'].add(df['D'], fill_value=0)
    df['O'] = df['N'].add(df['E'], fill_value=0)
    df['P'] = df['N'].div(df['F'], fill_value=0).replace([float('inf'), -float('inf')], None)
    df['Q'] = df['E'].div(df['F'], fill_value=0)
    df['R'] = df['O'].div(df['F'], fill_value=0)
    df['S'] = df['N'].mul(df['H'], fill_value=0)
    df['T'] = df['S'].div(df['F'], fill_value=0)
    df['U'] = df['H'].fillna(pd.NA)
    df['V'] = df['I'].fillna(pd.NA)
    df['W'] = df['J'].fillna(pd.NA)
    df['X'] = df['K'].fillna(pd.NA)
    df['Y'] = df['L'].fillna(pd.NA)


    
    af_values = [
        portfolio_name,
        # "SMFE",
        # "B&M 18-32",
        reference_name,
        "Portfolio relative",
        
        "Reference S12",
        "Reference avoided emissions",
        "Reference total",
        
        "Portfolio S12",
        "Portfolio avoided emissions",
        "Portfolio reduction",
        
        "Portfolio 2030",
        
        "Reference S12_a",
        "Reference avoided emissions_a",
        "Reference total_a",
        
        "Portfolio S12_b",
        "Portfolio avoided emissions_b",
        "Portfolio reduction_b",
        
        "Portfolio 2030_c"
    ]
    df['AF'] = None
    df.iloc[0:0+len(af_values), df.columns.get_loc('AF')] = af_values
    df = automated_calculation(df=df, portfolio_name=portfolio_name, reference_name=reference_name)
    relative_columns_to_calculate = ["AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO"]

    for column in relative_columns_to_calculate:
        df.loc[df['AF'] == 'Portfolio relative', column] = calculate_relative_difference(df, column, portfolio_name, reference_name)

    df.loc[df['AF'] == 'Reference S12', 'AG'] = df.loc[df['AF'] == reference_name, 'AG'].values[0]
    df.loc[df['AF'] == 'Reference avoided emissions', 'AG'] = df.loc[df['AF'] == reference_name, 'AH'].values[0]
    df.loc[df['AF'] == 'Reference total', 'AG'] = (
        df.loc[df['AF'] == 'Reference S12', 'AG'].values[0] +
        df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    )

    # df.loc[df['AF'] == 'Portfolio S12', 'AG'] = calculate_relative_difference(df, 'AG', 'GET', 'MSCI ACWI IMI')
    df.loc[df['AF'] == 'Portfolio S12', 'AG'] = calculate_relative_difference(df, 'AG', portfolio_name, reference_name)
    df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'] = df.loc[df['AF'] == portfolio_name, 'AH'].values[0] - df.loc[df['AF'] == reference_name, 'AH'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction', 'AG'] = df.loc[df['AF'] == portfolio_name, 'AJ'].values[0] - df.loc[df['AF'] == reference_name, 'AJ'].values[0]
    df.loc[df['AF'] == 'Portfolio 2030', 'AG'] = df.loc[df['AF'] == 'Reference total', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio reduction', 'AG'].values[0]

    df.loc[df['AF'] == 'Reference S12_a', 'AG'] = df.loc[df['AF'] == 'Reference S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Reference avoided emissions_a', 'AG'] = df.loc[df['AF'] == 'Reference S12', 'AG'].values[0] + df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Reference total_a', 'AG'] = df.loc[df['AF'] == 'Reference avoided emissions_a', 'AG'].values[0]

    df.loc[df['AF'] == 'Portfolio S12_b', 'AG'] = df.loc[df['AF'] == 'Reference total_a', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AG'] = df.loc[df['AF'] == 'Portfolio S12_b', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction_b', 'AG'] = df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio 2030_c', 'AG'] = df.loc[df['AF'] == 'Portfolio 2030', 'AG'].values[0]


    df.loc[df['AF'] == 'Reference avoided emissions_a', 'AH'] = - df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio S12_b', 'AH'] = - df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AH'] = df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction_b', 'AH'] = df.loc[df['AF'] == 'Portfolio reduction_b', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio reduction', 'AG'].values[0]
    # print(time.time() - s2)

    static_value = df.loc[df['AF'] == reference_name, 'AG'].values[0]
    mask = pd.notna(df['P']) & pd.notna(df['AA'])
    df['AQ'] = None  # Ініціалізуємо колонку AQ значенням None
    df.loc[mask, 'AQ'] = df.loc[mask, 'P'] - static_value

    static_value_AH6 = df.loc[df['AF'] == reference_name, 'AH'].values[0]
    # df['AR'] = df.apply(lambda row: row['Q'] - static_value_AH6 if pd.notna(row['P']) and pd.notna(row['AA']) else None, axis=1)
    mask = pd.notna(df['P']) & pd.notna(df['AA'])
    df['AR'] = None  # Ініціалізуємо колонку AR значенням None
    df.loc[mask, 'AR'] = df.loc[mask, 'Q'] - static_value_AH6

    static_value_AI6 = df.loc[df['AF'] == reference_name, 'AI'].values[0]
    mask = pd.notna(df['P']) & pd.notna(df['AA'])
    df['AS'] = None  # Ініціалізуємо колонку AS значенням None
    df.loc[mask, 'AS'] = df.loc[mask, 'R'] - static_value_AI6
    # df['AS'] = df.apply(lambda row: row['R'] - static_value_AI6 if pd.notna(row['P']) and pd.notna(row['AA']) else None, axis=1)

    static_value_AJ6 = df.loc[df['AF'] == reference_name, 'AJ'].values[0]
    # Виконання обчислень векторизовано
    mask = pd.notna(df['P']) & pd.notna(df['AA'])
    df['AT'] = None  # Ініціалізуємо колонку AT значенням None
    df.loc[mask, 'AT'] = df.loc[mask, 'T'] - static_value_AJ6
    # df['AT'] = df.apply(lambda row: row['T'] - static_value_AJ6 if pd.notna(row['P']) and pd.notna(row['AA']) else None, axis=1)

    # df['AV'] = df.apply(lambda row: row['AQ'] * row['AA'] if pd.notna(row['AQ']) and pd.notna(row['AA']) else None, axis=1)
    # df['AW'] = df.apply(lambda row: row['AR'] * row['AA'] if pd.notna(row['AR']) and pd.notna(row['AA']) else None, axis=1)
    # df['AX'] = df.apply(lambda row: row['AS'] * row['AA'] if pd.notna(row['AS']) and pd.notna(row['AA']) else None, axis=1)
    # df['AY'] = df.apply(lambda row: row['AT'] * row['AA'] if pd.notna(row['AT']) and pd.notna(row['AA']) else None, axis=1)
    # Маски для перевірки на не NaN значення
    mask_AV = pd.notna(df['AQ']) & pd.notna(df['AA'])
    mask_AW = pd.notna(df['AR']) & pd.notna(df['AA'])
    mask_AX = pd.notna(df['AS']) & pd.notna(df['AA'])
    mask_AY = pd.notna(df['AT']) & pd.notna(df['AA'])

    # Ініціалізація колонок None
    df['AV'] = None
    df['AW'] = None
    df['AX'] = None
    df['AY'] = None

    # Векторизоване обчислення
    df.loc[mask_AV, 'AV'] = df.loc[mask_AV, 'AQ'] * df.loc[mask_AV, 'AA']
    df.loc[mask_AW, 'AW'] = df.loc[mask_AW, 'AR'] * df.loc[mask_AW, 'AA']
    df.loc[mask_AX, 'AX'] = df.loc[mask_AX, 'AS'] * df.loc[mask_AX, 'AA']
    df.loc[mask_AY, 'AY'] = df.loc[mask_AY, 'AT'] * df.loc[mask_AY, 'AA']
    # print(df[["AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AQ", "AR", "AS", "AT"]].head(20))
    bv_values = [
        "WACI 12", "WACI 12 rel", "Avoided intensity", "Avoided intensity rel", "WACI", 
        "WACI rel", "% SBTi committed", "% change through 2030", "% change through 2030 rel", 
        "Emissions change through 2030", "2030 emissions change intensity", 
        "2030 emissions change intensity rel"
    ]
    df['BV'] = None
    df.iloc[0:0+len(bv_values), df.columns.get_loc('BV')] = bv_values

    df['BW'] = None 
    df.loc[df['BV'] == 'WACI 12', 'BW'] = calculate_formula_new(df, 'P', 'AA')

    df['BX'] = None 
    df.loc[df['BV'] == 'WACI 12', 'BX'] = calculate_formula_new(df, 'P', 'AB')

    df['BY'] = None 
    df.loc[df['BV'] == 'WACI 12', 'BY'] = calculate_formula_new(df, 'P', 'AC')

    df['BZ'] = None 
    df.loc[df['BV'] == 'WACI 12', 'BZ'] = calculate_formula_new(df, 'P', 'AD')
    # print("*"*10)
    # print(calculate_formula(df, 'P', 'AD'))
    # print("*"*10)
    # print(calculate_formula_new(df, 'P', 'AD'))
    # print("*"*10)
    # print("*"*10)

    df.loc[df['BV'] == 'WACI 12 rel', 'BW'] = df.loc[df['BV'] == 'WACI 12', 'BW'].values[0] - df.loc[df['BV'] == 'WACI 12', 'BZ'].values[0]
    df.loc[df['BV'] == 'WACI 12 rel', 'BX'] = df.loc[df['BV'] == 'WACI 12', 'BX'].values[0] - df.loc[df['BV'] == 'WACI 12', 'BZ'].values[0]
    df.loc[df['BV'] == 'WACI 12 rel', 'BY'] = df.loc[df['BV'] == 'WACI 12', 'BY'].values[0] - df.loc[df['BV'] == 'WACI 12', 'BZ'].values[0]
    df.loc[df['BV'] == 'WACI 12 rel', 'BZ'] = df.loc[df['BV'] == 'WACI 12', 'BZ'].values[0] - df.loc[df['BV'] == 'WACI 12', 'BZ'].values[0]

    df.loc[df['BV'] == 'Avoided intensity', 'BW'] = calculate_formula_new_minus(df, 'Q', 'AA')
    df.loc[df['BV'] == 'Avoided intensity', 'BX'] = calculate_formula_new_minus(df, 'Q', 'AB')
    df.loc[df['BV'] == 'Avoided intensity', 'BY'] = calculate_formula_new_minus(df, 'Q', 'AC')
    df.loc[df['BV'] == 'Avoided intensity', 'BZ'] = calculate_formula_new_minus(df, 'Q', 'AD')

    df.loc[df['BV'] == 'Avoided intensity rel', 'BW'] = df.loc[df['BV'] == 'Avoided intensity', 'BW'].values[0] - df.loc[df['BV'] == 'Avoided intensity', 'BZ'].values[0]
    df.loc[df['BV'] == 'Avoided intensity rel', 'BX'] = df.loc[df['BV'] == 'Avoided intensity', 'BX'].values[0] - df.loc[df['BV'] == 'Avoided intensity', 'BZ'].values[0]
    df.loc[df['BV'] == 'Avoided intensity rel', 'BY'] = df.loc[df['BV'] == 'Avoided intensity', 'BY'].values[0] - df.loc[df['BV'] == 'Avoided intensity', 'BZ'].values[0]
    df.loc[df['BV'] == 'Avoided intensity rel', 'BZ'] = df.loc[df['BV'] == 'Avoided intensity', 'BZ'].values[0] - df.loc[df['BV'] == 'Avoided intensity', 'BZ'].values[0]

    df.loc[df['BV'] == 'WACI', 'BW'] = calculate_formula_new(df, 'R', 'AA')
    df.loc[df['BV'] == 'WACI', 'BX'] = calculate_formula_new(df, 'R', 'AB')
    df.loc[df['BV'] == 'WACI', 'BY'] = calculate_formula_new(df, 'R', 'AC')
    df.loc[df['BV'] == 'WACI', 'BZ'] = calculate_formula_new(df, 'R', 'AD')

    df.loc[df['BV'] == 'WACI rel', 'BW'] = custom_formula(df.loc[df['BV'] == 'WACI', 'BW'].values[0], df.loc[df['BV'] == 'WACI', 'BZ'].values[0])
    df.loc[df['BV'] == 'WACI rel', 'BX'] = custom_formula(df.loc[df['BV'] == 'WACI', 'BX'].values[0], df.loc[df['BV'] == 'WACI', 'BZ'].values[0])
    df.loc[df['BV'] == 'WACI rel', 'BY'] = custom_formula(df.loc[df['BV'] == 'WACI', 'BY'].values[0], df.loc[df['BV'] == 'WACI', 'BZ'].values[0])
    df.loc[df['BV'] == 'WACI rel', 'BZ'] = custom_formula(df.loc[df['BV'] == 'WACI', 'BZ'].values[0], df.loc[df['BV'] == 'WACI', 'BZ'].values[0])

    df.loc[df['BV'] == '% SBTi committed', 'BW'] = calculate_formula(df, 'G', 'AA')
    df.loc[df['BV'] == '% SBTi committed', 'BX'] = calculate_formula(df, 'G', 'AB')
    df.loc[df['BV'] == '% SBTi committed', 'BY'] = calculate_formula(df, 'G', 'AC')
    df.loc[df['BV'] == '% SBTi committed', 'BZ'] = calculate_formula(df, 'G', 'AD')

    df.loc[df['BV'] == '% change through 2030', 'BW'] = calculate_formula(df, 'H', 'AA')
    df.loc[df['BV'] == '% change through 2030', 'BX'] = calculate_formula(df, 'H', 'AB')
    df.loc[df['BV'] == '% change through 2030', 'BY'] = calculate_formula(df, 'H', 'AC')
    df.loc[df['BV'] == '% change through 2030', 'BZ'] = calculate_formula(df, 'H', 'AD')

    df.loc[df['BV'] == '% change through 2030 rel', 'BW'] = df.loc[df['BV'] == '% change through 2030', 'BW'].values[0] - df.loc[df['BV'] == '% change through 2030', 'BZ'].values[0]
    df.loc[df['BV'] == '% change through 2030 rel', 'BX'] = df.loc[df['BV'] == '% change through 2030', 'BX'].values[0] - df.loc[df['BV'] == '% change through 2030', 'BZ'].values[0]
    df.loc[df['BV'] == '% change through 2030 rel', 'BY'] = df.loc[df['BV'] == '% change through 2030', 'BY'].values[0] - df.loc[df['BV'] == '% change through 2030', 'BZ'].values[0]
    df.loc[df['BV'] == '% change through 2030 rel', 'BZ'] = df.loc[df['BV'] == '% change through 2030', 'BZ'].values[0] - df.loc[df['BV'] == '% change through 2030', 'BZ'].values[0]

    df.loc[df['BV'] == 'Emissions change through 2030', 'BW'] = sumproduct(df, 'S', 'AA')
    df.loc[df['BV'] == 'Emissions change through 2030', 'BX'] = sumproduct(df, 'S', 'AB')
    df.loc[df['BV'] == 'Emissions change through 2030', 'BY'] = sumproduct(df, 'S', 'AC')
    df.loc[df['BV'] == 'Emissions change through 2030', 'BZ'] = sumproduct(df, 'S', 'AD')

    df.loc[df['BV'] == '2030 emissions change intensity', 'BW'] = calculate_formula(df, 'T', 'AA')
    df.loc[df['BV'] == '2030 emissions change intensity', 'BX'] = calculate_formula(df, 'T', 'AB')
    df.loc[df['BV'] == '2030 emissions change intensity', 'BY'] = calculate_formula(df, 'T', 'AC')
    df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'] = calculate_formula(df, 'T', 'AD')

    df.loc[df['BV'] == '2030 emissions change intensity rel', 'BW'] = df.loc[df['BV'] == '2030 emissions change intensity', 'BW'].values[0] - df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'].values[0]
    df.loc[df['BV'] == '2030 emissions change intensity rel', 'BX'] = df.loc[df['BV'] == '2030 emissions change intensity', 'BX'].values[0] - df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'].values[0]
    df.loc[df['BV'] == '2030 emissions change intensity rel', 'BY'] = df.loc[df['BV'] == '2030 emissions change intensity', 'BY'].values[0] - df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'].values[0]
    df.loc[df['BV'] == '2030 emissions change intensity rel', 'BZ'] = df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'].values[0] - df.loc[df['BV'] == '2030 emissions change intensity', 'BZ'].values[0]
    print(df[['BV', 'BW', 'BX', 'BY', 'BZ']].head(12))
    return df


def calculation_prtfolio(df=None, portfolios=None):
    current_column_index = 1  # Індекс для відстеження поточної назви колонки
    columns = [f"POR{i}" for i in range(1, len(portfolios) + 1)]
    last_column = columns[-1]
    for portfolio_df in portfolios:
        # Очищаємо дані в кожному DataFrame
        portfolio_df = portfolio_df.dropna(subset=['ISIN', 'Weight'], how='all')
        portfolio_df['ISIN'] = portfolio_df['ISIN'].str.strip()

        # Додаємо нову колонку до основного DataFrame, маплячи по 'ISIN'
        new_column_name = f'POR{current_column_index}'
        # print(new_column_name)
        df[new_column_name] = df['A'].map(portfolio_df.set_index('ISIN')['Weight'])

        # Переходимо до наступної колонки (наступна літера)
        current_column_index += 1
    df['N'] = df['C'].add(df['D'], fill_value=0)
    df['O'] = df['N'].add(df['E'], fill_value=0)
    df['P'] = df['N'].div(df['F'], fill_value=0).replace([float('inf'), -float('inf')], None)
    df['Q'] = df['E'].div(df['F'], fill_value=0)
    df['R'] = df['O'].div(df['F'], fill_value=0)
    df['S'] = df['N'].mul(df['H'], fill_value=0)
    df['T'] = df['S'].div(df['F'], fill_value=0)
    df['U'] = df['H'].fillna(pd.NA)
    df['V'] = df['I'].fillna(pd.NA)
    df['W'] = df['J'].fillna(pd.NA)
    df['X'] = df['K'].fillna(pd.NA)
    df['Y'] = df['L'].fillna(pd.NA)
    bv_values = [
        "WACI 12", "WACI 12 rel", "Avoided intensity", "Avoided intensity rel", "WACI", 
        "WACI rel", "% SBTi committed", "% change through 2030", "% change through 2030 rel", 
        "Emissions change through 2030", "2030 emissions change intensity", 
        "2030 emissions change intensity rel"
    ]
    # Створюємо новий DataFrame для зберігання результатів
    df2 = pd.DataFrame(index=range(len(bv_values)))  # Встановлюємо кількість рядків відповідно до bv_values
    
    # Заповнюємо BV колонку у df2
    df2['BV'] = bv_values  # Заповнюємо колонку 'BV' значеннями
    
    # Створюємо колонки у df2 для результатів обчислень
    for col in columns:
        df2[col] = None  # Створюємо нові стовпці у df2 для результатів
    
    # Обчислюємо значення для кожної колонки
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == 'WACI 12', col] = calculate_formula_new(df, 'P', col)

    for idx, col in enumerate(columns):
        if df2.loc[df2['BV'] == 'WACI 12', col].values[0] is not None and df2.loc[df2['BV'] == 'WACI 12', last_column].values[0] is not None:
            df2.loc[df2['BV'] == 'WACI 12 rel', col] = (
                df2.loc[df2['BV'] == 'WACI 12', col].values[0] - df2.loc[df2['BV'] == 'WACI 12', last_column].values[0]
            )
    for idx, col in enumerate(columns):   
        df2.loc[df2['BV'] == 'Avoided intensity', col] = calculate_formula_new_minus(df, 'Q', col)
    for idx, col in enumerate(columns):
        if df2.loc[df2['BV'] == 'Avoided intensity', col].values[0] is not None and df2.loc[df2['BV'] == 'Avoided intensity', last_column].values[0] is not None:
            df2.loc[df2['BV'] == 'Avoided intensity rel', col] = (
                df2.loc[df2['BV'] == 'Avoided intensity', col].values[0] - df2.loc[df2['BV'] == 'Avoided intensity', last_column].values[0]
            )
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == 'WACI', col] = calculate_formula_new(df, 'R', col)
    for idx, col in enumerate(columns):
        if df2.loc[df2['BV'] == 'WACI', col].values[0] is not None and df2.loc[df2['BV'] == 'WACI', last_column].values[0] is not None:
            df2.loc[df2['BV'] == 'WACI rel', col] = custom_formula(
                df2.loc[df2['BV'] == 'WACI', col].values[0], df2.loc[df2['BV'] == 'WACI', last_column].values[0]
            )
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == '% SBTi committed', col] = calculate_formula(df, 'G', col)
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == '% change through 2030', col] = calculate_formula(df, 'H', col)
        
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == 'Emissions change through 2030', col] = sumproduct(df, 'S', col)
    for idx, col in enumerate(columns):
        df2.loc[df2['BV'] == '2030 emissions change intensity', col] = calculate_formula(df, 'T', col)
    for idx, col in enumerate(columns):   
        # Перевірка перед відніманням для 'rel' показників
        if df2.loc[df2['BV'] == '2030 emissions change intensity', col].values[0] is not None and df2.loc[df2['BV'] == '2030 emissions change intensity', last_column].values[0] is not None:
            df2.loc[df2['BV'] == '2030 emissions change intensity rel', col] = (
                df2.loc[df2['BV'] == '2030 emissions change intensity', col].values[0] - df2.loc[df2['BV'] == '2030 emissions change intensity', last_column].values[0]
            )
    for idx, col in enumerate(columns):
        if df2.loc[df2['BV'] == '% change through 2030', col].values[0] is not None and df2.loc[df2['BV'] == '% change through 2030', last_column].values[0] is not None:
            df2.loc[df2['BV'] == '% change through 2030 rel', col] = (
                df2.loc[df2['BV'] == '% change through 2030', col].values[0] - df2.loc[df2['BV'] == '% change through 2030', last_column].values[0]
            )
    print('.'*50)
    print(df2.head(12))  # Виводимо результат для перегляду
    print('.'*50)
    return df2, df, columns
def prepare_data_for_response(df2, names):
    result = []

    # Перевіряємо, чи маємо достатньо імен у списку
    if len(names) != len(df2.columns) - 1:
        raise ValueError("Кількість імен має відповідати кількості стовпців у DataFrame.")

    # Витягуємо рядки для 'WACI rel' і '% change through 2030 rel'
    waci_rel_row = df2.loc[df2['BV'] == 'WACI rel']
    change_2030_rel_row = df2.loc[df2['BV'] == '% change through 2030 rel']

    # Перебираємо всі колонки (крім 'BV'), витягуємо значення X і Y
    for idx, col in enumerate(df2.columns[1:]):  # Пропускаємо колонку 'BV'
        x_value = change_2030_rel_row[col].values[0] if not pd.isna(change_2030_rel_row[col].values[0]) else None
        y_value = waci_rel_row[col].values[0] if not pd.isna(waci_rel_row[col].values[0]) else None
        
        # Перетворюємо np.float64 в стандартний float
        x_value = float(x_value) if isinstance(x_value, np.float64) else x_value
        y_value = float(y_value) if isinstance(y_value, np.float64) else y_value
        # Якщо x_value не None, перетворюємо його у відсотки і округлюємо до 1 знака після коми
        if x_value is not None:
            x_value = round(x_value * 100, 1)
        
        result.append({
            'x': x_value,
            'y': y_value,
            'text': names[idx]
        })

    return result
def convert_to_json_ready(value):
    """Функція для конвертації значень у формат, готовий до JSON."""
    if isinstance(value, np.float64):
        return float(value)  # Конвертуємо np.float64 у стандартний float
    return value

def waterfall_chunk(df=None, portfolio_name=None, reference_name=None):
    print(df.head())
    print(df.columns)
    print(f"portfolio_name: {portfolio_name}")
    print(f"reference_name: {reference_name}")
    af_values = [
        portfolio_name,
        # "SMFE",
        # "B&M 18-32",
        reference_name,
        "Portfolio relative",
        
        "Reference S12",
        "Reference avoided emissions",
        "Reference total",
        
        "Portfolio S12",
        "Portfolio avoided emissions",
        "Portfolio reduction",
        
        "Portfolio 2030",
        
        "Reference S12_a",
        "Reference avoided emissions_a",
        "Reference total_a",
        
        "Portfolio S12_b",
        "Portfolio avoided emissions_b",
        "Portfolio reduction_b",
        
        "Portfolio 2030_c"
    ]
    df['AF'] = None
    df.iloc[0:0+len(af_values), df.columns.get_loc('AF')] = af_values
    #
    columns_to_calculate = ['AH', 'AI', 'AJ']
    base_columns = ['Q', 'R', 'T']

    df.loc[df['AF'] == portfolio_name, 'AG'] = calculate_formula_new(df, 'P', portfolio_name)
    df.loc[df['AF'] == reference_name, 'AG'] = calculate_formula_new(df, 'P', reference_name)
    
    for col_base, col_target in zip(base_columns, columns_to_calculate):
        print(f"col_target: {col_target}")
        print(f"col_base: {col_base}")
        df[col_target] = None
        # print('-'*50)
        # print(col_base)
        # print(portfolio_name)
        # print(calculate_formula_new(df, col_base, portfolio_name))
        df.loc[df['AF'] == portfolio_name, col_target] = calculate_formula(df, col_base, portfolio_name)
        # print(calculate_formula_new(df, col_base, reference_name))
        df.loc[df['AF'] == reference_name, col_target] = calculate_formula(df, col_base, reference_name)
        # print('-'*50)
    # print(df[columns_to_calculate])
    #
    # df = automated_calculation(df=df, portfolio_name=portfolio_name, reference_name=reference_name)
    relative_columns_to_calculate = ["AG", "AH", "AI", "AJ"]

    for column in relative_columns_to_calculate:
        df.loc[df['AF'] == 'Portfolio relative', column] = calculate_relative_difference(df, column, portfolio_name, reference_name)

    df.loc[df['AF'] == 'Reference S12', 'AG'] = df.loc[df['AF'] == reference_name, 'AG'].values[0]
    df.loc[df['AF'] == 'Reference avoided emissions', 'AG'] = df.loc[df['AF'] == reference_name, 'AH'].values[0]
    df.loc[df['AF'] == 'Reference total', 'AG'] = (
        df.loc[df['AF'] == 'Reference S12', 'AG'].values[0] +
        df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    )

    # df.loc[df['AF'] == 'Portfolio S12', 'AG'] = calculate_relative_difference(df, 'AG', 'GET', 'MSCI ACWI IMI')
    df.loc[df['AF'] == 'Portfolio S12', 'AG'] = calculate_relative_difference(df, 'AG', portfolio_name, reference_name)
    df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'] = df.loc[df['AF'] == portfolio_name, 'AH'].values[0] - df.loc[df['AF'] == reference_name, 'AH'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction', 'AG'] = df.loc[df['AF'] == portfolio_name, 'AJ'].values[0] - df.loc[df['AF'] == reference_name, 'AJ'].values[0]
    df.loc[df['AF'] == 'Portfolio 2030', 'AG'] = df.loc[df['AF'] == 'Reference total', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio reduction', 'AG'].values[0]

    df.loc[df['AF'] == 'Reference S12_a', 'AG'] = df.loc[df['AF'] == 'Reference S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Reference avoided emissions_a', 'AG'] = df.loc[df['AF'] == 'Reference S12', 'AG'].values[0] + df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Reference total_a', 'AG'] = df.loc[df['AF'] == 'Reference avoided emissions_a', 'AG'].values[0]

    df.loc[df['AF'] == 'Portfolio S12_b', 'AG'] = df.loc[df['AF'] == 'Reference total_a', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AG'] = df.loc[df['AF'] == 'Portfolio S12_b', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction_b', 'AG'] = df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio 2030_c', 'AG'] = df.loc[df['AF'] == 'Portfolio 2030', 'AG'].values[0]


    df.loc[df['AF'] == 'Reference avoided emissions_a', 'AH'] = - df.loc[df['AF'] == 'Reference avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio S12_b', 'AH'] = - df.loc[df['AF'] == 'Portfolio S12', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AH'] = df.loc[df['AF'] == 'Portfolio avoided emissions_b', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio avoided emissions', 'AG'].values[0]
    df.loc[df['AF'] == 'Portfolio reduction_b', 'AH'] = df.loc[df['AF'] == 'Portfolio reduction_b', 'AG'].values[0] + df.loc[df['AF'] == 'Portfolio reduction', 'AG'].values[0]
    print("#"*50)
    print(df[['AF', 'AG', 'AH', "AI", "AJ"]].head(20))
    print("#"*50)
    # Створюємо словник для результатів
    result = []


    for row_title in ['Portfolio S12_b', 'Portfolio avoided emissions_b', 'Portfolio reduction_b', 'Portfolio 2030_c', 'Reference avoided emissions_a', 'Reference S12_a', 'Reference total_a']:
        ag_value = df.loc[df['AF'] == row_title, 'AG'].values[0] if not df.loc[df['AF'] == row_title, 'AG'].isna().values[0] else None
        ah_value = df.loc[df['AF'] == row_title, 'AH'].values[0] if not df.loc[df['AF'] == row_title, 'AH'].isna().values[0] else None

        # Конвертуємо значення у формат, готовий для JSON
        result.append({
            "title": row_title.split("_")[0],
            "AG": convert_to_json_ready(ag_value),
            "AH": convert_to_json_ready(ah_value)
        })

    return result

def calculation_waterfall(df=None, columns=None):
    order = [
        "Reference S12",
        "Reference avoided emissions",
        "Reference total",
        "Portfolio S12",
        "Portfolio avoided emissions",
        "Portfolio reduction",
        "Portfolio 2030"
    ]
    last_column = columns[-1]
    output_list = []
    for obj in columns[:-1]:
        single = waterfall_chunk(df=df, portfolio_name=obj, reference_name=last_column)
        sorted_data = sorted(single, key=lambda x: order.index(x['title']))
        output_list.append(sorted_data)
    return output_list

def transform_data_for_multiple_series(data_lists):
    result = []
    
    # Перевіряємо, що всі лістові мають однакову кількість рядків і категорій
    if not all(len(data_list) == len(data_lists[0]) for data_list in data_lists):
        raise ValueError("Всі списки даних мають мати однакову кількість рядків.")

    previous_close = 0  # Ініціалізуємо попереднє значення `close` як 0

    for idx in range(len(data_lists[0])):  # Проходимо по кількості рядків
        category = data_lists[0][idx]['title']  # Витягуємо назву категорії
        row_data = {
            'category': category
        }
        
        # Обробляємо кожен ліст (серію даних)
        for series_idx, data_list in enumerate(data_lists):
            open_key = f'open{series_idx + 1}'  # Динамічно генеруємо ключ для open
            close_key = f'close{series_idx + 1}'  # Динамічно генеруємо ключ для close
            
            ag_value = data_list[idx]['AG'] if data_list[idx]['AG'] is not None else 0
            ah_value = data_list[idx]['AH'] if data_list[idx]['AH'] is not None else None
            
            if ah_value is None:
                # Якщо `AH` відсутнє, `open` = 0, `close` = `AG`
                row_data[open_key] = 0
                row_data[close_key] = ag_value
            else:
                # Якщо є `AH`, то `open` = попереднє значення `close`, а `close` = AG - AH
                row_data[open_key] = ag_value
                # row_data[close_key] = ag_value - ah_value
                row_data[close_key] = ag_value + ah_value
            
            # Оновлюємо `previous_close` для наступного ряду
            previous_close = row_data[close_key]

        result.append(row_data)
    result.insert(3, {})
    result.insert(7, {})
    return result
