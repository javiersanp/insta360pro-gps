usage = """python insta360pro-gps PATH_TO_INPUT_FILE [PATH_TO_OUTPUT_FILE]

Converts to GPX format a file with the GPS track extracted from a Insta360 Pro 
video using the GPSreader.exe tool included in the Insta360 Stitcher software."""

__author__ = "Javier Sanchez Portero"
__copyright__  = "Copyright 2018, Javier Sanchez Portero"
__license__ = "GNU v3"
__version__ = "1.0"
__email__ = "javiersanp@gmail.com"


from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
import json
import os

sep = '\n'
tab = '  '
gpxatrs = OrderedDict()
gpxatrs['version'] = "1.1"
gpxatrs['creator'] = "insta360pro-gps"
gpxatrs['xmlns'] = "http://www.topografix.com/GPX/1/1"
gpxatrs['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
gpxatrs['xsi:schemaLocation'] = "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"

def read(inputfile):
    with open(inputfile, 'r') as fo:
        data = json.loads(fo.read())
    track = data['extended_gps_info']
    assert isinstance(track, (list, tuple))
    return track

def writeln(fo, text, tabs=0):
    for i in range(tabs):
        fo.write(tab)
    fo.write(text)
    fo.write(sep)

def togpx(track, fo):
    writeln(fo, "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>")
    writeln(fo, '<gpx ' + ' '.join(['{}="{}"'.format(k, v) \
        for (k, v) in list(gpxatrs.items())]) + '>')
    writeln(fo, '<trk>', 1)
    writeln(fo, '<trkseg>', 2)
    for tp in track:
        lat = tp['latitude']
        lon = tp['longitude']
        ele = tp['altitude']
        dt = datetime.fromtimestamp(tp['time_gps_epoch'])
        writeln(fo, '<trkpt lat="{}" lon="{}">'.format(lat, lon), 3)
        writeln(fo, '<ele>{}</ele>'.format(ele), 4)
        qwriteln(fo, '<time>{}</time>'.format(dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')), 4)
        writeln(fo, '</trkpt>', 3)
    writeln(fo, '</trkseg>', 2)
    writeln(fo, '</trk>', 1)
    writeln(fo, '</gpx>')
    

if __name__ == "__main__":
    parser = ArgumentParser(usage=usage)
    parser.add_argument('inpath', help="Path to input file")
    parser.add_argument('outpath', nargs='?', help="Optionally path to output file")
    args = parser.parse_args()
    try:
        track = read(args.inpath)
    except IOError as e:
        print(e)
    except (ValueError, KeyError, AssertionError) as e:
        print("Bad input file")
    fn = args.outpath if args.outpath else os.path.splitext(args.inpath)[0] + '.gpx'
    with open(fn, 'w') as fo:
        togpx(track, fo)

