import os
import sys
import h5py
import numpy
import gc
from multiprocessing import Pool

def count_number_states(case):
    """
    Returns the total number of data points for the provided key.
    """
    state_list = ['STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008','STATE_0009',
                  'STATE_0010','STATE_0011','STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016','STATE_0017',
                  'STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022','STATE_0023','STATE_0024','STATE_0025']
    key_params = ['cool_boron','cool_nickel_particulate','pin_powers','pin_avg_crud_massdensity','pin_avg_crud_thickness']

    count = 0
    for state in state_list:
        if state in case.keys():
            all_params = True
            for key in key_params:
                if key not in case[state].keys():
                    all_params = False
            if all_params:
                count += 1
            else:
                print(case[state])

    return count

def extract_data(file_name):
    """
    Extracts the data from the case and returns it as a series of numpy matrices.
    """
    case_dictionary = {}
    case_dictionary['second_library.h5'] = ['linear_age_increase','linear_mass_increase','new_cycle_7','new_cycle_8']
    case_dictionary['massive_one.h5'] = ['cycle_1_v2','cycle_2_v1','cycle_2_v2']
    case_dictionary['massive_three.h5'] = ['cycle_5','new_cycle_5','new_cycle_6']
    case_dictionary['massive_two.h5'] = ['cycle_3','cycle_4','new_cycle_4']

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

    state_list_list = []
    for i in range(25):
        state_list_list.append(None)
    integrated_pin_matrix = numpy.zeros([25,17*8,17*8,49])
    regular_pin_matrix = numpy.zeros([25,17*8,17*8,49])
    crud_input_matrix  = numpy.zeros([25,17*8,17*8,49])
    crud_output_matrix = numpy.zeros([25,17*8,17*8,49])
    core_parameters = numpy.zeros([25,3])

    name_list = []
    tcc = 0
    data_file = h5py.File(file_name,'r')
    for case in case_dictionary[file_name]:
        for run in data_file[file_name][case].keys():
            current_run = data_file[file_name][case][run]        
            for i,state in enumerate(state_list[1:]):
                    if state in current_run.keys():
                        previous_state = state_list[i]
                        if previous_state in current_run.keys():
                            all_params = True
                            for key in key_params:
                                if key not in current_run[state].keys():
                                    all_params = False
                                elif key not in current_run[previous_state].keys():
                                    all_params = False
                            if all_params:    
                                for assem in position_map:
                                    x1 = position_map[assem]['x'][0]
                                    x2 = position_map[assem]['x'][1]
                                    y1 = position_map[assem]['y'][0]
                                    y2 = position_map[assem]['y'][1]    
                                    for i in range(49):
                                        integrated_pin_matrix[tcc,x1:x2,y1:y2,i] = numpy.divide(numpy.sum(current_run[state]['pin_powers'][:,:,:i,assem],axis=2),
                                                                                                numpy.sum(current_run[state]['pin_powers'][:,:,:,assem],axis=2))
                                    regular_pin_matrix[tcc,x1:x2,y1:y2,:] = current_run[state]['pin_powers'][:,:,:,assem]
                                    crud_input_matrix[tcc,x1:x2,y1:y2,:]  = current_run[previous_state]['pin_avg_crud_massdensity'][:,:,:,assem]
                                    crud_output_matrix[tcc,x1:x2,y1:y2,:] = current_run[state]['pin_avg_crud_massdensity'][:,:,:,assem]
                                core_parameters[tcc,0] = current_run[state]['cool_boron'][()]
                                core_parameters[tcc,1] = current_run[state]['cool_nickel_particulate'][()]
                                core_parameters[tcc,2] = current_run[state]['EFPD'][()]
                                state_list_list[tcc] = state
                                tcc += 1 
                
            tcc = 0
            out_name = "F:"+file_name.replace(".h5",f"_{case}_{run}")
            out_library = h5py.File(out_name,'w')
            out_library.create_dataset('pin_in',data=regular_pin_matrix)
            out_library.create_dataset('int_pin_in',data=integrated_pin_matrix)
            out_library.create_dataset('crud_in',data=crud_input_matrix)
            out_library.create_dataset('crud_out',data=crud_output_matrix)
            out_library.create_dataset('core_in',data=core_parameters)
            out_library.create_dataset('state_list',data=state_list)
            out_library.close()
            regular_pin_matrix[:,:,:,:] = 0.
            integrated_pin_matrix[:,:,:,:] = 0.
            crud_input_matrix[:,:,:,:] = 0.
            crud_output_matrix[:,:,:,:] = 0.
            core_parameters[:,:] = 0. 
            state_list[:] = None
            name_list.append(out_name)
    data_file.close()

    return name_list

