# Notes on PDAL Pipelines
###### spestana@uw.edu

[_PDAL - Point Data Abstraction Library_](https://www.pdal.io/)

### Splitting LAS Files
* Specify input filepath
* Use [filters.divider](https://www.pdal.io/stages/filters.divider.html) with the following options:
  * `mode` - "partition" (default) or "round_robin" processing
  * `count` - Provide number of output files to create from single input
  * `capacity` - Alternatively, provide the number of points to be contained in each output file
* Use [writers.las](https://www.pdal.io/stages/writers.las.html) to write out new las files
  * `filename` - include "#" character in output filename for incremental numbering of split files

```
{
  "pipeline":[
    "\input\filepath\filename.las",
    {
      "tag" : "splitLasFile",
      "type" : "filters.divider",
      "mode" : "partition",
      "count" : "10"
    },
    {
      "tag" : "writeOutLasSplits",
      "type":"writers.las",
      "filename":"\output\filepath\filename_split_#.las"
    }
  ]
}
```

### Filter Discrete Returns
* [filters.range](https://www.pdal.io/stages/filters.range.html) simple filter for specified dimension(s):
  * `limits` - dimension name and range to include 
    * _e.g._ filter to values of R where x <= R <= y --> "R[x:y]
    * _e.g._ filter to values of R where R is NOT a < R <= b --> "R!(a:b]"

```
 ...
    {
      "tag" : "filterReturns",
      "type" : "filters.range",
      "limits" : "ReturnNumber[1:1]"
    },
 ...
```

### Write Out a Raster
* [writers.gdal](https://www.pdal.io/stages/writers.gdal.html) GDAL raster writer:
  * `resolution` - length of raster pixel edges (in same units as x,y from las file)
  * `radius` - radius from pixel center to calculate pixel value (default radius = resolution * sqrt(2))
  * `dimension` - value of pixel to output taken from points within the pixel (min, max, mean, idw, count, or stdev)
  * `gdaldriver` - "GTiff" for GeoTiff (default)
  * `filename` - output filename for raster
  * see online documentation for further optional parameters

```
 ...
   {
      "tag" : "pointDensityRaster",
      "type" : "writers.gdal",
      "resolution": 10,
      "output_type" : "count",
      "gdaldriver" : "GTiff",
      "filename" : "pointDensityRater_10m.tif"
    }
 ...
```

### Specifying Pipeline Command Inputs
* Within a [pipeline](https://www.pdal.io/pipeline.html) JSON file, outputs from one step can be used as inputs for following steps by use of the "inputs" option:
  * `tag` - provide a tag name for previous steps to reference in later input arrays
  * `inputs` specifies an array of tags from previous steps to use as inputs for the current step

```
 ...
    {
    ...
      "tag" : "firstStep",
    ...
    },
    {
    ...
      "tag" : "secondStep",
    ...
    },
    {
    ...
      "tag" : "lastStep"
      "inputs" : [
                    "firstStep",
                    "secondStep"
                 ],
    ...
    }
 ...
```

---

# Executing Pipelines
* From a terminal, call up the pipeline json file that is to be executed
  * (Optionally include variables as arguments)
```
    pdal pipeline filename.json
```

# DTMs
#### Extracting ground points
```
pdal translate "input_file.las" -o "output_file.las" smrf range --filters.range.limits="Classification[2:2]" -v 4
```

#### Extracting Non-ground points
```
pdal translate "input_file.las" -o "output_file.las" smrf range --filters.range.limits="Classification![2:2]" -v 4
```

#### Writing to raster GeoTiff

```
{
    "pipeline": [
        "input_filename.las",
        {   
		    "type" : "writers.gdal",
			"gdaldriver" : "Gtiff",
            "resolution": 5,
            "filename":"output_filename.tif"
        }
     ]
}
```

#### LAStools - lasdiff
```
lasdiff -i "input_ground_surface.las" -i "input_nonground_surface.las" -o "output_diff.las"
```