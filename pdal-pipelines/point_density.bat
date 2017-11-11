@echo off
setlocal
set "LASdir=G:\Olympics\snow-on\29-30_Mar_2016\las\filtered_las"
set "PIPELINE=C:\Users\Steven\OneDrive\Documents\School Stuff\UW\Mountain Hydrology Research Group\PDAL\pipelines\first_return_point_density.json"
set "LASext=las"
pushd %LASdir%
for /R %LASdir% %%f in (*.%LASext%) do (
echo %%f
pdal pipeline "%PIPELINE%"^
 --readers.las.filename="%%f"^
 --writers.gdal.filename="G:\%%~nf_1STreturn_pointDensity_10m.tif"
)
endlocal