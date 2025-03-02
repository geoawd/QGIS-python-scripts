import os
import sys
from osgeo import gdal

def get_pixel_sizes(file_list):
    """
    Get the pixel sizes (width and height) of a list of GeoTIFF files.
    
    Args:
        file_list (list): List of paths to GeoTIFF files
        
    Returns:
        list: List of dictionaries containing filename and pixel size
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
            
            # Get the geotransform which contains pixel dimensions
            gt = ds.GetGeoTransform()
            if gt:
                # Pixel width is the absolute value of gt[1]
                # Pixel height is the absolute value of gt[5]
                pixel_width = abs(gt[1])
                pixel_height = abs(gt[5])
            else:
                pixel_width = None
                pixel_height = None
            
            # Store the results
            results.append({
                'filename': os.path.basename(file_path),
                'pixel_width': pixel_width,
                'pixel_height': pixel_height
            })
            
            print(f"Processed: {os.path.basename(file_path)}")
            
            # Close the dataset
            ds = None
            
        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
    
    # Sort results by filename
    results.sort(key=lambda x: x['filename'])
    
    return results

def print_results(results):
    """
    Prints the pixel size results in a formatted way similar to the earlier script.
    
    Args:
        results (list): List of dictionaries containing filename and pixel size info
    """
    print("\nGeoTIFF Pixel Size Results:")
    print("-" * 80)
    print(f"{'Filename':<40} {'Pixel Width':<20} {'Pixel Height':<20}")
    print("-" * 80)
    
    for result in results:
        width_str = f"{result['pixel_width']:.6f}" if result['pixel_width'] is not None else "N/A"
        height_str = f"{result['pixel_height']:.6f}" if result['pixel_height'] is not None else "N/A"
        
        print(f"{result['filename']:<40} {width_str:<20} {height_str:<20}")

if __name__ == "__main__":
    # Example usage
    import glob
    
    # Replace this with your directory path containing GeoTIFF files
    geotiff_dir = "/lidar"
    file_list = glob.glob(os.path.join(geotiff_dir, "*.tif"))
    
    if not file_list:
        print(f"No GeoTIFF files found in {geotiff_dir}")
    else:
        results = get_pixel_sizes(file_list)
        print_results(results)
