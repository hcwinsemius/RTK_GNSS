import os
import shutil
import argparse

from utils import convert_ubx
from RoverPositionExporter import RoverPositionExporter

def main():
    convbin_exec_path = '/home/hot-admin/Documents/git/RTKLIB/'\
                        'app/convbin/gcc/convbin'
    gfzrnx_exec_path = '/home/hot-admin/Documents/RTK/gfzrnx_lx'
    rnx2rtkp_exec_path = '/home/hot-admin/Documents/git/RTKLIB/app'\
                         '/rnx2rtkp/gcc/rnx2rtkp'

    ubx_dir = '/home/hot-admin/Documents/RTK/Data/ubx/'
    rnx_dir = '/home/hot-admin/Documents/RTK/Data/rnx/'
    nav_dir = '/home/hot-admin/Documents/RTK/Data/nav/'
    csv_dir = '/home/hot-admin/Documents/RTK/Data/csv/'

    convert_rinex(convbin_exec_path, gfzrnx_exec_path,\
                  rnx2rtkp_exec_path, ubx_dir, rnx_dir, nav_dir)
    # export_rover_positions(ubx_dir, csv_dir)

def export_rover_positions(ubx_dir, csv_dir):
    stations = 'drainage.ubx surveyedMarker.ubx bridgeCorner.ubx'\
               'bridge_valley.ubx backyardValley.ubx'.split()
    for i, station in enumerate(stations):
        RoverPositionExporter(f'{ubx_dir}{station}', \
                              f'{csv_dir}{station[0:-4]}.csv')

def convert_rinex(convbin_exec_path, gfzrnx_exec_path, \
                  rnx2rtkp_exec_path, ubx_dir, rnx_dir, nav_dir):
    input_files = [
	#'base_log_2019_11_19_06_13.ubx',
	#'base_log_2019_11_19_12_11.ubx',
	'base_log_2019_11_19_12_32.ubx'
    ]
    marker_names = [
        #'Point_1',
	#'Point_2',
	'Point_3'
        
    ]
    observer = 'Iddy Chazua / HOT TZ'
    receiver = ' /U-blox ZEDF9P'
    antenna = ' /UNKNOWN'
    country_code = 'TZN'
    convert_ubx(ubx_dir, input_files, marker_names, observer, \
                receiver, antenna, country_code, \
                convbin_exec_path, gfzrnx_exec_path)
    move_rnx_nav(ubx_dir, rnx_dir, nav_dir)


def move_rnx_nav(ubx_dir, rnx_dir, nav_dir):
    files = os.listdir(ubx_dir)
    for f in files:
        if f.endswith('.rnx'):
            shutil.copy(f'{ubx_dir}{f}', f'{rnx_dir}{f}')
            os.remove(f'{ubx_dir}{f}')
        if f.endswith('.nav'):
            shutil.copy(f'{ubx_dir}{f}', f'{nav_dir}{f}')
            os.remove(f'{ubx_dir}{f}')


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('log.txt')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s p%(process)s '\
                                  '{%(pathname)s:%(lineno)d} - %(name)s - '\
                                  '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    p = argparse.ArgumentParser()
    p.add_argument(-i, --infile, nargs =  argparse.REMAINDER)
    args = p.parse_args()
    print('infiles include {}'.format(args))
    
    main()
