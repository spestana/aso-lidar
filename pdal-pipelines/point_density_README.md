# Lidar Point Density Workflow
###### spestana@uw.edu

### First Return Point Density Pipeline (_first_return_point_density.json_)
* Input and output filepaths are substituted in batch run
* Using [filters.range](https://www.pdal.io/stages/filters.range.html) to select first returns:
  * `limits` - selecting only the first returns (range from 1 to 1)
* Using [writers.gdal](https://www.pdal.io/stages/writers.gdal.html) to write out raster image
  * `resolution` - pixel side length in units of original las file (use [lasinfo](https://rapidlasso.com/lastools/lasinfo/) or [pdal info](https://www.pdal.io/apps/info.html) to get file metadata and statistics)
  * `output_type` - "count" for number of points within each pixel ([other options](https://www.pdal.io/stages/writers.gdal.html#options))
  * `gdaldriver` - GeoTiff
  
```
{
  "pipeline":[
	"input.las",
    {
	  "tag" : "firstReturns",
      "type" : "filters.range",
      "limits" : "ReturnNumber[1:1]"
    },
    {
	  "tag" : "densityRaster",
      "type" : "writers.gdal",
	  "inputs" : [
					"firstReturns"
				 ],
	  "resolution": 10,
	  "output_type" : "count",
	  "gdaldriver" : "GTiff",
      "filename" : "output.tif"
    }
  ]
}
```

### Batch Script (_point_density.bat_)
* Find files to process: (CAUTION - All files matching LASdir and LASext will be processed)
  * `LASdir` - set to directory containing files to process
  * `LASext` - file extention (.las or .laz) to identify files to process in LASdir
* `PIPELINE` - point to .json pipeline file to run each .las file through
* Change output filename by editing the line ` --writers.gdal.filename="G:\%%~nf_xxxxxx.tif"`
* Run 

```
@echo off
setlocal
set "LASdir=C:\lasfiles_to_process"
set "PIPELINE=C:\pdal-pipelines\first_return_point_density.json"
set "LASext=las"
pushd %LASdir%
for /R %LASdir% %%f in (*.%LASext%) do (
echo %%f
pdal pipeline "%PIPELINE%"^
 --readers.las.filename="%%f"^
 --writers.gdal.filename="G:\%%~nf_1STreturn_pointDensity_10m.tif"
)
endlocal
```

---

