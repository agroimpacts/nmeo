# arable_physics
# operands are prefixed with x to distinguish them from variables and functions
# used elsewhere function defs are suffixed with _ to distinguish them from
# variables and functions used elsewhere

##AW Changes
# added constants to physics
# changed math ops to numpy for array-safe operations
# changed to use Datetime library appropriately
# changed to use UTC time not local time, chiefly in solar_utc_ and solar_theta
# added equation of time correction to adjustment to mean solar noon
# Solar delta now uses two args, not one
# removed rain intensity, I don't know where it came from and its not in production
# added SWP calculation

import calendar

from numpy import pi, log, exp, sin, cos, tan, arcsin, arccos, arctan2
import numpy as np
import pandas as pd

# Physical constants

Mh2o = 18  # molecular weight of water: g/mol
Mco2 = 44  # molecular weight of CO2: g/mol
Mair = 29  # molecular weight of dry air: g/mol
R = 8.314  # gas constant: J / mol k gas constant
Cp = 1004.67  # specific heat per mass: J / kg air / k
Cp_mol = Cp / 1000 * Mair  # specific heat per mol: J / mol air / k
P = 101.325  # sea level pressure: kPa
SBC = 5.67e-8  # Stefan-Boltzman Const
g = 9.80665  # gravitational acceleration constant m/s^2
SUN = 1367.0  # Solar Constant W/m2
VIS = 600.0  # Solar energy 400-700nm: W/m2 (0.45)
NIR = 720.0  # Solar energy 700-3000nm: W/m2 (0.54)

k = 0.41  # von Karman's Konstant

seconds_per_day = 86400.

eot = np.array([
-3.4,-3.9,-4.4,-4.8,-5.3,-5.7,-6.2,-6.6,-7.0,-7.4,-7.8,-8.2,-8.6,-8.9,-9.3,-9.7,-10.0,-10.3,-10.6,-10.9,-11.2,-11.5,-11.8,-12.0,-12.2,-12.5,-12.7,-12.9,-13.1,-13.2,-13.4,-13.5,-13.7,-13.8,-13.9,-14.0,-14.0,-14.1,-14.1,-14.2,-14.2,-14.2,-14.2,-14.2,-14.2,-14.1,-14.1,-14.0,-13.9,-13.8,-13.7,-13.6,-13.5,-13.4,-13.2,-13.1,-12.9,-12.7,-12.6,-12.4,-12.2,-12.0,-11.8,-11.5,-11.3,-11.1,-10.8,-10.6,-10.3,-10.1,-9.8,-9.5,-9.3,-9.0,-8.7,-8.4,-8.1,-7.8,-7.5,-7.2,-6.9,-6.6,-6.3,-6.0,-5.7,-5.4,-5.1,-4.8,-4.5,-4.2,-3.9,-3.7,-3.4,-3.1,-2.8,-2.5,-2.2,-1.9,-1.7,-1.4,-1.1,-0.8,-0.6,-0.3,-0.1,0.1,0.4,0.6,0.8,1.0,1.3,1.5,1.6,1.8,2.0,2.2,2.3,2.5,2.6,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.4,3.5,3.6,3.6,3.6,3.7,3.7,3.7,3.7,3.7,3.6,3.6,3.6,3.5,3.4,3.4,3.3,3.2,3.1,3.0,2.9,2.8,2.6,2.5,2.4,2.2,2.1,1.9,1.7,1.6,1.4,1.2,1.0,0.8,0.6,0.4,0.2,0.0,-0.2,-0.4,-0.6,-0.8,-1.1,-1.3,-1.5,-1.7,-1.9,-2.1,-2.4,-2.6,-2.8,-3.0,-3.2,-3.4,-3.6,-3.8,-4.0,-4.2,-4.4,-4.5,-4.7,-4.9,-5.0,-5.2,-5.3,-5.5,-5.6,-5.7,-5.8,-5.9,-6.0,-6.1,-6.2,-6.3,-6.3,-6.4,-6.4,-6.5,-6.5,-6.5,-6.5,-6.5,-6.5,-6.5,-6.5,-6.4,-6.4,-6.3,-6.2,-6.1,-6.0,-5.9,-5.8,-5.7,-5.5,-5.4,-5.2,-5.1,-4.9,-4.7,-4.5,-4.3,-4.1,-3.9,-3.7,-3.4,-3.2,-3.0,-2.7,-2.4,-2.2,-1.9,-1.6,-1.3,-1.0,-0.7,-0.4,-0.1,0.2,0.6,0.9,1.2,1.6,1.9,2.2,2.6,2.9,3.3,3.6,4.0,4.3,4.7,5.1,5.4,5.8,6.1,6.5,6.8,7.2,7.5,7.9,8.2,8.6,8.9,9.3,9.6,9.9,10.2,10.6,10.9,11.2,11.5,11.8,12.1,12.4,12.7,12.9,13.2,13.5,13.7,13.9,14.2,14.4,14.6,14.8,15.0,15.2,15.3,15.5,15.6,15.8,15.9,16.0,16.1,16.2,16.3,16.3,16.4,16.4,16.4,16.4,16.4,16.4,16.4,16.3,16.3,16.2,16.1,16.0,15.9,15.8,15.6,15.5,15.3,15.1,14.9,14.7,14.4,14.2,13.9,13.7,13.4,13.1,12.8,12.5,12.1,11.8,11.4,11.1,10.7,10.3,9.9,9.5,9.1,8.7,8.2,7.8,7.4,6.9,6.4,6.0,5.5,5.0,4.5,4.0,3.6,3.1,2.6,2.1,1.6,1.1,0.6,0.1,-0.4,-0.9,-1.4,-1.9,-2.4,-2.9,-3.1
])

