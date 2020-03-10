import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

def rename_wx_daily_for_merge(df):
    df = df.rename(columns={
        'date': 'date',
        'Tmin': 'Tmin_twc',
        'Tmax': 'Tmax_twc',
        'Tavg': 'Tavg_twc',
        'RH_min': 'RH_min_twc',
        'RH_max': 'RH_max_twc',
        'P': 'P_twc',
        'SLP': 'SLP_twc',
        'U': 'U_twc',
        'Udir': 'Udir_twc',
        'Precip_1d': 'Precip_1d_twc',
        'SWdw_sum': 'SWdw_sum_twc',
        'ETo_sum': 'ETo_sum_twc'
    })
    
    return df