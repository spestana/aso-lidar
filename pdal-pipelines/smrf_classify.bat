@echo off
setlocal
set "LASdir=G:\Olympics\snow-on\8-9_Feb_2016\las\filtered_las"
set "LASext=las"
pushd %LASdir%
for /R %LASdir% %%f in (*.%LASext%) do (
echo %%f
pdal translate "%%f"^
 -o "G:\smrf classified\%%~nf_smrf_classified.las"^
 smrf -v 4
)
endlocal