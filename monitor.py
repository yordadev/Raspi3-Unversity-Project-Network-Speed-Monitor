
import os
import re
import subprocess
import time
import tweepy


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# your plans down, up and your threshold % to message your ISP
expected_download = 100
expected_upload = 10
threshold = 0.20

# ISP Twitter Handle
ISP_Handle = ""
Owner_Handle = ""

response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

try:
    f = open('/home/pi/speedtest/speedtest.csv', 'a+')
    if os.stat('/home/pi/speedtest/speedtest.csv').st_size == 0:
            f.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\r\n')
except:
    pass

f.write('{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))


# lets do some math
download_check = float(expected_download) * float(threshold)
download_check = float(expected_download) - float(download_check)

upload_check = float(expected_upload) * float(threshold)
upload_check = float(expected_upload) - float(upload_check)

if float(download_check) >= float(download) or float(upload_check) >= float(upload):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweet = api.update_status("Hello Spectrum, my owner is currently only getting: " + str(download) + " Mbps down and " + str(upload) + " Mbps Up. Their plan is " + str(expected_download) + " Mpbs down and " + str(expected_upload)+ " M$


