import os
import sys
import h5py
from matplotlib import pyplot

if __name__ == "__main__":
    file_1 = h5py.File('second_library.h5','r')
    file_2 = h5py.File('massive_one.h5','r')

    values_list = ['core_crud_mass','core_crud_boron_mass','FDH','Fq']
    state_list = ['STATE_0001','STATE_0002','STATE_0003','STATE_0004','STATE_0005','STATE_0006','STATE_0007','STATE_0008','STATE_0009','STATE_0010','STATE_0011',
                  'STATE_0012','STATE_0013','STATE_0014','STATE_0015','STATE_0016','STATE_0017','STATE_0018','STATE_0019','STATE_0020','STATE_0021','STATE_0022',
                  'STATE_0023','STATE_0024']
    
    max_fdh_list = []
    max_Fq_list = []
    crud_mass_list = []
    boron_mass_list = []
    beginning_nickel_list = []
    average_nickel_list = []
    ending_nickel_list = []
    beginner_crud_list = []
    for case in file_1['new_cycle_7'].keys():
        FDH_val = 0.
        Fq_val = 0.
        crud_val = 0.
        boron_val = 0.
        nickel_count = 0
        nickel_sum = 0.
        for state in state_list:
            if state in file_1['new_cycle_7'][case]:
                current_case = file_1['new_cycle_7'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    if current_case['core_crud_mass'][()] > crud_val:
                        crud_val = current_case['core_crud_mass'][()]
                    if current_case['FDH'][()] > FDH_val:
                        FDH_val = current_case['FDH'][()]
                    if current_case['Fq'][()] > Fq_val:
                        Fq_val = current_case['Fq'][()]
                    if current_case['core_crud_boron_mass'][()] > boron_val:
                        boron_val = current_case['core_crud_boron_mass'][()]
                    nickel_val = current_case['cool_nickel_particulate'][()]
                    nickel_count +=1
                    nickel_sum += nickel_val
                    if state == 'STATE_0002':
                        beginning_nickel_list.append(nickel_val)
                        beginner_crud_list.append(crud_val)
        average_nickel = nickel_sum/nickel_count
        average_nickel_list.append(average_nickel)
        ending_nickel_list.append(nickel_val)
        max_fdh_list.append(FDH_val) 
        max_Fq_list.append(Fq_val)
        crud_mass_list.append(crud_val)
        boron_mass_list.append(boron_val)
    for case in file_1['new_cycle_8'].keys():
        FDH_val = 0.
        Fq_val = 0.
        crud_val = 0.
        boron_val = 0.
        for state in state_list:
            if state in file_1['new_cycle_8'][case]:
                current_case = file_1['new_cycle_8'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    if current_case['core_crud_mass'][()] > crud_val:
                        crud_val = current_case['core_crud_mass'][()]
                    if current_case['FDH'][()] > FDH_val:
                        FDH_val = current_case['FDH'][()]
                    if current_case['Fq'][()] > Fq_val:
                        Fq_val = current_case['Fq'][()]
                    if current_case['core_crud_boron_mass'][()] > boron_val:
                        boron_val = current_case['core_crud_boron_mass'][()]
                        beginner_crud_list.append(crud_val)
                    nickel_val = current_case['cool_nickel_particulate'][()]
                    nickel_count +=1
                    nickel_sum += nickel_val
                    if state == 'STATE_0002':
                        beginning_nickel_list.append(nickel_val)
        average_nickel = nickel_sum/nickel_count
        average_nickel_list.append(average_nickel)
        ending_nickel_list.append(nickel_val)
        max_fdh_list.append(FDH_val) 
        max_Fq_list.append(Fq_val)
        crud_mass_list.append(crud_val)
        boron_mass_list.append(boron_val)    
    for case in file_2['cycle_1_v2'].keys():
        FDH_val = 0.
        Fq_val = 0.
        crud_val = 0.
        boron_val = 0.
        for state in state_list:
            if state in file_2['cycle_1_v2'][case]:
                current_case = file_2['cycle_1_v2'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    if current_case['core_crud_mass'][()] > crud_val:
                        crud_val = current_case['core_crud_mass'][()]
                    if current_case['FDH'][()] > FDH_val:
                        FDH_val = current_case['FDH'][()]
                    if current_case['Fq'][()] > Fq_val:
                        Fq_val = current_case['Fq'][()]
                    if current_case['core_crud_boron_mass'][()] > boron_val:
                        boron_val = current_case['core_crud_boron_mass'][()]
                    nickel_val = current_case['cool_nickel_particulate'][()]
                    nickel_count +=1
                    nickel_sum += nickel_val
                    if state == 'STATE_0002':
                        beginning_nickel_list.append(nickel_val)
                        beginner_crud_list.append(crud_val)
        average_nickel = nickel_sum/nickel_count
        average_nickel_list.append(average_nickel)
        ending_nickel_list.append(nickel_val)
        max_fdh_list.append(FDH_val) 
        max_Fq_list.append(Fq_val)
        crud_mass_list.append(crud_val)
        boron_mass_list.append(boron_val)
    for case in file_2['cycle_2_v1'].keys():
        FDH_val = 0.
        Fq_val = 0.
        crud_val = 0.
        boron_val = 0.
        for state in state_list:
            if state in file_2['cycle_2_v1'][case]:
                current_case = file_2['cycle_2_v1'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    if current_case['core_crud_mass'][()] > crud_val:
                        crud_val = current_case['core_crud_mass'][()]
                    if current_case['FDH'][()] > FDH_val:
                        FDH_val = current_case['FDH'][()]
                    if current_case['Fq'][()] > Fq_val:
                        Fq_val = current_case['Fq'][()]
                    if current_case['core_crud_boron_mass'][()] > boron_val:
                        boron_val = current_case['core_crud_boron_mass'][()]
                    nickel_val = current_case['cool_nickel_particulate'][()]
                    nickel_count +=1
                    nickel_sum += nickel_val
                    if state == 'STATE_0002':
                        beginning_nickel_list.append(nickel_val)
                        beginner_crud_list.append(crud_val)
        average_nickel = nickel_sum/nickel_count
        average_nickel_list.append(average_nickel)
        ending_nickel_list.append(nickel_val)
        max_fdh_list.append(FDH_val) 
        max_Fq_list.append(Fq_val)
        crud_mass_list.append(crud_val)
        boron_mass_list.append(boron_val)
    for case in file_2['cycle_2_v2'].keys():
        FDH_val = 0.
        Fq_val = 0.
        crud_val = 0.
        boron_val = 0.
        for state in state_list:
            if state in file_2['cycle_2_v2'][case]:
                current_case = file_2['cycle_2_v2'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    if current_case['core_crud_mass'][()] > crud_val:
                        crud_val = current_case['core_crud_mass'][()]
                    if current_case['FDH'][()] > FDH_val:
                        FDH_val = current_case['FDH'][()]
                    if current_case['Fq'][()] > Fq_val:
                        Fq_val = current_case['Fq'][()]
                    if current_case['core_crud_boron_mass'][()] > boron_val:
                        boron_val = current_case['core_crud_boron_mass'][()]
                    nickel_val = current_case['cool_nickel_particulate'][()]
                    nickel_count +=1
                    nickel_sum += nickel_val
                    if state == 'STATE_0002':
                        beginning_nickel_list.append(nickel_val)
                        beginner_crud_list.append(crud_val)
        average_nickel = nickel_sum/nickel_count
        average_nickel_list.append(average_nickel)
        ending_nickel_list.append(nickel_val)
        max_fdh_list.append(FDH_val) 
        max_Fq_list.append(Fq_val)
        crud_mass_list.append(crud_val)
        boron_mass_list.append(boron_val)
    
    list_of_crud_list = []
    for case in file_1['new_cycle_7'].keys():
        temp_crud_list = []
        for state in state_list:
            if state in file_1['new_cycle_7'][case]:
                current_case = file_1['new_cycle_7'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    temp_crud_list.append(current_case['core_crud_mass'][()])
        list_of_crud_list.append(temp_crud_list)
    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.title("New Cycle 7 Cases")
    pyplot.xlabel("Depletion States")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.show()
    list_of_crud_list = []
    for case in file_1['new_cycle_8'].keys():
        temp_crud_list = []
        for state in state_list:
            if state in file_1['new_cycle_8'][case]:
                current_case = file_1['new_cycle_8'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    temp_crud_list.append(current_case['core_crud_mass'][()])
        list_of_crud_list.append(temp_crud_list)
    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.title("New Cycle 8 Cases")
    pyplot.xlabel("Depletion States")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.show()
    list_of_crud_list = []    
    for case in file_2['cycle_1_v2'].keys():
        temp_crud_list = []
        for state in state_list:
            if state in file_2['cycle_1_v2'][case]:
                current_case = file_2['cycle_1_v2'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    temp_crud_list.append(current_case['core_crud_mass'][()])
        list_of_crud_list.append(temp_crud_list)
    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.title("Cycle 1 v2 Cases")
    pyplot.xlabel("Depletion States")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.show()
    list_of_crud_list = []
    for case in file_2['cycle_2_v1'].keys():
        temp_crud_list = []
        for state in state_list:
            if state in file_2['cycle_2_v1'][case]:
                current_case = file_2['cycle_2_v1'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    temp_crud_list.append(current_case['core_crud_mass'][()])
        list_of_crud_list.append(temp_crud_list)
    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.title("Cycle 2 V1 Cases")
    pyplot.xlabel("Depletion States")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.show()
    list_of_crud_list = []
    for case in file_2['cycle_2_v2'].keys():
        temp_crud_list = []
        for state in state_list:
            if state in file_2['cycle_2_v2'][case]:
                current_case = file_2['cycle_2_v2'][case][state]
                if 'core_crud_mass' in current_case.keys():
                    temp_crud_list.append(current_case['core_crud_mass'][()])
        list_of_crud_list.append(temp_crud_list)
    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.title("Cycle 2 V2 Cases")
    pyplot.xlabel("Depletion States")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.show()

    file_1.close()
    file_2.close()

    pyplot.figure()
    for crud_list in list_of_crud_list:
        pyplot.plot(range(len(crud_list)),crud_list)
    pyplot.show()

    crud_diff_list = []
    for i,j in zip(crud_mass_list,beginner_crud_list):
        print(i,j)
        crud_diff_list.append(i-j)
    pyplot.figure()
    pyplot.hist(crud_diff_list)
    pyplot.title("Histogram of crud mass growth")
    pyplot.xlabel("Growth of Core Crud Mass (Kg)")
    pyplot.ylabel("Number of Instances")
    pyplot.savefig("histogram_crud_mass_diff.png")
    pyplot.close()

    pyplot.figure()
    pyplot.scatter(max_fdh_list,crud_mass_list)
    pyplot.title("Core Crud Mass vs. F$\Delta$H")
    pyplot.xlabel("F$\Delta$H")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.savefig("scatter_FDH_crud_mass.png")
    pyplot.close()

    pyplot.figure()
    pyplot.scatter(max_Fq_list,crud_mass_list)
    pyplot.title("Core Crud Mass vs. Fq")
    pyplot.xlabel("Fq")
    pyplot.ylabel("Core Crud Mass (Kg)")
    pyplot.savefig("scatter_fq_crud_mass.png")
    pyplot.close()

    pyplot.figure()
    pyplot.scatter(max_fdh_list,boron_mass_list)
    pyplot.title("Core Boron Crud Mass vs. F$\Delta$H")
    pyplot.xlabel("F$\Delta$H")
    pyplot.ylabel("Core Boron Crud Mass (Kg)")
    pyplot.savefig("scatter_FDH_boron_mass.png")
    pyplot.close()

    pyplot.figure()
    pyplot.scatter(max_Fq_list,boron_mass_list)
    pyplot.title("Core Boron Crud Mass vs. Fq")
    pyplot.xlabel("Fq")
    pyplot.ylabel("Core Boron Crud Mass (Kg)")
    pyplot.savefig("scatter_Fq_boron_mass.png")
    pyplot.close()

    print(len(max_fdh_list),len(beginning_nickel_list),len(crud_mass_list))
    pyplot.figure()
    pyplot.scatter(max_fdh_list,beginning_nickel_list,c=crud_mass_list)
    pyplot.colorbar()
    pyplot.xlabel("F$\Delta$H")
    pyplot.ylabel('BOC Nickel Particulate')
    pyplot.title("Comparison of F$\Delta$H, BOC Nickel Particulate, and Crud Mass")

    pyplot.figure()
    pyplot.scatter(max_fdh_list,average_nickel_list,c=crud_mass_list)
    pyplot.colorbar()
    pyplot.xlabel("F$\Delta$H")
    pyplot.ylabel('Average Nickel Particulate')
    pyplot.title("Comparison of F$\Delta$H, Average Nickel Particulate, and Crud Mass")

    pyplot.figure()
    pyplot.scatter(max_fdh_list,ending_nickel_list,c=crud_mass_list)
    pyplot.colorbar()
    pyplot.xlabel("F$\Delta$H")
    pyplot.ylabel('EOC Nickel Particulate')
    pyplot.title("Comparison of F$\Delta$H, EOC Nickel Particulate, and Crud Mass")
    pyplot.show()