<<<<<<< HEAD
import os
import argparse
import h5py

def parse_solutions(file_name):
    """
    Opens the text file containing the solutions to evaluate, reads it, and returns a list
    of the names.
    """
    file_ = open(file_name,'r')
    file_lines = file_.readlines()
    file_.close()

    file_list = []
    for line in file_lines:
        name = line.strip()
        file_list.append(name)

    return file_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name',help="The name of the new output file.",
                        required=True,type=str)
    parser.add_argument('--solution_file',help="The name of the text file containing the list of solutions to read.",
                        required=True,type=str)

    args = parser.parse_args()

    solution_list = parse_solutions(args.solution_file)

    skip_list = ['CORE','SHA1D']
    single_values = ['cool_boron','cool_hydrogen','cool_lithium','cool_mass',
                     'cool_nickel_particulate','cool_soluble_iron']

    matrix_values = ['pin_powers','pin_avg_crud_thickness','pin_avg_boron_thickness']

    output_file = h5py.File(args.name,'w')
    for solution in solution_list:
        g1 = output_file.create_group(solution)
        big_file = h5py.File("{}/deck.ctf.h5".format(solution),'r')
        key_list = big_file.keys()
        for key in key_list:
            if key in skip_list:
                pass
            else:
                g2 = g1.create_group(key)
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
        big_file.close()
    output_file.close()
        











=======
import os
import argparse
import h5py

def parse_solutions(file_name):
    """
    Opens the text file containing the solutions to evaluate, reads it, and returns a list
    of the names.
    """
    file_ = open(file_name,'r')
    file_lines = file_.readlines()
    file_.close()

    file_list = []
    for line in file_lines:
        name = line.strip()
        file_list.append(name)

    print(file_list)
    return file_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name',help="The name of the new output file.",
                        required=True,type=str)
    parser.add_argument('--solution_file',help="The name of the text file containing the list of solutions to read.",
                        required=True,type=str)

    args = parser.parse_args()

    solution_list = parse_solutions(args.solution_file)

    skip_list = ['CORE','SHA1D']
    single_values = ['cool_boron','cool_hydrogen','cool_lithium','cool_mass',
                     'cool_nickel_particulate','cool_soluble_iron']

    matrix_values = ['pin_powers','pin_avg_crud_thickness','pin_avg_boron_thickness']

    output_file = h5py.File(args.name,'w')
    for solution in solution_list:
        print(solution)
        g1 = output_file.create_group(solution)
        big_file = h5py.File("{}/deck.ctf.h5".format(solution),'r')
        print(output_file.keys())
        key_list = big_file.keys()
        for key in key_list:
            if key in skip_list:
                pass
            else:
                print(key)
                print(output_file[solution].keys())
                g2 = g1.create_group(key)
                for property_ in single_values:
                    print(property_)
                    if property_ in big_file[key]:
                        value = big_file[key][property_][()]
                        g2.create_dataset(property_,data=value)
                    else:
                        print(f"Property {property_} does not exist")
                for property_ in matrix_values:
                    print(property_)
                    if property_ in big_file[key]:
                        value = big_file[key][property_][:,:,:,:]
                        g2.create_dataset(property_,data=value)
                    else:
                        print(f"Property {property_} does not exist")    
        big_file.close()
    output_file.close()
        











>>>>>>> 934df281423d237098624b98f1ab85f706ca7a45
