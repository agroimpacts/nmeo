# implementation biological basics like thermal time

def GDD(df, Tlo=10., Thi=44., method='I', **kwargs):
    """
    Wrapper for daily thermal time (GDD) calculations
    Method I: takes sub-daily resolved data (eg from Mark)
    Method II: takes daily max/min data (eg from ERA, GFS)
    Method III: takes daily avg + range data (eg from NMME) 
    
    kwargs is used to rename column name for Tmax, Tmin, Tair, Tavg
    """
    
    if method=='I':
        # Note, takes sub-daily and returns daily df
        df = GDD_I(df, Tlo, Thi, **kwargs)
    elif method=='II':
        df = GDD_II(df, Tlo, Thi, **kwargs)
    elif method=='III':
        df = GDD_III(df, Tlo, Thi, **kwargs)
    elif method=='IV':
        df = GDD_IV(df, Tlo, **kwargs)
    else:
        # error: must use a method
        return df
        
    return df.V.tolist()
        
def GDD_I(df, Tlo=10., Thi=44., **kwargs):
    """
    Method I: Takes T and aggregates by day
    
    expects T to be in a dataframe that has a time index and the name of T as 'Tair'
    
    takes kwargs Tcol
    
    # Note, takes sub-daily and returns daily df
    
    """
    import pandas as pd
    from numpy import max, min
    
    if 'Tcol' in kwargs:
        Tval = kwargs['Tcol']
    else:
        Tval = 'Tair'

    df['V'] = max(min(df[Tval], Thi), Tlo)
    
    # handles data hourly, 3 hourly, 6 hourly or irregular
    df = df.resample('60T').mean()
    df = df.groupby(pd.Grouper(freq='D')).mean()
    
    return df
    
    
def GDD_II(df, Tlo=10., Thi=44., **kwargs):
    """
    Method II: Takes one Tmin, Tmax per day
    
    Compute degree days using single sin method and horizontal cutoff
    
    Takes account of 6 cases:    
    1. Above both thresholds.
    2. Below both thresholds.
    3. Between both thresholds.
    4. Intercepted by the lower threshold.
    5. Intercepted by the upper threshold.
    6. Intercepted by both thresholds.
    
    cases 4-6 assume a form that includes a
    LEFT half (positive sin from 0 to pi added to Tavg-Tlo)
    RIGHT half (negative sin from pi to 2pi)
    for the purposes of this calculation, a day is 2*pi long
    
    takes kwargs Tmaxcol and Tmincol
    
    Example invocation with kwargs to rename columns:
    df = GDD_II(df, Tlo=10, Tmaxcol='Tmx', Tmincol='Tmn')
    
    """
    import numpy as np
    import pandas as pd
    from numpy import cos, arcsin, pi
    import warnings
    
    warnings.simplefilter("ignore")
    
    if 'Tmincol' in kwargs:
        Tmin = kwargs['Tmincol']
    else:
        Tmin = 'Tmin'
        
    if 'Tmaxcol' in kwargs:
        Tmax = kwargs['Tmaxcol']
    else:
        Tmax = 'Tmax'
        

    twopi = 2*pi
    
    case = np.zeros(len(df))
    case[(df[Tmax] <  Thi) & (df[Tmin] >= Tlo)] = 3
    case[(df[Tmax] <  Thi) & (df[Tmin] <  Tlo)] = 4
    case[(df[Tmax] >= Thi) & (df[Tmin] >= Tlo)] = 5
    case[(df[Tmax] >= Thi) & (df[Tmin] <  Tlo)] = 6
    case[df[Tmin] >= Thi] = 1
    case[df[Tmax] <  Tlo] = 2
    
    df['debug'] = case

    Tavg = (df[Tmax]+df[Tmin])/2.
    a = (df[Tmax]-df[Tmin])/2. # half amplitude of sin
    b = (Tavg-Tlo)     # offset of sin from Tlo
    c = (Thi - Tavg)

    df['V'] = 0.
    case3_temp = np.where(case==3, Tavg-Tlo, 0)
    df.loc[df.debug == 3, 'V'] = case3_temp[case3_temp != 0]
    
    # df.V.loc[case == 1] = 0.
    # df.V.loc[case == 2] = 0.
    # df.V.loc[case == 3] = Tavg - Tlo
    
    # if out-of-case, the arcsin arguments are guaranteed to cause a warning
    warnings.simplefilter("ignore")
    
    # Case 4
    LEFT = (pi*b + 2*a)/twopi
    tao = pi+arcsin(b/a)
    RIGHT = 2*((tao-pi)*b + a*(cos(pi) - cos(tao)))/twopi
    left_right4 = np.where(case==4, LEFT + RIGHT, 0)
    df.loc[left_right4 != 0, 'V'] = left_right4[left_right4 != 0]
    # df.V.loc[case == 4] = LEFT + RIGHT
    
    # Case 5
    tao2 = arcsin(c/a)
    LEFT = ((pi-2*tao2)*c + pi*b + 2*a*(1-cos(tao2)))/twopi
    RIGHT = (pi*b - 2*a)/twopi
    left_right5 = np.where(case==5, LEFT + RIGHT, 0)
    df.loc[df.debug == 5, 'V'] = left_right5[left_right5 != 0]
    # df.V[case == 5] = LEFT + RIGHT
    
    # Case 6
    tao2 = arcsin(c/a)
    LEFT = ((pi-2*tao2)*c + pi*b + 2*a*(1-cos(tao2)))/twopi
    tao = pi+arcsin(b/a)
    RIGHT = 2*((tao-pi)*b + a*(cos(pi) - cos(tao)))/twopi
    left_right6 = np.where(case==6, LEFT + RIGHT, 0)
    df.loc[df.debug == 6, 'V'] = left_right6[left_right6 != 0]
    # df.V[case == 6] = LEFT + RIGHT
    
    warnings.resetwarnings()
    
    return df

def GDD_III(df, Tlo=10., Thi=44., **kwargs):
    """
    Method III: Takes Tavg and diurnal T range (DTR) to compute Tmin, Tmax
    
    takes kwargs Tavgcol and DTRcol
    
    Invokes Method II
    """
    
    import pandas as pd
    from numpy import cos, arcsin, pi
    import warnings
    
    if 'Tavgcol' in kwargs:
        Tavg = kwargs['Tavgcol']
    else:
        Tavg = 'Tavg'
        
    if 'DTRcol' in kwargs:
        DTR = kwargs['DTRcol']
    else:
        DTR = 'DTR'
    
    df['Tmax'] = df.Tavg + df.DTR/2.
    df['Tmin'] = df.Tavg - df.DTR/2.
    
    df = GDD_II(df, Tlo=10., Thi=44., **kwargs)
    
    return df

def GDD_IV(df, Tlo=10., **kwargs):
    """
    Method IV: Simple average minus base, no upper limit allowed
    
    takes kwargs Tcol
    
    
    """
    import pandas as pd
    from numpy import max, min
    
    if 'Tmincol' in kwargs:
        Tmin = kwargs['Tmincol']
    else:
        Tmin = 'Tmin'
        
    if 'Tmaxcol' in kwargs:
        Tmax = kwargs['Tmaxcol']
    else:
        Tmax = 'Tmax'

    df['V'] = (df[Tmax] + df[Tmin])/2.0 - Tlo
    df[df.V < 0] = 0
        
    return df
