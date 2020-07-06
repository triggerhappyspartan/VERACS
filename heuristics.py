import os
import sys
import h5py
import numpy
import argparse
from matplotlib import pyplot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(required=True,type=str,help="File listing the directories to open for heuristic analysis")
    args = parser.parse_args()
    file_ = open(args.input,'r')
    file_lines = file_.readlines()
    file_.close()

    value_dictionary = {'cool_boron':{},'cool_hydrogen':{},'core_crud_boron_mass':{},'core_crud_mass':{},'cool_lithium':{},'cool_nickel_particulate':{},
                        "cool_soluble_iron":{},"cool_soluble_nickel":{}}
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008','STATE_0009','STATE_0010','STATE_0011',
                  'STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016','STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022',
                  'STATE_0023']
    numeric_states = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for key in value_dictionary:
        for state in state_list:
            value_dictionary[key][state] = []

    for line in file_lines:
        name = line.strip()
        file_ = h5py.File(name,'r')
        for state in state_list:
            if state in file_.keys():
                for key in value_dictionary:
                    value_dictionary[key][state].append(file_[state][key][()])
            else:
                value_dictionary[key][state].append(0.)

    for key in value_dictionary:
        min_list = []
        max_list = []
        average_list = []
        std_list = []
        all_values_list = []
        for state in state_list:
            min_list.append(min(value_dictionary[key][state]))
            max_list.append(min(value_dictionary[key][state]))
            average_list.append(numpy.average(value_dictionary[key][state]))
            std_list.append(numpy.std(value_dictionary[key][state]))
            all_values_list.extend(value_dictionary[key][state])

            pyplot.figure()
            pyplot.hist(value_dictionary[key][state],bins=20)
            pyplot.xlabel(key)
            pyplot.ylabel("Number of Instances")
            pyplot.title("{} for {}".format(key,state))
            pyplot.savefig("histogram_{}_{}.png".format(key,state))
            pyplot.close()

        pyplot.figure()
        pyplot.plot(numeric_states,min_list,label="minimum",color='black')
        pyplot.plot(numeric_states,max_list,label="maximum",color='red')
        pyplot.plot(numeric_states,average_list,label="average",color='green')
        pyplot.plot(numeric_states,average_list-std_list,label="variance",color='blue')
        pyplot.plot(numeric_states,average_list+std_list,color='blue')
        pyplot.xlabel("State Number")
        pyplot.ylabel(key)
        pyplot.title("Distribution of {} for All States".format(key))
        pyplot.savefig("distribution_{}.png".format(key))

        pyplot.figure()
        pyplot.hist(all_values_list,bins=100)
        pyplot.xlabel(key)
        pyplot.ylabel("Number of Instances")
        pyplot.title("{} for {}".format(key,state))
        pyplot.savefig("histogram_{}_all_values.png".format(key))
        pyplot.close()