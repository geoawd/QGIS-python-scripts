from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsProject
import os
import requests

def test_url_access(url):
    """Test if URL is accessible"""
    try:
        response = requests.head(url)
        return response.status_code == 200
    except:
        return False

def clean_url(url):
    """Clean URL by removing www. if present"""
    return url.replace('www.', '')

def get_layer_name_from_url(url):
    """Extract layer name from URL filename without extension"""
    filename = url.split('/')[-1]  # Get the last part after /
    return os.path.splitext(filename)[0]  # Remove the extension

def add_rasters_from_urls(url_list, layer_name_prefix=None):
    """
    Add raster layers to QGIS from a list of URLs using VSICURL with GDAL provider.
    
    Parameters:
    url_list (list): List of HTTP URLs pointing to raster files
    layer_name_prefix (str, optional): Prefix for layer names, if None uses filename
    
    Returns:
    list: List of successfully added layer names
    """
    added_layers = []
    
    # Get the project instance
    project = QgsProject.instance()
    
    for index, url in enumerate(url_list):
        try:
            # Clean and validate URL
            url = clean_url(url)
            if not test_url_access(url):
                print(f"URL not accessible: {url}")
                continue
                
            # Create the VSICURL path (remove any double slashes except for http://)
            vsicurl_path = f"/vsicurl/{url}"
            
            # Use filename as layer name instead of numbered prefix
            layer_name = get_layer_name_from_url(url)
            if layer_name_prefix:
                layer_name = f"{layer_name_prefix}_{layer_name}"
            
            # Create the raster layer with GDAL provider
            layer = QgsRasterLayer(vsicurl_path, layer_name, "gdal")
            
            if layer.isValid():
                # Add the layer to the project
                if project.addMapLayer(layer):
                    added_layers.append(layer_name)
                    print(f"Successfully added layer: {layer_name}")
                else:
                    print(f"Failed to add layer to map: {layer_name}")
            else:
                print(f"Invalid layer from URL: {url}")
                print(f"Error: {layer.error().message()}")
                
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    
    return added_layers

# Example usage with a single test URL
test_urls = [
    'https://better-open-data.com/lidar/Ardquin_DSM.tif'
]

# Test single URL first (without prefix)
print("Testing with single URL...")
added_layers = add_rasters_from_urls(test_urls)

