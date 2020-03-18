import os
import sys
import h5py
import numpy
from matplotlib import pyplot as plt

def h5_converter(file_name):
    """
    Function for converting simulate output files to an H5 File using the VERA naming conventions.
    """
    file_ = open(file_name,'r')
    file_lines = file_.readlines()
    file_.close()

    SE = Simulate_Extractor()

    pin_power_dictionary = SE.full_core_powers3D(file_lines,17)
    exposure_efpds = SE.efpd_list(file_lines)
    exposures = SE.burnup_list(file_lines)
    boron = SE.boron_list(file_lines)
    pressure = SE.pressure(file_lines)
    flow = SE.relative_flow(file_lines)
    power = SE.relative_power(file_lines)
    core_inlet_temps = SE.inlet_temperatures(file_lines)
    keffs = SE.core_keff_list(file_lines)
    FDH_list = SE.FDH_list(file_lines)
    thermal_powers = SE.thermal_power(file_lines)
    core_flows = SE.core_flow(file_lines)
    Fqs = SE.pin_peaking_list(file_lines)

    print(f"List of Exposures in EFPD {exposure_efpds} Length {len(exposure_efpds)}")
    print(f"List of exposures in GWDMTU {exposures} Length {len(exposures)}")
    print(f"List of boron values {boron} Length {len(boron)}")
    print(f"List of pressure values {pressure} Length {len(pressure)}")
    print(f"List of flow values {flow} Length {len(flow)}")
    print(f"List of power values {power} Length {len(power)}")
    print(f"List of core inlet temps {core_inlet_temps} Length {len(core_inlet_temps)}")
    print(f"List of core keff values {keffs} Length {len(keffs)}")
    print(f"List of FDH values {FDH_list} Length {len(FDH_list)}")
    print(f"List of actual thermal power {thermal_powers} Length {len(thermal_powers)}")
    print(f"Core flow rate {core_flows} Length {len(core_flows)}")
    print(f"List of Fq values {Fqs} Length {len(Fqs)}")

    file_ = h5py.File(file_name.replace(".out",".h5"),'w')
    key_list = list(pin_power_dictionary.keys())
    for i,key in enumerate(key_list):
        g1 = file_.create_group(key)
        g1.create_dataset("pin_powers",data=pin_power_dictionary[key])
        g1.create_dataset("exposure_efpds",data=exposure_efpds[i+1])
        g1.create_dataset("boron",data=boron[i+1])
        g1.create_dataset("pressure",data=pressure[i+1])
        g1.create_dataset("flow",data=flow[i+1])
        g1.create_dataset("exposure",data=exposures[i+1])
        g1.create_dataset("core_inlet_temp",data=core_inlet_temps[i+1])
        g1.create_dataset("tinlet",data=core_inlet_temps[i+1])
        g1.create_dataset("power",data=power[i+1])
        g1.create_dataset("total_power",data=thermal_powers[i+1])
        g1.create_dataset("keff",data=keffs[i+1])
        g1.create_dataset("FDH",data=FDH_list[i+1])
        g1.create_dataset("Fq",data=Fqs[i+1])

    file_.close()

