Python Explore Modules Func Tool

Usage   : pyproperty <module>
Example : pyproperty os
          pyproperty sys

Example Output : 

pyproperty time


         Module : time

Module : time.CLOCK_MONOTONIC | Output : 1
Module : time.CLOCK_MONOTONIC_RAW | Output : 4
Module : time.CLOCK_PROCESS_CPUTIME_ID | Output : 2
Module : time.CLOCK_REALTIME | Output : 0
Module : time.CLOCK_THREAD_CPUTIME_ID | Output : 3
Module : time._STRUCT_TM_ITEMS | Output : 11
Module : time.__doc__ | Output : This module provides various functions to manipulate time values.

There are two standard representations of time.  One is the number
of seconds since the Epoch, in UTC (a.k.a. GMT).  It may be an integer
or a floating point number (to represent fractions of seconds).
The Epoch is system-defined; on Unix, it is generally January 1st, 1970.
The actual value can be retrieved by calling gmtime(0).

The other representation is a tuple of 9 integers giving local time.
The tuple items are:
  year (including century, e.g. 1998)
  month (1-12)
  day (1-31)
  hours (0-23)
  minutes (0-59)
  seconds (0-59)
  weekday (0-6, Monday is 0)
  Julian day (day in the year, 1-366)
  DST (Daylight Savings Time) flag (-1, 0 or 1)
If the DST flag is 0, the time is given in the regular time zone;
if it is 1, the time is given in the DST time zone;
if it is -1, mktime() should guess based on the date and time.

Module : time.__loader__ | Output : <class '_frozen_importlib.BuiltinImporter'>
Module : time.__name__ | Output : time
Module : time.__package__ | Output : 
Module : time.__spec__ | Output : ModuleSpec(name='time', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in')
Module : time.altzone | Output : -10800
Module : time.asctime | Output : <built-in function asctime>
Module : time.clock | Output : <built-in function clock>
Module : time.clock_getres | Output : <built-in function clock_getres>
Module : time.clock_gettime | Output : <built-in function clock_gettime>
Module : time.clock_settime | Output : <built-in function clock_settime>
Module : time.ctime | Output : <built-in function ctime>
Module : time.daylight | Output : 0
Module : time.get_clock_info | Output : <built-in function get_clock_info>
Module : time.gmtime | Output : <built-in function gmtime>
Module : time.localtime | Output : <built-in function localtime>
Module : time.mktime | Output : <built-in function mktime>
Module : time.monotonic | Output : <built-in function monotonic>
Module : time.perf_counter | Output : <built-in function perf_counter>
Module : time.process_time | Output : <built-in function process_time>
Module : time.sleep | Output : <built-in function sleep>
Module : time.strftime | Output : <built-in function strftime>
Module : time.strptime | Output : <built-in function strptime>
Module : time.struct_time | Output : <class 'time.struct_time'>
Module : time.time | Output : <built-in function time>
Module : time.timezone | Output : -10800
Module : time.tzname | Output : ('+03', '+03')
Module : time.tzset | Output : <built-in function tzset>
