import os
import sys
import h5py
import numpy
import argparse
import openpyxl
from matplotlib import pyplot as plt

def h5_converter(file_name):
    """
    Function for converting simulate output files to an H5 File using the VERA naming conventions.
    Also generates a VERA Input file based off the read output file. 
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
   # nominal_linear_power_rate = SE.nominal_core_wide_linear_power_rate(file_lines)
    apitch = SE.assembly_pitch(file_lines)
    axial_mesh_reverse = SE.axial_mesh_positions(file_lines)
    axial_mesh = []
    for axial in axial_mesh_reverse:
        axial_mesh.insert(0,axial)
    axial_mesh = [axial + 11.951 for axial in axial_mesh]
    maps = Maps(193)

    
    core_flower = Calculator.convert_tons_to_kg(core_flows[0])
    core_flower = Calculator.convert_hours_to_seconds(core_flower)
    vera_mesh = [11.951,15.817,24.028,32.239,40.45,48.662,56.873,65.084,73.295,77.105,
                 85.17,93.235,101.3,109.365,117.43,125.495,129.305,137.37,145.435,153.5,
                 161.565,169.63,177.695,181.505,189.57,197.635,205.7,213.765,221.83,229.895,
                 233.705,241.77,249.835,257.9,265.965,274.03,282.095,285.905,293.97,302.035,
                 310.1,318.165,326.23,334.295,338.105,346.0262,353.9474,361.8686,369.7898,377.711]
    file_ = h5py.File(file_name.replace(".out",".h5"),'w')
    g1 = file_.create_group("CORE")
    g1.create_dataset("apitch",data=apitch)
    g1.create_dataset("axial_mesh",data=axial_mesh)
    #g1.create_dataset("axial_mesh",data=vera_mesh)
    #g1.create_dataset("nominal_linear_heat_rate",data=nominal_linear_power_rate)
    g1.create_dataset('core_map',data=maps.array_assembly_map_15_15.astype(int))
    #g1.create_dataset('rated_flow',data=core_flower)
    #g1.create_dataset('rated_flow_units',data="Kg/s")
    g1.create_dataset('rated_power',data=thermal_powers[0])
    g1.create_dataset('core_sym',data=4)
 #   g1.create_dataset('xlabel',data=numpy.array['H','G','F','E','D',"C","B","A"].astype(str))
 #   g1.create_dataset('ylabel',data=numpy.array['1','2','3','4','5','6','7','8'].astype(str))
    key_list = list(pin_power_dictionary.keys())
    for i,key in enumerate(key_list):
        g1 = file_.create_group(key)
        vera_powers = Calculator.interpolate_powers_between_meshes(axial_mesh,
                                                                   vera_mesh,
                                                                   pin_power_dictionary[key])
        #g1.create_dataset("pin_powers",data=pin_power_dictionary[key])
        g1.create_dataset("pin_powers",data=vera_powers)
        g1.create_dataset("exposure_efpds",data=exposure_efpds[i])
        g1.create_dataset("boron",data=boron[i])
        g1.create_dataset("pressure",data=pressure[i])
        g1.create_dataset("flow",data=flow[i])
        g1.create_dataset("exposure",data=exposures[i])
        g1.create_dataset("core_inlet_temp",data=core_inlet_temps[i])
        g1.create_dataset("tinlet",data=core_inlet_temps[i])
        g1.create_dataset("power",data=power[i])
        g1.create_dataset("total_power",data=thermal_powers[i])
        g1.create_dataset("keff",data=keffs[i])
        g1.create_dataset("FDH",data=FDH_list[i])
        g1.create_dataset("Fq",data=Fqs[i])

    file_.close()


    file_ = open("vera_"+file_name.replace(".out",".inp"),'w')
    file_.write("[CASEID]\n")
    file_.write("    title 'VERA Test Writer'\n")
    file_.write("\n")
    current_tinlet = None
    current_flow = None
    current_pressure = None
    current_power = None
    first_state = True
    for i,key in enumerate(list(pin_power_dictionary.keys())):
        if key == "CORE":
            pass
        else:
            if first_state:
                first_state = False
                current_tinlet =   core_inlet_temps[i]
                current_flow =     flow[i]
                current_pressure = pressure[i]
                current_power =    power[i]
                file_.write("[STATE]\n")
                file_.write("    title 'VERAtest'\n")
                file_.write(f"    pressure {current_pressure}\n")
                file_.write("    sym      qtr\n")
                file_.write("    feedback    on\n")
                file_.write("    crud        on\n")
                file_.write("    search   boron\n")
                file_.write("    cool_chem 35E-6  2.2  0.19  4.0  1.8\n")
                file_.write("\n")
                file_.write("    rodbank SA 230 \nSB 230\n")
                file_.write("            SC 230\n")
                file_.write("            SD 230\n")
                file_.write("            A 230\n")
                file_.write("            B 230\n")
                file_.write("            C 230\n")
                file_.write("            D 230\n")
                file_.write("\n")
                file_.write("    thexp       off\n")
                file_.write("\n")
                file_.write(f"    power {current_power}\n")
                file_.write(f"    flow {current_flow}\n")  
                file_.write(f"    tinlet {current_tinlet} F\n")
                file_.write("     deplete EFPD 0.0\n")
                file_.write(f"     boron {boron[i]}\n")
            else:
                file_.write("[STATE]  ")
                if current_tinlet == core_inlet_temps[i]:
                    pass
                else:
                    current_tinlet = core_inlet_temps[i]
                    file_.write(f"tinlet {current_tinlet} F; ")
                if current_flow == flow[i]:
                    pass
                else:
                    current_flow = flow[i]
                    file_.write(f"flow {current_flow} ; ")
                if current_pressure == pressure[i]:
                    pass
                else:
                    current_pressure = pressure[i]
                    file_.write(f"pressure {current_pressure} ; ")
                if current_power == power[i]:
                    pass
                else:
                    current_power = power[i]
                    file_.write(f"power {current_power} ; ")
                file_.write(f" deplete EFPD {exposure_efpds[i]} ; boron {boron[i]} \n")

    file_.write("[CORE]\n")
    file_.write("  name   WBN\n")
    file_.write("  unit   1\n")
    file_.write("  size   15              ! assemblies across core\n")
    file_.write(f"  apitch {apitch}\n")
    file_.write(f"  rated  {thermal_powers[0]} {core_flows[0]}     ! MW, Mlbs/hr\n")
    file_.write("  height 406.337\n")
    file_.write("\n")
    file_.write("  xlabel  R P N M L K J H G  F  E  D  C  B  A\n")
    file_.write("  ylabel  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n")
    file_.write("\n")
    file_.write("  core_shape\n")
    file_.write("    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n")
    file_.write("    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n")
    file_.write("    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n")
    file_.write("    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n")
    file_.write("    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n")
    file_.write("    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n")
    file_.write("    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n")
    file_.write("    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n")
    file_.write("\n")
    file_.write("  assm_map\n")
    file_.write("    1\n")
    file_.write("    2 1\n")
    file_.write("    1 2 1\n")
    file_.write("    2 1 2 1\n")
    file_.write("    1 2 1 2 2\n")
    file_.write("    2 1 2 1 2 3\n")
    file_.write("    1 3 1 3 3 3 \n")
    file_.write("    3 3 3 3 \n")
    file_.write("\n")
    file_.write("  insert_map\n")
    file_.write("     -     \n")
    file_.write("    20 TP    \n")
    file_.write("     - 24  -   \n")
    file_.write("    20 TP 20  -  \n")
    file_.write("     - 20 TP 20  - \n")
    file_.write("    20  - 16  - 24 12\n")
    file_.write("     - 24  - 16  - TP\n")
    file_.write("    12 TP  8 TP\n")
    file_.write("\n")
    file_.write("  crd_map\n")
    file_.write("    1 \n")
    file_.write("    - - \n")
    file_.write("    1 - 1 \n")
    file_.write("    - - - 1 \n")
    file_.write("    1 - - - 1 \n")
    file_.write("    - 1 - 1 - - \n")
    file_.write("    1 - 1 - 1 - \n")
    file_.write("    - - - - \n")
    file_.write("\n")
    file_.write("  crd_bank\n")
    file_.write("     D  -  A  -  D  -  C  -\n")
    file_.write("     -  -  -  -  - SB  -  -\n")
    file_.write("     A  -  C  -  -  -  B  -\n")
    file_.write("     -  -  -  A  - SC  -  -\n")
    file_.write("     D  -  -  -  D  - SA \n")
    file_.write("     - SB  - SD  -  -  - \n")
    file_.write("     C  -  B  - SA  - \n")
    file_.write("     -  -  -  -\n")
    file_.write("\n")
    file_.write("  det_map 193*2\n")
    file_.write("!# det_map\n")
    file_.write("!#           - - 1 - - 1 - \n")
    file_.write("!#       1 - - 1 - 1 - - - - - \n")
    file_.write("!#     - - - - - - 1 - 1 - 1 - 1\n")
    file_.write("!#     1 1 - - - - 1 - - - - - -\n")
    file_.write("!#   - - - - 1 - - - 1 - 1 - 1 - -\n")
    file_.write("!#   1 - 1 - - 1 - 1 - - - - - 1 -\n")
    file_.write("!#   - - - 1 - - 1 - - 1 - - 1 - -\n")
    file_.write("!#   1 - 1 - 1 - 1 - - 1 - 1 1 1 -\n")
    file_.write("!#   - 1 - - - - - - 1 - 1 - - - 1\n")
    file_.write("!#   - - - - 1 - 1 - - - - 1 - - -\n")
    file_.write("!#   1 - - - 1 - - 1 - - 1 - - - 1\n")
    file_.write("!#     - - - - 1 - - 1 - - 1 - - \n")
    file_.write("!#     - 1 - 1 - - 1 - - - - - 1 \n")
    file_.write("!#       1 - - - 1 - - 1 - 1 - \n")
    file_.write("!#           1 - - 1 - - - \n")
    file_.write("\n")
    file_.write("  baffle ss 0.19 2.85\n") 
    file_.write('\n')
    file_.write("  vessel  mod 187.96        ! barrel IR (cm)\n")
    file_.write("           ss 193.68        ! barrel OR (cm)\n")
    file_.write("          mod 219.15        ! vessel liner IR (cm)\n")
    file_.write("           ss 219.71        ! vessel liner OR / vessel IR (cm)\n")
    file_.write("           cs 241.70        ! vessel OR (cm)\n")
    file_.write("\n")
    file_.write("  pad ss  194.64 201.63 32 45 135 225 315 ! neutron pad ID,OD arc lenth (degrees), and angular positions (degrees)\n")
    file_.write("\n")
    file_.write("  lower_plate ss  5.0 0.5   ! mat, thickness, vol frac\n")
    file_.write("  upper_plate ss  7.6 0.5   ! mat, thickness, vol frac\n")
    file_.write("\n")
    file_.write("! lower_ref  mod 20.0 1.0   ! not needed\n")
    file_.write("! upper_ref  mod 20.0 1.0   !\n")
    file_.write('\n')
    file_.write("  xlabel  R P N M L K J H G  F  E  D  C  B  A\n")
    file_.write("  ylabel  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n")
    file_.write("\n")
    file_.write("[ASSEMBLY]\n")
    file_.write('  title "Westinghouse 17x17"\n')
    file_.write("  npin 17 \n")
    file_.write("  ppitch 1.260\n")
    file_.write("  \n")
    file_.write("  fuel U21 10.257 94.5 / 2.110 u-234 0.017364\n")
    file_.write("  fuel U26 10.257 94.5 / 2.619 u-234 0.021947\n")
    file_.write("  fuel U31 10.257 94.5 / 3.100 u-234 0.026347 \n")
    file_.write("\n")
    file_.write("  cell 1     0.4096 0.418 0.475 / U21 he zirc4\n")
    file_.write("  cell 2     0.4096 0.418 0.475 / U26 he zirc4\n")
    file_.write("  cell 3     0.4096 0.418 0.475 / U31 he zirc4\n")
    file_.write("  cell 4            0.561 0.602 / mod    zirc4      ! guide/instrument tube\n")
    file_.write("  cell 5            0.418 0.475 /     he zirc4      ! plenum\n")
    file_.write("  cell 6                  0.475 /        zirc4      ! plug\n")
    file_.write("  cell 7                  0.475 /        mod        ! empty\n")
    file_.write("\n")
    file_.write("  lattice LAT21 \n")
    file_.write("       4\n")
    file_.write("       1 1\n")
    file_.write("       1 1 1\n")
    file_.write("       4 1 1 4\n")
    file_.write("       1 1 1 1 1\n")
    file_.write("       1 1 1 1 1 4\n")
    file_.write("       4 1 1 4 1 1 1\n")
    file_.write("       1 1 1 1 1 1 1 1\n")
    file_.write("       1 1 1 1 1 1 1 1 1\n")
    file_.write("\n")
    file_.write("  lattice LAT26  \n")
    file_.write("       4\n")
    file_.write("       2 2\n")
    file_.write("       2 2 2\n")
    file_.write("       4 2 2 4\n")
    file_.write("       2 2 2 2 2\n")
    file_.write("       2 2 2 2 2 4\n")
    file_.write("       4 2 2 4 2 2 2\n")
    file_.write("       2 2 2 2 2 2 2 2\n")
    file_.write("       2 2 2 2 2 2 2 2 2\n")
    file_.write("\n")
    file_.write("  lattice LAT31 \n")
    file_.write("       4\n")
    file_.write("       3 3\n")
    file_.write("       3 3 3\n")
    file_.write("       4 3 3 4\n")
    file_.write("       3 3 3 3 3\n")
    file_.write("       3 3 3 3 3 4\n")
    file_.write("       4 3 3 4 3 3 3\n")
    file_.write("       3 3 3 3 3 3 3 3\n")
    file_.write("       3 3 3 3 3 3 3 3 3\n")
    file_.write("\n")
    file_.write("  lattice PLEN\n")
    file_.write("       4\n")
    file_.write("       5 5\n")
    file_.write("       5 5 5\n")
    file_.write("       4 5 5 4\n")
    file_.write("       5 5 5 5 5\n")
    file_.write("       5 5 5 5 5 4\n")
    file_.write("       4 5 5 4 5 5 5\n")
    file_.write("       5 5 5 5 5 5 5 5\n")
    file_.write("       5 5 5 5 5 5 5 5 5\n")
    file_.write("\n")
    file_.write("  lattice PLUG\n")
    file_.write("       4\n")
    file_.write("       6 6\n")
    file_.write("       6 6 6\n")
    file_.write("       4 6 6 4\n")
    file_.write("       6 6 6 6 6\n")
    file_.write("       6 6 6 6 6 4\n")
    file_.write("       4 6 6 4 6 6 6\n")
    file_.write("       6 6 6 6 6 6 6 6\n")
    file_.write("       6 6 6 6 6 6 6 6 6\n")
    file_.write("\n")
    file_.write("  lattice GAP \n")
    file_.write("       4\n")
    file_.write("       7 7\n")
    file_.write("       7 7 7\n")
    file_.write("       4 7 7 4\n")
    file_.write("       7 7 7 7 7\n")
    file_.write("       7 7 7 7 7 4\n")
    file_.write("       4 7 7 4 7 7 7\n")
    file_.write("       7 7 7 7 7 7 7 7\n")
    file_.write("       7 7 7 7 7 7 7 7 7\n")
    file_.write("\n")
    file_.write("  axial  1  6.053 GAP 10.281 PLUG 11.951 LAT21 377.711 PLEN 393.711 PLUG 395.381 GAP 397.51\n")
    file_.write("  axial  2  6.053 GAP 10.281 PLUG 11.951 LAT26 377.711 PLEN 393.711 PLUG 395.381 GAP 397.51\n")
    file_.write("  axial  3  6.053 GAP 10.281 PLUG 11.951 LAT31 377.711 PLEN 393.711 PLUG 395.381 GAP 397.51\n")
    file_.write("\n")
    file_.write("  grid END inc    3.866 1017 !0.9070 ! grid height (cm), mass (g), loss coef\n")
    file_.write("  grid MID zirc4  3.810 875  !0.9065 ! grid height (cm), mass (g), loss coef\n")
    file_.write("\n")
    file_.write("  grid_axial\n")
    file_.write("      END  13.884\n")
    file_.write("      MID  75.2\n")
    file_.write("      MID 127.4\n")
    file_.write("      MID 179.6\n")
    file_.write("      MID 231.8\n")
    file_.write("      MID 284.0\n")
    file_.write("      MID 336.2\n")
    file_.write("      END 388.2\n")
    file_.write("\n")
    file_.write("  lower_nozzle  ss 6.053 6250.0  ! mat, height, mass (g)\n")
    file_.write("  upper_nozzle  ss 8.827 6250.0  ! mat, height, mass (g)\n")
    file_.write("\n")
    file_.write("[INSERT]\n")
    file_.write('  title "Pyrex"\n')
    file_.write("  npin 17\n")
    file_.write("\n")
    file_.write("  cell X  0.214 0.231 0.241 0.427 0.437 0.484 / he ss he pyrex-vera he ss ! pyrex\n")
    file_.write("  cell P                          0.437 0.484 /                     he ss ! plenum\n")
    file_.write("  cell G                                0.484 /                        ss ! plug/cap\n")
    file_.write("  cell T                                0.538 /                        ss ! thimble plug\n")
    file_.write(" \n")
    file_.write("  rodmap  PY8 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     X - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - X\n")
    file_.write("     - - - - - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PY12 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     X - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - -\n")
    file_.write("     - - - X - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PY16\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     X - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - X\n")
    file_.write("     - - - X - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PY20\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     X - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - X\n")
    file_.write("     X - - X - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PY24  \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     X - - X\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - X\n")
    file_.write("     X - - X - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PL8 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     - - - - - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PL12 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - -\n")
    file_.write("     - - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PL16\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     - - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PL20\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     P - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PL24  \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - P\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     P - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PG8 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - G\n")
    file_.write("     - - - - - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PG12 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - -\n")
    file_.write("     - - - G - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PG16\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - G\n")
    file_.write("     - - - G - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PG20\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - G\n")
    file_.write("     G - - G - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  PG24  \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - G\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - G\n")
    file_.write("     G - - G - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  TP8 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - T\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     T - - T - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  TP12 \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - T\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - T\n")
    file_.write("     T - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  TP16\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - T\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     T - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  TP20\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - T\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     P - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap  TP24  \n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     T - - T\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - T\n")
    file_.write("     T - - T - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("\n")
    file_.write("  axial   8  13.221 PG8  15.761 PY8  376.441 PL8  383.31 TP8  398.641\n")
    file_.write("  axial  12  13.221 PG12 15.761 PY12 376.441 PL12 383.31 TP12 398.641\n")
    file_.write("  axial  16  13.221 PG16 15.761 PY16 376.441 PL16 383.31 TP16 398.641\n")
    file_.write("  axial  20  13.221 PG20 15.761 PY20 376.441 PL20 383.31 TP20 398.641\n")
    file_.write("  axial  24  13.221 PG24 15.761 PY24 376.441 PL24             398.641\n")
    file_.write("  axial  TP                                       383.31 TP24 394.31\n")
    file_.write("\n")
    file_.write("[CONTROL]\n")
    file_.write('  title "B4C with AIC tips"\n')
    file_.write("  npin 17\n")
    file_.write("  stroke  365.125 230     ! approx for 1.5875 step sizes and 230 max stroke\n")
    file_.write("\n")
    file_.write("  cell A  0.382 0.386 0.484 / aic he ss\n")
    file_.write("  cell B  0.373 0.386 0.484 / b4c he ss\n")
    file_.write("  cell P        0.386 0.484 /     he ss ! plenum\n")
    file_.write("  cell G              0.484 /        ss ! plug   \n")
    file_.write("\n")
    file_.write("  rodmap AIC\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     A - - A\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - A\n")
    file_.write("     A - - A - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap B4C\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     B - - B\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - B\n")
    file_.write("     B - - B - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap PLEN\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     P - - P\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - P\n")
    file_.write("     P - - P - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  rodmap PLUG\n")
    file_.write("     -\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     G - - G\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - G\n")
    file_.write("     G - - G - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  axial  1    15.131\n")
    file_.write("        PLUG  17.031\n") 
    file_.write("         AIC 118.631\n") 
    file_.write("         B4C 377.711\n") 
    file_.write("        PLEN 388.411\n")
    file_.write("        PLUG 390.311\n")
    file_.write("\n")
    file_.write("[DETECTOR]\n")
    file_.write('  title "Incore instrument thimble"\n')
    file_.write("  npin 17\n")
    file_.write("\n")
    file_.write("  cell 1  0.258 0.382 / he ss\n")
    file_.write("\n")
    file_.write("  rodmap  LAT  \n")
    file_.write("     1\n")
    file_.write("     - -\n")
    file_.write("     - - -\n")
    file_.write("     - - - -\n")
    file_.write("     - - - - -\n")
    file_.write("     - - - - - -\n")
    file_.write("     - - - - - - -\n")
    file_.write("     - - - - - - - -\n")
    file_.write("     - - - - - - - - -\n")
    file_.write("\n")
    file_.write("  axial 1  0.0 LAT 397.51 \n")
    file_.write("  axial 2  0.0 LAT 397.51 \n")
    file_.write("\n")
    file_.write("[EDITS]\n")
    file_.write("  axial_edit_bounds \n")
    file_.write("      11.951\n")
    file_.write("      15.817 \n")
    file_.write("      24.028 \n")
    file_.write("      32.239 \n")
    file_.write("      40.45 \n")
    file_.write("      48.662 \n")
    file_.write("      56.873 \n")
    file_.write("      65.084 \n")
    file_.write("      73.295 \n")
    file_.write("      77.105 \n")
    file_.write("      85.17 \n")
    file_.write("      93.235 \n")
    file_.write("      101.3 \n")
    file_.write("      109.365 \n")
    file_.write("      117.43 \n")
    file_.write("      125.495 \n")
    file_.write("      129.305 \n")
    file_.write("      137.37 \n")
    file_.write("      145.435 \n")
    file_.write("      153.5 \n")
    file_.write("      161.565 \n")
    file_.write("      169.63 \n")
    file_.write("      177.695 \n")
    file_.write("      181.505 \n")
    file_.write("      189.57 \n")
    file_.write("      197.635 \n")
    file_.write("      205.7 \n")
    file_.write("      213.765 \n")
    file_.write("      221.83 \n")
    file_.write("      229.895 \n")
    file_.write("      233.705 \n")
    file_.write("      241.77 \n")
    file_.write("      249.835 \n")
    file_.write("      257.9 \n")
    file_.write("      265.965 \n")
    file_.write("      274.03 \n")
    file_.write("      282.095 \n")
    file_.write("      285.905 \n")
    file_.write("      293.97 \n")
    file_.write("      302.035 \n")
    file_.write("      310.1 \n")
    file_.write("      318.165 \n")
    file_.write("      326.23 \n")
    file_.write("      334.295 \n")
    file_.write("      338.105 \n")
    file_.write("      346.0262 \n")
    file_.write("      353.9474 \n")
    file_.write("      361.8686 \n")
    file_.write("      369.7898 \n")
    file_.write("      377.711\n")
    file_.write("\n")
    file_.write("[MPACT]\n")
    file_.write("  num_space   464\n")
    file_.write("\n")
    file_.write("\n")
    file_.write("[COBRATF]\n")
    file_.write("  proc_per_assem 4\n")
    file_.write("  crud_details   1           \n")       
    file_.write("  model_corrosion 1\n")
    file_.write("\n")
    file_.write("[MAMBA]\n")
    file_.write("! ----- settings to generate sufficient CRUD for CIPS demonstration\n")
    file_.write("  !!ksnb_Fe2O4  4.0E-3\n")
    file_.write("  !!chimney_htc 50.0\n")
    file_.write("  !!chimney_vf  0.90\n")
    file_.write("  model_erosion 2  \n")
    file_.write("LTB_dissolve_scale 0.5\n")
    file_.close()

def quantum_converter(output_file,file_list):
    file_ = open(file_list,'r')
    file_lines = file_.readlines()
    file_.close()
    
    excel = openpyxl.Workbook()
    print(excel.sheetnames)
    excel.save(f'{output_file}.xlsx')

    excel['Sheet']["A1"] = "Assemblies"
    L1 = get_cell_column(70)
    L2 = get_cell_column(71)
    excel['Sheet'][f"{L1}1"] = "EFPD"
    excel['Sheet'][f"{L2}1"] = "Fq"
    for row,folder in enumerate(file_lines):
        folder = folder.strip().split()
        folder = folder[0]
        in_file = open(f'{folder}/{folder}_sim.inp','r') #Simulate input file
        in_lines = in_file.readlines()
        in_file.close()

        out_file = open(f'{folder}/{folder}_sim.out','r') #Simulate output file
        out_lines = out_file.readlines()
        out_file.close()

        Fq_list = Simulate_Extractor.pin_peaking_list(out_lines)
        efpd_list = Simulate_Extractor.efpd_list(out_lines)

        loading_pattern = []
        for line in in_lines:
            elems = line.strip().split()
            if not elems:
                pass
            else:
                for el in elems[2:]:
                    if el == '5':
                        loading_pattern.append(0)
                    elif el == '15':
                        loading_pattern.append(1)
                    
        for i,assem in enumerate(loading_pattern):
            col = get_cell_column(i)
            excel['Sheet'][f"{col}{row+2}"] = assem
        excel['Sheet'][f"{L1}{row+2}"] = efpd_list[-1]
        excel['Sheet'][f"{L2}{row+2}"] = max(Fq_list)

    excel.save(f'{output_file}.xlsx')

def simulateh5_2_veraH5(vera_name,simulate_file,template_h5):
    """
    Correctly sets up the VERA H5 file for runs.
    """
    sim = h5py.File(simulate_file,'r')

    vera_mesh = [11.951,15.817,24.028,32.239,40.45,48.662,56.873,65.084,73.295,77.105,
                 85.17,93.235,101.3,109.365,117.43,125.495,129.305,137.37,145.435,153.5,
                 161.565,169.63,177.695,181.505,189.57,197.635,205.7,213.765,221.83,229.895,
                 233.705,241.77,249.835,257.9,265.965,274.03,282.095,285.905,293.97,302.035,
                 310.1,318.165,326.23,334.295,338.105,346.0262,353.9474,361.8686,369.7898,377.711]
    key_list = list(sim.keys())
    print(f"copy {template_h5} {vera_name}")
    os.system(f"copy {template_h5} {vera_name}")
    vera = h5py.File(vera_name,'a')
    map_ = Maps(193)
    for key in key_list:
        print(key)
        if key == 'CORE':
            pass
        else:
            g1 = vera.create_group(key)
            for cool in sim[key]:
                if cool == 'pin_powers':
                    vera_powers = Calculator.interpolate_powers_between_meshes(sim['CORE']['axial_mesh'],
                                                                               vera_mesh,
                                                                               sim[key]['pin_powers'])
                    g1.create_dataset('pin_powers',data=vera_powers)
                else:
                    g1.create_dataset(cool,data=sim[key][cool])

    sim.close()
    vera.close()

def vera_writer(sim_file,vera_template):
    """
    Does the full VERA input analysis
    """
    h5_converter(sim_file)
    simulateh5_2_veraH5("vera_"+sim_file.replace(".out",".h5"),sim_file.replace(".out",".h5"),vera_template)

class Maps(object):
    """
    Class for the assembly maps used in the simulate extractor.
    """
    def __init__(self,number_assemblies):
        self.dict_assembly_map_157 = {}
        self.dict_assembly_map_157[8] =  {8: 1,9:2 ,10:3 ,11:4 ,12:5 ,13:6 , 14:7,15:8 }
        self.dict_assembly_map_157[9] =  {8: 9,9:10,10:11,11:12,12:13,13:14,14:15,15:16}
        self.dict_assembly_map_157[10] = {8:17,9:18,10:19,11:20,12:21,13:22,14:23}
        self.dict_assembly_map_157[11] = {8:24,9:25,10:26,11:27,12:28,13:29,14:30}
        self.dict_assembly_map_157[12] = {8:31,9:32,10:33,11:34,12:35,13:36}
        self.dict_assembly_map_157[13] = {8:37,9:38,10:39,11:40,12:41}
        self.dict_assembly_map_157[14] = {8:42,9:43,10:44,11:45}
        self.dict_assembly_map_157[15] = {8:46,9:47}
        
        self.dict_assembly_map_193 = {}
        self.dict_assembly_map_193[8] =  {8: 1,9:2 ,10:3 ,11:4 ,12:5 ,13:6 , 14:7,15:8 }
        self.dict_assembly_map_193[9] =  {8: 9,9:10,10:11,11:12,12:13,13:14,14:15,15:16}
        self.dict_assembly_map_193[10] = {8:17,9:18,10:19,11:20,12:21,13:22,14:23,15:24}
        self.dict_assembly_map_193[11] = {8:25,9:26,10:27,11:28,12:29,13:30,14:31,15:32}
        self.dict_assembly_map_193[12] = {8:33,9:34,10:35,11:36,12:37,13:38,14:39}
        self.dict_assembly_map_193[13] = {8:40,9:41,10:42,11:43,12:44,13:45,14:46}
        self.dict_assembly_map_193[14] = {8:47,9:48,10:49,11:50,12:51,13:52}
        self.dict_assembly_map_193[15] = {8:53,9:54,10:55,11:56}

        if number_assemblies == 157:
            array_dict = {0 :{0:None, 1:None,  2:None,  3:None,  4:None,  5:None,  6:47,  7:46,  8:16,  9:None,  10:None  , 11:None, 12:None, 13:None, 14:None},
                          1 :{0:None, 1:None,  2:None,  3:None,  4:45,    5:44,    6:43,  7:42,  8:15,  9:23,    10:30,     11:None, 12:None, 13:None, 14:None},
                          2 :{0:None, 1:None,  2:None,  3:41,    4:40,    5:39,    6:38,  7:37,  8:14,  9:22,    10:29,     11:36,   12:None, 13:None, 14:None},
                          3 :{0:None, 1:None,  2:36,    3:35,    4:34,    5:33,    6:32,  7:31,  8:13,  9:21,    10:28,     11:35,   12:41,   13:None, 14:None},
                          4 :{0:None, 1:30,    2:29,    3:28,    4:27,    5:26,    6:25,  7:24,  8:12,  9:20,    10:27,     11:34,   12:40,   13:45,   14:None},
                          5 :{0:None, 1:23,    2:22,    3:21,    4:20,    5:19,    6:18,  7:17,  8:11,  9:19,    10:26,     11:33,   12:39,   13:44,   14:None},
                          6 :{0:16,   1:15,    2:14,    3:13,    4:12,    5:11,    6:10,  7:9,   8:10,  9:18,    10:25,     11:32,   12:38,   13:43,   14:47},
                          7 :{0:8,    1:7,     2:6,     3:5,     4:4,     5:3,     6:2,   7:1,   8:2,   9:3,     10:4,      11:5,    12:6,    13:7,    14:8},
                          8 :{0:47,   1:43,    2:38,    3:32,    4:25,    5:18,    6:10,  7:9,   8:10,  9:11,    10:12,     11:13,   12:14,   13:15,   14:16},                                                           
                          9 :{0:None, 1:44,    2:39,    3:33,    4:26,    5:19,    6:11,  7:17,  8:18,  9:19,    10:20,     11:21,   12:22,   13:23,   14:None},
                          10:{0:None, 1:45,    2:40,    3:34,    4:27,    5:20,    6:12,  7:24,  8:25,  9:26,    10:27,     11:28,   12:29,   13:30,   14:None},
                          11:{0:None, 1:None,  2:41,    3:35,    4:28,    5:21,    6:13,  7:31,  8:32,  9:33,    10:34,     11:35,   12:36,   13:None, 14:None},
                          12:{0:None, 1:None,  2:None,  3:36,    4:29,    5:22,    6:14,  7:37,  8:38,  9:39,    10:40,     11:41,   12:None, 13:None, 14:None},
                          13:{0:None, 1:None,  2:None,  3:None,  4:30,    5:23,    6:15,  7:42,  8:43,  9:44,    10:45,     11:None, 12:None, 13:None, 14:None},
                          14:{0:None, 1:None,  2:None,  3:None,  4:None,  5:None,  6:16,  7:46,  8:47,  9:None,  10:None  , 11:None, 12:None, 13:None, 14:None}} 

            self.array_assembly_map_15_15 = numpy.zeros([15,15])
            for i in range(15):
                for j in range(15):
                    if not array_dict[i][j]:
                        pass
                    else:
                        self.array_assembly_map_15_15[i][j] = array_dict[i][j]
        elif number_assemblies == 193:
            array_dict = {0 :{0:None, 1:None,  2:None,  3:None,  4:56, 5:55, 6:54,  7:53,  8:16,  9:24,  10:32, 11:None, 12:None, 13:None, 14:None},
                          1 :{0:None, 1:None,  2:52,    3:51,    4:50, 5:49, 6:48,  7:47,  8:15,  9:23,  10:31, 11:39,   12:46,   13:None, 14:None},
                          2 :{0:None, 1:46,    2:45,    3:44,    4:43, 5:42, 6:41,  7:40,  8:14,  9:22,  10:30, 11:38,   12:45,   13:52,   14:None},
                          3 :{0:None, 1:39,    2:38,    3:37,    4:36, 5:35, 6:34,  7:33,  8:13,  9:21,  10:29, 11:37,   12:44,   13:51,   14:None},
                          4 :{0:32,   1:31,    2:30,    3:29,    4:28, 5:27, 6:26,  7:25,  8:12,  9:20,  10:28, 11:36,   12:43,   13:50,   14:56},
                          5 :{0:24,   1:23,    2:22,    3:21,    4:20, 5:19, 6:18,  7:17,  8:11,  9:19,  10:27, 11:35,   12:42,   13:49,   14:55},
                          6 :{0:16,   1:15,    2:14,    3:13,    4:12, 5:11, 6:10,  7:9,   8:10,  9:18,  10:26, 11:34,   12:41,   13:48,   14:54},
                          7 :{0:8,    1:7,     2:6,     3:5,     4:4,  5:3,  6:2,   7:1,   8:2,   9:3,   10:4,  11:5,    12:6,    13:7,    14:8},
                          8 :{0:54,   1:48,    2:41,    3:34,    4:26, 5:18, 6:10,  7:9,   8:10,  9:11,  10:12, 11:13,   12:14,   13:15,   14:16},                                                           
                          9 :{0:55,   1:49,    2:42,    3:35,    4:27, 5:19, 6:11,  7:17,  8:18,  9:19,  10:20, 11:21,   12:22,   13:23,   14:24},
                          10:{0:56,   1:50,    2:43,    3:36,    4:28, 5:20, 6:12,  7:25,  8:26,  9:27,  10:28, 11:29,   12:30,   13:31,   14:32},
                          11:{0:None, 1:51,    2:44,    3:37,    4:29, 5:21, 6:13,  7:33,  8:34,  9:35,  10:36, 11:37,   12:38,   13:39,  14:None},
                          12:{0:None, 1:52,    2:45,    3:38,    4:30, 5:22, 6:14,  7:40,  8:41,  9:42,  10:43, 11:44,   12:45,   13:46,  14:None},
                          13:{0:None, 1:None,  2:46,    3:39,    4:31, 5:23, 6:15,  7:47,  8:48,  9:49,  10:50, 11:51,   12:52,   13:None, 14:None},
                          14:{0:None, 1:None,  2:None,  3:None,  4:32, 5:24, 6:16,  7:53,  8:54,  9:55,  10:56, 11:None, 12:None, 13:None, 14:None}} 

            self.array_assembly_map_15_15 = numpy.zeros([15,15])
            for i in range(15):
                for j in range(15):
                    if not array_dict[i][j]:
                        pass
                    else:
                        self.array_assembly_map_15_15[i][j] = array_dict[i][j]

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
            errmessage = f"The number of assembly rows {rows} and columns {cols} is unrecognized"
            return ValueError(errmessage)
        
        for i in range(state_count):
            power_dict[f"STATE_{(i+1):04d}"] = numpy.zeros([number_pins,number_pins,axial,number_assemblies])

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

class Calculator(object):
    """
    General class for performing different calculations.
    """
    @staticmethod
    def convert_tons_to_kg(number):
        """
        Multiplies the provided number by 2000 to convert from metric tons
        to kilograms.
        """
        return number*1000.

    @staticmethod
    def convert_hours_to_seconds(number):
        """
        Converts the provided rate from something/hour to something/second.
        """
        return number/3600.

    @staticmethod
    def interpolate_powers_between_meshes(simulate_mesh,VERA_mesh,simulate_powers):
        rows,columns,meshes,assemblies = simulate_powers.shape
        number_new_meshes = len(VERA_mesh) - 1
        VERA_powers = numpy.zeros([rows,columns,number_new_meshes,assemblies]) 
        simulate_midpoints = []
        VERA_midpoints = []
        for i,value in enumerate(simulate_mesh[:-1]):
            simulate_midpoints.append((value + simulate_mesh[i+1])/2.)
        for i,value in enumerate(VERA_mesh[:-1]):
            VERA_midpoints.append((value + VERA_mesh[i+1])/2.)
        print(f"VERA Midpoints {VERA_midpoints}")
        for i,mid in enumerate(VERA_midpoints):
            if mid < simulate_midpoints[0]:
                slope = numpy.divide(simulate_powers[:,:,0,:]-simulate_powers[:,:,1,:],simulate_midpoints[0]-simulate_midpoints[1])
                intercept = simulate_powers[:,:,1,:] - slope*simulate_midpoints[1]
                VERA_powers[:,:,i,:] = slope*mid + intercept
            elif mid > simulate_midpoints[-1]:
                slope = numpy.divide(simulate_powers[:,:,-1,:]-simulate_powers[:,:,-2,:],simulate_midpoints[-1]-simulate_midpoints[-2])
                intercept = simulate_powers[:,:,-2,:] - slope*simulate_midpoints[-2]
                VERA_powers[:,:,i,:] = slope*mid + intercept
                #temp = mid - simulate_midpoints[-1]
                #temp /= (simulate_mesh[-1]-simulate_midpoints[-1])
                ##VERA_powers[:,:,i,:] = simulate_powers[:,:,-1,:] - simulate_powers[:,:,-1,:]*temp
                #VERA_powers[:,:,i,:] = simulate_powers[:,:,-1,:]*temp
            else:
                for j,value in enumerate(simulate_midpoints):
                    if value < mid and mid < simulate_midpoints[j+1]:
                        temp = mid - value
                        temp /= (simulate_midpoints[j+1]-value)
                        VERA_powers[:,:,i,:] = (simulate_powers[:,:,j+1,:] - simulate_powers[:,:,j,:])*temp
                        VERA_powers[:,:,i,:] += simulate_powers[:,:,j,:]
                        break

        return VERA_powers

def get_cell_column(number):
    """
    For a specified number returns the corresponding alphabetic value, i.e. 26=AA,
    B=1, etc.
    """
    alphabet = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N',
               'O','P','Q','R','S','T','U','V','W','X','Y','Z']
    first_count = 1
    second_count = 0
    third_count = 0
    fourth_count = 0
    fifth_count = 0
    for i in range(number):
        first_count += 1
        if first_count == len(alphabet):
            first_count = 1
            second_count +=1
        if second_count == len(alphabet):
            second_count = 1
            third_count += 1
        if third_count == len(alphabet):
            third_count = 1
            fourth_count += 1
        if fourth_count == len(alphabet):
            fourth_count = 1
            fifth_count += 1

    column = alphabet[fifth_count] + alphabet[fourth_count] + alphabet[third_count]
    column += alphabet[second_count] + alphabet[first_count]

    return column

if __name__ == "__main__":
    input_message = "The simulate file you want to analyze and convert to VERA input."
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",help=input_message,required=True,type=str)

    arg = parser.parse_args()
    h5_converter(arg.file)