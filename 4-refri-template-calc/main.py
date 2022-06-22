# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import iapws
from iapws.ammonia import NH3
from iapws._iapws import _Liquid
import numpy as np

global hNH3, IAPWS97, NH3, uNH3, sNH3, TNH3, _Liquid, cpHO2, rhoHO2, math, py, CompTags


# get specific enthalpy
def hNH3(**kwargs):
    try:
        result = NH3(**kwargs).h
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get specific internal energy
def uNH3(**kwargs):
    try:
        result = NH3(**kwargs).u
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get specific internal energy of ammonia
def sNH3(**kwargs):
    try:
        result = NH3(**kwargs).s
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get specific internal energy of ammonia
def sNH3(**kwargs):
    try:
        result = NH3(**kwargs).s
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get Temperature of ammonia
def TNH3(**kwargs):
    try:
        result = NH3(**kwargs).T
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get specific heat capacity at constant pressure of water
def cpHO2(T):
    try:
        result = _Liquid(T)['cp']
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


# get density at constant pressure
def rhoHO2(T):
    try:
        result = _Liquid(T)['rho']
        return result
        if result is None:
            raise Exception("Null Value")
    except Exception as e:
        raise e


'''
C_TagsInput = {'C_PI'  : 2.5      #bar  - Compressor inlet pressure
               'C_PO'  : 10.0     #bar  - Compressor outlet pressure
               'C_TI'  : False    #C    - Compressor inlet Temperature
               'C_TO'  : False    #C    - Compressor outlet Temperature
               'C_DW'  : False    #kW   - Compressor electrical power
               'C_AMP' : False    #AMPS - Compressir current
               "C_VOLT": False   #VOLTS - Compressor line voltage 3PH(LINE)
               "C_PF"    : 0.85*.95       - Compressor power factor
               "C_VF"    : False   #kg/s  - Compressor Refrigerant flowrate
               "C_N"   : False          - Compressor Polytropic index
               "CT_TO" : False  #C      - Condensor exit temperature 
               }
'''

# NEED TO CONSIDER OFF STATE MAYBE


C_TagsInput = {'C_PI': 2.7, \
               'C_PO': 10, \
               'C_TI': False, \
               'C_TO': False, \
               'C_DW': False, \
               'C_AMP': False, \
               "C_VOLT": False, \
               "C_PF": False, \
               "C_MF": False, \
               "C_N": False, \
               "CT_TO": False \
               }


