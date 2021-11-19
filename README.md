# Dynamic temperature calculation on surfaces in solar radiance and radiation exchange with environment

Engin Bagda, Manfred Hermann, Erkam Talha Öztürk

Heat flow through walls depends on the surface temperature between the inside and the outside. If the surface
temperatures change, the heat flow gets dynamic. In this work is a calculation method explained, and a code
`SurfaceTemp.py` given to determine the surface temperature of materials at changing solar radiation and air
temperature. It is shown how the surface temperature depends on beside the intensity of the solar radiation, and the air
temperature on the solar absorptions' coefficient of the surface, thermal conductivity of the material and the emission
coefficients of surface and environment.

The code `SurfaceTemp.py` calculates in a good approximation the surface temperature of a material in
dependence of the sun radiation and air temperature. This is shown by using the measurements in the excel sheet
`Garden.xlsx`.

The code `SurfaceTemp.py` use for the calculation of the dynamic heat flow through walls the numerical
Crank-Nicolson method as explained in [erkam-o/DynamicHeatFlow](https://github.com/erkam-o/DynamicHeatFlow/blob/master/Calc_Dynamic%20Heat%20Flow_2020_07_05.pdf).

You can find theoretical background information and explanation to the code [here](https://github.com/Heating-and-cooling/surface_temp/blob/main/Surface_temp.pdf).
