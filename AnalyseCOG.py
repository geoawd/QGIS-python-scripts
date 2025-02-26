import os
import glob
from osgeo import gdal

def analyze_geotiff_files(file_list):
    """
    Analyses a list of single-band GeoTIFF files and returns their
    filename, no data value, min value, and max value using GDAL.
    
    Args:
        file_list (list): List of paths to GeoTIFF files
        
    Returns:
        list: List of dictionaries containing analysis results for each file
    """
    # Register all GDAL drivers
    gdal.AllRegister()
    
    results = []
    
    for file_path in file_list:
        try:
            # Open the dataset
            ds = gdal.Open(file_path)
            if ds is None:
                print(f"Error: Could not open {os.path.basename(file_path)}")
                continue
            
            # Check if it's a single band file
            if ds.RasterCount != 1:
                print(f"Warning: {os.path.basename(file_path)} has {ds.RasterCount} bands, not a single band file.")
                continue
            
            # Get the band
            band = ds.GetRasterBand(1)
            
            # Get the no data value
            nodata = band.GetNoDataValue()
            
            # Get statistics (min, max, mean, stddev)
            # Set the second parameter to 1 to force computation if statistics don't exist
            stats = band.GetStatistics(1, 1)
            min_val = stats[0]
            max_val = stats[1]
            
            # Store the results
            results.append({
                'filename': os.path.basename(file_path),
                'nodata_value': nodata,
                'min_value': min_val,
                'max_value': max_val
            })
            
            print(f"Processed: {os.path.basename(file_path)}")
            
            # Close the dataset
            ds = None
            
        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
    
    return results

def print_results(results):
    """
    Prints the analysis results in a formatted way.
    
    Args:
        results (list): List of dictionaries containing analysis results
    """
    print("\nGeoTIFF Analysis Results:")
    print("-" * 80)
    print(f"{'Filename':<30} {'No Data Value':<15} {'Min Value':<15} {'Max Value':<15}")
    print("-" * 80)
    
    for result in results:
        nodata_str = str(result['nodata_value']) if result['nodata_value'] is not None else "None"
        print(f"{result['filename']:<30} {nodata_str:<15} {result['min_value']:<15.6f} {result['max_value']:<15.6f}")

if __name__ == "__main__":
    geotiff_dir = "/var/www/html2/lidar"
    file_list = glob.glob(os.path.join(geotiff_dir, "*.tif"))
    
    if not file_list:
        print(f"No GeoTIFF files found in {geotiff_dir}")
    else:
        results = analyze_geotiff_files(file_list)
        print_results(results)
