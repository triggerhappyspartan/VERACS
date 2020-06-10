import os
import h5py
import numpy
from matplotlib import pyplot

h5_list = ['second_new_settings/deck.ctf.h5',
           'third_new_settings/deck.ctf.h5',
           'fourth/deck.ctf.h5',
           'fifth/deck.ctf.h5',
           'sixth/deck.ctf.h5',
           'seventh/deck.ctf.h5',
           'eighth/deck.ctf.h5',
           'ninth/deck.ctf.h5']

single_parameters = ['core_crud_mass','cool_boron','cool_hydrogen','cool_lithium',
                    'cool_nickel_particulate','cool_soluble_iron',
                    'cool_soluble_nickel']

matrix_parameters = ['pin_powers','pin_steamrate','pin_avg_boron_thickness',
                     'pin_avg_crud_borondensity','pin_avg_crud_thickness',
                     'pin_avg_crud_massdensity']

input_parameters = ['cool_boron','cool_hydrogen','cool_lithium','cool_nickel_particulate',
                    'cool_soluble_iron','cool_soluble_nickel','pin_powers','pin_steamrate']

output_parameters = ['core_crud_mass','pin_avg_boron_thickness','pin_avg_crud_borondensity','pin_avg_crud_thickness',
                     'pin_avg_crud_massdensity']                    

value_dictionary = {}
for param in input_parameters:
    value_dictionary[param] = []
for param in output_parameters:
    value_dictionary[param] = []

for name in h5_list:
    file_ = h5py.File(name,'r')
    for key in file_.keys():
        for param in input_parameters:
            if param in file_[key].keys():
                if param in matrix_parameters:
                    value_dictionary[param].append(file_[key][param][8,8,19,18])
                else:
                    value_dictionary[param].append(file_[key][param][()])

covariance_dictionary = {}
for param_one in value_dictionary:
    covariance_dictionary[param_one] = {} 
    for param_two in value_dictionary:
        if param_one == param_two:
            pass
        else:
            pyplot.scatter(value_dictionary[param_one],value_dictionary[param_two])
            pyplot.xlabel(param_one)
            pyplot.ylabel(param_two)
            pyplot.title(param_one +" vs. " + param_two)
            pyplot.savefig(param_one +"_vs_" + param_two)
            pyplot.close()
        mean_param_one = numpy.average(value_dictionary[param_one])
        mean_param_two = numpy.average(value_dictionary[param_two])
        covariance_dictionary[param_one][param_two] = 0
        count = 0
        for i,j in zip(value_dictionary[param_one],value_dictionary[param_two]):
            temp1 = i-mean_param_one
            temp2 = i-mean_param_two
            covariance_dictionary[param_one][param_two] += temp1*temp2
            count += 1
        covariance_dictionary[param_one][param_two] /= count-1

values = open("parameter_values.txt",'w')
values.write("Values\n")
for param in value_dictionary:
    values.write(param+",   ")
    for val in value_dictionary[param]:
        values.write(str(val)+",   ")
    values.write('\n')
values.write("Covariance Matrix\n                ,   ")
for param_one in covariance_dictionary:
    values.write(param_one + ",    ")
values.write("\n")
for param_one in covariance_dictionary:
    values.write(param_one + ",  ")
    for param_two in covariance_dictionary[param_one]:
        values.write(covariance_dictionary[param_one][param_two]+ ",  ")
    values.write("\n")
values.close()