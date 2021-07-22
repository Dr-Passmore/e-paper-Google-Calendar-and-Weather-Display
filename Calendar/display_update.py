import sys
import os
import logging
from PIL import Image,ImageDraw,ImageFont
import time
from datetime import datetime as dt
from dateutil.parser import parse as dtparse


# directory paths
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


#import waveshare epd
from waveshare_epd import epd7in5b_V2

try:
    logging.info("Updating display")
    epd = epd7in5b_V2.EPD()
    
    #Fonts
    robotoblack18 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Black.ttf'), 18)
    robotoblack24 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Black.ttf'), 24)
    robotoblack32 = ImageFont.truetype(os.path.join(picdir, 'Roboto-Black.ttf'), 32)
    
    
    #Images
    wind_small = Image.open(os.path.join(picdir, 'windSmall.bmp'))
    
    #Initial loading message
    import random_loading_messages
    
    message = random_loading_messages.loading_message
    
    logging.info("initialising and clearing display")
    epd.init()
    
    logging.info("Drawing new image")
    Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    lOther = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_Himage = ImageDraw.Draw(Limage)
    draw_other = ImageDraw.Draw(lOther)
    
    draw_Himage.text((25, 250), message, font = robotoblack24, fill = 0)
    draw_other.text((350, 30), "LOADING", font = robotoblack32, fill = 0)
    
    draw_Himage.line((0, 1, 800, 1), fill = 0)     # Top Black line
    draw_other.rectangle((0, 2, 800, 10), fill = 0)  # Red Rectangle
    draw_other.rectangle((0, 81, 800, 89), fill = 0)
    draw_Himage.line((10, 80, 800, 80), fill = 0)
    draw_Himage.line((10, 90, 800, 90), fill = 0)
    draw_other.rectangle((0, 1, 10, 479), fill = 0)
    draw_other.rectangle((790, 2, 800, 479), fill = 0)
    draw_other.rectangle((0, 471, 800, 479), fill = 0)
    epd.Clear()
    epd.display(epd.getbuffer(Limage),epd.getbuffer(lOther))
    time.sleep(2)
    
    
    #import weather
    print ("Getting weather data")
    import weather
    
    #weather 
    sunrise = weather.sunrise
    sunset = weather.sunset
    description = weather.description
    temp_min = weather.temp_min
    temp_max = weather.temp_max
    temp_curr = weather.temp_curr
    humidity = weather.humidity
    wind_speed = weather.speed 
    cardinal_wind_dir = weather.cardinal
    icon = weather.icon
    
    #convert Tuple to String
    def convertTuple(tup):
        description =  ''.join(tup)
        return description

    description = convertTuple(description)
    
    #capitalize the first letter of each word
    description = description.title()
    
    humidity = int(''.join(map(str,humidity)))
    
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    Other = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_Himage = ImageDraw.Draw(Himage)
    draw_other = ImageDraw.Draw(Other)
    
    #external border
    draw_other.rectangle((0, 0, 800, 10), fill = 0)  
    draw_other.rectangle((0, 80, 800, 90), fill = 0)
    draw_other.rectangle((790, 0, 800, 480), fill = 0)
    draw_other.rectangle((0, 470, 800, 480), fill = 0)
    draw_other.rectangle((0, 0, 10, 480), fill = 0)
    draw_other.rectangle((0, 130, 800, 140), fill = 0)
    draw_other.rectangle((150, 80, 160, 480), fill = 0)
    draw_other.rectangle((380, 80, 390, 480), fill = 0)
    
    print ('Drawing Weather Data')
    
    #weather data
    draw_Himage.text((25, 15), description, font = robotoblack24, fill = 0)
    draw_Himage.text((140, 45), sunset, font = robotoblack24, fill = 0)
    draw_Himage.text((25, 45), sunrise, font = robotoblack24, fill = 0)
    draw_Himage.text((540, 15), "Temp - " + str(temp_curr) + "°C", font = robotoblack18, fill = 0)
    draw_Himage.text((540, 35), "High - " + str(temp_max) + "°C", font = robotoblack18, fill = 0)
    draw_Himage.text((540, 55), "Low - " + str(temp_min) + "°C", font = robotoblack18, fill = 0)
    draw_Himage.text((710, 15), cardinal_wind_dir, font = robotoblack32, fill = 0)
    draw_Himage.text((710, 50), str(wind_speed) + " MPS", font = robotoblack24, fill =0)
    
    weather_icon = Image.open(os.path.join(picdir, icon + '.bmp'))
    Himage.paste(wind_small, (660, 30))
    Himage.paste(weather_icon, (370,15))
    
    epd.Clear()
    epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))
    
    from calendar_item_list import calendar_events
    print ("Connecting to Google Calendar")
    #calendar
    events = calendar_events.events 
    
    print("Preparing Events")
    e_date = []
    e_time = []
    end_time = []
    e_summary = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime')
        event_date = dt.strftime(dtparse(start), format='%d-%m-%Y')
        event_time = dt.strftime(dtparse(start), format='%I:%M%p')
        event_end = dt.strftime(dtparse(end), format='%I:%M%p')
        summary = event['summary']
        e_date.append(
            event_date
            )
        e_time.append(
            event_time
            )
        end_time.append(
            event_end
        )
        e_summary.append (
            summary
        )
    
    draw_Himage.text((15, 95), "Date", font = robotoblack24, fill = 0)
    draw_Himage.text((165, 95), "Time", font = robotoblack24, fill = 0)
    draw_Himage.text((400, 95), "Event", font = robotoblack24, fill = 0)
    
    draw_Himage.text((15, 150), e_date[0], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 150), e_time[0] + "-" + end_time[0], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 150), e_summary[0], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 180), e_date[1], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 180), e_time[1] + "-" + end_time[1], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 180), e_summary[1], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 210), e_date[2], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 210), e_time[2] + "-" + end_time[2], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 210), e_summary[2], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 240), e_date[3], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 240), e_time[3] + "-" + end_time[3], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 240), e_summary[3], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 270), e_date[4], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 270), e_time[4] + "-" + end_time[4], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 270), e_summary[4], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 300), e_date[5], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 300), e_time[5] + "-" + end_time[5], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 300), e_summary[5], font = robotoblack24, fill = 0) 
    draw_Himage.text((15, 330), e_date[6], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 330), e_time[6] + "-" + end_time[6], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 330), e_summary[6], font = robotoblack24, fill = 0)
    draw_Himage.text((15, 360), e_date[7], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 360), e_time[7] + "-" + end_time[7], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 360), e_summary[7], font = robotoblack24, fill = 0)
    draw_Himage.text((15, 390), e_date[8], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 390), e_time[8] + "-" + end_time[8], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 390), e_summary[8], font = robotoblack24, fill = 0)
    draw_Himage.text((15, 420), e_date[9], font = robotoblack24, fill = 0)
    draw_Himage.text((165, 420), e_time[9] + "-" + end_time[9], font = robotoblack24, fill = 0)
    draw_Himage.text((400, 420), e_summary[9], font = robotoblack24, fill = 0)
    
    print ("Completed data preperation and printing to screen")

    epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))
    time.sleep(2)
    logging.info("Putting display to sleep")
    epd.sleep()
    
    print ("Completed")
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit()
    exit()
    