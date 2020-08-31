import os
import sys
import h5py
import numpy
import gc

def extract_data(case):
    """
    Extracts the data from the case and returns it as a series of numpy matrices.
    """
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008',
                  'STATE_0009','STATE_0010','STATE_0011','STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016',
                  'STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022','STATE_0023','STATE_0024',
                  'STATE_0025']
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
    
    for i,state in enumerate(state_list[1:]):
        if state in case.keys():
            previous_state = state_list[i]
            if previous_state in case.keys():
                all_params = True
                for key in key_params:
                    if key not in case[state].keys():
                        all_params = False
                    elif key not in case[previous_state].keys():
                        all_params = False
                if all_params:    
                    for assem in position_map:
                        x1 = position_map[assem]['x'][0]
                        x2 = position_map[assem]['x'][1]
                        y1 = position_map[assem]['y'][0]
                        y2 = position_map[assem]['y'][1]    
                        for i in range(49):
                            integrated_pin_matrix[tcc,x1:x2,y1:y2,i] = numpy.divide(numpy.sum(case[state]['pin_powers'][:,:,:i,assem],axis=2),
                                                                                    numpy.sum(case[state]['pin_powers'][:,:,:,assem],axis=2))
                        regular_pin_matrix[tcc,x1:x2,y1:y2,:] = case[state]['pin_powers'][:,:,:,assem]
                        crud_input_matrix[tcc,x1:x2,y1:y2,:]  = case[previous_state]['pin_avg_crud_massdensity'][:,:,:,assem]
                        crud_output_matrix[tcc,x1:x2,y1:y2,:] = case[state]['pin_avg_crud_massdensity'][:,:,:,assem]
                        crud_diff_matrix[tcc,x1:x2,y1:y2,:] = case[state]['pin_avg_crud_massdensity'][:,:,:,assem] - case[previous_state]['pin_avg_crud_massdensity'][:,:,:,assem]
                    core_parameters[tcc,0] = case[state]['cool_boron']
                    core_parameters[tcc,1] = case[state]['cool_nickel_particulate']
                    core_parameters[tcc,2] = case[state]['EFPD']/365.
                    state_list[tcc] = state
                    tcc += 1

if __name__ == "__main__":
    file_list = ['E:massive_one.h5','E:massive_two.h5','E:massive_three.h5','E:second_library.h5']
    
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008',
                  'STATE_0009','STATE_0010','STATE_0011','STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016',
                  'STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022','STATE_0023','STATE_0024',
                  'STATE_0025']

    matrix_parameter_list = ['previous_pin_powers','pin_powers','pin_avg_crud_massdensity','pin_avg_crud_borondensity']
    single_parameter_list = ['EFPD','cool_boron','cool_nickel_particulate']

    new_library = h5py.File('Final_library.h5','r')
    tcc = 0
    for file_ in file_list:
        data_file = h5py.File(file_,'r')
        for group in file_.key():
            for case in file_[group].keys():
                h5_case = file_[group][case]
                extract_data(h5_case)
        data_file.close()




























