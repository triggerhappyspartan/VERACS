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

    value_dictionary = {'cool_boron':{},'cool_hydrogen':{},'core_crud_boron_mass':{},'core_crud_mass':{},'cool_lithium':{},'cool_nickel_particulate':{},
                        "cool_soluble_iron":{},"cool_soluble_nickel":{}}
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008','STATE_0009','STATE_0010','STATE_0011',
                  'STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016','STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022',
                  'STATE_0023']
    numeric_states = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for key in value_dictionary:
        for state in state_list:
            value_dictionary[key][state] = []
        value_dictionary[key]['max'] = 0.00
        value_dictionary[key]['min'] = 100000.0
        value_dictionary[key]['last_values'] = []

    for key in file1['actual_cycle_3'].keys():
        for state in file1['actual_cycle_3'][key].keys():
            for property_ in value_dictionary:
                if property_ in file1['actual_cycle_3'][key][state].keys():
                    val = file1['actual_cycle_3'][key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val

    for key in file2['cycle_4'].keys():
        for state in file2['cycle_4'][key].keys():
            for property_ in value_dictionary:
                if property_ in file2['cycle_4'][key][state].keys():
                    val = file2['cycle_4'][key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val

    for key in file3['cycle_5'].keys():
        for state in file3['cycle_5'][key].keys():
            for property_ in value_dictionary:
                if property_ in file3['cycle_5'][key][state].keys():
                    val = file3['cycle_5'][key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val
    
    for key in file4.keys():
        for state in file4[key].keys():
            for property_ in value_dictionary:
                if property_ in file4[key][state].keys():
                    val = file4[key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val

    for key in file5.keys():
        for state in file5[key].keys():
            for property_ in value_dictionary:
                if property_ in file5[key][state].keys():
                    val = file5[key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val

    for key in file6.keys():
        for state in file6[key].keys():
            for property_ in value_dictionary:
                if property_ in file6[key][state].keys():
                    val = file6[key][state][property_][()]
                    value_dictionary[property_][state].append(val)
                    if val > value_dictionary[property_]['max']:
                        value_dictionary[property_]['max'] = val
                    if val < value_dictionary[property_]['min']:
                        value_dictionary[property_]['min'] = val

    for key in value_dictionary:
        print(key)
        min_list = []
        max_list = []
        average_list = []
        std_list = []
        all_values_list = []
        minus_std_1 = []
        plus_std_1 = []
        for state in state_list:
            if value_dictionary[key][state]:
                print(value_dictionary[key][state])
                min_list.append(min(value_dictionary[key][state]))
                max_list.append(max(value_dictionary[key][state]))
                average_list.append(numpy.average(value_dictionary[key][state]))
                std_list.append(numpy.std(value_dictionary[key][state]))
                plus_std_1.append(average_list[-1]+std_list[-1])
                minus_std_1.append(average_list[-1]-std_list[-1])
                all_values_list.extend(value_dictionary[key][state])

                pyplot.figure()
                pyplot.hist(value_dictionary[key][state],bins=100)
                pyplot.xlabel(key)
                pyplot.ylabel("Number of Instances")
                pyplot.title("{} for {}".format(key,state))
                pyplot.xlim(value_dictionary[key]["min"],value_dictionary[key]["max"])
                pyplot.savefig("histogram_{}_{}.png".format(key,state))
                pyplot.close()
            else:
                min_list.append(0)
                max_list.append(0)
                average_list.append(0)
                std_list.append(0)
                plus_std_1.append(0)
                minus_std_1.append(0)

        pyplot.figure()
        pyplot.plot(numeric_states,min_list,label="minimum",color='black')
        pyplot.plot(numeric_states,max_list,label="maximum",color='red')
        pyplot.plot(numeric_states,average_list,label="average",color='green')
        pyplot.plot(numeric_states,plus_std_1,label="variance",color='blue')
        pyplot.plot(numeric_states,minus_std_1,color='blue')
        pyplot.xlabel("State Number")
        pyplot.legend()
        pyplot.ylabel(key)
        pyplot.title("Distribution of {} for All States".format(key))
        pyplot.savefig("plot_{}.png".format(key))
        pyplot.close()

        pyplot.figure()
        pyplot.hist(all_values_list,bins=100)
        pyplot.xlabel(key)
        pyplot.ylabel("Number of Instances")
        pyplot.title("Histogram of {} for all states".format(key))
        pyplot.savefig("histogram_{}_all_values.png".format(key))
        pyplot.close()

    for key in file1['actual_cycle_3'].keys():
        for property_ in value_dictionary:
            for state in file1['actual_cycle_3'][key].keys():
                if property_ in file1['actual_cycle_3'][key][state].keys():
                    val = file1['actual_cycle_3'][key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)

    for key in file2['cycle_4'].keys():
        for property_ in value_dictionary:
            for state in file2['cycle_4'][key].keys():
                if property_ in file2['cycle_4'][key][state].keys():
                    val = file2['cycle_4'][key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)

    for key in file3['cycle_5'].keys():
        for property_ in value_dictionary:
            for state in file3['cycle_5'][key].keys():
                if property_ in file3['cycle_5'][key][state].keys():
                    val = file3['cycle_5'][key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)
    
    for key in file4.keys():
        for property_ in value_dictionary:
            for state in file4[key].keys():
                if property_ in file4[key][state].keys():
                    val = file4[key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)

    for key in file5.keys():
        for property_ in value_dictionary:
            for state in file5[key].keys():
                if property_ in file5[key][state].keys():
                    val = file5[key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)

    for key in file6.keys():
        for property_ in value_dictionary:
            for state in file6[key].keys():
                if property_ in file6[key][state].keys():
                    val = file6[key][state][property_][()]
            value_dictionary[property_]['last_values'].append(val)
                    
    for key in value_dictionary:
        pyplot.figure()
        pyplot.hist(value_dictionary[key]['last_values'],bins=100)
        pyplot.xlabel(key)
        pyplot.ylabel("Number of Instances")
        pyplot.title("Histogram of {} final values".format(key))
        pyplot.savefig("histogram_{}_final_values.png".format(key,state))
        pyplot.close()