# If test successful, update all URLs to remove www.
raster_urls = [clean_url(url) for url in [
'https://www.better-open-data.com/lidar/Ardquin_DSM.tif',
'https://www.better-open-data.com/lidar/Ardquin_DTM.tif',
'https://www.better-open-data.com/lidar/Ardstraw_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Ardstraw_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Ardtole_DSM.tif',
'https://www.better-open-data.com/lidar/Ardtole_DTM.tif',
'https://www.better-open-data.com/lidar/Armagh-Dungannon-Coalisland_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ballinamallard_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Ballinamallard_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Ballycastle_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ballyclare_23_04_2009_DTM.tif',
'https://www.better-open-data.com/lidar/Ballygalley_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ballygowan_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ballymena_23_04_2009_DSM.tif',
'https://www.better-open-data.com/lidar/Ballymena_23_04_2009_DTM.tif',
'https://www.better-open-data.com/lidar/Ballynahinch_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ballynavally_04_04_2007_DTM.tif',
'https://www.better-open-data.com/lidar/Banbridge_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Bangor_04_04_2007_DTM.tif',
'https://www.better-open-data.com/lidar/Belleek_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Belleek_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Beragh_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Beragh_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Black_Pigs_Dyke_DSM.tif',
'https://www.better-open-data.com/lidar/Black_Pigs_Dyke_DTM.tif',
'https://www.better-open-data.com/lidar/Blackwater_16_06_2014_DSM.tif',
'https://www.better-open-data.com/lidar/Blackwater_16_06_2014_DTM.tif',
'https://www.better-open-data.com/lidar/Boneamargy_DSM.tif',
'https://www.better-open-data.com/lidar/Boneamargy_DTM.tif',
'https://www.better-open-data.com/lidar/Burren_03_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Burren_03_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Bushmills_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Cahery_DSM.tif',
'https://www.better-open-data.com/lidar/Cahery_DTM.tif',
'https://www.better-open-data.com/lidar/Camowen_16_06_2014_DSM.tif',
'https://www.better-open-data.com/lidar/Camowen_16_06_2014_DTM.tif',
'https://www.better-open-data.com/lidar/Carrickfergus_04_04_2007_DTM.tif',
'https://www.better-open-data.com/lidar/Carryduff_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Castlederg_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Castlederg_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Castlereagh_04_04_2007_DTM.tif',
'https://www.better-open-data.com/lidar/Cave_Hill_DSM.tif',
'https://www.better-open-data.com/lidar/Cave_Hill_DTM.tif',
'https://www.better-open-data.com/lidar/Charlemont_DSM.tif',
'https://www.better-open-data.com/lidar/Charlemont_DTM.tif',
'https://www.better-open-data.com/lidar/Clady_10_03_2009_DSM.tif',
'https://www.better-open-data.com/lidar/Clady_10_03_2009_DTM.tif',
'https://www.better-open-data.com/lidar/Clandeboye_DSM.tif',
'https://www.better-open-data.com/lidar/Clandeboye_DTM.tif',
'https://www.better-open-data.com/lidar/Clogher_DSM.tif',
'https://www.better-open-data.com/lidar/Clogher_DTM.tif',
'https://www.better-open-data.com/lidar/Cloghmills_16_06_2014_DSM.tif',
'https://www.better-open-data.com/lidar/Cloghmills_16_06_2014_DTM.tif',
'https://www.better-open-data.com/lidar/Cookstown_06_06_2013_DSM.tif',
'https://www.better-open-data.com/lidar/Cookstown_06_06_2013_DTM.tif',
'https://www.better-open-data.com/lidar/Cornashee_DSM.tif',
'https://www.better-open-data.com/lidar/Cornashee_DTM.tif',
'https://www.better-open-data.com/lidar/Crossmurrin_DSM.tif',
'https://www.better-open-data.com/lidar/Crossmurrin_DTM.tif',
'https://www.better-open-data.com/lidar/Cullybackey_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Cushendall_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Devenish_DSM.tif',
'https://www.better-open-data.com/lidar/Devenish_DTM.tif',
'https://www.better-open-data.com/lidar/Dohertys_Tower_DSM.tif',
'https://www.better-open-data.com/lidar/Dohertys_Tower_DTM.tif',
'https://www.better-open-data.com/lidar/Donegore_DSM.tif',
'https://www.better-open-data.com/lidar/Donegore_DTM.tif',
'https://www.better-open-data.com/lidar/Dougary_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Dougary_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Downpatrick_05_05_2009_DSM.tif',
'https://www.better-open-data.com/lidar/Downpatrick_05_05_2009_DTM.tif',
'https://www.better-open-data.com/lidar/Dundrum_DSM.tif',
'https://www.better-open-data.com/lidar/Dundrum_DTM.tif',
'https://www.better-open-data.com/lidar/Dunluce_DSM.tif',
'https://www.better-open-data.com/lidar/Dunluce_DTM.tif',
'https://www.better-open-data.com/lidar/Dunmull_DSM.tif',
'https://www.better-open-data.com/lidar/Dunmull_DTM.tif',
'https://www.better-open-data.com/lidar/Dunmurry_04_04_2007_DTM.tif',
'https://www.better-open-data.com/lidar/Dunseverick_DSM.tif',
'https://www.better-open-data.com/lidar/Dunseverick_DTM.tif',
'https://www.better-open-data.com/lidar/East Belfast_29_05_2013_DSM.tif',
'https://www.better-open-data.com/lidar/East Belfast_29_05_2013_DTM.tif',
'https://www.better-open-data.com/lidar/Eglinton_11_12_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Eglinton_11_12_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Enniskillen_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Enniskillen_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Fintona_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Fintona_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Folk Park Newtownstewart_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Folk Park Newtownstewart_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Foyle_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Foyle_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Garron_DSM.tif',
'https://www.better-open-data.com/lidar/Garron_DTM.tif',
'https://www.better-open-data.com/lidar/Giants_Sconce_DSM.tif',
'https://www.better-open-data.com/lidar/Giants_Sconce_DTM.tif',
'https://www.better-open-data.com/lidar/Glenavy_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Glenavy_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Glynn_DSM.tif',
'https://www.better-open-data.com/lidar/Glynn_DTM.tif',
'https://www.better-open-data.com/lidar/Greyabbey_Ballywalter_DSM.tif',
'https://www.better-open-data.com/lidar/Greyabbey_Ballywalter_DTM.tif',
'https://www.better-open-data.com/lidar/Inch_Abbey_DSM.tif',
'https://www.better-open-data.com/lidar/Inch_Abbey_DTM.tif',
'https://www.better-open-data.com/lidar/Keady_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Keady_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Killyleagh__15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Kiltierney_DSM.tif',
'https://www.better-open-data.com/lidar/Kiltierney_DTM.tif',
'https://www.better-open-data.com/lidar/Larne_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Limavady_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Limavady_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Linford_DSM.tif',
'https://www.better-open-data.com/lidar/Linford_DTM.tif',
'https://www.better-open-data.com/lidar/Lisbellaw_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Lisbellaw_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Lisburn_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Londonderry_30_04_2009_DTM.tif',
'https://www.better-open-data.com/lidar/LowerBann_16_06_2014_DSM.tif',
'https://www.better-open-data.com/lidar/LowerBann_16_06_2014_DTM.tif',
'https://www.better-open-data.com/lidar/Lurgan_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Lurgan_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Lyles_Hill_DSM.tif',
'https://www.better-open-data.com/lidar/Lyles_Hill_DTM.tif',
'https://www.better-open-data.com/lidar/Maghera_20_04_2009_DSM.tif',
'https://www.better-open-data.com/lidar/Maghera_20_04_2009_DTM.tif',
'https://www.better-open-data.com/lidar/Magherafelt_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Magheramore_DSM.tif',
'https://www.better-open-data.com/lidar/Magheramore_DTM.tif',
'https://www.better-open-data.com/lidar/Maguiresbridge_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Maguiresbridge_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Mobuoy_DSM.tif',
'https://www.better-open-data.com/lidar/Mobuoy_DTM.tif',
'https://www.better-open-data.com/lidar/Moneymore_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Moneymore_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Mossley_05_03_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Mossley_05_03_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Mount_Stewart_DSM.tif',
'https://www.better-open-data.com/lidar/Mount_Stewart_DTM.tif',
'https://www.better-open-data.com/lidar/Navan_DSM.tif',
'https://www.better-open-data.com/lidar/Navan_DTM.tif',
'https://www.better-open-data.com/lidar/Newcastle_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Newry_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Newtownards_10_06_2008_DSM.tif',
'https://www.better-open-data.com/lidar/Newtownards_10_06_2008_DTM.tif',
'https://www.better-open-data.com/lidar/Newtownstewart_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Newtownstewart_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Omagh_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Omagh_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Omagh_Town_11_12_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Omagh_Town_11_12_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Portadown_27_04_2009_DSM.tif',
'https://www.better-open-data.com/lidar/Portadown_27_04_2009_DTM.tif',
'https://www.better-open-data.com/lidar/PortadownExtension_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/PortadownExtension_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Raholp_DSM.tif',
'https://www.better-open-data.com/lidar/Raholp_DTM.tif',
'https://www.better-open-data.com/lidar/Randalstown_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/Ringreagh_DSM.tif',
'https://www.better-open-data.com/lidar/Ringreagh_DTM.tif',
'https://www.better-open-data.com/lidar/Saintfield_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/Saintfield_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Saul_DSM.tif',
'https://www.better-open-data.com/lidar/Saul_DTM.tif',
'https://www.better-open-data.com/lidar/Scrabo_DSM.tif',
'https://www.better-open-data.com/lidar/Scrabo_DTM.tif',
'https://www.better-open-data.com/lidar/SionMills_02_02_2012_DSM.tif',
'https://www.better-open-data.com/lidar/SionMills_02_02_2012_DTM.tif',
'https://www.better-open-data.com/lidar/Slemish_DSM.tif',
'https://www.better-open-data.com/lidar/Slemish_DTM.tif',
'https://www.better-open-data.com/lidar/Slemish_DTM.tif',
'https://www.better-open-data.com/lidar/Stonyford_16_06_2014_DSM.tif',
'https://www.better-open-data.com/lidar/Strabane_23_05_2004_DSM.tif',
'https://www.better-open-data.com/lidar/Strabane_23_05_2004_DTM.tif',
'https://www.better-open-data.com/lidar/Struell_DSM.tif',
'https://www.better-open-data.com/lidar/Struell_DTM.tif',
'https://www.better-open-data.com/lidar/Tandragee_15_03_2010_DTM.tif',
'https://www.better-open-data.com/lidar/The_Dorsey_DSM.tif',
'https://www.better-open-data.com/lidar/The_Dorsey_DTM.tif',
'https://www.better-open-data.com/lidar/Tirgoland_DSM.tif',
'https://www.better-open-data.com/lidar/Tirgoland_DTM.tif',
'https://www.better-open-data.com/lidar/Tullaghoge_DSM.tif',
'https://www.better-open-data.com/lidar/Tullaghoge_DTM.tif',
]]

# Uncomment to load all layers after successful test:
# added_layers = add_rasters_from_urls(raster_urls, "LIDAR")

