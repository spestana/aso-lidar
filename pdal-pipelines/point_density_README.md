# ASO Olympics Lidar Point Density
###### spestana@uw.edu
---

The point density of a lidar dataset can be quantified as the average number of laser pulse return signals detected per unit area. Alternatively, this can also be reported as a linear measurement of the average spacing between points. Point density of lidar data acquired from an aircraft is a function of instrument parameters and aircraft motion. The instrument's laser pulse rate, and scan rate (the oscillating or rotating mirror's angular velocity) can provide information about the minimum cross-track point spacing. The down-track point spacing is controlled by the aircraft's ground speed, the instrument's scan rate, and scan pattern. The scan angles covered by the instrument, the aircraft's altitude (AGL), and the flight line control the overlapping of ground tracks (swath width) that can greatly increase point density and help to minimize errors by scanning locations from multiple angles. [1] Point density can change at a finer scale within a single flight line as changes in aircraft pitch can cause scan line overlaps or gaps. Surfaces closer to normal with the incident laser pulse (smaller angle of incidence) can return higher intensity reflections, 

![alt text](source to image "image title text")

* a.	Lidar “shadow” between steep rock outcrops with very low point density (Little Mystery)
* b.	Bright (higher point density) band possibly from slight change in aircraft speed or pitch causing scan line overlaps
* c.	Region within flight line overlaps with higher overall average point density
* d.	Low point density nearest to river surface (Dosewallips River)

The point density of a lidar product provides information about how the data can be used in further analysis, and if special considerations need to be made in areas of greatly differing point density. Many applications utilizing lidar data rely on creating a digital surface model (DSM) from the collected point cloud (such as in the case of determining snow depth by subtracting snow-off from snow-on DSMs). These DSM are created by methods of interpolation (such as inverse distance weighting, IDW) between observed points. The resulting DSM grid element size should match the magnitude of the average point spacing (a measure of point density). Performing interpolation with low point density data can lead to a smoother DSM and the loss of sub-grid features. [1]

Errors in measured lidar points can be introduced from the instrument itself, complex or sloping terrain, thick vegetation, and absorptive or scattering surfaces. Instrument/aircraft position errors from the GPS/INS (< 0.1 m) are of smaller magnitude than external error sources (0.1 - 0.5 m). Steeply sloping terrain can induce apparent errors in the Z (height) direction when errors (from other sources) occur in X and/or Y. Similarly, "timewalk" errors occur when a diverged laser beam reflects off a steep slope, causing a delay in the return time of the wavepacket intensity threshold for a discrete return, and an over-estimate in the distance to the measured point. Minimizing the number of laser pulses with large incidence angles (such as nadir pulses onto steep slopes) can help avoid these types of errors (which can be on the order of 0.5 m). Thick vegetation can make determining the ground surface beneath the vegetation more difficult and introduce errors on the order of 0.1 m. Regarding the measurement of surfaces coated in snow and ice, changes in grain size can alter the returned wavepacket intensity, and can introduce further errors. [1]




where the data came from
- ASO - JPL --> website link
- dates of flights, location of flights
- Data set requirements (citation?)
-- 1st return Nominal Point Spacing (NPS) = 0.3 m (12 pts/m^2) ???
-- Ground NPS = 0.5m (4pts/m^2)??
-- lambda (wavelength) = 1064 nm (NIR) which provides high snow reflectance, minimal penetration depth (reference and figures?)
- las files have filtered discrete returns from return wavepacket (where the wavepacket exceeded a certain threshold) (citation from workflow flowchart)
- 1 las file per flightline
- snow free areas (from CASI) force the lidar snowdepth data to zero in those areas
and how it was obtained
 (Lidar Altimetry - Deems SnowEx 2016)
 - look @ table of flight altitudes, pulse rates, footprint sizes, swath widths etc.
a little bit of background on lidar?
(Lidar Measurement of Snow Depth Accuracy and Error Sources - Deems, Painter)
- lidar calculates distance by return time of flight of reflected laster (using GPS, INS)
- laser beam divergence ~0.3-1 rad ... ~0.3-1m @ 1000m AGL
- divergence allows multiple returns (fraction of footprint reflects off diferent objects)
-- "waveform" returned from the reflection can be split into descrete returns with a certain reflection intensity threshold
- (citation?) -- instrument documentation?
-- 800kHz pulse rate
-- 2 lasers, fore/aft pointing?
-- 5000m AGL range
-- beam divergence (25cm / 1000m)



 
how I prepared the data pre-processing
any calculations made, tools used

why i chose the particular techniques used

problems anticipated with method,
things i did to prevent them from occurring
or how they were minimized
or why these problems do not impact in any meaningful way


what I did, 
calculations made, 
tools used



does this agree with values others have reported,
does this agree with the values stated in ASO docs?
---

Used LAStools Lastile to split large .las files into tiles.



# Workflow
---

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

