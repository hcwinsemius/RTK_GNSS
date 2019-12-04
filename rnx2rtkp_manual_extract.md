# Excerpt from RTKLIB manual for rnx2rtkp

## SYNOPSIS

```rnx2rtkp [option ...] file file [...]```
 
## DESCRIPTION
Read  RINEX  OBS/NAV/GNAV/HNAV/CLK,  SP3,  SBAS  message  log  files  and  compute  receiver  (rover) positions and output position solutions.

The  first  RINEX  OBS  file  shall  contain  receiver  (rover)  observations.  For  the  relative  mode,  the  second RINEX  OBS  file  shall  contain  reference  (base  station)  receiver  observations.  At  least  one  RINEX NAV/GNAV/HNAV file shall be included in input files. To use SP3 precise ephemeris, specify the path in the  files.  The  extension  of  the  SP3  file  shall  be .sp3   or  .eph .  All  of  the  input  file  paths  can  include wild‐cards ( * ). To avoid command line deployment of wild‐cards, use ʺ...ʺ for paths with wild‐cards.

Command line options are as follows ([]:default). With ‐k option, the processing options are input from the configuration  file.  In  this  case,  command  line  options  precede  options  in  the  configuration  file.  For  the configuration file, refer B.4. 
 
OPTIONS
```
-? print help
-k file input options from configuration file [off]
-o file set output file [stdout]
-ts ds ts start day/time (ds=y/m/d ts=h:m:s) [obs start time]
-te de te end day/time
(de=y/m/d te=h:m:s) [obs end time]
-ti tint time interval (sec) [all]
-p mode mode (0:single,1:dgps,2:kinematic,3:static,4:moving-base,
5:fixed,6:ppp-kinematic,7:ppp-static) [2]
-m mask elevation mask angle (deg) [15]
-f freq number of frequencies for relative mode (1:L1,2:L1+L2,3:L1+L2+L5) [2]
-v thres validation threshold for integer ambiguity (0.0:no AR) [3.0]
-b backward solutions [off]
-c forward/backward combined solutions [off]
-i instantaneous integer ambiguity resolution [off]
-h fix and hold for integer ambiguity resolution [off]
-e output x/y/z-ecef position [latitude/longitude/height]
-a output e/n/u-baseline [latitude/longitude/height]
```