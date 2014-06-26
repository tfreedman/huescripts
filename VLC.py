#!/usr/bin/python

from AppKit import NSWorkspace
from AppKit import NSWindow
import Quartz.CoreGraphics as CG
from time import sleep

from phue import Bridge
b = Bridge('YOUR.IP.ADDRESS.HERE')

# Get a dictionary with individual light numbers as the key (1,2,3,etc.)
lights = b.get_light_objects('id')

# Get a dictionary with the each light's name as the key (Kitchen, Bedroom, etc.)
light_names = b.get_light_objects('name')

# Get a flat list of the light objects
light_list = b.get_light_objects('list')

# Will turn on all lights in system
def all_on():
  b.set_light(lights,'on',True)

# Will turn off all lights in system
def all_off():
  b.set_light(lights,'on',False)

is_on = 1

while True:  
  windlst = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionAll, CG.kCGNullWindowID)
  tgtwind = None
  for w in windlst:
    tgtwind = w
    w = int(tgtwind['kCGWindowBounds']['Width'])
    h = int(tgtwind['kCGWindowBounds']['Height'])
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    if tgtwind['kCGWindowOwnerName'] == "VLC" and 'kCGWindowIsOnscreen' in tgtwind and tgtwind['kCGWindowIsOnscreen'] == 1 and is_on == 1 and w == 2560 and h == 1440:
        print "All Off!"
        all_off()
        is_on = 0
    elif is_on == 0:
      if tgtwind['kCGWindowOwnerName'] != "VLC" and activeAppName != "VLC":
        print "All On! >> 1"
        all_on()
        is_on = 1
      elif (tgtwind['kCGWindowOwnerName'] == "VLC" and 'kCGWindowName' in tgtwind and tgtwind['kCGWindowName'] != "Window" and activeAppName == "VLC" and 'kCGWindowIsOnscreen' in tgtwind and tgtwind['kCGWindowIsOnscreen'] == 1 and w != 2560 and h != 1440):
        print "All On! >> 2"      
        all_on()      
        is_on = 1
  sleep(1)
