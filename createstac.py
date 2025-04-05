import os
import rasterio
import pystac
from pystac.extensions.projection import ProjectionExtension
from datetime import datetime
from pathlib import Path

def create_stac_catalog(geotiff_dir, base_url, catalog_title="better-open-data.com STAC Catalog", output_dir="stac-catalog"):
    geotiff_dir = Path(geotiff_dir)
    output_dir = Path(output_dir)
    catalog = pystac.Catalog(id="better-open-data.com", description=catalog_title)

    collection = pystac.Collection(
        id="lidar-collection",
        description="A collection of LiDAR GeoTIFF files (COGs) with EPSG:29902 CRS",
        extent=pystac.Extent(
            spatial=pystac.SpatialExtent([[-180.0, -90.0, 180.0, 90.0]]),
            temporal=pystac.TemporalExtent([[datetime.utcnow(), None]])
        ),
        license="OGL V3"
    )
    catalog.add_child(collection)

    for geotiff_path in geotiff_dir.glob("*.tif"):
        with rasterio.open(geotiff_path) as dataset:
            bounds = dataset.bounds
            bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
            datetime_str = datetime.utcnow().isoformat() + "Z"

            item_id = geotiff_path.stem
            item = pystac.Item(
                id=item_id,
                geometry={
                    "type": "Polygon",
                    "coordinates": [[
                        [bounds.left, bounds.bottom],
                        [bounds.left, bounds.top],
                        [bounds.right, bounds.top],
                        [bounds.right, bounds.bottom],
                        [bounds.left, bounds.bottom]
                    ]]
                },
                bbox=bbox,
                datetime=datetime.utcnow(),
                properties={}
            )

            # Add projection extension with EPSG code
            ProjectionExtension.add_to(item)
            proj = ProjectionExtension.ext(item)
            proj.epsg = 29902

            # Full asset URL using the base URL
            asset_url = f"{base_url.rstrip('/')}/{geotiff_path.name}"

            item.add_asset(
                key="cog",
                asset=pystac.Asset(
                    href=asset_url,
                    media_type=pystac.MediaType.COG,
                    roles=["data"]
                )
            )

            collection.add_item(item)

    # Set catalog root href to base URL (for link generation)
    catalog.set_self_href(f"{base_url.rstrip('/')}/catalog.json")

    # Save to local directory but with absolute URLs pointing to base_url
    catalog.normalize_and_save(
        root_href=str(output_dir),
        catalog_type=pystac.CatalogType.ABSOLUTE_PUBLISHED
    )

    original_path = "/Users/alexdonald/Downloads/stac"
    replacement_url = "https://better-open-data.com/lidar"
    for json_file in output_dir.rglob("*.json"):
        try:
            print(f"Processing: {json_file}")
            
            # Read the file content
            with open(json_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if the original path exists in the content
            if original_path in content:
                # Replace the path
                updated_content = content.replace(original_path, replacement_url)
                
                # Write the updated content back to the file
                with open(json_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                
                print(f"✓ Updated: {json_file}")
            else:
                print(f"- No replacements needed in: {json_file}")
                
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
    
    print("Path replacement completed!")


    print(f"STAC catalog created at {output_dir.resolve()}")
    print(f"🔗 All local hrefs updated to use base URL: {base_url.rstrip('/')}")


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a STAC catalog from GeoTIFF files.")
    parser.add_argument("geotiff_folder", help="Path to the folder containing GeoTIFF files.")
    parser.add_argument("base_url", help="Base URL where the GeoTIFFs will be hosted.")
    parser.add_argument("--output", default="stac-catalog", help="Output directory for the STAC catalog.")
    args = parser.parse_args()

    create_stac_catalog(args.geotiff_folder, args.base_url, output_dir=args.output)


# python create_stac_from_geotiffs.py lidar https://better-open-data.com/lidar --output stac
