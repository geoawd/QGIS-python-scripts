import os
import zipfile
from osgeo import gdal
import requests


class ZipRasterProcessor:
    def __init__(self, url_list, output_dir):
        self.url_list = url_list
        self.output_dir = output_dir
        self.projection = 'EPSG:29902'

    def download_zip(self, url, output_path):
        if os.path.exists(output_path):
            print(f"File already exists: {output_path}. Skipping download.")
            return
        try:
            r = requests.get(url)
            with open(output_path, 'wb') as f:
                f.write(r.content)
                
            with open('processed/logfile.txt', 'a') as f:
                f.write(url + '\n')
                print(f"Downloaded and logged: {url}")
            
        except Exception as e:
            print(e)

    def process_zip(self, zip_path):
        if not os.path.exists(zip_path):
            print(f"ZIP file not found: {zip_path}. Skipping processing.")
            return
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                base_folder = os.path.commonpath([name for name in z.namelist() if name.endswith('/')]).split('/')[0]

                for folder_prefix in ['DSM', 'DTM']:
                    folder_files = [f for f in z.namelist() if f"{folder_prefix}" in f and f.endswith('.asc') and 'ITM' not in f]
                    print(folder_files)

                    if not folder_files:
                        print(f"No files found in {folder_prefix} folder within {zip_path}")
                        continue

                    vrt_path = self.create_virtual_raster(z, folder_files, folder_prefix)
                    self.convert_to_cog(vrt_path, folder_prefix, zip_path)
        except zipfile.BadZipFile as e:
            print(f"Bad zip file: {zip_path}. Error: {e}")

    def delete_zip(self, zip_path):
        try:
            os.remove(zip_path)
            print(f"Deleted ZIP file: {zip_path}")
        except OSError as e:
            print(f"Error deleting file {zip_path}: {e}")

    def create_virtual_raster(self, zip_file, file_list, folder_name):
        vrt_options = gdal.BuildVRTOptions()
        vrt_path = os.path.join(self.output_dir, f"{os.path.basename(zip_file.filename).replace('.zip', '')}_{folder_name}.vrt")
        
        tif_files = []
        for file in file_list:
            with zip_file.open(file) as src:
                tif_files.append(f'/vsimem/{file}')
                gdal.FileFromMemBuffer(f'/vsimem/{file}', src.read())
        
        gdal.BuildVRT(vrt_path, tif_files, options=vrt_options)
        return vrt_path

    def convert_to_cog(self, vrt_path, folder_name, zip_path):
        cog_path = os.path.join(self.output_dir, f"{os.path.basename(zip_path).replace('.zip', '')}_{folder_name}.tif")
        
        translate_options = gdal.TranslateOptions(format='COG', creationOptions=["COMPRESS=LZW", "NUM_THREADS=ALL_CPUS"],
                                                  outputSRS=self.projection)
        
        gdal.Translate(cog_path, vrt_path, options=translate_options)
        print(f"Converted to COG: {cog_path}")

    def run(self):
        for url in self.url_list:
            zip_file_name = os.path.basename(url.strip())
            zip_path = os.path.join(self.output_dir, zip_file_name)
            
            # Download the zip file
            self.download_zip(url, zip_path)
            
            # Process the downloaded zip file
            self.process_zip(zip_path)
            
            # Delete the zip file
            self.delete_zip(zip_path)



url_list = [
'https://opendatani.blob.core.windows.net/lpslidar/Castlederg_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Foyle_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Limavady_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Newtownstewart_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Omagh_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Strabane_23_05_2004.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballynavally_04_04_2007.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Bangor_04_04_2007.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Carrickfergus_04_04_2007.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Castlereagh_04_04_2007.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Dunmurry_04_04_2007.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Newtownards_10_06_2008.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballyclare_23_04_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballymena_23_04_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Clady_10_03_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Downpatrick_05_05_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Londonderry_30_04_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Maghera_20_04_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Portadown_27_04_2009.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballycastle_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballygalley_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballygowan_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballynahinch_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Banbridge_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Bushmills_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Carryduff_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Cullybackey_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Cushendall_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Killyleagh__15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Larne_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Lisburn_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Magherafelt_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Newcastle_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Newry_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Newtownabbey_15_03_2010.zip  ',
'https://opendatani.blob.core.windows.net/lpslidar/Randalstown_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Tandragee_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ardstraw_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Ballinamallard_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Belleek_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Beragh_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Burren_03_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Dougary_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Eglinton_11_12_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Enniskillen_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Fintona_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Glenavy_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Keady_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Lisbellaw_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Lurgan_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Maguiresbridge_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Moneymore_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Mossley_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Omagh_Town_11_12_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Saintfield_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Sion Mills_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Cookstown_06_06_2013.zip',
'https://opendatani.blob.core.windows.net/lpslidar/East Belfast_29_05_2013.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Blackwater_16_06_2014.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Camowen_16_06_2014.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Cloghmills_16_06_2014.zip',
'https://opendatani.blob.core.windows.net/lpslidar/LowerBann_16_06_2014.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Stonyford_16_06_2014.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Armagh-Dungannon-Coalisland_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Coleraine-Portstewart_15_03_2010.zip',
'https://opendatani.blob.core.windows.net/lpslidar/BangorExtension_05_03_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/Folk Park Newtownstewart_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/lpslidar/PortadownExtension_02_02_2012.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Ardquin.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Ardtole.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Black%20Pigs%20Dyke.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Bonamargy.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Cahery.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Cave%20Hill.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Charlemont.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Clandeboye.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Clogher.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Cornashee.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Crossmurrin.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Devenish.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Dohertys%20Tower.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Donegore.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Dundrum.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Dunluce.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Dunmull.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Dunseverick.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Garron.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Giants%20Sconce.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Glynn.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Greyabbey%20%26%20Ballywalter.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Inch%20Abbey.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Kiltierney.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Linford.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Lyles%20Hill.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Magheramore.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Mobuoy.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Mount%20Stewart.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Navan.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Raholp.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Ringreagh.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Saul.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Scrabo.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Slemish.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Struell.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/The%20Dorsey.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Tirgoland.zip',
'https://opendatani.blob.core.windows.net/archaeologylidar/Tullaghoge.zip',
]


output_dir = 'processed'

logfile_path = os.path.join(output_dir, 'logfile.txt')
with open(logfile_path, 'r') as f:
    log_content = f.read().splitlines()

for url in url_list:
    if url.strip() not in log_content:
        print(f"Processing URL: {url}")
        processor = ZipRasterProcessor([url], output_dir)
        processor.run()
    else:
        print(f"URL already processed: {url}. Skipping download.")