# General utility functions

def doy_(xDatetime):
    doy = xDatetime.dayofyear
    dayfrac = ((xDatetime.hour)*3600. + (xDatetime.minute)*60 + xDatetime.second) / seconds_per_day
    return doy+dayfrac

# Static properties of air

def Tk_(xT):  # pragma: no cover
    """

    :param xT - temperature (C):
    :return:
    """
    return xT + 273.2


def lambda_(xTk):  # pragma: no cover
    """ latent heat of vaporization: J / g

    :param xTk - temperature (K):
    :return:
    """
    return 3149 - 2.370 * xTk


def lambda_mol_(xTk):  # pragma: no cover
    """ latent heat of vaporization: J / mol

    :param xTk - temperature (C):
    :return:
    """
    return lambda_(xTk) * Mh2o


def esat_(xT):  # pragma: no cover
    """ saturation vapor pressure: kPa
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (617.4 + 42.22 * xT + 1.675 * xT ** 2 + 0.01408 * xT ** 3 +
            0.0005818 * xT ** 4) / 1000  # Paw U formulation


def ea_(xT, xRH):
    """vapor pressure: kPa 
    
    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT)*xRH


def tdew(xT, xRH):
    """ Dewpoint temperature: C
         Eqn from Allen FAO 56
    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:    
    """
    ea = ea_(xT, xRH)
    return (116.91+237.3*log(ea)) / (16.78 - log(ea))


def s_(xT):  # pragma: no cover
    """ derivative of saturation vapor pressure: kPa / C
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (42.22 + 2 * 1.675 * xT + 3 * 0.01408 * xT ** 2 +
            4 * 0.0005818 * xT ** 3) / 1000  # Paw U formulation


def dsdT_(xT):  # pragma: no cover
    """ second derivative of saturation vapor pressure: kPa / C^2
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (2.0 * 1.675 + 6 * 0.01408 * xT + 12.0 * 0.0005818 * xT ** 2) / 1000.0  # NOQA


def ea_(xT, xRH):  # pragma: no cover
    """ vapor pressure: kPa

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT) * xRH


def VPD_(xT, xRH):  # pragma: no cover
    """ vapor pressure deficit: kPa

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT) * (1.0 - xRH)


def dry_air_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of dry air: kg / m3   (n/V = P/RT)

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    ea = ea_(xT, xRH)
    return ((xP - ea) * Mair) / (R * Tk_(xT))


def air_h2o_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of water in air: gH2O / m3

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    ea = ea_(xT, xRH)
    return (ea / xP) * 622.0 * dry_air_(xT, xRH)


def dry_air_mol_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of dry air: mol / m3

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    return dry_air_(xT, xRH, xP) * 1000.0 / Mair