def CompTags(C_TagsInput):
    global NH3, math, py

    C_Tags = {}
    C_Tags = C_TagsInput

    # print(C_Tags)

    if C_TagsInput["C_PI"] and C_TagsInput["C_TI"]:
        C_TI = C_Tags['C_TI'] + 273.15  # K
        C_PI = C_Tags['C_PI'] / 10  # MPa
        C_HI = NH3(T=C_TI, P=C_PI).h  # kJ/kg
        C_VI = NH3(T=C_TI, P=C_PI).v  # m^3/kg

    if not C_TagsInput["C_TI"]:
        C_PI = C_Tags['C_PI'] / 10  # MPa
        C_TI = NH3(P=C_PI, x=1).T  # K
        C_HI = NH3(P=C_PI, x=1).h  # kJ/kg
        C_VI = NH3(P=C_PI, x=1).v  # m^3/kg

    if not C_TagsInput["C_PI"]:
        C_TI = C_Tags['C_TI'] + 273.15  # K
        C_HI = NH3(T=C_TI, x=1).h  # kJ/kg
        C_PI = NH3(T=C_TI, x=1).P  # MPa
        C_VI = NH3(T=C_TI, x=1).v  # m^3/kg

    if C_TagsInput["C_TO"] and C_TagsInput["C_PO"]:
        C_TO = C_Tags['C_TO'] + 273.15  # K
        C_PO = C_Tags['C_PO'] / 10  # MPa
        C_VO = NH3(T=C_TO, P=C_PO).v  # m^3/kg
        if C_PO != 0:
            C_N = math.log(C_PI / C_PO) / math.log(C_VO / C_VI)
        else:
            print("C_PO is zero")
        C_HO = NH3(T=C_TO, P=C_PO).h  # kJ/kg

    if C_TagsInput["C_TO"] and not C_TagsInput["C_PO"] and C_TagsInput["CT_TO"]:
        C_TO = C_Tags['C_TO'] + 273.15  # K
        CT_TO = C_Tags['CT_TO'] + 273.15  # K
        C_PO = NH3(T=CT_TO, x=1).P  # MPa
        C_VO = NH3(T=CT_TO, P=C_PO).v
        if C_PO != 0:
            C_N = math.log(C_PI / C_PO) / math.log(C_VO / C_VI)
        else:
            print("C_PO is zero")
        C_HO = NH3(T=C_TO, P=C_PO).h  # kJ/kg
        C_VO = NH3(T=C_TO, P=C_PO).v  # m^3/kg

    if not C_TagsInput["C_TO"] and C_TagsInput["C_N"]:
        print("we are assuming a constant polytropic index from measurements")
        C_N = C_TagsInput["C_N"]
        C_PO = C_Tags['C_PO'] / 10  # MPa
        if C_PO != 0 and C_N != 0:
            C_VO = ((C_PI / C_PO) * C_VI ** C_N) ** (1 / C_N)  # m^3/kg
        else:
            print("C_PO or C_N is zero")
        C_TO = NH3(P=C_PO, v=C_VO).T  # K
        C_HO = NH3(T=C_TO, P=C_PO).h  # kJ/kg

    if not C_TagsInput["C_TO"] and not C_TagsInput["C_N"]:
        print("we are assuming isentropic compression")
        C_N = 1.3
        C_PO = C_Tags['C_PO'] / 10  # MPa
        # print("C_VI",C_VI)
        if C_PO != 0 and C_N != 0:
            C_VO = ((C_PI / C_PO) * C_VI ** C_N) ** (1 / C_N)  # m^3/kg
        else:
            print("C_PO or C_N is zero")
        print("C_VO", C_VO)
        C_TO = NH3(P=C_PO, v=C_VO).T  # K
        C_HO = NH3(T=C_TO, P=C_PO).h  # kJ/kg

    ''' This case needs further attention        
    if not C_TagsInput["C_PO"] and not C_TagsInput["CT_TO"] and C_TagsInput["C_N"]:
        #print(we are assuming a constant polytropic index from measurements)
        C_N = C_TagsInput["C_N"]
        C_TO = C_Tags['C_TO'] + 273.15             #K
        Vo = 1
        a = 1
        while a > 10**-3:  
            Vo += -10**-2
            C_PO = NH3(T = C_TO,v = Vo).P
            C_VO = ((C_PI/C_PO)*C_VI**C_N)**(1/C_N)
            a = C_VO - Vo
        C_HO = NH3(T = C_TO,P = C_PO).h  #kJ/kg
        C_VO = NH3(T = C_TO,P = C_PO).v  #m^3/kg
    '''

    if not C_TagsInput["C_PO"] and not C_TagsInput["C_N"] and not C_TagsInput["CT_TO"]:
        print("we are assuming isentropic compression")
        C_N = 1.3
        C_SO = NH3(T=C_TI, P=C_PI).s
        C_PO = NH3(T=C_TO, s=C_SO).P
        C_HO = NH3(T=C_TO, P=C_PO).h  # kJ/kg
        C_VO = NH3(T=C_TO, P=C_PO).v  # m^3/kg

    if C_N != 0:
        C_DWS = -1 * (C_PO * (10 ** 6) * C_VO - C_PI * (10 ** 6) * C_VI) / (1 - C_N) / 1000  # kJ/kg
    else:
        print("C_N is zero")

    if C_TagsInput['C_AMP'] and C_TagsInput['C_VOLT']:
        C_Tags["C_DW"] = math.sqrt(3) * C_Tags['C_PF'] * C_Tags['C_AMP'] * C_Tags['C_VOLT'] / 1000

    if C_TagsInput['C_MF'] and C_Tags["C_DW"]:
        C_DW = C_Tags["C_DW"]
        C_MF = C_Tags['C_MF']
        if C_DW != 0:
            C_Tags["C_ETA"] = C_DWS * C_MF / C_DW

    if not C_TagsInput['C_TI']: C_Tags['C_TI'] = C_TI - 273.15
    if not C_TagsInput["C_PI"]: C_Tags["C_PI"] = C_PI * 10
    if not C_TagsInput['C_TO']: C_Tags['C_TO'] = C_TO - 273.15
    if not C_TagsInput["C_PO"]: C_Tags["C_PO"] = C_PO * 10

    C_Tags['C_HI'] = C_HI
    C_Tags['C_VI'] = C_VI
    C_Tags['C_HO'] = C_HO
    C_Tags['C_VO'] = C_VO
    C_Tags['C_N'] = C_N
    C_Tags["C_DWS"] = C_DWS

    return C_Tags


def sum_x_y(x, y):
    return (x + y)


if __name__ == '__main__':
    # Read csv
    pdf = pd.read_csv("Refrigeration Dataset Trimmed for Calculations CSV.csv", delimiter=',')

    pdf.replace(to_replace=np.nan, value=1,inplace=True)

    result = [sum_x_y(x, y) for x, y in zip(pdf['REF_2L.LI1.PV_C_TI'], pdf['REF_2L.LI1.PV_C_PI'])]
    result = [sum_x_y(x, y) for x, y in zip(pdf['REF_2L.LI1.PV_C_TI'], pdf['REF_2L.LI1.PV_C_PI'])]
    print(result)



    #result = [sum_x_y(x, y) for x, y in zip(pdf['REF_2L.LI1.PV_C_TI'], pdf['REF_2L.LI1.PV_C_PI'])]  test


    # for row in pdf.iterrows():
    # row['LI1.C_VI'] = NH3(T=row['REF_2L.LI1.PV_C_TI'], P=row['REF_2L.LI1.PV_C_PI'])
    # if type(row['REF_2L.LI1.PV_C_TI']) == float:
    # print(row['REF_2L.LI1.PV_C_TI'].dtype)
    # row.

    # testing
    # C_Tags = CompTags(C_TagsInput)
    # print(C_Tags)
    # if type(pdf['REF_2L.LI1.PV_C_PO']) == 'float':
    # print(type(pdf['REF_2L.LI1.PV_C_PO']))

    pdf.to_csv("Refrigeration Dataset Trimmed for Calculations CSV_Modf.csv")