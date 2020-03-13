import os
import sys
import h5py
import numpy
from matplotlib import pyplot as plt
from modularOptimizationFramework.simulate import VERA_Extractor as VE

def h5_converter(file_name):
    """
    Function for converting simulate output files to an H5 File using the VERA naming conventions.
    """
    file_ = open(file_name,'r')
    file_lines = file_.readlines()
    file_.close()

    pin_power_dictionary = VE.full_core_powers3D(file_lines,17)
    exposure_efpds = VE.efpd_list(file_lines)
    exposures = VE.burnup_list(file_lines)
    boron = VE.boron_list(file_lines)
    pressure = VE.pressure(file_lines)
    flow = VE.relative_flow(file_lines)
    power = VE.relative_power(file_lines)
    core_inlet_temps = VE.inlet_temperatures(file_lines)
    keffs = VE.core_keff_list(file_lines)
    FDH_list = VE.FDH_list(file_lines)
    thermal_powers = VE.thermal_power(file_lines)
    core_flows = VE.core_flow(file_lines)
    Fqs = VE.pin_peaking_list(file_lines)

    file_ = h5py.File(file_name.replace(".out",".h5"),'w')
    key_list = list(pin_power_dictionary.keys())
    for i,key in enumerate(key_list):
        g1 = file_.create_group(key)
        g1.create_dataset("pin_powers",data=pin_power_dictionary[key])
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

if __name__ == "__main__":
    pass    