def moist_air_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of moist air: kg / m3

    :param xT:
    :param xRH:
    :param xP:
    :return:
    """
    return dry_air_(xT, xRH, xP) + air_h2o_(xT, xRH, xP) / 1000.0


def gamma_(xT, xP=P):  # pragma: no cover
    """ psychrometric constant kPa / C

    :param xT - temperature (C):
    :param xP - pressure (kPa):
    :return:
    """
    return Cp_mol / lambda_mol_(Tk_(xT)) * xP


def Tbb_(xLW):  # pragma: no cover
    """ effective blackbody temperature

    :param xLW - Longwave radiation (W/m2):
    :return:
    """
    return (xLW / SBC) ** (0.25) - 273.2


def LWbb_(xT):  # pragma: no cover
    """ Stefan Boltzman equation: W/m2

    :param xT - temperature (C):
    :return:
    """
    return SBC * (Tk_(xT) ** 4)


# Radiation and Solar energy

def solar_phi_(xLat):  # pragma: no cover
    """ Latitude in radians pi/2 at the poles, 0 at the equator

    :param xLat - Latitude (decimal degree):
    :return:
    """
    return xLat * pi / 180.0


def solar_utc_offset_(xDatetime, xLon):  # pragma: no cover
    """ difference between solar time and utc time, in fractions of a day

    :param xDatetime:
    :param xLon:
    :return:
    """  

    dayfrac = ((xDatetime.hour)*3600. + (xDatetime.minute)*60 + xDatetime.second) / seconds_per_day
    solar_utc_offset = xLon / 360.0 + eot[xDatetime.dayofyear-1]/1440. # fractions of day, ranging from -0.5 to +0.5
    
    return  dayfrac + solar_utc_offset

def solar_noon_(xDatetime, xLon, datetime=True):
    """ difference between solar time and utc time, in fractions of a day

    :param xDatetime:
    :param xLon:
    :return: datetime or decimal day
    """                  
    solar_noon_offset = 0.5 - (xLon / 360.0 + eot[xDatetime.dayofyear-1]/1440.)
    
    td = pd.to_timedelta(solar_noon_offset, unit = 'd')#.to_pytimedelta()
    
    if (datetime):
        solar_noon = xDatetime.normalize() + td
    else:
        solar_noon = xDatetime.dayofyear + solar_noon_offset
        
    return solar_noon

def solar_delta_(xDatetime, xLon):  # pragma: no cover
    """ declination angle, varying over the year

    :param xDatetime:
    :return:
    """
    tropic = 23.45 * pi / 180.0
    leap = (xDatetime.year % 4 == 0) | (xDatetime.year % 100 == 0)
    yearl = np.ones((xDatetime.year.size)) * 365. + leap
    equinox = np.ones((xDatetime.year.size)) * 173. + leap
    solar_utc_offset = solar_utc_offset_(xDatetime, xLon)
    fdoy = (xDatetime.dayofyear - equinox + solar_utc_offset) / yearl # fractions of year
    return tropic * cos(2.0 * pi * fdoy)


def solar_theta_(xDatetime, xLon):  # pragma: no cover
    """ hour angle, the fraction of a full rotation has turned after local solar noon 
        cos(theta) is 1 at solar noon

    :param xDatetime:
    :param xLon:
    :return:
    """

    solar_utc_offset = solar_utc_offset_(xDatetime, xLon) - 0.5
    
    theta0 = (solar_utc_offset - 1)*(solar_utc_offset >= 1)
    theta1 = solar_utc_offset*((solar_utc_offset >= 0) & (solar_utc_offset < 1))
    theta2 = (solar_utc_offset + 1)*(solar_utc_offset < 0)
    theta = theta0 + theta1 + theta2
    
    return 2 * pi * theta


def solar_psi_(xDatetime, xLat, xLon):  # pragma: no cover
    """ solar zenith angle (0 overhead, pi/2 at horizon)
        typically, allowed to go 9 deg below the horizon

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    phi = solar_phi_(xLat)
    delta = solar_delta_(xDatetime, xLon)
    theta = solar_theta_(xDatetime, xLon)
    psi = arccos(sin(phi) * sin(delta) + cos(phi) * cos(delta) * cos(theta))
    return psi


