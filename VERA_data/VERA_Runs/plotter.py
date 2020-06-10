import os
import sys
import h5py
from matplotlib import pyplot
from multiprocessing import Pool

def maker(state):
    file1 = h5py.File('trial_one/trial_one.h5','r')
    parameter_list = ['pin_avg_crud_thickness','pin_exposures','pin_powers','pin_steamrate']

    non_crud_params = ['pin_exposures','pin_powers','pin_steamrate']

    crud_params = ['pin_avg_crud_thickness','pin_steamrate']
    
    value_dictionary = {}
    statecount = 0

    print(state)
    if state == 'CORE':
        pass
    elif state == "INPUT":
        pass
    elif state == "SHA1D":
        pass
    elif state == 'title':
        pass
    elif state == 'veraout_version':
        pass
    else:
        for parameter in parameter_list:
            value_dictionary[parameter] = []
            #value_dictionary[parameter].extend(file1[state][parameter][:,:,:,:])
            w,x,y,z = file1[state][parameter].shape
            #temp = []*w*x*y*z
            for wv in range(w):
                for xv in range(x):
                    #for yv in range(y):
                        for zv in range(z):
                            value_dictionary[parameter].append(file1[state][parameter][wv,xv,35,zv])
        for param_one in non_crud_params:
            for param_two in crud_params:
                if param_one == param_two:
                    n_bins = 20
                    print(value_dictionary[param_one][0])
                    print(len(value_dictionary[param_one]))
                    pyplot.hist(value_dictionary[param_one])
                    pyplot.ylabel("Number Instances")
                    pyplot.xlabel("Values")
                    pyplot.title(f"Histogram {param_one}")
                    pyplot.savefig(f"{state}_{param_one}_histogram.png")
                    pyplot.close()
                else:
                    pyplot.scatter(value_dictionary[param_one],value_dictionary[param_two])
                    pyplot.xlabel(f"{param_one}")
                    pyplot.ylabel(f"{param_two}")
                    pyplot.title(f"{param_one} vs {param_two}")
                    pyplot.savefig(f"scatter_{state}_{param_one}_{param_two}.png")
                    pyplot.close()
    file1.close()
if __name__ == "__main__":
    
    #file2 = h5py.File('trial_two/trial_two.h5','r')
    file1 = h5py.File('trial_one/trial_one.h5','r')
    state_list1 = list(file1.keys())
    file1.close()
    #state_list2 = list(file2.keys())

    pool = Pool(8)

    pool.map(maker,state_list1)

    #for param in previous_list:
    #    pyplot.scatter(value_dictionary["current_"+param_one],value_dictionary["previous_"+param_two])
    #    pyplot.xlabel(f"Current")
    #    pyplot.ylabel(f"Previous")
    #    pyplot.title(f"Previous State Comparison {param}")
    #    pyplot.savefig(f"time_comparison_{param}.png")
    #    pyplot.close()
    
  #  statecount = 0
  #  for state in state_list2:
  #      print(state)
  #      if state == 'CORE':
  #          pass
  #      elif state == "INPUT":
  #          pass
  #      elif state == "SHA1D":
  #          pass
  #      elif state == 'title':
  #          pass
  #      elif state == 'veraout_version':
  #          pass
  #      elif not statecount:
  #          for parameter in parameter_list:
  #              value_dictionary[parameter].extend(file2[state][parameter][:,:,:,:])
  #          statecount += 4
  #      else:
  #          for parameter in parameter_list:
  #              value_dictionary[parameter].extend(file2[state][parameter][:,:,:,:])
  #          pstate = state_list2[statecount-1]
  #          print(f"Pstate {pstate}")
  #          for parameter in previous_list:
  #              value_dictionary["current_"+parameter].extend(file2[state][parameter][:,:,:,:])
  #              value_dictionary["previous_"+parameter].extend(file2[pstate][parameter][:,:,:,:])
  #          statecount += 1

    
   # file2.close()
    