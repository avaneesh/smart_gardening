'''
Reads data in csv format and creates QR code for the url
Saves qr code in png format. name: 'id.png' ex. '1.png'

For Writting text on png, use PIL
# sudo pip install Pillow
'''
import csv
import urllib
import os

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


if __name__ == '__main__':
    with open('data.csv') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for gid, gurl, gdesc in reader:
            generate_sg_tag(gid, gurl, gdesc)
