import os
import numpy
import argparse
import h5py

class Simulate_Extractor(object):
    """
    Class for organizing the functions used to read the output files produced
    by Simulate.

    Written by Brian Andersen. 1/8/2020
    """
    @staticmethod
    def core_keff_list(file_lines):
        """
        Extracts the core K-effective value from the provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        keff_list = []
        for line in file_lines:
            if "K-effective . . . . . . . . . . . . ." in line:
                elems = line.strip().split()
                keff_list.append(float(elems[-1]))

        return keff_list
    
    @staticmethod
    def powers3D(file_lines,number_pins):
        """
        Extracts the pin powers from the output solution file as a dictionary
        with the assembly labels as the dictionary keys. 
 
        Parameters
        --------------
        file_lines: List
            The lines of the Simulate output file being analyzed.
        tag: STR
            The tag being used to define the assembly.

        Written by Brian Andersen. 1/9/2020
        """
        assembly_dictionary = {}
        boundary_list = []
        nodal_boundary_search_elems = ['Plane','Nodal','Boundaries:']
        assigning_axial_heights = False
        
        searching_for_powers = False
        for line in file_lines:
            elems = line.strip().split()
            if not elems:
                pass
            else:
                if elems == nodal_boundary_search_elems:
                    assigning_axial_heights = True
                if assigning_axial_heights:
                    if elems[0] == '*******************************************':
                        if elems[1] == '0.000':
                            assigning_axial_heights = False
                        else:
                            boundary_list.insert(0,elems[1])
                if 'Assembly Label:' in line:
                    line = line.replace(","," ")
                    elems = line.strip().split()
                    current_label = elems[3]
                    current_height = boundary_list[int(elems[13])-1]
                    if current_label in assembly_dictionary:
                        pass
                    else:
                        assembly_dictionary[current_label] = {}
                    if current_burnup in assembly_dictionary[current_label]:
                        pass
                    else:
                        assembly_dictionary[current_label][current_burnup] = {}
                        for height in boundary_list:
                            assembly_dictionary[current_label][current_burnup][height] = {}
                            for i in range(number_pins):
                                assembly_dictionary[current_label][current_burnup][height][i] = None
                if 'Case  1 Step' in line:
                    current_burnup = float(elems[-2])
                if "'3PXP' - Pin Power  Distribution:" in line:
                    searching_for_powers = True
                    pin_count = 0
                if searching_for_powers:
                    line = line.replace(":"," ")
                    elems = line.strip().split()
                    if len(elems) > 1:
                        if elems[0] == "'3PXP'":
                            pass
                        else:
                            for el in elems:
                                assembly_dictionary[current_label][current_burnup][current_height][pin_count] = float(el)
                                pin_count += 1
                            if pin_count == number_pins:
                                searching_for_powers = False

        return assembly_dictionary

    @staticmethod
    def powers2D(file_lines,number_pins):
        """
        Extracts the radial power matrix from the simulate output file as
        a dictionary with the assembly label and depletion as the keys.

        Parameters
            file_lines: list
                All the output lines of the simulate file as a list.
            number_pins: int
                The number of fuel rods in each assembly.
        
        Written by Brian Andersen. 1/9/2020
        """
        assembly_dictionary = {}
        boundary_list = []
        nodal_boundary_search_elems = ['Plane','Nodal','Boundaries:']
        assigning_axial_heights = False
        
        searching_for_powers = False
        for line in file_lines:
            elems = line.strip().split()
            if not elems:
                pass
            else:
                if elems == nodal_boundary_search_elems:
                    assigning_axial_heights = True
                if assigning_axial_heights:
                    if elems[0] == '*******************************************':
                        if elems[1] == '0.000':
                            assigning_axial_heights = False
                        else:
                            boundary_list.insert(0,elems[1])
                if 'Assembly Label:' in line:
                    line = line.replace(","," ")
                    elems = line.strip().split()
                    current_label = elems[3]
                    current_height = boundary_list[int(elems[13])-1]
                    if current_label in assembly_dictionary:
                        pass
                    else:
                        assembly_dictionary[current_label] = {}
                    if current_burnup in assembly_dictionary[current_label]:
                        pass
                    else:
                        assembly_dictionary[current_label][current_burnup] = {}
                        for height in boundary_list:
                            assembly_dictionary[current_label][current_burnup][height] = {}
                            for i in range(number_pins):
                                assembly_dictionary[current_label][current_burnup][height][i] = None
                if 'Case  1 Step' in line:
                    current_burnup = float(elems[-2])
                if "'2PXP' - Planar Pin Powers" in line:
                    searching_for_powers = True
                    pin_count = 0
                if searching_for_powers:
                    line = line.replace(":"," ")
                    elems = line.strip().split()
                    if len(elems) > 1:
                        if elems[0] == "'2PXP'":
                            pass
                        else:
                            for el in elems:
                                assembly_dictionary[current_label][current_burnup][current_height][pin_count] = float(el)
                                pin_count += 1
                            if pin_count == number_pins:
                                searching_for_powers = False

        return assembly_dictionary

    @staticmethod
    def assembly_peaking_factors(file_lines):
        """
        Extracts the assembly radial power peaking factors as a dictionary
        with the depletion step in GWD/MTU as the dictionary keys.

        Parameters
            file_lines: list
                All the output lines of the simulate file as a list.

        Written by Brian Andersen. 1/9/2020
        """
        radial_power_dictionary = {}
        searching_ = False
        for line in file_lines:
            if "Case" in line and "GWd/MT" in line:
                elems = line.strip().split()
                depl = elems[-2]
                if depl in radial_power_dictionary:
                    pass
                else:
                    radial_power_dictionary[depl] = {}
            if "**   H-     G-     F-     E-     D-     C-     B-     A-     **" in line:
                searching_ = False
                
            if searching_:
                elems = line.strip().split()
                if elems[0] == "**":
                    pos_list = elems[1:-1]
                else:
                    radial_power_dictionary[depl][elems[0]] = {}
                    for i,el in enumerate(elems[1:-1]):
                        radial_power_dictionary[depl][elems[0]][pos_list[i]] = float(el)
                        
            if "PRI.STA 2RPF  - Assembly 2D Ave RPF - Relative Power Fraction" in line:
                searching_ = True

        return radial_power_dictionary

    @staticmethod
    def linear_power_rate_3D(file_lines):
        """
        Extracts the linear power rate from Simulate as a dictionary.

        Parameters
            file_lines: list
                All the output lines of the simulate file as a list.

        Written by Brian Andersen. 1/9/2020
        """
        state_count = -1
        for line in file_lines:
            if "Fuel Assemblies . . ." in line:
                elems = line.strip().split()
                number_assemblies = int(elems[-1])
            if 'DIM.PWR' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'DIM.CAL' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.CAL'":
                    axial = int(elems[1])
            if 'Output Summary' in line:
                state_count += 1

        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps(193)
            core_map = core_map.dict_assembly_map_157
        else:
            errmessage = "The number of assembly rows {} and columns {} is unrecognized".format(rows,cols)
            return ValueError(errmessage)

        for i in range(state_count):
            power_dict["STATE_{}".format((i+1):04d)] = numpy.zeros([axial,number_assemblies])

        state_list = list(power_dict.keys())
        state_count = -1
        current_state = state_list[state_count]
        searching_powers = False
        in_power_region = False
        for line in file_lines:
            if "PIN.EDT 3KWF  - Peak Pin Power:(kW/ft)       Assembly 3D" in line:
                in_power_region = True
            if in_power_region:
                if "**   H-     G-     F-     E-     D-     C-     B-     A-     **" in line:
                    searching_powers = False
                    in_power_region = False
                if searching_powers:
                    elems = line.strip().split()
                    key_list = list(core_map[int(elems[0])])
                    for i,val in enumerate(elems[1:-1]):
                        assembly = core_map[int(elems[0])][key_list[i]]
                        power_dict[current_state][axial_position,assembly] = float(val)
                if "Renorm =" in line and "Axial Plane =" in line:
                    elems = line.strip().split()
                    axial_position = int(elems[-1]) - 1
                if "**    8      9     10     11     12     13     14     15     **" in line:
                    searching_powers = True
                if "Output Summary" in line:
                    state_count += 1
                    if state_count < len(state_list):
                        current_state = state_list[state_count]

        return power_dict

    @staticmethod
    def efpd_list(file_lines):
        """
        Returns a list of EFPD values for each cycle exposure in the simulate
        file.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        list_ = []
        for line in file_lines:
            if "Cycle Exp." in line:
                if "EFPD" in line:
                    elems = line.strip().split()
                    spot = elems.index('EFPD')
                    list_.append(float(elems[spot-1]))

        return list_

    @staticmethod
    def FDH_list(file_lines):
        """
        Returns a list of F-delta-H values for each cycle exposure in the simulate
        file.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        list_ = []
        for line in file_lines:
            if "F-delta-H" in line:
                elems = line.strip().split()
                spot = elems.index('F-delta-H')
                list_.append(float(elems[spot+1]))

        return list_

    @staticmethod
    def pin_peaking_list(file_lines):
        """
        Returns a list of pin peaking values, Fq, for each cycle exposure in the simulate
        file.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        list_ = []
        for line in file_lines:
            if " Peak Nodal Power (Location)" in line:
                elems = line.strip().split()
                spot = elems.index('(Location)')
                list_.append(float(elems[spot+1]))

        return list_

    @staticmethod
    def radial_assembly_power_2D(file_lines):
        """
        Extracts the radial power matrix from the simulate output file and 
        returns them as a dictionary.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        state_count = -1
        for line in file_lines:
            if 'DIM.PWR' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.dict_assembly_map_15_15
        else:
            errmessage = "The number of assembly rows {} and columns {} is unrecognized".format(rows,cols)
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict["STATE_{}".format((i+1):04d)] = numpy.zeros([1,number_assemblies])

        state_list = list(power_dict.keys())
        state_count = -1
        current_state = state_list[state_count]
        searching_powers = False
        for line in file_lines:
            if "**   H-     G-     F-     E-     D-     C-     B-     A-     **" in line:
                searching_powers = False
            if searching_powers:
                if "**    8      9     10     11     12     13     14     15     **" in line:
                    pass
                else:
                    elems = line.strip().split()
                    key_list = list(core_map[int(elems[0])])
                    for i,val in enumerate(elems[1:-1]):
                        assembly = core_map[int(elems[0])][key_list[i]]
                        power_dict[current_state][0,assembly] = float(val)
            if "PRI.STA 2RPF  - Assembly 2D Ave RPF - Relative Power Fraction" in line:
                searching_powers = True
            
        return power_dict

    @staticmethod
    def radial_assembly_exposure_2D(file_lines):
        """
        Extracts the radial power matrix from the simulate output file and 
        returns them as a dictionary.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        state_count = -1
        for line in file_lines:
            if 'DIM.PWR' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.dict_assembly_map_15_15
        else:
            errmessage = "The number of assembly rows {} and columns {} is unrecognized".format(rows,cols)
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict["STATE_{}".format((i+1):04d)] = numpy.zeros([1,number_assemblies])

        state_list = list(power_dict.keys())
        state_count = -1
        current_state = state_list[state_count]
        searching_powers = False
        for line in file_lines:
            if "**   H-     G-     F-     E-     D-     C-     B-     A-     **" in line:
                searching_powers = False
            if searching_powers:
                if "**    8      9     10     11     12     13     14     15     **" in line:
                    pass
                else:
                    elems = line.strip().split()
                    key_list = list(core_map[int(elems[0])])
                    for i,val in enumerate(elems[1:-1]):
                        assembly = core_map[int(elems[0])][key_list[i]]
                        power_dict[current_state][0,assembly] = float(val)
            if "PRI.STA 2EXP  - Assembly 2D Ave EXPOSURE  - GWD/T" in line:
                searching_powers = True
            
        return power_dict

    @staticmethod
    def boron_list(file_lines):
        """
        Returns a list of boron values in PPM at each depletion step.

        Parameters:
        file_lines: list
            All the output lines of the simulate file as a list.

        Written by Brian Andersen 12/7/2019
        """
        boron_list = []
        for line in file_lines:
        #    if "Boron" in line and "(ppm)" in line:
        #        elems = line.strip().split()
        #        boron_list.append(float(elems[-1]))

            if "Boron Conc. . . . . . . . . . BOR" in line:
                elems = line.strip().split()
                spot = elems.index("ppm")
                boron_list.append(float(elems[spot-1]))

        return boron_list

    @staticmethod
    def keff_list(file_lines,assembly_type):
        """
        Returns a list of kinf values from Simulate3.
        """
        kinf_list = []
        searching_for_kinf = False
        for line in file_lines:
            elems = line.strip().split()
            if not elems:
                pass
            else:
                if assembly_type.upper() == 'BWR':
                    if searching_for_kinf:
                        if elems[0] == '1':
                            kinf_list.append(float(elems[1]))
                            searching_for_kinf = False
                    if "PRI.STA 2KIN  - Assembly 2D Ave KINF - K-infinity" in line:
                        searching_for_kinf = True

        return kinf_list

    @staticmethod
    def relative_power(file_lines):
        """
        Extracts the Relative Core Power from the provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        relative_powers = []
        for line in file_lines:
            if "Relative Power. . . . . . .PERCTP" in line:
                p1 = line.index("PERCTP")
                p2 = line.index("%")
                search_space = line[p1:p2]
                search_space = search_space.replace("PERCTP","")
                relative_powers.append(float(search_space))

        return relative_powers

    @staticmethod
    def relative_flow(file_lines):
        """
        Extracts the Relative Core Flow rate from the provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        relative_flows = []
        for line in file_lines:
            if "Relative Flow . . . . . .  PERCWT" in line:
                p1 = line.index("PERCWT")
                p2 = line.index("%")
                search_space = line[p1:p2]
                search_space = search_space.replace("PERCWT","")
                relative_flows.append(float(search_space))

        return relative_flows

    @staticmethod
    def thermal_power(file_lines):
        """
        Extracts the operating thermal power in MW from the provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        powers = []
        for line in file_lines:
            if "Thermal Power . . . . . . . . CTP" in line:
                elems = line.strip().split()
                spot = elems.index('MWt')
                powers.append(float(elems[spot-1]))

        return powers

    @staticmethod
    def core_flow(file_lines):
        """
        Returns the core coolant flow in Mlb/hr from the provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        flows = []
        for line in file_lines:
            if "Core Flow . . . . . . . . . . CWT" in line:
                elems = line.strip().split()
                spot = elems.index("Mlb/hr")
                flows.append(float(elems[spot-1]))

        return flows

    @staticmethod
    def inlet_temperatures(file_lines):
        """
        Returns the core inlet temperatures in degrees Fahrenheit from the 
        provided simulate file lines.

        Written by Brian Andersen. 3/13/2020
        """
        temperatures = []
        for line in file_lines:
            if "Inlet . . . .TINLET" in line:
                p1 = line.index("K")
                p2 = line.index("F")
                search_space = line[p1:p2]
                search_space = search_space.replace("K","")
                temperatures.append(float(search_space))

        return temperatures

    @staticmethod
    def pressure(file_lines):
        """
        Returns the core exit pressure in PSIA.

        Written by Brian Andersen. 3/13/2020
        """
        pressure = []
        for line in file_lines:
            if "Core Exit Pressure  . . . . .  PR" in line:
                p1 = line.index("bar")
                p2 = line.index("PSIA")
                search_space = line[p1:p2]
                search_space = search_space.replace("bar","")
                pressure.append(float(search_space))

        return pressure

    @staticmethod
    def burnup_list(file_lines):
        """
        Extracts the cycle burnups at a each state point within the depletion.

        Written by Brian Andersen. 3/13/2020
        """
        burnups = []
        for line in file_lines:
            if "Cycle Exp." in line:
                elems = line.strip().split()
                spot = elems.index('GWd/MT')
                burnups.append(float(elems[spot-1]))

        return burnups

    @staticmethod
    def full_core_powers3D(file_lines,number_pins):
        """
        Extracts the pin powers from the output solution file as a dictionary
        with the assembly labels as the dictionary keys. 
 
        Parameters
        --------------
        file_lines: List
            The lines of the Simulate output file being analyzed.
        number_pins: INT
            The number of pins used per assembly.

        Written by Brian Andersen. 3/13/2020
        """
        state_count = 0
        rows = 0
        cols = 0
        axial = 0
        for line in file_lines:
            if "Full Core Assembly Map Width" in line:
                if not rows:
                    elems = line.strip().split()
                    rows = int(elems[-1])
                    cols = int(elems[-1])
            if 'DIM.CAL' in line:
                line = line.replace(",","")
                line = line.replace("/","")
                elems = line.strip().split()
                if elems[0] == "'DIM.CAL'":
                    axial = int(elems[1])
            if "Fueled Axial Nodes" in line:
                if not axial:
                    elems = line.strip().split()
                    spot = elems.index("Fueled")
                    axial = int(elems[spot-1])
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 56
            core_map = Maps(193)
            core_map = core_map.dict_assembly_map_193
        else:
            errmessage = "The number of assembly rows {} and columns {} is unrecognized".format(rows,cols)
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict["STATE_{}".format((i+1):04d)] = numpy.zeros([number_pins,number_pins,axial,number_assemblies])

        state_list = list(power_dict.keys())
        print(state_list)
        state_count = 0
        current_state = state_list[state_count]
        searching_pin_powers = False
        for line in file_lines:
            if 'Assembly Label' in line:
                row_count = 0
                new_line = line.replace(","," ")
                p1 = new_line.index("IA")
                p2 = new_line.index("Seg")
                section = new_line[p1:p2]
                section = section.replace("IA","")
                section = section.replace("JA","")
                section = section.replace("K","")
                section = section.replace("=","")
                elems = section.strip().split()
                current_assembly = core_map[int(elems[0])][int(elems[1])] - 1
                axial_position = int(elems[2]) - 1
            if " Studsvik CMS Steady-State" in line or "PIN.EDT 3PIN  - Peak Pin Power:              Assembly 3D" in line:
                searching_pin_powers = False
            elif "PIN.EDT 2PIN  - Peak Pin Power:              Assembly 2D" in line:
                searching_pin_powers = False
            if searching_pin_powers:
                line = line.replace(":","")
                line = line.replace("-","")
                line = line.replace("+","")
                elems = line.strip().split()
                if not elems:
                    pass
                else:
                    for i,value in enumerate(elems):
                        power_dict[current_state][row_count,i,axial_position,current_assembly] = float(value)
                    row_count += 1
            if "'3PXP' - Pin Power  Distribution:" in line:
                searching_pin_powers = True
            if "Output Summary" in line:
                state_count += 1
                if state_count < len(state_list):
                    current_state = state_list[state_count]

        return power_dict

    @staticmethod
    def assembly_pitch(file_lines):
        """
        Extracts the assembly pitch from the provided simulate output file lines
        """
        for line in file_lines:
            if "Assembly Pitch (Cold)" in line:
                elems = line.strip().split()
                assembly_pitch = float(elems[-2])
                break

        return assembly_pitch

    @staticmethod
    def nominal_core_wide_linear_power_rate(file_lines):
        """
        Returns the nominal core wide linear power rate. Its a derived property,
        so what the function really returns is the core rated power divided by the 
        total fuel rod length in the core.
        """
        core_power = None
        fuel_length = None
        for line in file_lines:
            if "Thermal Power . . . . . . . .CTP" in line:
                elems = line.strip().split()
                spot = elems.index("MWt")
                core_power = float(elems[spot-1])* 1.e3
            elif "Total Fuel Rod Length in Core" in line:
                elems = line.strip().split()
                fuel_length = float(elems[-2])
            if fuel_length and core_power:
                linear_power_rate = core_power/fuel_length
                break

        return linear_power_rate

    @staticmethod
    def axial_mesh_positions(file_lines):
        axial_positions = []
        searching_heights = False
        for line in file_lines:
            if "** Studsvik CMS Steady-State 3-D Reactor Simulator **" in line:
                searching_heights = False   #Found the Axial Powers.
                                       #Don't need to go through any more of file 
            if "Grid Location Information" in line:
                searching_heights = False
                break
            if searching_heights:
                line = line.replace("-","")
                elems = line.strip().split()
                if elems:
                    axial_positions.append(float(elems[-1]))
            if "Axial Nodal Boundaries (cm)" in line:
                searching_heights = True

        axial_positions.pop(0)  #I don't care about the axial positions in the reflectors
        axial_positions.pop(-1) #I only want positions in the active fuel region.

        return axial_positions

    @staticmethod
    def core_size(file_lines):
        """
        Extracts the number of rows and columns in the reactor core.
        """
        for line in file_lines:
            if 'DIM.PWR' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    rows = int(elems[2])
                    cols = int(elems[3])
                    break
                elif "IAFULL" in elems:
                    rows = int(elems[-1])
                    cols = int(elems[-1])
        
        return rows,cols

    @staticmethod
    def count_number_assemblies(file_lines):
        """
        Counts the number of assemblies utilized in the reactor core.
        """
        assembly_count = 0
        in_core_map = False
        for line in file_lines:
            if in_core_map:
                elems = line.strip().split()
                if elems[0] == "0" and elems[1] == '0':
                    in_core_map = False
                else:
                    assembly_count += len(elems) - 2
            if "'FUE.LAB'" in line:
                in_core_map = True

        return assembly_count

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
        











