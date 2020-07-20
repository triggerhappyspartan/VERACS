import os
import h5py
import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

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
for prop1 in value_list:
    for prop2 in value_list:
        for prop3 in value_list:
            total_list_1 = []
            total_list_2 = []
            total_list_3 = []
            if prop1 == prop2:
                pass
            else:
                for state in state_list:
                    print(f"State {state}")
                    print(f"Properties {prop1} {prop2}")
                    value1_state = []
                    value2_state = []
                    value3_state = []

                    for key in file1['actual_cycle_3'].keys():
                        if state in file1['actual_cycle_3'][key].keys():
                            if prop1 in file1['actual_cycle_3'][key][state].keys():
                                val1 = file1['actual_cycle_3'][key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop2 in file1['actual_cycle_3'][key][state].keys():
                                val2 = file1['actual_cycle_3'][key][state][prop2][()]
                                value2_state.append(val2)
                                total_list_2.append(val2)
                            if prop3 in file1['actual_cycle_3'][key][state].keys():
                                val3 = file1['actual_cycle_3'][key][state][prop3][()]
                                value3_state.append(val3)
                                total_list_3.append(val3)

                    for key in file2['cycle_4'].keys():
                        if state in file2['cycle_4'][key].keys():
                            if prop1 in file2['cycle_4'][key][state].keys():
                                val1 = file2['cycle_4'][key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop3 in file2['cycle_4'][key][state].keys():
                                val2 = file2['cycle_4'][key][state][prop2][()]
                                value2_state.append(val2)
                                total_list_2.append(val2)
                            if prop2 in file2['cycle_4'][key][state].keys():
                                val3 = file2['cycle_4'][key][state][prop3][()]
                                value3_state.append(val3)
                                total_list_3.append(val3)

                    for key in file3['cycle_5'].keys():
                        if state in file3['cycle_5'][key].keys():
                            if prop1 in file3['cycle_5'][key][state].keys():
                                val1 = file3['cycle_5'][key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop3 in file3['cycle_5'][key][state].keys():
                                val2 = file3['cycle_5'][key][state][prop2][()]
                                value2_state.append(val2)
                                total_list_2.append(val2)
                            if prop2 in file3['cycle_5'][key][state].keys():
                                val3 = file3['cycle_5'][key][state][prop3][()]
                                value3_state.append(val3)
                                total_list_3.append(val3)

                    for key in file4.keys():
                        if state in file4[key].keys():
                            if prop1 in file4[key][state].keys():
                                val1 = file4[key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop2 in file4[key][state].keys():
                                val2 = file4[key][state][prop2][()]
                                value2_state.append(val2)
                                total_list_2.append(val2)
                            if prop3 in file4[key][state].keys():
                                val3 = file4[key][state][prop3][()]
                                value3_state.append(val3)
                                total_list_3.append(val3)

                    for key in file5.keys():
                        if state in file5[key].keys():
                            if prop1 in file5[key][state].keys():
                                val1 = file5[key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop2 in file5[key][state].keys():
                                val2 = file5[key][state][prop2][()]
                                val3 = file5[key][state][prop3][()]
                                value2_state.append(val2)
                            if prop3 in file5[key][state].keys():
                                value3_state.append(val3)
                                total_list_2.append(val2)
                                total_list_3.append(val3)

                    for key in file6.keys():
                        if state in file6[key].keys():
                            if prop1 in file6[key][state].keys():
                                val1 = file6[key][state][prop1][()]
                                value1_state.append(val1)
                                total_list_1.append(val1)
                            if prop2 in file6[key][state].keys():
                                val2 = file6[key][state][prop2][()]
                                value2_state.append(val2)
                                total_list_2.append(val2)
                            if prop3 in file6[key][state].keys():
                                val3 = file6[key][state][prop3][()]
                                value3_state.append(val3)
                                total_list_3.append(val3)

                    if value1_state:
                        if value2_state:
                            print(state)
                            pyplot.figure()
                            pyplot.scatter(value1_state,value2_state)
                            pyplot.xlabel(prop1)
                            pyplot.ylabel(prop2)
                            pyplot.title(f"{prop1} vs. {prop2} at {state}")
                            pyplot.savefig(f"{prop1}_v_{prop2}_{state}.png")
                            pyplot.close()

            if total_list_1:
                if total_list_2:
                    pyplot.figure()
                    pyplot.scatter(total_list_1,total_list_2)
                    pyplot.xlabel(prop1)
                    pyplot.ylabel(prop2)
                    pyplot.title(f"{prop1} vs. {prop2} for all states")
                    pyplot.savefig(f"{prop1}_v_{prop2}_total.png")
                    pyplot.close()

                    if total_list_3:
                        pyplot.figure()
                        pyplot.scatter(total_list_1,total_list_2,c=total_list_3)
                        pyplot.colorbar()
                        pyplot.xlabel(prop1)
                        pyplot.ylabel(prop2)
                        pyplot.title(f"{prop1} vs. {prop2} vs. {prop3} for all states")
                        pyplot.show()

massive_list ={'pin_powers':{},'pin_avg_boron_thickness':{},'pin_avg_crud_thickness':{}}
for prop in massive_list:
    for state in state_list:
        massive_list[prop][state] = {}
        for i in range(49):
            massive_list[prop][state][i] = []

for state in state_list:
    print(f"State {state}")
    for key in file1['actual_cycle_3'].keys():
        if state in file1['actual_cycle_3'][key].keys():
            for prop in massive_list:
                if prop in file1['actual_cycle_3'][key][state].keys():
                    for i in range(49):
                        val = numpy.average(file1['actual_cycle_3'][key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)
                    

    for key in file2['cycle_4'].keys():
        if state in file2['cycle_4'][key].keys():
            for prop in massive_list:
                if prop in file2['cycle_4'][key][state].keys():
                    for i in range(49):
                        val = numpy.average(file2['cycle_4'][key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)

    for key in file3['cycle_5'].keys():
        if state in file3['cycle_5'][key].keys():
            for prop in massive_list:
                if prop in file3['cycle_5'][key][state].keys():
                    for i in range(49):
                        val = numpy.average(file3['cycle_5'][key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)

    for key in file4.keys():
        if state in file4[key].keys():
            for prop in massive_list:
                if prop in file4[key][state].keys():
                    for i in range(49):
                        val = numpy.average(file4[key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)

    for key in file5.keys():
        if state in file5[key].keys():
            for prop in massive_list:
                if prop in file5[key][state].keys():
                    for i in range(49):
                        val = numpy.average(file5[key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)

    for key in file6.keys():
        if state in file6[key].keys():
            for prop in massive_list:
                if prop in file6[key][state].keys():
                    for i in range(49):
                        val = numpy.average(file6[key][state][prop][:,:,i,:])
                        massive_list[prop][state][i].append(val)

for prop in massive_list:
    for state in state_list:
        ave_plot_list = []
        min_plot_list = []
        max_plot_list = []
        std_plus_list = []
        std_minu_list = []
        for i in range(49):
            if massive_list[prop][state][i]:
                ave = numpy.average(massive_list[prop][state][i])
                min_ = numpy.min(massive_list[prop][state][i])
                max_ = numpy.max(massive_list[prop][state][i])
                std_ = numpy.std(massive_list[prop][state][i])
                minus = ave-std_
                plus = ave+std_
                ave_plot_list.append(ave)
                min_plot_list.append(min_)
                max_plot_list.append(max_)
                std_plus_list.append(plus)
                std_minu_list.append(minus)
            else:
                ave_plot_list.append(0)
                min_plot_list.append(0)
                max_plot_list.append(0)
                std_plus_list.append(0)
                std_minu_list.append(0)
        pyplot.figure()
        pyplot.plot(ave_plot_list,range(49),label='average',color='blue')
        pyplot.plot(min_plot_list,range(49),label="minimum",color='black')
        pyplot.plot(max_plot_list,range(49),label='maximum',color='green')
        pyplot.plot(std_plus_list,range(49),label='Variance',color='red')
        if prop == 'pin_avg_boron_thickness':
            pass
        else:
            pyplot.plot(std_minu_list,range(49),color='red')
        pyplot.legend()
        pyplot.xlabel(prop)
        pyplot.ylabel("Axial Position")
        pyplot.title("Average Axial Distrubtion of {} for {}".format(prop,state))
        pyplot.savefig(f"axial_{prop}_{state}.png")
        pyplot.close()