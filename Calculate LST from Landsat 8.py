"""
  LST CALCULATOR FOR LANDSAT 8
  
  Updated on: 17 September 2022
  Written by HaKaN OGUZ
  Description: This python code calculates land surface temperature (LST) from Landsat 8 imagery 
"""
import arcpy
from sys import argv

s
def CalculateLSTfromLandsat8(band4="E:\\Desktop 17_Sep_2022\\ICIAS 2022\\LC08_L1TP_027037_20220707_20220721_02_T1\\LC08_L1TP_027037_20220707_20220721_02_T1_B4.TIF", band5="E:\\Desktop 17_Sep_2022\\ICIAS 2022\\LC08_L1TP_027037_20220707_20220721_02_T1\\LC08_L1TP_027037_20220707_20220721_02_T1_B5.TIF", band10="E:\\Desktop 17_Sep_2022\\ICIAS 2022\\LC08_L1TP_027037_20220707_20220721_02_T1\\LC08_L1TP_027037_20220707_20220721_02_T1_B10.TIF", Sun_Elevation_Angle=62.75, Downwelling_Radiance=5.46, Upwelling_Radiance=3.48, Atmospheric_Transmission=0.62, LST="C:\\Landsat_5\\lst"):  # Calculate LST from Landsat 8

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")


    # Process: Convert to Reflectance for band5 (Raster Calculator) 
    band5_ref = "C:\\Landsat_5\\band5_ref"
    arcpy.gp.RasterCalculator_sa(expression=[band5, Sun_Elevation_Angle], output_raster=band5_ref)

    # Process: Convert to Reflectance for band4 (Raster Calculator) 
    band4_ref = "C:\\Landsat_5\\band4_ref"
    arcpy.gp.RasterCalculator_sa(expression=[band4, Sun_Elevation_Angle], output_raster=band4_ref)

    # Process: Calculate NDVI (Raster Calculator) 
    ndvi = "C:\\Landsat_5\\ndvi"
    arcpy.gp.RasterCalculator_sa(expression=[band5_ref, band4_ref, band5_ref, band4_ref], output_raster=ndvi)

    # Process: Correct ndvi (Raster Calculator) 
    ndvi_corrected = "C:\\Landsat_5\\ndvi_correct"
    arcpy.gp.RasterCalculator_sa(expression=[ndvi, ndvi, ndvi, ndvi, ndvi], output_raster=ndvi_corrected)

    # Process: Fractional Vegetation Cover (Raster Calculator) 
    fvc = "C:\\Landsat_5\\fvc"
    arcpy.gp.RasterCalculator_sa(expression=[ndvi_corrected], output_raster=fvc)

    # Process: Fractional Vegetation Cover Correction (Raster Calculator) 
    fvc_corrected = "C:\\Landsat_5\\fvc_corrected"
    arcpy.gp.RasterCalculator_sa(expression=[fvc, fvc, fvc, fvc, fvc], output_raster=fvc_corrected)

    # Process: Emissivity Calculation (Raster Calculator) 
    emissivity = "C:\\Landsat_5\\emissivity"
    arcpy.gp.RasterCalculator_sa(expression=[fvc_corrected, band4_ref, fvc_corrected, fvc_corrected, fvc_corrected, fvc_corrected, fvc_corrected], output_raster=emissivity)

    # Process: Convert to Radiance for band10 (Raster Calculator) 
    band10_rad = "C:\\Landsat_5\\band10_rad"
    arcpy.gp.RasterCalculator_sa(expression=[band10], output_raster=band10_rad)

    # Process: Calculate Lsen (Raster Calculator) 
    Lsen = "C:\\Landsat_5\\l_sen"
    arcpy.gp.RasterCalculator_sa(expression=[emissivity, band10_rad, emissivity, Downwelling_Radiance, Atmospheric_Transmission, Upwelling_Radiance], output_raster=Lsen)

    # Process: Calculate LST (Raster Calculator) 
    lst_calc = "C:\\Landsat_5\\calc_lst"
    arcpy.gp.RasterCalculator_sa(expression=[Lsen, Upwelling_Radiance, Atmospheric_Transmission, emissivity, Downwelling_Radiance, Atmospheric_Transmission, emissivity], output_raster=lst_calc)

    # Process: LST in Degree Celsius (Raster Calculator) 
    lst_celsius = "C:\\Landsat_5\\lst_celsius"
    arcpy.gp.RasterCalculator_sa(expression=[lst_calc], output_raster=lst_celsius)

    # Process: SetNull (Raster Calculator) 
    lst_setnull = "C:\\Landsat_5\\lst_setnull"
    arcpy.gp.RasterCalculator_sa(expression=[lst_celsius, lst_celsius], output_raster=lst_setnull)

    # Process: Remove Cloud (Raster Calculator) 
    arcpy.gp.RasterCalculator_sa(expression=[lst_setnull, lst_setnull], output_raster=LST)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\h_ogu\Documents\ArcGIS\Projects\MyProject5\MyProject5.gdb", workspace=r"C:\Users\h_ogu\Documents\ArcGIS\Projects\MyProject5\MyProject5.gdb"):
        CalculateLSTfromLandsat8(*argv[1:])
