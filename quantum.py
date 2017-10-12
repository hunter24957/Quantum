import xbmcaddon
import xbmcgui
import requests
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = "Hello world"
line2 = "We can write anything we want here"
line3 = "Using Python"
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)