if __name__ == "__main__":
    file_list = ['E:massive_one.h5','E:massive_two.h5','E:massive_three.h5','E:second_library.h5']
    
    number_list = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen',
                   'fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twenty-one','twenty-two','twenty-three']

    poolypool = Pool(4)

    name_list = poolypool.map(extract_data,file_list)

    state_list_list = []
    for i in range(2000):
        state_list_list.append(None)
    gc.collect()
    integrated_pin_matrix = numpy.zeros([2000,17*8,17*8,49])
    regular_pin_matrix = numpy.zeros([2000,17*8,17*8,49])
    crud_input_matrix  = numpy.zeros([2000,17*8,17*8,49])
    crud_output_matrix = numpy.zeros([2000,17*8,17*8,49])
    core_parameters = numpy.zeros([2000,3])
    print("Allocated Memory")
    tcc = 0 #total_case_count
    out_library = h5py.File('F:new_library.h5','w')
    gcount = 0 #group count
    g1 = out_library.create_group(number_list[gcount])
    for cases in name_list:
        for run in cases:
            h5_file = h5py.File(run,'r')
            for i,state in enumerate(h5_file['state_list'][()]):
                state_list_list[tcc] = state
                integrated_pin_matrix[tcc,:,:,:] = h5_file['pin_in'][i,:,:,:]
                regular_pin_matrix[tcc,:,:,:] = h5_file['int_pin_in'][i,:,:,:]
                crud_input_matrix[tcc,:,:,:]  = h5_file['crud_in'][i,:,:,:]
                crud_output_matrix[tcc,:,:,:] = h5_file['crud_out'][i,:,:,:]
                core_parameters[tcc,:] = h5_file['core_in'][i,:]
                tcc += 1 
                if tcc == 2000:
                    tcc = 0
                    gcount += 1
                    g1.create_dataset('pin_in',data=regular_pin_matrix)
                    g1.create_dataset('int_pin_in',data=integrated_pin_matrix)
                    g1.create_dataset('crud_in',data=crud_input_matrix)
                    g1.create_dataset('crud_out',data=crud_output_matrix)
                    g1.create_dataset('core_in',data=core_parameters)
                    g1.create_dataset('state_list',data=state_list_list)
                    g1 = out_library.create_group(number_list[gcount])
                    print(gcount)
                    regular_pin_matrix[:,:,:,:] = 0.
                    integrated_pin_matrix[:,:,:,:] = 0.
                    crud_input_matrix[:,:,:,:] = 0.
                    crud_output_matrix[:,:,:,:] = 0.
                    core_parameters[:,:] = 0. 
                    state_list_list[:] = None
            h5_file.close()
    g1.create_dataset('pin_in',data=regular_pin_matrix)
    g1.create_dataset('int_pin_in',data=integrated_pin_matrix)
    g1.create_dataset('crud_in',data=crud_input_matrix)
    g1.create_dataset('crud_out',data=crud_output_matrix)
    g1.create_dataset('core_in',data=core_parameters)
    g1.create_dataset('state_list',data=state_list_list)
    out_library.close()