def solar_alpha_(xDatetime, xLat, xLon):  # pragma: no cover
    """ solar azimuth angle relative to due north
    # typically, allowed zero at night, ie when sza >9 deg below the horizon

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    psi = solar_psi_(xDatetime, xLat, xLon)
    delta = solar_delta_(xDatetime, xLon)
    theta = solar_theta_(xDatetime, xLon)
    phi = solar_phi_(xLat)
    
    ca = (sin(delta) - sin(phi)*cos(psi)) / (cos(phi)*sin(psi))
    ca = np.clip(ca, -1.0, 1.0)
    
    solar_utc_offset = solar_utc_offset_(xDatetime, xLon)
    
    alpha0 = arccos(ca)*((theta >= pi) & (solar_utc_offset < 2*pi))  
    alpha1 = (2*pi - arccos(ca))*((theta >= 0.0) & (theta < pi))  
    
    return alpha0 + alpha1

def solar_daylength_(xDatetime, xLat, xLon):  # pragma: no cover
    """ returns daylength in hours
    NOT TESTED

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    
    # Very clearly wrong (inverse pattern; quantitatively off)
    #phi = solar_phi_(xLat)
    #delta = solar_delta_(xDatetime, xLon)
    #return (2.0 * 24.0 / pi) * arccos(np.tan(phi) * tan(delta))
    
    # Cribbed from CERES-MAIZE
    # Seems plausible but not safe for areas above arctic circle
    # At equator is biased above 12 hours/day
    phi = solar_phi_(xLat)
    delta = solar_delta_(xDatetime, xLon)
    DLV = (-sin(phi)*sin(delta) - 0.1047) / (cos(phi)*cos(delta))
    HRLT = 7.639 * arccos(DLV)
    return HRLT
    
def sunrise_sunset_(xDatetime, xLat, xLon):  # pragma: no cover
    """ returns sunrise and sunset in UTC time
    NOT TESTED

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """

    solar_noon = solar_noon_(xDatetime, xLon)
    daylength = solar_daylength_(xDatetime, xLat, xLon)

    td = pd.to_timedelta(daylength, unit = 'h')#.to_pytimedelta()

    sunrise = solar_noon-td
    sunset = solar_noon+td

    return sunrise, sunset 

