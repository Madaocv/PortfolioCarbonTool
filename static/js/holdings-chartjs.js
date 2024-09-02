const data = {
    labels: [
        'Nextracker Inc', 'Solaria Energia y Medio Ambiente, S.A.', 'OX2 AB (publ)', 
        'ENPHASE ENERGY, INC.', 'Alfen NV', 'CORPORACION ACCIONA ENERGIAS RENOVABLES SA', 
        'ARRAY TECHNOLOGIES, INC.', 'EDP Renovaveis, S.A.', 'Sungrow Power Supply Co., Ltd.', 
        'NEOEN SA', 'SOLAREDGE TECHNOLOGIES, INC.', 'VESTAS WIND SYSTEMS A/S', 
        'ITRON, INC.', 'SCHNEIDER ELECTRIC SE', 'Landis+Gyr Group AG', 
        'Shoals Technologies Group Inc', 'LEGRAND SA', 'SMA Solar Technology AG', 
        'INDUSTRIE DE NORA S.P.A.', 'Nordex SE', 'VOLTALIA SA', 'HYDRO ONE LIMITED', 
        'STEM, INC.', 'JOHNSON CONTROLS INTERNATIONAL PLC', 'Fluence Energy Inc', 
        'SPIE SA', 'FIRST SOLAR, INC.', 'Contemporary Amperex Technology Co., Ltd.', 
        'ORMAT TECHNOLOGIES, INC.', 'MASTEC, INC.', 'Ariston Holding N.V.', 
        'FORVIA SE', 'Signify N.V.', 'REDEIA CORPORACION, S.A.', 'NEXANS SA', 
        'SAMSUNG SDI CO., LTD.', 'ELIA GROUP SA', 'JOHNSON MATTHEY PLC', 
        'Gurit Holding AG', 'UMICORE SA', 'COMPAGNIE PLASTIC OMNIUM SE', 
        'Sif Holding N.V.', 'DEME GROUP NV', 'LG CHEM LTD', 'Wacker Chemie AG'
    ],
    datasets: [{
        label: 'Scatter Plot',
        data: [
            {x: -76.13935698, y: 8.255768293},
            {x: -76.10528032, y: 8.232982448},
            {x: -76.08568612, y: 8.263939185},
            {x: -75.63419241, y: 8.255768293},
            {x: -75.57344927, y: 8.255768293},
            {x: -75.56337382, y: 7.704648558},
            {x: -75.45931492, y: 8.255768293},
            {x: -75.16829311, y: 7.965298216},
            {x: -74.18828859, y: 8.255768293},
            {x: -73.71505513, y: 8.255768293},
            {x: -73.65519195, y: 8.442520119},
            {x: -73.38539493, y: 7.745119061},
            {x: -72.70352611, y: 8.519348773},
            {x: -72.20611959, y: 8.146691203},
            {x: -72.2039764, y: 6.226267928},
            {x: -71.75121094, y: 8.255768293},
            {x: -71.58498334, y: 7.344192048},
            {x: -68.21317886, y: 8.730979396},
            {x: -67.67248096, y: 8.255768293},
            {x: -67.65396755, y: 5.567882294},
            {x: -66.414741, y: 8.255768293},
            {x: -65.78658197, y: 8.255768293},
            {x: -64.76345192, y: 8.255768293},
            {x: -60.59958488, y: 8.563222623},
            {x: -60.59759513, y: 8.255768293},
            {x: -59.89188398, y: 9.449072845},
            {x: -56.63005023, y: 1.979046912},
            {x: -51.78276439, y: 8.255768293},
            {x: -47.18726408, y: 8.255768293},
            {x: -46.84275609, y: 8.255768293},
            {x: -44.93369699, y: -0.885584034},
            {x: -37.50635314, y: -30.42281695},
            {x: -35.66736662, y: -15.28197427},
            {x: -27.71907875, y: -7.260995097},
            {x: -27.39848046, y: 7.32496544},
            {x: -21.00090598, y: 11.45318168},
            {x: -18.55819334, y: -2.429323794},
            {x: -9.347318763, y: 4.370580535},
            {x: -6.785252873, y: 8.255768293},
            {x: -5.481676292, y: 9.648197616},
            {x: 5.971138979, y: 3.55225503},
            {x: 76.99519941, y: 8.255768293},
            {x: 80.54734943, y: 8.255768293},
            {x: 109.3048168, y: 17.97542363},
            {x: 248.5449476, y: -87.6305008},
            {x: 452.9421889, y: 8.255768293}
        ],
        backgroundColor: 'rgba(75, 192, 192, 1)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        showLine: false // важливо для відображення лише точок без ліній
    }]
};

// config 
const config = {
    type: 'scatter',
    data: data,
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
            },
            y: {
                beginAtZero: true,
            }
        },
        plugins: {
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'xy',
                },
                zoom: {
                    wheel.enabled: true,
                    mode: 'xy',
                }
            },
            legend: {
                display: false // вимикає відображення легенди
            }
        }
    }
};

// render init block
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);