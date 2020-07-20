import os
import sys
import h5py
import numpy
import argparse
from matplotlib import pyplot

if __name__ == "__main__":
    file1 = h5py.File('libraries/cycle_3_library.h5','r')
    file2 = h5py.File("libraries/cycle_4_library.h5",'r')
    file3 = h5py.File("libraries/cycle_5_library.h5",'r')
    file4 = h5py.File("libraries/Cycle_2.h5",'r')
    file5 = h5py.File("libraries/run_two.h5",'r')
    file6 = h5py.File("libraries/run_four.h5",'r')

    value_list = ['cool_boron','core_crud_boron_mass','core_crud_mass','cool_nickel_particulate']
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008','STATE_0009','STATE_0010','STATE_0011',
                  'STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016','STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022',
                  'STATE_0023']
    numeric_states = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    for property_ in value_list:
        pyplot.figure()
        for key in file1['actual_cycle_3'].keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file1['actual_cycle_3'][key].keys()):
                if property_ in file1['actual_cycle_3'][key][state].keys():
                    val = file1['actual_cycle_3'][key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)
            

        for key in file2['cycle_4'].keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file2['cycle_4'][key].keys()):
                if property_ in file2['cycle_4'][key][state].keys():
                    val = file2['cycle_4'][key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)

        for key in file3['cycle_5'].keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file3['cycle_5'][key].keys()):
                if property_ in file3['cycle_5'][key][state].keys():
                    val = file3['cycle_5'][key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)
    
        for key in file4.keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file4[key].keys()):
                if property_ in file4[key][state].keys():
                    val = file4[key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)

        for key in file5.keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file5[key].keys()):
                if property_ in file5[key][state].keys():
                    val = file5[key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)

        for key in file6.keys():
            plot_list = []
            other_list = []
            for i,state in enumerate(file6[key].keys()):
                if property_ in file6[key][state].keys():
                    val = file6[key][state][property_][()]
                    plot_list.append(val)
                    other_list.append(i)
            pyplot.plot(other_list,plot_list)

    
        pyplot.xlabel("State Number")
        pyplot.ylabel(property_)
        pyplot.title("Distribution of {} for All Cases".format(property_))
    
    pyplot.show()