def solar_psi_refr_(xDatetime, xLat, xLon, xT, xP):  # pragma: no cover
    """ refraction corrected solar zenith angle (0 overhead, pi/2 at horizon)
        typically, allowed to go 9 deg below the horizon
        http://rredc.nrel.gov/solar/codesandalgorithms/solpos/solpos.c

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    
    psi = solar_psi_(xDatetime, xLat, xLon)
                    
    elev = pi - psi
    tanelev = tan(elev)

    refcor1 = 0*(elev >= 85.*pi/180.)
    
    test2 = ((elev >= 5.*pi/180.) & (elev < 85.*pi/180.))
    refcor2 = (58.1/tanelev - 0.07/tanelev**3. + 0.000086/tanelev**5.) * test2

    test3 = ((elev >= -0.575*pi/180.) & (elev < 5.*pi/180.))
    refcor3 = (1735. + elev*(-518.2 + elev*(103.4 + elev*(-12.79 + elev*0.711)))) * test3

    refcor4 = (-20.774 / tanelev) * (elev < -0.575*pi/180.)

    prestemp = xP*Tk_(10.) / (P*Tk_(xT)) / 3600.

    refcor = (refcor1 + refcor2 + refcor3 + refcor4) * prestemp
                                                                                     
    return psi - refcor


def erv_(xDatetime):
    """ 
    Earth radius vector * solar constant = solar energy
    Spencer, J. W.  1971.  Fourier series representation of the
            position of the sun.  Search 2 (5), page 172
    Iqbal, M.  1983.  An Introduction to Solar Radiation. 
            Academic Press, NY., page 3 
    """ 
    leap = (xDatetime.year % 4 == 0) | (xDatetime.year % 100 == 0)
    yearl = np.ones((xDatetime.year.size)) * 365. + leap

    day = 2.*pi * xDatetime.dayofyear / yearl
    
    erv = 1.000110 + 0.34221*cos(day) + 0.001280*sin(day) + 0.000719*cos(day*2) + 0.000077*sin(day*2)
    
    return erv


def SWP_(xDatetime, xLat, xLon):
    
    psi = solar_psi_(xDatetime, xLat, xLon)
    etrn = SUN*erv_(xDatetime)  # this is not used while ERV is not tested
    
    etr0 = 0 * (cos(psi) < 0)
    etr1 = SUN * cos(psi) * (cos(psi) >= 0)
    
    return etr0 + etr1

def Kt_(xSWdw, xDatetime, xLat, xLon):
    """Clearness Index, Actual/Potential shortwave
    
    :param xSWdw:
    :param xDatetime:
    :param xLat:
    :param xLon:
    :return Kt [0 - 1]:
    """
    
    SWP = SWP_(xDatetime, xLat, xLon)
    Kt = xSWdw / SWP
    
    return np.clip(Kt, 0, 1)

def Kd_(xSWdw, xDatetime, xLat, xLon):
    """Diffuse Fraction, SW_diffuse / (SW_beam + SW_diffuse)
    Skartveit, Olseth and Tuft, 1998: An hourly diffuse fraction 
        model with correction for variability and surface albedo
        Solar Energy 63(3) p173-183
    
    :param xSWdw:
    :param xDatetime:
    :param xLat:
    :param xLon:
    :return Kd [0 - 1]:
    """
        
    df = pd.DataFrame()
        
    df['Kt'] = Kt_(xSWdw, xDatetime, xLat, xLon)
    df['h'] = 90 - solar_psi_(xDatetime, xLat, xLon)*180/pi
    df['Kd'] = np.ones(len(df))

    np.seterr(invalid='ignore')
    
    # Uncorrected model: non-variable, snow-free albedo
    # first segment: very cloudy, no beam radiation
    kmn = 0.22
    
    # second segment: broken clouds that partly obscure the sun
    k1 = 0.83 - 0.56*np.exp(-0.06*df.h)
    d1 = 0.07 + 0.046*(90-df.h)/(df.h+3)
    K_ = 0.5*(1+np.sin(pi*(df.Kt - kmn)/(k1 - kmn) - pi/2)) # this throws an error in sin; many k1 < kmn instances
    d_ = 1 - (1-d1)*(0.11*np.sqrt(K_) + 0.15*K_ + 0.74*K_**2)

    # third segment: cloudless skies prevail, diffuse light from high SZA & turbidity
    k2 = 0.95*k1
    K2 = 0.5*(1 + np.sin(pi*(k2 - kmn)/(k1 - kmn) - pi/2)) # this throws an error in sin; many k1 < kmn instances
    d2 = 1 - (1-d1)*(0.11*np.sqrt(K2) + 0.15*K2 + 0.74*K2**2) 
    d__ = d2*k2*(1-df.Kt)/(df.Kt*(1-k2))

    # fourth segment: silver linings: increases in irradiance from clouds not obscuring the sun
    alpha = np.power(1/np.sin(df.h*pi/180.), 0.6) # this returns nan if 1/0 
    kbmx = np.power(0.81, alpha) # this returns nan if alpha is nan
    kmx = (kbmx + d2*k2/(1-k2))/(1+ d2*k2/(1-k2))
    dmx = d2*k2*(1-kmx)/(kmx*(1-k2))
    d___ = 1-kmx*(1-dmx)/df.Kt

    # first segment assignment
    df.Kd.loc[df.Kt < kmn] = 1.

    # second segment assigment
    condition = (df.Kt >= kmn) & (df.Kt<k2)
    df.Kd.loc[condition] = d_.loc[condition] 

    # third segment assigment
    condition = (df.Kt>=k2) & (df.Kt<kmx)
    df.Kd.loc[condition] = d__.loc[condition] 

    # fourth segment assigment    
    condition = df.Kt>=kmx
    df.Kd.loc[condition] = d___.loc[condition] 

    # Correction for variable conditions
    df['rho'] = df.Kt/k1
    df['sigma3'] = np.abs(df.rho - df.rho.shift(1))

    df['delta'] = np.zeros(len(df))

    kx = 0.56-0.32*np.exp(-0.06*df.h)
    kL = (df.Kt - 0.14)/(kx - 0.14)
    kR = (df.Kt - kx)/0.71

    del1 = -3*(kL**2)*(1-kL)*(df.sigma3**1.3)
    condition = (df.Kt>0.14) & (df.Kt<kx) & (df.sigma3 > 0.0)
    df.delta.loc[condition] = del1.loc[condition]

    del2 = 3*kR*(1-kR)**2*(df.sigma3**0.6)
    condition = (df.Kt>kx) & (df.Kt<=(kx+0.71)) & (df.sigma3 > 0.0)
    df.delta.loc[condition] = del2.loc[condition]

    condition = (df.Kt<=0.14) | (df.Kt>(kx+0.71))
    df.delta.loc[condition] = 0.

    df.Kd = df.Kd + df.delta

    df.Kd[~np.isfinite(df.Kd)] = 1.

    np.seterr(all='warn')
    
    return np.clip(df.Kd, 0, 1)

def SW_zenith_corr_(xSW, xDatetime, xLat, xLon):
    # SW parameters provided by NREL
    a = -0.00002578
    b = 2.273
    c = 0.9586
    c = 1.0
    d = [0.000002, 0.000015]


    df = pd.DataFrame(xSW)
    df['azi'] = solar_alpha_(xDatetime, xLat, xLon)
    df['sza'] = solar_psi_(xDatetime, xLat, xLon)
    df['fz'] = 1.
    df.loc[df.azi<=pi,'fz'] = 1./((a+d[0])*(df.sza*180./pi)**b + c)
    df.loc[df.azi>pi,'fz'] = 1./((a+d[1])*(df.sza*180./pi)**b + c)
    df.loc[df.sza>=pi/2.,'fz'] = 0.

    return xSW*df.fz


def SW_azimuth_corr_(xSW, xDatetime, xLat, xLon):
    saa = solar_alpha_(xDatetime, xLat, xLon)*180/pi
    sza = solar_psi_(xDatetime, xLat, xLon)
    
    kt =xSW/SWP_(xDatetime, xLat, xLon)
    
    m6 =4.19424E-10;
    m5= -4.57449E-07;
    m4=0.000203792;
    m3=-0.047423074;
    m2=6.064225982;
    m1=-401.836849;
    b =10671.14743;

    # polynomial uses SAA in degrees, not radians
    corr= m6*(saa**6) + m5*(saa**5) + m4*(saa**4) + m3*(saa**3) + m2*(saa**2) + m1*saa + b
    
    # only works within certain azimuthal bounds

    test = ((sza*180/pi < 80.) & (kt > 0.2) & (saa > 80) & (saa < 280))
    SWcorr1 = (xSW - corr)*test
    SWcorr2 = xSW*(~test)
    
    return SWcorr1 + SWcorr2

def atmos_tau_(xPsi, xP=P):  # pragma: no cover
    """ 1 / sin(psi) = optical mass of the atmosphere
        return (xP / P) * sin(xPsi)
        Young 1994 Applied Optics

    :param xPsi:
    :param xP:
    :return:
    """
    return (xP / P) * (
        1.002432 * cos(xPsi) ** 2 + 0.148386 * cos(xPsi) + 0.0096467) / \
        (cos(xPsi) ** 3 + 0.149864 * cos(xPsi) ** 2 + 0.0102963 * cos(xPsi) + 0.000303978)  # NOQA


def vapor_tau_(xPsi, xP=P):  # pragma: no cover
    """ water absorption in NIR for 10 mm precipitable water (from ???)

    :param xPsi:
    :param xP:
    :return:
    """
    ru = atmos_tau_(xPsi)
    tau = (NIR + VIS) * 0.77 * (2.0 * ru) ** 0.3
    return tau


def rdvis_(xPsi, xP=P):  # pragma: no cover
    """ potential direct VIS: W/m**2

    :param xPsi:
    :param xP:
    :return:
    """
    ru = atmos_tau_(xPsi, xP)
    return VIS * exp(-0.185 * ru) * sin(xPsi)


def rsvis_(xPsi, xP=P):  # pragma: no cover
    """ potential diffuse VIS: W/m**2

    :param xPsi:
    :param xP:
    :return:
    """
    rdvis = rdvis_(xPsi, xP)
    return 0.4 * (VIS - rdvis) * sin(xPsi)


def rdnir_(xPsi, xP=P):  # pragma: no cover
    """ potential direct NIR: W/m**2

    :param xPsi:
    :param xP:
    :return:
    """
    ru = atmos_tau_(xPsi, xP)
    wa = vapor_tau_(xPsi, xP)
    rdnir = (NIR * exp(-0.065 * ru) - wa) * sin(xPsi)
    return max(rdnir, 0.0)


def rsnir_(xPsi, xP=P):  # pragma: no cover
    """ potential diffuse NIR: W/m**2

    :param xPsi:
    :param xP:
    :return:
    """
    wa = vapor_tau_(xPsi, xP)
    rdnir = rdnir_(xPsi, xP)
    rsnir = (0.6 * (NIR - wa - rdnir)) * sin(xPsi)
    return max(rsnir, 0.0)


def a_rayleigh_(xLambda_nm):  # pragma: no cover
    """ Rayleigh (molecular) component of atmospheric scattering, Bucholtz 1995

    :param xLambda_nm:
    :return:
    """
    if xLambda_nm > 500:
        # coeffs in um
        A = 8.64627e-3
        B = 3.99668
        C = B
        D = 2.71393e-2
    else:
        A = 6.50362e-3
        B = 3.55212
        C = B
        D = 0.11563

    xLambda_um = xLambda_nm / 1000
    return A * xLambda_um ** (-(B + C * xLambda_um + D * xLambda_um))


# Aerodynamics
def zo_(h=1.):  # pragma: no cover
    """
    :param h: canopy height (m)
    :return: roughness length
    """
    return 10 ** (0.997 * log(h) - 0.883)


def d_(h=1.):  # pragma: no cover
    """
    :param h: canopy height (m)
    :return: zero-plane displacement
    """
    return 10 ** (0.979 * log(h) - 0.154)


def ustar_(U, h=1., z=2.):  # pragma: no cover
    """
    :param xU:
    :param xh: canopy height (m)
    :param xz: measurement height (m)
    :return:
    """
    zo = zo_(h)
    d = d_(h)
    return (k * U) / (log((z - d) / zo)) + 0.01

def u2_(U1, h=1., z1=2., z2=10.):  # pragma: no cover
    """
    :param xU1: measurement at one height
    :param xh: canopy height (m)
    :param xz: measurement height (m)
    :return u2: wind at another height
    """
    zo = zo_(h)
    d = d_(h)
    return U1*(log((z2 - d) / zo))/(log((z1 - d) / zo))

def udir_(U, V):  # pragma: no cover
    """
    :param xU: EW component of wind
    :param xV: NS component of wind
    :return u2: wind direction in degrees
    """
    return 180. + (180./pi) * arctan2(V, U)


def rpbl_(xU, xh, xz):  # pragma: no cover
    """ resistance as inverse velocity: s/m
        conductance = (density)/(resistance) = (kg/m3)/(s/m) = (kg/m2/s)
        includes no excess scalar resistance

    :param xU:
    :param xh:
    :param xz:
    :return:
    """
    ustar = ustar_(xU, xh, xz)
    return xU / (ustar ** 2)


def rpbl_heat_(xU, xh, xz):  # pragma: no cover
    """ includes excess resistance for heat scalar

    :param xU:
    :param xh:
    :param xz:
    :return:
    """
    ustar = ustar_(xU, xh, xz)
    return rpbl_(xU, xh, xz) + (2 / (k * ustar))


def rpbl_h2o_(xU, xh, xz):  # pragma: no cover
    """ includes excess resistance for water vapor scalar """
    ustar = ustar_(xU, xh, xz)
    # 0.92 = kappa/Dh2o**0.67
    return rpbl_(xU, xh, xz) + (2 / (k * ustar)) * 0.92


def rpbl_co2_(xU, xh, xz):  # pragma: no cover
    """ includes excess resistance for water vapor scalar

    :param xU:
    :param xh:
    :param xz:
    :return:
    """
    ustar = ustar_(xU, xh, xz)
    # 1.29 = kappa/Dco2**0.67
    return rpbl_(xU, xh, xz) + (2 / (k * ustar)) * 1.29
    
