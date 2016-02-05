"""
This is simple script to invoke parallel conversion function from um2grb2
and pass the assimilated / forecasted hour as argument.

UTC : 12Z
fcst hour : 006hr, 012hr, 018hr, ..., 234hr, 240hr
Output : It creates forecast - 40 files 
         (um_prg_006hr_date_12Z.grib2, ..., um_prg_240hr_date_12Z.grib2).
Written by : Arulalan.T
Date : 19.Jan.2016
"""

import os, sys, datetime
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from loadconfigure import inPath, outPath, tmpPath, date, loadg2utils, \
                   debug, targetGridResolution, overwriteFiles, neededVars, \
                   requiredLat, requiredLon, max_long_fcst_hours_at_12z

if loadg2utils == 'system':
    # Load g2utils from system python which has installed through setup.py
    from g2utils.um2grb2 import convertFcstFiles
    print "INFO : imported g2utils.um2grb2 from system python"
elif loadg2utils == 'local':
    # Load g2utils from previous directory for the operational purpose, 
    # where normal user don't have write permission to change the g2utils!
    g2utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            '../g2utils'))
    sys.path.append(g2utils_path)
    from um2grb2 import convertFcstFiles
    print "INFO : imported g2utils.um2grb2 from local previous directory"
    print "loaded from g2utils_path : ", g2utils_path
    
if isinstance(date, tuple):
    # Got tuple of date string.
    startdate, enddate = date
    sDay = datetime.datetime.strptime(startdate, "%Y%m%d")
    eDay = datetime.datetime.strptime(enddate, "%Y%m%d")
    lag = datetime.timedelta(days=1)
    print "Got tuple dates"
    print "So um2grb2 ana 00hr conversion - from %s to %s" % (startdate, enddate)
    while sDay <= eDay:
        # loop through until startdate incremented upto enddate
        print "Going to start progress on", startdate
        # call forecast conversion function w.r.t data assimilated 
        # during long forecast hour - 12UTC.
        convertFcstFiles(inPath, outPath, tmpPath, 
                        targetGridResolution=targetGridResolution, 
                 date=startdate, utc='12', convertVars=neededVars,
                      latitude=requiredLat, longitude=requiredLon, 
                   max_long_fcst_hours=max_long_fcst_hours_at_12z,
                           overwrite=overwriteFiles, lprint=debug)
        print "Time lag incremented by 1"
        sDay += lag
        startdate = sDay.strftime('%Y%m%d')
    # end of while sDay <= eDay:
    print "Successfully completed all the dates till", enddate
elif isinstance(date, str):
    # only single date 
    # call forecast conversion function w.r.t data assimilated 
    # during long forecast hour - 00UTC.
    print "um2grb2 fcst conversion - date", date
    convertFcstFiles(inPath, outPath, tmpPath, 
                        targetGridResolution=targetGridResolution, 
                      date=date, utc='12', convertVars=neededVars, 
                      latitude=requiredLat, longitude=requiredLon,
                   max_long_fcst_hours=max_long_fcst_hours_at_12z,
                           overwrite=overwriteFiles, lprint=debug)
# end of if isinstance(date, tuple):