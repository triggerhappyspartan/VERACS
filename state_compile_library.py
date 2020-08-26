import os
import sys
import h5py
import numpy
import gc

def extract_data(case):
    """
    Extracts the data from the case and returns it as a series of numpy matrices.
    """
    key_params = ['cool_boron','cool_nickel_particulate','pin_powers','pin_avg_crud_massdensity','pin_avg_crud_thickness']
    position_map = {0:{'x':[0,17],    'y':[0,17]},     1:{'x':[17,34],   'y':[0,17]},
                    2:{'x':[34,51],   'y':[0,17]},     3:{'x':[51,68],   'y':[0,17]},
                    4:{'x':[68,85],   'y':[0,17]},     5:{'x':[85,102],  'y':[0,17]},
                    6:{'x':[102,119], 'y':[0,17]},     7:{'x':[119,136], 'y':[0,17]},
                    8:{'x':[0,17],    'y':[17,34]},    9:{'x':[17,34],   'y':[17,34]},
                    10:{'x':[34,51],  'y':[17,34]},    11:{'x':[51,68],  'y':[17,34]},
                    12:{'x':[68,85],  'y':[17,34]},    13:{'x':[85,102], 'y':[17,34]},
                    14:{'x':[102,119],'y':[17,34]},    15:{'x':[119,136],'y':[17,34]},
                    16:{'x':[0,17],   'y':[34,51]},    17:{'x':[17,34],  'y':[34,51]},
                    18:{'x':[34,51],  'y':[34,51]},    19:{'x':[51,68],  'y':[34,51]},
                    20:{'x':[68,85],  'y':[34,51]},    21:{'x':[85,102], 'y':[34,51]},
                    22:{'x':[102,119],'y':[34,51]},    23:{'x':[119,136],'y':[34,51]},
                    24:{'x':[0,17],   'y':[51,68]},    25:{'x':[17,34],  'y':[51,68]},
                    26:{'x':[34,51],  'y':[51,68]},    27:{'x':[51,68],  'y':[51,68]},
                    28:{'x':[68,85],  'y':[51,68]},    29:{'x':[85,102], 'y':[51,68]},
                    30:{'x':[102,119],'y':[51,68]},    31:{'x':[119,136],'y':[51,68]},
                    32:{'x':[0,17],   'y':[68,85]},    33:{'x':[17,34],  'y':[68,85]},
                    34:{'x':[34,51],  'y':[68,85]},    35:{'x':[51,68],  'y':[68,85]},
                    36:{'x':[68,85],  'y':[68,85]},    37:{'x':[85,102], 'y':[68,85]},
                    38:{'x':[102,119],'y':[68,85]},    39:{'x':[0,17],   'y':[85,102]},
                    40:{'x':[17,34],  'y':[85,102]},   41:{'x':[34,51],  'y':[85,102]},
                    42:{'x':[51,68],  'y':[85,102]},   43:{'x':[68,85],  'y':[85,102]},
                    44:{'x':[85,102], 'y':[85,102]},   45:{'x':[102,119],'y':[85,102]},
                    46:{'x':[0,17],   'y':[102,119]},  47:{'x':[17,34],  'y':[102,119]},
                    48:{'x':[34,51],  'y':[102,119]},  49:{'x':[51,68],  'y':[102,119]},
                    50:{'x':[68,85],  'y':[102,119]},  51:{'x':[85,102], 'y':[102,119]},
                    52:{'x':[0,17],   'y':[119,136]},  53:{'x':[17,34],  'y':[119,136]},
                    54:{'x':[34,51],  'y':[119,136]},  55:{'x':[51,68],  'y':[119,136]}}
    
    all_params = True
    for key in key_params:
        if key not in case.keys():
            all_params = False    
    if all_params:    
        for assem in position_map:
            x1 = position_map[assem]['x'][0]
            x2 = position_map[assem]['x'][1]
            y1 = position_map[assem]['y'][0]
            y2 = position_map[assem]['y'][1]    
            regular_pin_matrix[tcc,x1:x2,y1:y2,:] = case['pin_powers'][:,:,:,assem]
            crud_matrix[tcc,x1:x2,y1:y2,:]  = case['pin_avg_crud_massdensity'][:,:,:,assem]
        core_parameters[tcc,0] = case['cool_boron'][()]
        core_parameters[tcc,1] = case['cool_nickel_particulate'][()]
        core_parameters[tcc,2] = case['EFPD'][()] 

if __name__ == "__main__":
    data_file = h5py.File('E:cycle_10_compiled.h5','r')
    
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008',
                  'STATE_0009','STATE_0010','STATE_0011','STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016',
                  'STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022','STATE_0023','STATE_0024',
                  'STATE_0025']

    count = 0
    key_list = list(data_file.keys())
    regular_pin_matrix = numpy.zeros([len(key_list),17*8,17*8,49])
    crud_matrix  = numpy.zeros([len(key_list),17*8,17*8,49])
    core_parameters    = numpy.zeros([len(key_list),3])

    outfile = h5py.File('E:test_library.h5','w')
    for state in state_list:
        for tcc,key in enumerate(data_file.keys()):
            if state in data_file[key]:
                extract_data(data_file[key][state])
        g1 = outfile.create_group(state)    
        g1.create_dataset('pin_in',data=regular_pin_matrix)
        g1.create_dataset('crud',data=crud_matrix)
        g1.create_dataset('core_in',data=core_parameters)
        regular_pin_matrix[:,:,:,:] = 0. 
        crud_matrix[:,:,:,:] = 0.
        core_parameters[:,:] = 0.

    outfile.close()






