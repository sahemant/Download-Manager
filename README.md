# Download-Manager
Download Files from Internet at maximum speed possible

# Requirements
Any Windows System with Python v2 Installed

# Usage
Simpy Run the Python File from Command Prompt by passed file URL as an argument. Downloaded file will be available in C:/Downloads <br/>
```bash
C:\Users\noobmaster69\download-Manager>py -2 downloader.py http://director.downloads.raspberrypi.org/rpd_x86/images/rpd_x86-2019-04-12/2019-04-11-rpd-x86-stretch.iso
```

# Stats
Above example contains URL for raspberry pi os iso file which is of 2.4GB<br/>
```bash
Download-Manager : ~2.6 Mins
Chrome           : ~6 Mins
```
![CAPTURE](/docs/Capture.JPG)

# Info
This Program downloads file by creating Multiple Threads and downloads Chunks of data.
As there are many Threads most of the available bandwidth is used by our program.<br/>

# Note
This works only for the URLs that support downloading in CHUNKS <br/>
