# SurfaceTemp_2021_03_11
# Calculation of surface temperature at sun radiation
# for the sample Fibre cement board on extrudet polystyrene
# By Engin Bagda and Erkam Talha Öztürk
# Measurements by Manfred Hermann


# Crank Nicolson function
def CrankNicolson():
    e[0] = 0
    f[0] = Temp[0]
    for i in range (1, n-1, 1):
        r = Lambda[i]*dTime / (Hcap[i]*Rho[i]*x[i]*x[i])
        K1 = Lambda[i-1]*x[i] / (Lambda[i]*x[i-1])
        K2 = Lambda[i]*x[i+1] / (Lambda[i+1]*x[i])
        g1 = r * (1 - K1) / (1 + K1)
        g2 = r * (1 - K2) / (1 + K2)
        a = r - g1
        b = 2 + (2*r) - g1 + g2
        c = r + g2
        d = (a * Temp[i-1]) + (2-(2*r)+g1-g2) * Temp[i] + (c*Temp[i+1])
        e[i] = c / (b - (a*e[i-1]))
        f[i] = (d + a*f[i-1]) / (b - a*e[i-1])

# Thomas algorithm
    for i in range (n-2, 0, -1):
        Temp[i] = (e[i]*Temp[i+1]) + f[i]

def HeatBalance(s):
    q_solar = I_sun * Absorp * dTime
    q_emiss = (Emiss * 5.7 * m.pow(10, -8) * (
                (0.9 * m.pow((273 + Temp_air_ext-8), 4)) - m.pow(273 + Temp[n - 1], 4))) * dTime
    q_conv = Heattrans_ext * (Temp_air_ext - Temp[n - 1]) * dTime
    q_trans = 2*Lambda[n-1]*Lambda[n-2]*(Temp[n - 2] - Temp[n - 1]) * dTime/ (x[n - 1]*Lambda[n-2] + x[n - 2]*Lambda[n-1])
    q_cont = Hcap[n - 1] * Rho[n - 1] * (Temp_old - Temp[n - 1]) * x[n - 1]

    # for the time when the samples are not exposed to radiation exchange with the sky
    if Index>255 and Index<268:
        q_emiss = 0
    if Index>303:
        q_emiss = 0

    q[s] = q_cont + q_conv + q_trans + q_solar + q_emiss

# Trail and Error function to find the minimum level for the heat balance
def TaE():

    s = 1
    HeatBalance(s)

    for s in range(s+1, 25, 1):
        Temp[n-1] = Temp[n-1] - 0.2
        HeatBalance(s)

        if abs(q[s]) > abs(q[s-1]):
            break

    for s in range(s+1, 25, 1):
        Temp[n - 1] = Temp[n - 1] + 0.2
        HeatBalance(s)

        if abs(q[s]) > abs(q[s - 1]):
            break

    Temp[n-1] = Temp[n-1] - 0.2
    HeatBalance(s)

global x, e, f, s, HeatFlow, n, dTime, Temp, Lambda, Rho, Hcap  # global variables

# Definitions
import numpy as arr # to set up arrays
import math as m # for power
import pandas as pd # to read_excel data
import xlsxwriter # to export to excel

# Initialization values

x = arr.empty(50)
e = arr.empty(50)
f = arr.empty(50)
Temp = arr.empty(50)
Lambda = arr.empty(50)
Rho = arr.empty(50)
Hcap = arr.empty(50)
HeatFlow = arr.empty(50)
q = arr.empty(50)

# reading inputs from excel
Inputs_Excel=pd.read_excel('Garden_2021_03_08.xlsx', sheet_name='Table',dtype={'Air':float, 'Pyranometer':float})
Input_Temp_Air = Inputs_Excel['Air']  # Input for Temp exterieur
Input_I_sun = Inputs_Excel['Pyranometer']  # Input for sun radiation

# Output file definition
workbook = xlsxwriter.Workbook('Output_SurfaceTemp.xlsx') # output file name
worksheet_temp = workbook.add_worksheet('Temperature Profile')

# Set up conditions and material properties

dTime = 300.00 # duration of the steps seconds

# Extrudet poystyrene foam XPS
n1 = 10 # elements
n1 = n1 + 1 # one element is added for dummy at Biot figure Temp_air_int
for i in range (0, n1, 1): # loop stops at i[n1-1]
    x[i] = 0.005 # thickness of each element
    Lambda[i] = 0.035 # thermal conductivity W/m/K
    Rho[i] = 15  # density kg/m3
    Hcap[i] = 1450 # heat capacity Joule/m3
    Temp[i] = 20 # °C, primary definition

# Fibre cement board
n2 = 1 # elements for expanded polystyrene
n = n1 + n2
for i in range (n1, n, 1): # loop stops at i[n1+n2-1]
    x[i] = 0.005 # thickness of each element
    Lambda[i] = 0.580 # thermal conductivity W/m/K
    Rho[i] = 1650  # density kg/m3
    Hcap[i] = 960 # Heat capacity Joule/m3
    Temp[i] = 20 # °C, primary definition

Heattrans_int = 7 # surface heat transition coefficient backside oriented 1 m to ground, W/m2/K
Heattrans_ext = 10 # surface heat transition coefficient horizontal surface, wind: calm, W/m2/K

Absorp = 0.95 # dark black coating absorption measured 390 nm - 1100 nm
Emiss = 0.92 # for organic materials according their carbon bondings

Bi_int = (Heattrans_int*x[0])/(2*Lambda[0]) # Biot number backside

# Headers to output excel file
worksheet_temp.write(0, 0, "Minutes")  # writing to column A
worksheet_temp.write(0, 1, "Temp_air_ext")
worksheet_temp.write(0, 2, "Temp[n-1]")

# Main run
for Index, row in enumerate(Input_I_sun): #

    I_sun = float(Input_I_sun[Index])
    Temp_air_ext = float(Input_Temp_Air[Index])

    Temp_air_int = Temp_air_ext
    Temp[0] = (Temp[1] * (1 - Bi_int) / (1 + Bi_int)) + (2 * Bi_int * Temp_air_int / (1 + Bi_int))

    Temp_old = Temp[n-1]

    TaE()
    CrankNicolson()

    worksheet_temp.write(Index+1, 0, Index*5)  # writing to column A in minutes because dTime is 300 sec
    worksheet_temp.write(Index+1, 1, Temp_air_ext)
    worksheet_temp.write(Index+1, 2, Temp[n-1])

workbook.close()


