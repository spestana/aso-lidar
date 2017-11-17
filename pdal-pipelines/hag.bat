@echo off
setlocal
set "LASdir=G:\10m_hag"
set "PIPELINE=C:\Users\Steven\OneDrive\Documents\School Stuff\UW\Mountain Hydrology Research Group\PDAL\pipelines\hag.json"
set "LASext=las"
pushd %LASdir%
for /R %LASdir% %%f in (*.%LASext%) do (
echo %%f
pdal pipeline "%PIPELINE%"^
 --readers.las.filename="%%f"^
 --writers.gdal.filename="G:\%%~nf_hag_10m.tif"
)
endlocal