class Maps(object):
    """
    Class for the assembly maps used in the simulate extractor.
    """
    def __init__(self):
        self.assembly_map_15_15 = {}
        self.assembly_map_15_15[8] =  {8: 0,9:1 ,10:2 ,11:3 ,12:4 ,13:5 , 14:6,15:8 }
        self.assembly_map_15_15[9] =  {8: 9,9:10,10:11,11:12,12:13,13:14,14:15,15:16}
        self.assembly_map_15_15[10] = {8:17,9:18,10:19,11:20,12:21,13:22,14:23}
        self.assembly_map_15_15[11] = {8:24,9:25,10:26,11:27,12:28,13:29,14:30}
        self.assembly_map_15_15[12] = {8:31,9:32,10:33,11:34,12:35,13:36}
        self.assembly_map_15_15[13] = {8:37,9:38,10:39,11:40,12:41}
        self.assembly_map_15_15[14] = {8:42,9:43,10:44,11:45}
        self.assembly_map_15_15[15] = {8:46,9:47}

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
    def linear_power_rate_3D(,file_lines):
        """
        Extracts the linear power rate from Simulate as a dictionary.

        Parameters
            file_lines: list
                All the output lines of the simulate file as a list.

        Written by Brian Andersen. 1/9/2020
        """
        state_count = -1
        for line in file_lines:
            if 'DIM.PWR' in line:
                print(line)
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'DIM.CAL' in line:
                elems = line.strip().split()
                if elems[0] == "'DIM.CAL'":
                    axial = int(elems[1])
                    print(axial)
            if 'Output Summary' in line:
                state_count += 1

        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.assembly_map_15_15
        else:
            errmessage = f"The number of assembly rows {rows} and columns {cols} is unrecognized"
            return ValueError(errmessage)

        for i in range(state_count):
            power_dict[f"STATE_{(i+1):04d}"] = numpy.zeros([axial,number_assemblies])

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
                print(line)
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    print(elems[2])
                    print(elems[3])
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.assembly_map_15_15
        else:
            errmessage = f"The number of assembly rows {rows} and columns {cols} is unrecognized"
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict[f"STATE_{(i+1):04d}"] = numpy.zeros([1,number_assemblies])

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
                print(line)
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    print(elems[2])
                    print(elems[3])
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.assembly_map_15_15
        else:
            errmessage = f"The number of assembly rows {rows} and columns {cols} is unrecognized"
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict[f"STATE_{(i+1):04d}"] = numpy.zeros([1,number_assemblies])

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
        state_count = -1
        for line in file_lines:
            if 'DIM.PWR' in line:
                print(line)
                elems = line.strip().split()
                if elems[0] == "'DIM.PWR'":
                    print(elems[2])
                    print(elems[3])
                    rows = int(elems[2])
                    cols = int(elems[3])
            if 'DIM.CAL' in line:
                print(line)
                elems = line.strip().split()
                if elems[0] == "'DIM.CAL'":
                    print("Fuck")
                    print(elems[1])
                    axial = int(elems[1])
                    print(axial)
            if 'Output Summary' in line:
                state_count += 1
        
        power_dict = {}
        if rows == 15 and cols == 15:
            number_assemblies = 48
            core_map = Maps()
            core_map = core_map.assembly_map_15_15
        else:
            errmessage = f"The number of assembly rows {rows} and columns {cols} is unrecognized"
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict[f"STATE_{(i+1):04d}"] = numpy.zeros([number_pins,number_pins,axial,number_assemblies])

        state_list = list(power_dict.keys())
        state_count = -1
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
                current_assembly = core_map[int(elems[0])][int(elems[1])]
                axial_position = int(elems[2]) - 1
            if " Studsvik CMS Steady-State" in line:
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

class Full_Core_Cobra_Writer(object):
    """
    Writes input files for a full reactor core in CTF utilizing the CTF preprocessor.
    """
    def __init__(self):
        self.radial_assembly_powers = None #The assembly peaking. Not FdeltaH or Fq.
        self.linear_powers = None #The linear power rate for each assembly
        self.pin_powers = None #The three dimensional pin powers of each assembly. 

    def extract_data_from_simulate(self,file_name):
        """
        Opens the provided simulate data file and extracts everything needed to write the CTF preprocessor file.
        """
        file_ = open(file_name,'r')
        file_lines = file_.readlines()
        file_.close()

        self.radial_assembly_powers = Extractor.radial_assembly_power_2D(file_lines)
        self.linear_powers = Extractor.linear_power_rate_3D(file_lines)
        self.pin_powers = Extractor.full_core_powers3D(file_lines)

    def write_input_files(self,state):
        """
        Function for writing the CTF preprocessor input files.
        """

if __name__ == "__main__":
    pass    

