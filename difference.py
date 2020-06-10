import os
import sys
import h5py
import numpy

if __name__ == "__main__":
    f1 = h5py.File('VERA_data/VERA_Runs/no_bp/trial_one.h5','r')
    f2 = h5py.File('Simulate_Files/more_hand_design/no_bp.h5','r')
    f3 = h5py.File('diff_no_bp.h5','w')

    core = f3.create_group('CORE')
    for dataset in f1['CORE']:
        print(dataset)
        print(f1['CORE'][dataset].shape)
        print(f1['CORE'][dataset][()])
        if not f1['CORE'][dataset].shape:
            core.create_dataset(dataset,data=f1['CORE'][dataset][()])
        else:
            core.create_dataset(dataset,data=f1['CORE'][dataset][:])
    
    list1 = list(f1.keys())
    list2 = list(f2.keys())

    check_list = ['pin_powers']

    for key in list1:
        if key == 'CORE':
            pass
        elif key == 'INPUT':
            pass
        elif key == 'SHA1D':
            pass
        elif key == 'title':
            pass
        elif key == 'veraout_version':
            pass
        else:
            g1 = f3.create_group(key)
            for param in check_list:
                diffs = f1[key][param][:,:,:,:] - f2[key][param][:,:,:,:]
                g1.create_dataset(param,data=diffs)

    f1.close()
    f2.close()
    f3.close()

    f1 = h5py.File('VERA_data/VERA_Runs/gad_only/trial_one.h5','r')
    f2 = h5py.File('Simulate_Files/more_hand_design/gad_only.h5','r')
    f3 = h5py.File('diff_gad_only.h5','w')

    core = f3.create_group('CORE')
    for dataset in f1['CORE']:
        print(dataset)
        print(f1['CORE'][dataset].shape)
        print(f1['CORE'][dataset][()])
        if not f1['CORE'][dataset].shape:
            core.create_dataset(dataset,data=f1['CORE'][dataset][()])
        else:
            core.create_dataset(dataset,data=f1['CORE'][dataset][:])
    
    list1 = list(f1.keys())
    list2 = list(f2.keys())

    check_list = ['pin_powers']

    for key in list1:
        if key == 'CORE':
            pass
        elif key == 'INPUT':
            pass
        elif key == 'SHA1D':
            pass
        elif key == 'title':
            pass
        elif key == 'veraout_version':
            pass
        else:
            g1 = f3.create_group(key)
            for param in check_list:
                diffs = f1[key][param][:,:,:,:] - f2[key][param][:,:,:,:]
                g1.create_dataset(param,data=diffs)

    f1.close()
    f2.close()
    f3.close()

    f1 = h5py.File('VERA_data/VERA_Runs/ifba_only/trial_one.h5','r')
    f2 = h5py.File('Simulate_Files/more_hand_design/ifba_only.h5','r')
    f3 = h5py.File('diff_ifba_only.h5','w')

    core = f3.create_group('CORE')
    for dataset in f1['CORE']:
        print(dataset)
        print(f1['CORE'][dataset].shape)
        print(f1['CORE'][dataset][()])
        if not f1['CORE'][dataset].shape:
            core.create_dataset(dataset,data=f1['CORE'][dataset][()])
        else:
            core.create_dataset(dataset,data=f1['CORE'][dataset][:])
    
    list1 = list(f1.keys())
    list2 = list(f2.keys())

    check_list = ['pin_powers']

    for key in list1:
        if key == 'CORE':
            pass
        elif key == 'INPUT':
            pass
        elif key == 'SHA1D':
            pass
        elif key == 'title':
            pass
        elif key == 'veraout_version':
            pass
        else:
            g1 = f3.create_group(key)
            for param in check_list:
                diffs = f1[key][param][:,:,:,:] - f2[key][param][:,:,:,:]
                g1.create_dataset(param,data=diffs)

    f1.close()
    f2.close()
    f3.close()