import os
import argparse
import h5py
from simulate_exchanger import Simulate_Extractor

def parse_solutions(file_name):
    """
    Opens the text file containing the solutions to evaluate, reads it, and returns a list
    of the names.
    """
    file_ = open(file_name,'r')
    file_lines = file_.readlines()
    file_.close()

    h5_file_list = []
    sim_file_list = []
    for line in file_lines:
        h5_name,sim_name = line.strip().split()
        h5_file_list.append(h5_name)
        sim_file_list.append(sim_name)

    return h5_file_list,sim_file_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name',help="The name of the new output file.",
                        required=True,type=str)
    parser.add_argument('--solution_file',help="The name of the text file containing the list of solutions to read.",
                        required=True,type=str)

    args = parser.parse_args()

    h5_solution_list,sim_solution_list = parse_solutions(args.solution_file)

    skip_list = ['CORE','SHA1D']
    single_values = ['cool_boron','cool_hydrogen','cool_lithium','cool_mass',
                     'cool_nickel_particulate','cool_soluble_iron','core_crud_mass','core_crud_boron_mass']

    matrix_values = ['pin_powers','pin_avg_crud_thickness','pin_avg_boron_thickness','pin_avg_crud_massdensity','pin_avg_crud_borondensity']

    output_file = h5py.File(args.name,'w')
    SE = Simulate_Extractor()
    for h5,sim in zip(h5_solution_list,sim_solution_list):
        g1 = output_file.create_group(h5)
        big_file = h5py.File(h5,'r')
        sim_file = open(sim,'r')
        sim_file_lines = sim_file.readlines()
        sim_file.close()
        efpd_values = SE.efpd_list(sim_file_lines)
        FDH_list = SE.FDH_list(sim_file_lines)
        Fqs = SE.pin_peaking_list(sim_file_lines)
        burnup = SE.burnup_list(sim_file_lines)
        key_list = big_file.keys()
        count = 0
        for key in key_list:
            if key in skip_list:
                pass
            else:
                g2 = g1.create_group(key)
                value = FDH_list[count]
                g2.create_dataset("FDH",data=value)
                value = Fqs[count]
                g2.create_dataset("Fq",data=value)
                value = efpd_values[count]
                g2.create_dataset("EFPD",data=value)
                value = burnup[count]
                g2.create_dataset("exposure",data=value)
                for property_ in single_values:
                    if property_ in big_file[key]:
                        value = big_file[key][property_][()]
                        g2.create_dataset(property_,data=value)
                    else:
                        print("Property "+property_+" does not exist")
                for property_ in matrix_values:
                    if property_ in big_file[key]:
                        value = big_file[key][property_][:,:,:,:]
                        g2.create_dataset(property_,data=value)
                    else:
                        print("Property {} does not exist".format(property_))    
                count += 1
        big_file.close()

    output_file.close()
        











