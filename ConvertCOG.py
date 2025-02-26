import os
import subprocess
from osgeo import gdal

def process_cog_files(input_files, output_folder, divisor=1000, nodata=-99):
    """
    Process COG files using gdal_calc and save results as new COG files.
    
    Args:
        input_files (list): List of input COG file paths
        output_folder (str): Folder to save the output COG files
        divisor (float): Value to divide the raster by
        nodata (float): NoData value for the output
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    for input_file in input_files:
        # Get the filename without path
        filename = os.path.basename(input_file)
        base_name = os.path.splitext(filename)[0]
        
        # Define temporary and output file paths
        temp_file = os.path.join(output_folder, f"{base_name}_temp.tif'
        output_file = os.path.join(output_folder, f"{base_name}_processed.tif'
        
        # Step 1: Perform raster calculation using gdal_calc.py
        calc_cmd = [
            "gdal_calc.py",
            "-A", input_file,
            "--outfile", temp_file,
            "--calc", f"A/{divisor}",
            "--NoDataValue", str(nodata),
            "--type", "Float32",
            "--quiet"
        ]
        
        print(f"Processing {input_file}...")
        subprocess.run(calc_cmd, check=True)
        
        # Step 2: Convert the result to COG format
        translate_options = gdal.TranslateOptions(
            format='COG', 
            creationOptions=["COMPRESS=LZW", "NUM_THREADS=ALL_CPUS"]
        )
        
        gdal.Translate(output_file, temp_file, options=translate_options)
        
        # Remove temporary file
        os.remove(temp_file)
        
        print(f"Created COG file: {output_file}")


files = [
r'/var/www/html2/lidar/Ballinamallard_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Ballinamallard_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Belleek_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Belleek_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Beragh_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Beragh_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Burren_03_03_2012_DSM.tif',
r'/var/www/html2/lidar/Burren_03_03_2012_DTM.tif',
r'/var/www/html2/lidar/Dougary_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Dougary_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Eglinton_11_12_2012_DSM.tif',
r'/var/www/html2/lidar/Eglinton_11_12_2012_DTM.tif',
r'/var/www/html2/lidar/Enniskillen_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Enniskillen_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Fintona_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Fintona_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Folk Park Newtownstewart_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Folk Park Newtownstewart_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Glenavy_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Glenavy_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Keady_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Keady_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Lisbellaw_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Lisbellaw_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Lurgan_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Lurgan_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Maguiresbridge_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Maguiresbridge_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Moneymore_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Moneymore_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Mossley_05_03_2012_DSM.tif',
r'/var/www/html2/lidar/Mossley_05_03_2012_DTM.tif',
r'/var/www/html2/lidar/Omagh_Town_11_12_2012_DSM.tif',
r'/var/www/html2/lidar/Omagh_Town_11_12_2012_DTM.tif',
r'/var/www/html2/lidar/PortadownExtension_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/PortadownExtension_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Saintfield_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Saintfield_02_02_2012_DTM.tif',
r'/var/www/html2/lidar/Sion Mills_02_02_2012_DSM.tif',
r'/var/www/html2/lidar/Sion Mills_02_02_2012_DTM.tif',
]

# Define output folder
output_folder = "~/processed_cogs"

# Process the files
process_cog_files(files, output_folder, divisor=1000, nodata=-99)
