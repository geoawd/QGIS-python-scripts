import os
from osgeo import gdal

vrt_path = r'path.vrt'
cog_path = r'path.tif'
translate_options = gdal.TranslateOptions(format='COG', creationOptions=["COMPRESS=LZW", "NUM_THREADS=ALL_CPUS"],
                                                  outputSRS='EPSG:29902')
        
gdal.Translate(cog_path, vrt_path, options=translate_options)
