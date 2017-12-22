import os
import arrow
import urllib.request
import zipfile
import time

count=0

# get times
timezone = 'Europe/Amsterdam'
timestamp_format = 'YYYY-MM-DD_HH-mm-ss'
log_timestamp_format = "YYYY-MM-DD HH:mm:ss.SSS ZZ"
name_format="YYYY-MM-DD"
name = "output_images-"+arrow.now().format(name_format)

def download():
    print("["+arrow.utcnow().to(timezone).format(log_timestamp_format)+"]: Downloading '"+filename+"'..")
    urllib.request.urlretrieve("https://api.sat24.com/mostrecent/EU/visual5hdcomplete", filename)

while True:
    # save image
    filename = name+"_" + arrow.utcnow().to(timezone).format(timestamp_format) + ".png"
    maxRetries = 3
    retries = 0
    download()
    while (retries < maxRetries) and (os.stat(filename).st_size == 0):
    	print("\n["+arrow.utcnow().to(timezone).format(log_timestamp_format)+"]: Error: File '"+filename+"' is empty ("+str(os.stat(filename).st_size)+" bytes). Trying again.. (attempt "+str(retries+1)+" of "+str(maxRetries)+")")
    	print("["+arrow.utcnow().to(timezone).format(log_timestamp_format)+"]: Removing '"+filename+"'..")
    	os.remove(filename)
    	retries += 1
    	time.sleep(5)
    	download()

    # append file to compressed archive
    zip_filename = name+".zip"
    z = zipfile.ZipFile(zip_filename, "a",zipfile.ZIP_STORED)
    z.write(filename)
    #z.printdir()
    z.close()

    # remove downloaded image
    os.remove(filename)

    count += 1
    print("Aantal frames: "+str(count))
    print("waiting 15 minutes for next snapshot")
    time.sleep(900)
