'''
Reads data in csv format and creates QR code for the url
Saves qr code in png format. name: 'id.png' ex. '1.png'

For Writting text on png, use PIL
# sudo pip install Pillow
# sudo pip install pandas
'''
import csv
import urllib
import os
#import pandas as pd
from collections import defaultdict
# Pandas could not install, so using defaultdict for now :(

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# Picasa: (no use)
# https://picasaweb.google.com/109958767957460003241/Geo_images#6245625532172215490


# Dropbox: (currently using)
# https://www.dropbox.com/s/00uv8gob21qeu34/IMG_4792.JPG?dl=0

# https://developers.google.com/chart/infographics/docs/qr_codes?hl=en
# https://chart.googleapis.com/chart?chl=any_string&chs=300x300&cht=qr
# https://chart.googleapis.com/chart?chl=https%3A%2F%2Fwww.dropbox.com%2Fs%2F00uv8gob21qeu34%2FIMG_4792.JPG%3Fdl%3D0&chs=300x300&cht=qr

# Google's charting API will generate QR code for us.
# https://developers.google.com/chart/infographics/docs/qr_codes?hl=en
root_url = 'https://chart.googleapis.com/chart?'
width=300; height=300
data_dir = 'data'
src_data_path='/Users/avkadam/Google Drive/Garden/data1.csv'

__author__ = "Avaneesh Kadam"
__copyright__ = "Copyright (C) 2016 Avaneesh Kadam"
__license__ = "Public Domain"
__version__ = "1.0"

def generate_sg_tag(git, gurl, gdesc):
    ''' Generate SmartGardening Tag from data
    '''
    query = dict(cht='qr', chs='%sx%s'%(width,height), chl=gurl)
    url = root_url + urllib.urlencode(query)
    u = urllib.urlopen(url)
    image = u.read()
    try:
        os.makedirs(data_dir)
    except OSError:
        pass
    filename = os.path.join(data_dir, '.'.join((gid, 'png')))

    with open(filename, 'wb') as ifile:
        ifile.write(image)
    # Now lets add header and footers
    add_header_footer(filename, gid, gdesc)

def add_header_footer(filename, gid, gdesc):
    ''' Add header footer to generated QR code
    '''
    # Now lets add some text, header and footer
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    header = '%s' % (gdesc) # Description
    footer = 'id:%s' % (gid)
    draw.text((10, 10), header, (250,0,0)) # header
    draw.text((10, height-20), footer, (250,0,0)) # footer
    img.save(filename)

def to_dict(csv_in_file):
    ''' Convert CSV to dict for easy reference '''
    columns = defaultdict(list) # each value in each column is appended to a list
    with open(csv_in_file) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value 
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    return columns



if __name__ == '__main__':
# Processing plain old csv
#    with open(src_data_path) as f:
#        reader = csv.reader(f)
#        next(reader, None)  # skip the headers
#        for gid, gurl, gdesc in reader:
#            generate_sg_tag(gid, gurl, gdesc)

    # Convert CSV to dict for easy reference
    col_dict = to_dict(src_data_path) 

    for i in range(len(col_dict['id'])):
        gid = col_dict['id'][i]
        gurl = col_dict['photo_url'][i]
        gphoto = col_dict['photo_1'][i]
        gurl = gurl + gid + '/' + gphoto
        gdesc = col_dict['description'][i]
        print 'Processing id:%s, url:%s' % (gid, gurl)
        # Now create QR code and add info to it
        generate_sg_tag(gid, gurl, gdesc)
