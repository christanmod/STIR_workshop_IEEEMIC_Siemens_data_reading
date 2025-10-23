#%%
### you'll need the functions from this module in "Visiondata_preprocess.py"

#%%
import os
import numpy as np
import sys
import re

import matplotlib.pyplot as plt

#%%
def change_datafilename_in_interfile_header(new_header_filename, header_filename, data_filename):
    with open(header_filename) as f:
        data = f.read()
    poss = re.search(r'name of data file\s*:=[^\n]*', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        'name of data file:={}'.format(data_filename))
    with open(new_header_filename, 'w') as f2:
        f2.write(data)

def DOI_adaption(projdata, DOI_new):
    proj_info = projdata.get_proj_data_info()

    DOI = proj_info.get_scanner().get_average_depth_of_interaction()
    print('Current Depth of interaction:', DOI)
    proj_info.get_scanner().set_average_depth_of_interaction(DOI_new)
    DOI = proj_info.get_scanner().get_average_depth_of_interaction()
    print('New Depth of interaction:', DOI)

def check_if_compressed(header_filename):
    with open(header_filename) as f:
        data = f.read()
    try:
        match = re.search(r'compression\s*:=\s*(\w+)', data)
        if match.group(1) == 'off':
            print('Compression is off, can proceed')
        else:
            print('You are trying to read e7tools compressed data. Please uncompress first!')
            sys.exit()
    except:
        print('No compression info found in header!')
        pass

def plot_2d_image(idx,vol,title,clims=None,cmap="viridis"):
    """Customized version of subplot to plot 2D image"""
    plt.subplot(*idx)
    plt.imshow(vol,cmap=cmap)
    if not clims is None:
        plt.clim(clims)
    plt.colorbar(shrink=.5, aspect=.9)
    plt.title(title)
    plt.axis("off")

def change_datatype_in_interfile_header(header_name, data_type, num_bytes_per_pixel):
    with open(header_name) as f:
        data = f.read()
    poss = re.search(r'number format\s*:=[^\n]*', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        '!number format:={}'.format(data_type))
    poss = re.search(r'!number of bytes per pixel\s*:=[^\n]*', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        '!number of bytes per pixel:={}'.format(num_bytes_per_pixel))
    with open(header_name, 'w') as f2:
        f2.write(data)

def remove_scan_data_lines_from_interfile_header(header_filename_new, header_filename_old):
    with open(header_filename_old) as f:
        data = f.read()

    data_type_string = 'scan data type description[^\n]*\s*:=\s*[^\n]*\n'
    data = re.sub(data_type_string, '', data)

    num_data_types_string = 'number of scan data types[^\n]*\s*:=\s*[^\n]*\n'
    data = re.sub(num_data_types_string, '', data)

    with open(header_filename_new, 'w') as f2:
        f2.write(data)

def remove_IMGDATADESC_lines_from_interfile_header(header_filename_new, header_filename_old):
    with open(header_filename_old) as f:
        data = f.read()

    pattern = r'!IMAGE DATA DESCRIPTION:=.*'
    data = re.sub(pattern, '', data, flags=re.DOTALL)

    with open(header_filename_new, 'w') as f2:
        f2.write(data)

def remove_data_offset(header_filename_new, header_filename_old):
    with open(header_filename_old) as f:
        data = f.read()

    data_type_string = 'data offset in bytes[^\n]*\s*:=\s*[^\n]*\n'
    data = re.sub(data_type_string, '', data)

    with open(header_filename_new, 'w') as f2:
        f2.write(data)

def add_data_offset(header_filename_new, header_filename_old):
    with open(header_filename_old) as f:
        data = f.read()

    offset_string = '\ndata offset in bytes[1]:= 84760000'
    pattern = r'(%TOF mashing factor\s*:=[^\n]*)'
    data = re.sub(pattern, r'\1' + offset_string, data)

    with open(header_filename_new, 'w') as f2:
        f2.write(data)

def replace_siemens_convention_in_interfile_header(header_name_new, header_name):
    with open(header_name) as f:
        data = f.read()

    poss = re.search('matrix axis label\[2\]:=plane', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        'matrix axis label[2]:=sinogram views')

    poss = re.search('matrix axis label\[3\]:=projection', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        'matrix axis label[3]:=number of sinograms')

    with open(header_name_new, 'w') as f2:
        f2.write(data)

def change_max_ring_distance(header_name_new, header_name, max_ring_diff):
    with open(header_name) as f:
        data = f.read()

    poss = re.search('%maximum ring difference\s*:=[^\n]*', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        '%maximum ring difference:={}'.format(int(max_ring_diff)))

    with open(header_name_new, 'w') as f2:
        f2.write(data)

def remove_tof_dimension(header_name_new, header_name):
    
    with open(header_name) as f:
        data = f.read()

    poss = re.search(r'number of dimensions\s*:=[^\n]*', data).span()
    data = data.replace(data[poss[0]:poss[1]], \
        'number of dimensions:={}'.format(3))

    data_type_string = 'matrix size\[4\]\s*:=[^\n]*\n'
    data = re.sub(data_type_string, '', data)

    data_type_string = 'matrix axis label\[4\]*\s*:=TOF bin*\n'
    data = re.sub(data_type_string, '', data)

    data_type_string = 'scale factor \(ps\/bin\) (.*)\n'
    data = re.sub(data_type_string, '', data)

    data_type_string = '%TOF mashing factor[^\n]*\s*:=\s*[^\n]*\n'
    data = re.sub(data_type_string, '%TOF mashing factor :=0\n', data)

    data_type_string = '%number of TOF time bins[^\n]*\s*:=\s*[^\n]*\n'
    data = re.sub(data_type_string, '', data)

    with open(header_name_new, 'w') as f2:
        f2.write(data)