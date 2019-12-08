import os
import subprocess

def convert_ubx(ubx_dir, input_files, marker_names, ho, hr, ha, \
                country_code, convbin_path, gfzrnx_path):
    options = '-os -od -v 3 -f 5 -ho "{}" -hr "{}" -ha "{}"'.format(ho, hr, ha)

    for i, f in enumerate(input_files):
        current_marker = marker_names[i]
        command_convbin = '{} {} -hm "{}" {}{}'\
                          .format(convbin_path, options, \
                                  current_marker, ubx_dir, f)
        if f.endswith('.ubx'):
            proc = subprocess.Popen('{}'.format(command_convbin), \
                                    shell=True, stderr=subprocess.STDOUT)
            proc.wait()

            new_file = f'{ubx_dir}{f[0:-4]}.obs'
            command_gfzrnx = '{} -finp {} -obs_types G:C1C,L1C,D1C,S1C,C2L,L2L,D2L,S2L+R:C1C,L1C,D1C,S1C,C2C,L2C,D2C,S2C+E:C1C,L1C,D1C,S1C,C7Q,L7Q,D7Q,S7Q+J:C1C,L1C,D1C,S1C,C2L,L2L,D2L,S2L+C:C2I,L2I,D2I,S2I,C7I,L7I,D7I,S7I -fout {}::RX3::{},00 -split 86400'.format(gfzrnx_path, new_file, ubx_dir, country_code)
            proc = subprocess.Popen('{}'.format(command_gfzrnx), shell=True, stderr=subprocess.STDOUT)
            proc.wait()

            try:
                os.remove(new_file)
            except Exception as e:
                print('Problem while attempting to remove {}'.format(new_file))
                print(e)



