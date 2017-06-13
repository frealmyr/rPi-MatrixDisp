import time
import datetime
import lxml.etree as etree
from threading import Thread
import urllib
import lcddriver # For writing to 4x20 LCD display

def threehourforecase(grab_weather):
    lcd = lcddriver.lcd() # For writing values to display
    while True:
        url = ("http://www.yr.no/place/Norway/Sør-Trøndelag/Trondheim/Trondheim/forecast_hour_by_hour.xml")
        scanfile = urllib.urlopen(url)
        contents = scanfile.read()
        file = open("export.xml", 'w') # Saving XML from yr to a temp location for local usage
        file.write(contents)
        file.close()
        now = datetime.datetime.now()

        hour_fix_plusone = (str(now.hour + 1)).zfill(2)
        hour_fix_plusthree = (str(now.hour + 3)).zfill(2)
        hour_fix_plussix = (str(now.hour + 6)).zfill(2)

        nexthour = '%s-%s-%sT%s:00:00' %(now.year,now.strftime("%m"),now.strftime("%d"),hour_fix_plusone)
        nextthreehours = '%s-%s-%sT%s:00:00' %(now.year,now.strftime("%m"),now.strftime("%d"),hour_fix_plusthree)
        nextsixhours = '%s-%s-%sT%s:00:00' %(now.year,now.strftime("%m"),now.strftime("%d"),hour_fix_plussix)
        print(nexthour)
        print(nextthreehours)
        print(nextsixhours)

        with open('export.xml', 'rt') as wreport: # Scanning XML file for search string, and returns values from weather data
            xml = etree.parse(wreport)
	    for record in xml.iter('time'):
                if record.attrib['from'] == nexthour:
                    for temp in record.iter('temperature'):
                        nexthour_temp = str(temp.attrib['value'])
                        print(nexthour_temp)
                    for perc in record.iter('precipitation'):
                        nexthour_perc = str(perc.attrib['value'])
                        print(nexthour_perc)
                    for wind in record.iter('windSpeed'):
                        nexthour_wind = str(wind.attrib['mps'])
                        print(nexthour_wind)
                    nexthour_lcdstring = '%s%sC - %smm - %sm/s' %(nexthour_temp, chr(223), nexthour_perc, nexthour_wind)
                if record.attrib['from'] == nextthreehours:
                    for temp in record.iter('temperature'):
                        nextthreehours_temp = str(temp.attrib['value'])
                        print(nextthreehours_temp)
                    for perc in record.iter('precipitation'):
                        nextthreehours_perc = str(perc.attrib['value'])
                        print(nextthreehours_perc)
                    for wind in record.iter('windSpeed'):
                        nextthreehours_wind = str(wind.attrib['mps'])
                        print(nextthreehours_wind)
                    nextthreehours_lcdstring = '%s%sC - %smm - %sm/s' %(nextthreehours_temp, chr(223), nextthreehours_perc, nextthreehours_wind)
                if record.attrib['from'] == nextsixhours:
                    for temp in record.iter('temperature'):
                        nextsixhours_temp = str(temp.attrib['value'])
                        print(nextsixhours_temp)
                    for perc in record.iter('precipitation'):
                        nextsixhours_perc = str(perc.attrib['value'])
                        print(nextsixhours_perc)
                    for wind in record.iter('windSpeed'):
                        nextsixhours_wind = str(wind.attrib['mps'])
                        print(nextsixhours_wind)
                    nextsixhours_lcdstring = '%s%sC - %smm - %sm/s' %(nextsixhours_temp, chr(223), nextsixhours_perc, nextsixhours_wind)
        lcd.lcd_display_string(nexthour_lcdstring, 1)
        lcd.lcd_display_string(nextthreehours_lcdstring, 2)
        lcd.lcd_display_string(nextsixhours_lcdstring, 3)
        lcd.lcd_display_string("Vær om 1H - 3H - 6H", 4)
        time.sleep(1800)
        lcd.lcd_clear()
        lcd.lcd_display_string("Now updating...", 2)
        time.sleep(5)

cur_forecast = Thread(target=threehourforecase, args=(10,))
cur_forecast.start()
