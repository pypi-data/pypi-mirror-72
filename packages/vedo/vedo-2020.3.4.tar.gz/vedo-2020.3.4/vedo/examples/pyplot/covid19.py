import numpy as np
import sys, datetime
import pandas as pd

# ----------------------------------------------------------------------
def load_data():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'

    if len(sys.argv)>1:
        date = sys.argv[1]
    else:
        for i in range(10):
            try:
                yesterday = datetime.datetime.now() - datetime.timedelta(days=i)
                date = yesterday.strftime("%m-%d-%Y")
                csvdata = pd.read_csv(url+'/csse_covid_19_daily_reports/'+date+'.csv')
                break
            except:
                continue
    data = []
    conf_us, reco_us, deat_us = 0,0,0
    for i, row in csvdata.iterrows():
        theta = -row['Lat']  /57.3+np.pi/2
        phi   =  row['Long_']/57.3+np.pi
        if np.isnan(theta): continue
        confirmed, deaths, recos = row['Confirmed'], row['Deaths'], row['Recovered']
        Admin, Province, Country = row['Admin2'], row['Province_State'], row['Country_Region'],
        if not deaths: continue
        if Country == 'US':  # group US data
            conf_us += confirmed
            deat_us += deaths
            reco_us += recos
            continue
        else:
            place = ''
            if Admin is not np.nan:    place += Admin+'\n'
            if Province is not np.nan: place += Province+'\n'
            if Country is not np.nan:  place += Country+'\n'
        data.append([place, theta, phi, confirmed, deaths, recos])
    data.append(['US\n', 0.9, 1.4, conf_us, deat_us, reco_us])
    return (date, data, csvdata['Confirmed'].sum(),
            csvdata['Deaths'].sum(), csvdata['Recovered'].sum())


# -------------------------------------------------------------------------
# Create the scene:
from vedo import *

date, data, allconf, alldeat, allreco = load_data()
for place, theta, phi, confd, deaths, recos in data:
    pos = spher2cart(1, theta, phi)
    fl = place + 'cases: '+str(confd)+'\ndeaths: '+str(deaths)
    Sphere(pos, np.power(confd,  1/3)/1500, alpha=0.4, res=12).flag(fl)
    Sphere(pos, np.power(deaths, 1/3)/1500, alpha=0.4, c='k', res=10)

Text2D('COVID-19 spread on '+date
        +'\n#cases : '+str(allconf)
        +'\n#deaths: '+str(alldeat)
        +'\n#recovd: '+str(allreco),
        font="Overspray", s=0.9)
Earth()
show(..., axes=12, bg2='lb', zoom=1.7, elevation=-70, size='fullscreen')

