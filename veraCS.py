import os
import sys
import copy
import yaml
import numpy
import random
import argparse
import h5py
from simulate_exchanger import Simulate_Extractor as SE
from simulate_exchanger import Calculator as cacl

class VERA_Assembly(object):
  """
  Class for writing VERA CS files.
  """
  def __init__(self):
    self.caseID = None
    self.title = None
    self.stateList = {}
    self.apitch = None
    self.height = None
    self.lower_plate = Plate()
    self.upper_plate = Plate()
    self.end_spacer_grid = Spacer_Grid()
    self.mid_spacer_grid = Spacer_Grid()
    self.power = None
    self.flow_rate = None
    self.fuel = {}
    self.cells = {}
    self.lattices = {}
    self.material = {}
    self.npin = None
    self.ppitch = None
    self.axial_lattice_locations = {}
    self.spacer_grid_locations = {}
    self.lower_nozzle = Nozzle()
    self.upper_nozzle = Nozzle()
    self.axial_mesh = []
    self.MPACT = {}
    self.COBRA = {}
    self.SHIFT = {}
    self.INSILICO = {}

  def write_file(self):
    """
    Writes VERA-CS input files.
    """
    #print(self.stateList)
    file_ = open(self.title+".inp",'w')
    file_.write("[CASEID] \n")
    file_.write(f'  title {self.caseID}\n')
    file_.write("\n")
    file_.write("[STATE]\n")
    file_.write("  power    {}\n".format(self.stateList['base'].power))
    file_.write("  flow     {}\n".format(self.stateList['base'].flow))
    file_.write("  tinlet   {} K\n".format(self.stateList['base'].tinlet))
    file_.write("  pressure {} ! psia\n".format(self.stateList['base'].pressure))
    file_.write("  boron    {} ! ppmB\n".format(self.stateList['base'].boron))
    for stateList in self.stateList:
      if stateList == 'base':
        pass
      else:
        file_.write("[STATE]\n")
        file_.write("  deplete GWDMT {}\n".format(self.stateList[stateList].depletion))
        if self.stateList[stateList].power == self.stateList['base'].power:
          pass
        else:
          file_.write("  power    {}\n".format(self.stateList[stateList].power))
        if self.stateList[stateList].flow == self.stateList['base'].flow:
          pass
        else:
          file_.write("  flow     {}\n".format(self.stateList[stateList].flow))
        if self.stateList[stateList].tinlet == self.stateList['base'].tinlet:
          pass
        else:
          file_.write("  tinlet   {} K\n".format(self.stateList[stateList].tinlet))
        if self.stateList[stateList].pressure == self.stateList['base'].pressure:
          pass
        else:
          file_.write("  pressure {} ! psia\n".format(self.stateList[stateList].pressure))
        if self.stateList[stateList].boron == self.stateList['base'].boron:
          pass
        else:
          file_.write("  boron    {} ! ppmB\n".format(self.stateList[stateList].boron))
    
    file_.write("\n")
    file_.write("  sym      qtr\n")
    file_.write("  feedback on\n")
    file_.write("\n")
    file_.write("[CORE]\n")
    file_.write("  size   1              ! one assembly\n")
    file_.write("  rated  20.67 0.6823   ! MW, Mlbs/hr\n")
    file_.write("  apitch {}\n".format(self.apitch))
    file_.write("  height {}\n".format(self.height))
    file_.write("\n")
    file_.write("  core_shape\n")
    file_.write("    1\n")
    file_.write("\n")
    file_.write("  assm_map\n")
    file_.write("    ASSY\n")
    file_.write("\n")
    file_.write("  lower_plate ss  {} {}\n".format(self.lower_plate.thickness,self.lower_plate.volume_fraction))
    file_.write("  upper_plate ss  {} {}\n".format(self.upper_plate.thickness,self.upper_plate.volume_fraction))
    file_.write("\n")
    file_.write("  bc_rad reflecting\n")
    file_.write("\n")
    file_.write("[ASSEMBLY]\n")
    file_.write('  title "{}" \n'.format(self.title))
    file_.write("  npin {}\n".format(self.npin))
    file_.write("  ppitch {}\n".format(self.ppitch))
    file_.write("\n")
    if not self.material:
      pass
    else:
      for mat in self.material:
        file_.write("  mat  {} {} ".format(mat,self.material[mat]['density']))
        for i,elem in enumerate(self.material[mat]['elements']):
          if i == 0:
            file_.write("{}={}\n".format(elem,self.material[mat]['elements'][elem]))
          else:
            file_.write("             {}={}\n".format(elem,self.material[mat]['elements'][elem]))
        file_.write("\n")
    for fu in self.fuel:
      file_.write("  fuel {}".format(fu))
      file_.write(" {}".format(self.fuel[fu].density))
      file_.write(" {} / ".format(self.fuel[fu].theory_dense))
      file_.write("{} ".format(self.fuel[fu].enrichment))
      if not self.fuel[fu].components:
        pass
      else:
        for comp in self.fuel[fu].components:
          file_.write(" {} ".format(comp))
      if not self.fuel[fu].gad_concentration:
        pass
      else:
        file_.write(" / {}={}".format(self.fuel[fu].gad_material,self.fuel[fu].gad_concentration))

      file_.write("\n")
    file_.write("\n")
    for cell in self.cells:
      file_.write("  cell {}   ".format(cell))
      for radius in self.cells[cell]['radius']:
        file_.write(" {}".format(radius))
      file_.write(" / ")
      for material in self.cells[cell]['material']:
        file_.write("{} ".format(material))
      if 'description' in self.cells[cell]:
        file_.write(" ! {}".format(self.cells[cell]['description']))
      file_.write("\n")
    file_.write("\n")
    for lattice in self.lattices:
      file_.write("  lattice {}\n".format(lattice))
      triangular_string = return_triangular_string(self.lattices[lattice],"       ")
      file_.write(triangular_string)
      file_.write("\n")
    for i,height,layer in zip(range(len(self.axial_lattice_locations['height'])),
                              self.axial_lattice_locations['height'],
                              self.axial_lattice_locations['order']):
      if i==0:
        file_.write("  axial {}   {}\n".format(layer,height))
      else:
        file_.write("        {}   {}\n".format(layer,height))
    file_.write("\n")
    file_.write("  grid END {}".format(self.end_spacer_grid.material))
    file_.write(" {}".format(self.end_spacer_grid.height))
    file_.write(" {}".format(self.end_spacer_grid.mass))
    file_.write(" / loss={}\n".format(self.end_spacer_grid.loss_coefficient))
    file_.write("  grid MID {}".format(self.mid_spacer_grid.material))
    file_.write(" {}".format(self.mid_spacer_grid.height))
    file_.write(" {}".format(self.mid_spacer_grid.mass))
    file_.write(" / loss={}\n".format(self.mid_spacer_grid.loss_coefficient))
    file_.write("\n")
    file_.write("  grid_axial\n")
    for i,j in zip(self.spacer_grid_locations['order'],self.spacer_grid_locations['height']):
      file_.write("      {}  {}\n".format(i,j))
    file_.write("\n")
    file_.write("  lower_nozzle  {}".format(self.lower_nozzle.material))
    file_.write(" {} {}\n".format(self.lower_nozzle.height,self.lower_nozzle.mass))
    file_.write("  upper_nozzle  {}".format(self.upper_nozzle.material))
    file_.write(" {} {}\n".format(self.upper_nozzle.height,self.upper_nozzle.mass))
    file_.write("\n")
    file_.write("[EDITS]\n")
    file_.write("  axial_edit_bounds\n")
    for mesh in self.axial_mesh:
      file_.write("      {}\n".format(mesh))
    file_.write("\n")
    if not self.MPACT:
      pass
    else:
      file_.write("[MPACT]\n")
      for key in self.MPACT:
        file_.write("  {} {}\n".format(key,self.MPACT[key]))
    file_.write("\n")
    if not self.COBRA:
      pass
    else:
      file_.write("[COBRATF]\n")
      for key in self.COBRA:
        file_.write("  {} {}\n".format(key,self.COBRA[key]))
    file_.write("\n")
    if not self.SHIFT:
      pass
    else:
      file_.write("[SHIFT]\n")
      for key in self.SHIFT:
        file_.write("  {} {}\n".format(key,self.SHIFT[key]))
    file_.write("\n")
    file_.close()

  def read_data_from_file(self,file_name):
    """
    Assembly Class Information determined from reading the VERA-CS input file.
    """
    file_ = open(file_name)
    file_lines = file_.readlines()
    file_.close()
  
    state_count = 0
    activate_depletion_state = False
    analyzing_material = False
    searching_fuel_lattice = False
    searching_assy = False
    searching_grid_axial = False
    searching_axial_edits = False
    searching_mpact = False
    searching_cobra = False
    searching_shift = False
    self.title = file_name
    for line in file_lines:
      elems = line.strip().split()
      if not elems:
        pass
      else:
        if elems[0] == 'title':
          self.caseID = line.replace('title',"")
        elif elems[0] == '[STATE]':
          if len(elems) == 1:
            activate_depletion_state = True
            base_state = Depletion_State()
          else:
            state_count += 1
            if activate_depletion_state == True:
              self.stateList['base'] = base_state
              activate_depletion_state = False
            current_state = Depletion_State()
            if 'power' in line:
              position = elems.index('power')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.power = float(foo)
            else:
              current_state.power = base_state.power
            if 'flow' in line:
              position = elems.index('flow')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.flow = float(foo)
            else:
              current_state.flow = base_state.flow
            if 'tinlet' in line:
              position = elems.index('tinlet')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.tinlet = float(foo)
            else:
              current_state.tinlet = base_state.tinlet
            if 'pressure' in line:
              position = elems.index('pressure')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.pressure = float(foo)
            else:
              current_state.pressure = base_state.pressure
            if 'boron' in line:
              position = elems.index('boron')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.boron = float(foo)
            else:
              current_state.boron = base_state.boron
            if 'deplete' in line:
              position = elems.index('deplete')
              foo = elems[position+2].replace(";","").replace(",",".")
              current_state.depletion = float(foo)
            else:
              current_state.depletion = base_state.depletion
            self.stateList[state_count] = current_state
        elif elems[0] == 'rated':
          self.power = float(elems[1])
          self.flow_rate = float(elems[2])
        elif elems[0] == 'apitch':
          self.apitch = float(elems[1])
        elif elems[0] == 'height':
          self.height = float(elems[1])
        elif elems[0] == 'lower_plate':
          self.lower_plate.material = elems[1]
          self.lower_plate.thickness = float(elems[2])
          self.lower_plate.volume_fraction = float(elems[3])
        elif elems[0] == 'upper_plate':
          self.upper_plate.material = elems[1]
          self.upper_plate.thickness = float(elems[2])
          self.upper_plate.volume_fraction = float(elems[3])
        elif elems[0] == 'npin':
          self.npin = int(elems[1])
        elif elems[0] == 'ppitch':
          self.ppitch = float(elems[1])
        elif elems[0] == 'mat':
          analyzing_material = True
          material = elems[1]
          self.material[material] = {}
          self.material[material]['density'] = float(elems[2])
          self.material[material][elems[3]] = float(elems[4])
        elif elems[0] == 'fuel':
          self.fuel[elems[1]] = Fuel()
          self.fuel[elems[1]].density = float(elems[2])
          self.fuel[elems[1]].theory_dense = float(elems[3])
          self.fuel[elems[1]].enrichment = float(elems[5])
          self.fuel[elems[1]].components.append(elems[6])
          analyzing_material = False
         # fuel_instance.gad_material =
         # fuel_instance.gad_concentration
        elif elems[0] == 'cell':
          self.cells[elems[1]] = {}
          self.cells[elems[1]]['radius'] = []
          slash = elems.index('/')
          self.cells[elems[1]]['radius'].extend(elems[2:slash])
          self.cells[elems[1]]['material'] = []
          self.cells[elems[1]]['material'].extend(elems[(slash+1):])
        elif elems[0] == 'lattice':
          current_lattice = elems[1]
         # print(current_lattice)
          self.lattices[current_lattice] = []
          searching_fuel_lattice = True
        elif elems[0] == 'axial':
          searching_fuel_lattice = False
          searching_assy = True
          self.axial_lattice_locations['height'] = []
          self.axial_lattice_locations['order'] = []
          self.axial_lattice_locations['order'].append(elems[1])
          self.axial_lattice_locations['height'].append(elems[2])
        elif elems[0] == 'grid':
          searching_assy = False
          if elems[1] == 'END':
            self.end_spacer_grid.material = elems[2]
            self.end_spacer_grid.height = float(elems[3])
            self.end_spacer_grid.mass   = float(elems[4])
            loss = elems[6].replace("loss=","")
            self.end_spacer_grid.loss_coefficient = loss
          elif elems[1] == 'MID':
            self.mid_spacer_grid.material = elems[2]
            self.mid_spacer_grid.height = float(elems[3])
            self.mid_spacer_grid.mass   = float(elems[4])
            loss = elems[6].replace("loss=","")
            self.mid_spacer_grid.loss_coefficient = loss
        elif elems[0] == 'grid_axial':
          searching_grid_axial = True
          self.spacer_grid_locations['order']  = []
          self.spacer_grid_locations['height'] = []
        elif elems[0] == 'lower_nozzle':
          searching_grid_axial = False
          self.lower_nozzle.material = elems[1]
          self.lower_nozzle.height = float(elems[2])
          self.lower_nozzle.mass = float(elems[3])
        elif elems[0] == 'upper_nozzle':
          self.lower_nozzle.material = elems[1]
          self.lower_nozzle.height = float(elems[2])
          self.lower_nozzle.mass   = float(elems[3])
        elif elems[0] == 'axial_edit_bounds':
          searching_axial_edits = True
        elif elems[0] == '[MPACT]':
          searching_mpact = True
          searching_axial_edits = False
        elif elems[0] == ['[COBRATF]']:
          searching_cobra = True
          searching_mpact = False
        elif elems[0] == '[SHIFT]':
          searching_cobra = False
          searching_shift = True
        if activate_depletion_state:
          if elems[0] == 'power':
            base_state.power = float(elems[1])
          elif elems[0] == 'flow':
            base_state.flow = float(elems[1])
          elif elems[0] == 'tinlet':
            base_state.tinlet = float(elems[1])
          elif elems[0] == 'pressure':
            base_state.pressure = float(elems[1])
          elif elems[0] == 'boron':
            base_state.boron = float(elems[1])
        if analyzing_material:
          if elems[0] == 'mat':
            pass
          else:
       #     print(elems)
            self.material[material][elems[0]] = float(elems[1])
        if searching_fuel_lattice:
          if elems[0] == 'lattice':
            pass
          else:
            self.lattices[current_lattice].extend(elems)
    #        print(self.lattices[current_lattice])
        if searching_assy:
          if elems[0] == 'axial':
            pass
          else:
            self.axial_lattice_locations['order'].append(elems[0])
            self.axial_lattice_locations['height'].append(elems[1])
        if searching_grid_axial:
          if elems[0] == 'grid_axial':
            pass
          else:
            self.spacer_grid_locations['order'].append(elems[0])
            self.spacer_grid_locations['height'].append(float(elems[1]))
        if searching_axial_edits:
          if elems[0] == 'axial_edit_bounds':
            pass
          else:
            self.axial_mesh.append(float(elems[0]))
        if searching_mpact:
          if len(elems) == 1:
            pass
          else:
            self.MPACT[elems[0]] = elems[1]
        if searching_cobra:
          if len(elems) == 1:
            pass
          else:
            self.COBRA[elems[0]] = elems[1]
        if searching_shift:
          if len(elems) == 1:
            pass
          else:
            self.SHIFT[elems[0]] = elems[1]

class Depletion_State(object):
  """
  Class instance fo rhte various parameters involved in a dpletion in VERA-CS.
  """
  def __init__(self,depletion=None,
               power=None,
               boron=None,
               flow=None,
               inlet=None,
               pressure=None,
               rodbank=None,
               restart=False,
               criticality=None
              ):

    self.depletion = depletion
    self.rodbank = rodbank
    self.restart = restart
    self.power = power
    self.boron = boron
    self.flow = flow
    self.tinlet = inlet
    self.tinlet_unit = None
    self.pressure = pressure
    self.criticality = criticality

class Base_Depletion_State(object):
  """
  Base or First Depletion state used to set most of the settings in VERA-CS over the course of the
  depletion.
  """
  def __init__(self):
    self.pressure = None
    self.symmetry = None 
    self.feedback = None
    self.search   = None
    self.power    = None
    self.flow     = None
    self.tinlet   = None
    self.tinlet_unit = None
    self.rodbank_names = []
    self.rodbank_positions = []
    self.thexp = None
    self.thexp_tmod = None
    self.thexp_tclad = None
    self.thexp_tfuel = None
    self.thexp_tmod_unit = None
    self.thexp_tclad_unit = None
    self.thexp_tfuel_unit = None

class Core(object):
    """
    Class for writing full core VERA CS Input Files.
    """
    def __init__(self):
        self.caseID = None
        self.title = None
        self.base_state = Base_Depletion_State()
        self.stateList = {}
        self.apitch = None
        self.height = None
        self.lower_plate = Plate()
        self.upper_plate = Plate()
        self.end_spacer_grid = Spacer_Grid()
        self.mid_spacer_grid = Spacer_Grid()
        self.power = None
        self.flow_rate = None
        self.fuel = {}
        self.cells = {}
        self.lattices = {}
        self.material = {}
        self.npin = None
        self.ppitch = None
        self.axial_lattice_locations = {}
        self.spacer_grid_locations = {}
        self.lower_nozzle = Nozzle()
        self.upper_nozzle = Nozzle()
        self.axial_mesh = []
        self.MPACT = {}
        self.COBRA = {}
        self.SHIFT = {}
        self.INSILICO = {}
        self.insert = None
        self.operating_date = None
        self.size = None
        self.rated_power = None
        self.rated_flow = None
        self.core_shape = None
        self.maps = {}
        self.baffle = None
        self.axial_lattice_dict = {}
        self.vessel_material = None
        self.vessel_size = None
        self.control = None
        self.pinpitch = None
        self.detector = None
        self.run = None
        self.axial_edit_bounds = []
        self.control_rod_bank = None
        self.number_assemblies = None

    def write_file(self):
        """
        Function for writing the VERA-CS input file.
        """
        file_ = open(self.title+".inp",'w')
        file_.write("[CASEID]\n")
        file_.write(f"  title '{self.caseID}'\n\n")
        file_.write("[STATE]\n")
        file_.write(f"  title '{self.title}'\n")
        file_.write(f"  pressure {self.base_state.pressure}\n")
        file_.write(f"  sym      {self.base_state.symmetry}\n")
        if self.base_state.feedback:
          file_.write("  feedback       on\n")
        else:
          file_.write("  feedback       off\n")  
        file_.write("  search   {}\n".format(self.base_state.search))
        file_.write("\n")
        count = 0
        for bank,pos in zip(self.base_state.rodbank_names,self.base_state.rodbank_positions):
          if not count:
            file_.write("  rodbank {} {}\n".format(bank,pos))
          else:
            file_.write("          {} {}\n".format(bank,pos))
          count += 1
        file_.write("\n")
        if self.base_state.thexp:
          file_.write("  thexp       on\n")
        else:
          file_.write("  thexp       off\n")
        if self.base_state.thexp_tmod:
          file_.write("  thexp_tmod  {} {}\n".format(self.base_state.thexp_tmod,
                                                     self.base_state.thexp_tmod_unit))
        if self.base_state.thexp_tclad:
          file_.write("  thexp_tclad {} {}\n".format(self.base_state.thexp_tclad,
                                                     self.base_state.thexp_tclad_unit))
        if self.base_state.thexp_tfuel:
          file_.write("  thexp_tfuel {} {}\n".format(self.base_state.thexp_tfuel,
                                                     self.base_state.thexp_tfuel_unit))
        file_.write("\n")
        file_.write("  power {}  \n tinlet {} {}\n".format(self.base_state.power,self.base_state.tinlet,
                                                                self.base_state.tinlet_unit))
        for state in self.stateList:
            file_.write("[STATE]\n")
            if self.stateList[state].power:
              file_.write("   power {}\n".format(self.stateList[state].power))
            if self.stateList[state].flow:
              file_.write("   flow {}\n".format(self.stateList[state].flow))
            if self.stateList[state].tinlet:
              file_.write("   tinlet {} {}\n".format(self.stateList[state].tinlet,
                                                     self.stateList[state].tinlet_unit))
            if self.stateList[state].rodbank:
              file_.write("   rodbank {} {}\n".format(self.stateList[state].rodbank_name,
                                                      self.stateList[state].rodbank_position))
            if self.stateList[state].boron:
              if self.base_state.search == "boron":
                pass
              else:
                file_.write("   boron {} \n".format(self.stateList[state].boron))
            if self.stateList[state].pressure:
              file_.write("   pressure {}\n".format(self.stateList[state].pressure))
            if self.stateList[state].restart:
              file_.write("   restart_write {} {}".format(self.stateList[state].restart_file,state))
            file_.write(f"   deplete {self.stateList[state].depletion_units} {self.stateList[state].depletion} \n")
        
        file_.write("        op_date {}\n".format(self.operating_date))
        file_.write("\n")
        file_.write("[CORE]\n")
        file_.write("  name   WBN\n")
        file_.write("  unit   1\n")
        file_.write("  size   {}              ! assemblies across core\n".format(self.size))
        file_.write("  apitch {}\n".format(self.apitch))
        file_.write("  rated  {} {}     ! MW, Mlbs/hr\n".format(self.rated_power,self.rated_flow)) 
        file_.write("  height {}\n".format(self.height))
        file_.write("\n")
        file_.write("  xlabel  R P N M L K J H G  F  E  D  C  B  A\n")
        file_.write("  ylabel  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n")
        file_.write("\n")
        file_.write("  core_shape\n")
        file_.write(self.core_shape)
        file_.write("\n")
        for map_ in self.maps:
          file_.write(f"  {map_}\n")
          map_string = return_8th_map_string(self.maps[map_])
          file_.write(map_string) 
          file_.write("\n")
        file_.write("  crd_bank\n")
        file_.write(self.control_rod_bank)
        file_.write("\n")
        file_.write(f"  det_map {self.number_assemblies}*2\n")
        file_.write("\n")
        file_.write(f"  baffle {self.baffle.material} {self.baffle.lower} {self.baffle.upper}\n") 
        file_.write("\n")
        count = 0
        for mat,pos in zip(self.vessel_material,self.vessel_size):
          if not count:
            file_.write(f"  vessel  {mat} {pos}        ! barrel IR (cm)\n")
          else:
            file_.write(f"           {mat} {pos}\n")     
          count += 1   
        file_.write("\n")
        file_.write("  pad ss  194.64 201.63 32 45 135 225 315 \n")
        file_.write("\n")
        file_.write("  lower_plate {}  {} {}   ! mat, thickness, vol frac\n".format(self.lower_plate.material,
                                                                                    self.lower_plate.thickness,
                                                                                    self.lower_plate.volume_fraction))
        file_.write("  upper_plate {}  {} {}   ! mat, thickness, vol frac\n".format(self.upper_plate.material,
                                                                                      self.upper_plate.thickness,
                                                                                      self.upper_plate.volume_fraction))
        file_.write("\n")
        file_.write("\n")
        file_.write("[ASSEMBLY]\n")
        file_.write('  title "Westinghouse 17x17"\n')
        file_.write("  npin   {}\n".format(self.npin))
        file_.write("  ppitch {}\n".format(self.ppitch))
        file_.write("  \n")
        file_.write("\n")
        for fu in self.fuel:
          file_.write("  fuel {}".format(fu))
          file_.write(" {}".format(self.fuel[fu].density))
          file_.write(" {} / ".format(self.fuel[fu].theory_dense))
          file_.write("{} ".format(self.fuel[fu].enrichment))
          if not self.fuel[fu].components:
            pass
          else:
            for comp in self.fuel[fu].components:
              file_.write(" {} ".format(comp))
          if not self.fuel[fu].gad_concentration:
            pass
          else:
            file_.write(" / {}={}".format(self.fuel[fu].gad_material,self.fuel[fu].gad_concentration))
          file_.write("\n")
        for cell in self.cells:
          file_.write("  cell {}   ".format(cell))
          for radius in self.cells[cell]['radius']:
            file_.write(" {}".format(radius))
          file_.write(" / ")
          for material in self.cells[cell]['material']:
            file_.write("{} ".format(material))
          if 'description' in self.cells[cell]:
            file_.write(" ! {}".format(self.cells[cell]['description']))
          file_.write("\n")
        file_.write("\n")
        for lattice in self.lattices:
          file_.write("  lattice {}\n".format(lattice))
          triangular_string = return_triangular_string(self.lattices[lattice],"       ")
          file_.write(triangular_string)
          file_.write("\n")
        for ax in self.axial_lattice_dict:
          str_ = "  axial  {}".format(ax)
          for pos,lat in zip(self.axial_lattice_dict[ax].height[:-1],self.axial_lattice_dict[ax].lattice):
            str_ += "  {}  {}".format(pos,lat)
          str_ += "  {}\n".format(self.axial_lattice_dict[ax].height[-1])
          file_.write(str_)
        file_.write("\n")
        file_.write("  grid END {}    {} {}\n".format(self.end_spacer_grid.material,
                                                      self.end_spacer_grid.height,
                                                      self.end_spacer_grid.mass))
        file_.write("  grid MID {}  {} {}\n".format(self.mid_spacer_grid.material,
                                                    self.mid_spacer_grid.height,
                                                    self.mid_spacer_grid.mass)) 
        file_.write("\n")
        file_.write("  grid_axial\n")
        for i,j in zip(self.spacer_grid_locations['order'],self.spacer_grid_locations['height']):
          file_.write("      {}  {}\n".format(i,j))
        file_.write("\n")
        file_.write("  lower_nozzle  {} {} {}  ! mat, height, mass (g)\n".format(self.lower_nozzle.material,
                                                                                 self.lower_nozzle.height,
                                                                                 self.lower_nozzle.mass))
        file_.write("  upper_nozzle  {} {} {}  ! mat, height, mass (g)\n".format(self.upper_nozzle.material,
                                                                                 self.upper_nozzle.height,
                                                                                 self.upper_nozzle.mass))
        file_.write("\n")
        if self.insert:
          file_.write("[INSERT]\n")
          file_.write('  title "{}"\n'.format(self.insert.title))
          file_.write("  npin {}\n".format(self.insert.npin))
          file_.write("\n")
          for cell in self.insert.cells:
            file_.write("  cell {}".format(cell))
            str_ = ""
            for rad in self.insert.cells[cell]['radius']:
              str_ += " {}".format(rad)
            str_ += " /"
            for mad in self.insert.cells[cell]['material']:
              str_ += " {}".format(mad)
            str_ += " ! {}\n".format(self.insert.cells[cell]['description'])
            file_.write(str_)
          file_.write("\n")
          for lattice in self.insert.lattices:
            file_.write("  lattice {}\n".format(lattice))
            triangular_string = return_triangular_string(self.insert.lattices[lattice],"       ")
            file_.write(triangular_string)
            file_.write("\n")
          file_.write("\n")
          for ax in self.insert.axial_lattice_dict:
            str_ = "  axial  {}".format(ax)
            for pos,lat in zip(self.insert.axial_lattice_dict[ax].height[-1],
                               self.insert.axial_lattice_dict[ax].lattice):
              str_ += "  {}  {}".format(pos,lat)
            str_ += "  {}\n".format(self.insert.axial_lattice_dict[ax].height[-1])
            file_.write(str_)
          file_.write("\n")
        if self.control:
          file_.write("[CONTROL]\n")
          file_.write('  title "{}"\n'.format(self.control.title))
          file_.write("  npin    {}\n".format(self.control.npin))
          file_.write("  stroke  {}  {}    ! approx for 1.5875 step sizes and 230 max stroke".format(self.control.stroke_one,
                                                                                                     self.control.stroke_two))
          file_.write("\n")
          for cell in self.control.cells:
            file_.write("  cell {}   ".format(cell))
            for radius in self.control.cells[cell]['radius']:
              file_.write(" {}".format(radius))
            file_.write(" / ")
            for material in self.control.cells[cell]['material']:
              file_.write("{} ".format(material))
            if 'description' in self.cells[cell]:
              file_.write(" ! {}".format(self.cells[cell]['description']))
            file_.write("\n")
          file_.write("\n")
          for lattice in self.control.lattices:
            file_.write("  lattice {}\n".format(lattice))
            triangular_string = return_triangular_string(self.control.lattices[lattice],"       ")
            file_.write(triangular_string)
            file_.write("\n")
          file_.write("\n")
          for ax in self.control.axial_lattice_dict:
            str_ = "  axial  {}".format(ax)
            for pos,lat in zip(self.control.axial_lattice_dict[ax].height[-1],
                               self.control.axial_lattice_dict[ax].lattice):
              str_ += "  {}  {}".format(pos,lat)
            str_ += "  {}\n".format(self.control.axial_lattice_dict[ax].height[-1])
            file_.write(str_)
          file_.write("\n")
          file_.write("\n")
        if self.detector:
          file_.write("[DETECTOR]\n")
          file_.write('  title "{}"\n'.format(self.detector.title))
          file_.write("  npin {}\n".format(self.detector.npin))
          file_.write("\n")
          file_.write("\n")
          for cell in self.detector.cells:
            file_.write("  cell {}   ".format(cell))
            for radius in self.detector.cells[cell]['radius']:
              file_.write(" {}".format(radius))
            file_.write(" / ")
            for material in self.detector.cells[cell]['material']:
              file_.write("{} ".format(material))
            if 'description' in self.detector.cells[cell]:
              file_.write(" ! {}".format(self.detector.cells[cell]['description']))
            file_.write("\n")
          file_.write("\n")
          for lattice in self.detector.lattices:
            file_.write("  lattice {}\n".format(lattice))
            triangular_string = return_triangular_string(self.insert.lattices[lattice],"       ")
            file_.write(triangular_string)
            file_.write("\n")
          file_.write("\n")
          for ax in self.detector.axial_lattice_dict:
            str_ = "  axial  {}".format(ax)
            for pos,lat in zip(self.detector.axial_lattice_dict[ax].height[-1],
                               self.detector.axial_lattice_dict[ax].lattice):
              str_ += "  {}  {}".format(pos,lat)
            str_ += "  {}\n".format(self.detector.axial_lattice_dict[ax].height[-1])
            file_.write(str_)
          file_.write("\n")
          file_.write("\n")
        file_.write("[EDITS]\n")
        file_.write("  axial_edit_bounds   ! problem 10 mesh for 4.0_RC7\n")
        for axial in self.axial_edit_bounds:
          file_.write("       {}\n".format(axial))
        file_.write("\n")
        file_.write("\n")
        if not self.MPACT:
          pass
        else:
          file_.write("[MPACT]\n")
          print(self.MPACT)
          print(type(self.MPACT))
          print(self.MPACT.keys())
          for key in self.MPACT:
            print(key)
            print(self.MPACT[key])
            file_.write(f"  {key} {self.MPACT[key]}\n")
        file_.write("\n")
        if not self.COBRA:
          pass
        else:
          file_.write("[COBRATF]\n")
          for key in self.COBRA:
            file_.write("  {} {}\n".format(key,self.COBRA[key]))
        file_.write("\n")
        if not self.SHIFT:
          pass
        else:
          file_.write("[SHIFT]\n")
          for key in self.SHIFT:
            file_.write("  {} {}\n".format(key,self.SHIFT[key]))
        file_.write("\n")
        if self.run:
          for key in self.run:
              file_.write("  {} {}\n".format(key,self.run[key]))
        file_.write("\n")
        file_.close()

    def build_case(self,file_):
      """
      Assigns all variables to a VERA class object based off of a provided yaml file.
      All values can come from the supplied yaml file, or simulate output files and HDF5 files may be 
      provided as well.
      """
      with open(file_) as yaml_file:
        dict_ = yaml.safe_load(yaml_file)

      if 'simulate_file' in dict_:
        self._assign_from_simulate_output(dict_['simulate_file'])
      if 'h5_file' in dict_:
        self._assign_from_h5(dict_['h5_file'])
      
      self.assign_from_dictionary(dict_)

    def assign_from_dictionary(self,dict_):
      """
      assigns class variables based off of a supplied dictionary.
      """
      if 'caseID' in dict_:
        self.caseID = dict_['caseID']
      if 'title' in dict_:
        self.title = dict_['title']
      if 'state' in dict_:
        for i, state in enumerate(dict_['state']):
          if not i:
            if not self.base_state.pressure: 
              self.base_state.pressure = dict_['state'][state]['pressure']
            if not self.base_state.power:
              self.base_state.power = dict_['state'][state]['power']
            if not self.base_state.flow:
              self.base_state.flow = dict_['state'][state]['flow']
            if not self.base_state.tinlet:
              if 'value' in dict_['state'][state]['tinlet']:
                self.base_state.tinlet = dict_['state'][state]['tinlet']['value']
            if not self.base_state.tinlet_unit:
              if 'unit' in dict_['state'][state]['tinlet']:
                self.base_state.tinlet_unit = dict_['state'][state]['tinlet']['unit']
            if not self.base_state.rodbank_names:
              self.base_state.rodbank_names = dict_['state'][state]['rodbank']['names']
            if not self.base_state.rodbank_positions:
              self.base_state.rodbank_positions = dict_['state'][state]['rodbank']['positions']
          else:
            if state in self.stateList:
              stator = self.stateList[state]
              if "tinlet" in dict_['state'][state]:
                if "value" in dict_['state'][state]['tinlet']:
                  stator.tinlet = dict_['state'][state]['tinlet']['value']
                if "unit" in dict_['state'][state]['tinlet']:
                  stator.tinlet_unit = dict_['state'][state]['tinlet']['unit']
              if "depletion" in dict_['state'][state]:
                if "value" in dict_['state'][state]['depletion']:
                  stator.depletion = dict_['state'][state]['depletion']['value']
                if "unit" in dict_['state'][state]['depletion']:
                  stator.depletion_units = dict_['state'][state]['depletion']['unit']
            else:
              stator = Depletion_State()
              stator.pressure = dict_['state'][state]['pressure']
              stator.power = dict_['state'][state]['power']
              stator.flow = dict_['state'][state]['flow']
              stator.tinlet = dict_['state'][state]['tinlet']
              stator.rodbank_names = dict_['state'][state]['rodbank']['names']
              stator.rodbank_positions = dict_['state'][state]['pressure']['positions']
              stator.depletion = dict_['state'][state]['depletion']['value']
              stator.depletion_units = dict_['state'][state]['depletion']['unit']
              stator.restart = dict_['state'][state]['restart']
              self.stateList[state] = stator
      if 'core_shape' in dict_:
        self.core_shape = dict_['core_shape']    
      if 'MPACT' in dict_:
        self.MPACT = dict_['MPACT']
      if 'RUN' in dict_:
        self.RUN = dict_['RUN']
      if 'maps' in dict_:
        self.maps = dict_['maps']
      if 'feedback' in dict_:
        self.base_state.feedback = dict_['feedback']
      if 'search' in dict_:
        self.base_state.search = dict_['search']
      if 'baffle' in dict_:
        self.baffle = Baffle()
        self.baffle.material = dict_['baffle']['material']
        self.baffle.lower = dict_['baffle']['lower']
        self.baffle.upper = dict_['baffle']['upper']
      if 'vessel' in dict_:
        self.vessel_material = dict_['vessel']['materials']
        self.vessel_size = dict_['vessel']['sizes']
      if 'plates' in dict_:
        self.lower_plate.material = dict_['plates']['lower']['material']
        self.lower_plate.thickness = dict_['plates']['lower']['thickness']
        self.lower_plate.volume_fraction = dict_['plates']['lower']['volume_fraction']
        self.upper_plate.material = dict_['plates']['upper']['material']
        self.upper_plate.thickness = dict_['plates']['upper']['thickness']
        self.upper_plate.volume_fraction = dict_['plates']['upper']['volume_fraction']
      if 'fuel' in dict_:
        for fu in dict_['fuel']:
          fuel_class = Fuel()
          fuel_class.name = fu
          fuel_class.designation = fu
          if 'density' in dict_['fuel'][fu]:
            fuel_class.density = dict_['fuel'][fu]['density']
          if 'theoretical_density' in dict_['fuel'][fu]:
            fuel_class.theory_dense = dict_['fuel'][fu]['theoretical_density']
          if 'enrichment' in dict_['fuel'][fu]:
            fuel_class.enrichment = dict_['fuel'][fu]['enrichment']
          if 'components' in dict_['fuel'][fu]:
            fuel_class.components = dict_['fuel'][fu]['components']
          if 'gad_material' in dict_['fuel'][fu]:
            fuel_class.gad_material = dict_['fuel'][fu]['gad_material']
          if 'gad_concentration' in dict_['fuel'][fu]:
            fuel_class.gad_concentration = dict_['fuel'][fu]['gad_concentration']
          self.fuel[fu] = fuel_class
          print(self.fuel[fu].enrichment)
      if 'cells' in dict_:
        self.cells = dict_['cells']
      if "nozzle" in dict_:
        if "lower" in dict_['nozzle']:
          self.lower_nozzle.material = dict_['nozzle']['lower']['material']
          self.lower_nozzle.height = dict_['nozzle']['lower']['height']
          self.lower_nozzle.mass   = dict_['nozzle']['lower']['mass']
        if "lower" in dict_['nozzle']:
          self.upper_nozzle.material = dict_['nozzle']['upper']['material']
          self.upper_nozzle.height =   dict_['nozzle']['upper']['height']
          self.upper_nozzle.mass   =   dict_['nozzle']['upper']['mass']
      if 'spacer_grid' in dict_:
        if "end" in dict_['spacer_grid']:
          self.end_spacer_grid.key = "END"
          self.end_spacer_grid.material = dict_['spacer_grid']['end']['material']
          self.end_spacer_grid.height = dict_['spacer_grid']['end']['height']
          self.end_spacer_grid.mass = dict_['spacer_grid']['end']['mass']
          self.end_spacer_grid.loss_coefficient = dict_['spacer_grid']['end']['loss_coefficient']
        if "mid" in dict_['spacer_grid']:
          self.mid_spacer_grid.key = "MID"
          self.mid_spacer_grid.material = dict_['spacer_grid']['mid']['material']
          self.mid_spacer_grid.height = dict_['spacer_grid']['mid']['height']
          self.mid_spacer_grid.mass = dict_['spacer_grid']['mid']['mass']
          self.mid_spacer_grid.loss_coefficient = dict_['spacer_grid']['mid']['loss_coefficient']
      if 'assembly_pitch' in dict_:
        self.assembly_pitch = dict_['assembly_pitch']
      if 'pin_pitch' in dict_:
        self.ppitch = dict_['pin_pitch']
      if 'npin' in dict_:
        self.npin = dict_['npin']
      if "search" in dict_:
        self.base_state.search = dict_['search']
      if 'symmetry' in dict_:
        self.base_state.symmetry = dict_['symmetry']
      if 'lattices' in dict_:
        self.lattices = dict_['lattices']
      if "axial_lattices" in dict_:
        for axial in dict_['axial_lattices']:
          ax_class = Axial_Grid()
          ax_class.height = dict_['axial_lattices'][axial]['height']
          ax_class.lattice = dict_['axial_lattices'][axial]['lattice']
          self.axial_lattice_dict[axial] = ax_class
      if 'spacer_grid_locations' in dict_:
        self.spacer_grid_locations = dict_['spacer_grid_locations']
      if 'axial_edit_bounds' in dict_:
        self.axial_edit_bounds = dict_['axial_edit_bounds']
      if 'height' in dict_:
        self.height = dict_['height']

    def _assign_from_simulate_output(self,file_name):
      """
      Assigns values to the VERA class instance based on data read from the
      provided simulate output file. 
      """
      file_ = open(file_name,'r')
      file_lines = file_.readlines()
      file_.close()

      exposure_efpds = SE.efpd_list(file_lines)
      expusures = SE.burnup_list(file_lines)
      boron = SE.boron_list(file_lines)
      pressure = SE.pressure(file_lines)
      flow = SE.relative_flow(file_lines)
      power = SE.relative_power(file_lines)
      core_inlet_temps = SE.inlet_temperatures(file_lines)
      apitch = SE.assembly_pitch(file_lines)
      rows,columns = SE.core_size(file_lines)
      rated_powers = SE.thermal_power(file_lines)
      rated_flow = SE.core_flow(file_lines)
      self.number_assemblies = SE.count_number_assemblies(file_lines)

      number_states = len(exposure_efpds)
      print(f"Length core relative power {len(power)}")
      print(power)
      print(f"Length exposure EFPD {len(exposure_efpds)}")
      print(exposure_efpds)
      for i in range(number_states):
        if not i:
          self.base_state.power = power[i]
          self.base_state.pressure = pressure[i]
          self.base_state.flow = flow[i]
          self.base_state.tinlet = core_inlet_temps[i]
        else:
          state_ = Depletion_State(depletion=exposure_efpds[i],
                                   power=power[i],
                                   boron=boron[i],
                                   pressure=pressure[i],
                                   flow=flow[i],
                                   inlet=core_inlet_temps[i])
          self.stateList[expusures[i]] = state_
      self.apitch = apitch
      self.size = rows
      self.rated_power = rated_powers[0]
      self.rated_flow = rated_flow[0]

      if self.number_assemblies == 157:
        self.core_shape  = "    0 0 0 0 0 0 1 1 1 0 0 0 0 0 0\n"
        self.core_shape += "    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n"                 
        self.core_shape += "    0 0 0 1 1 1 1 1 1 1 1 1 0 0 0\n"
        self.core_shape += "    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n"
        self.core_shape += "    0 0 0 1 1 1 1 1 1 1 1 1 0 0 0\n"
        self.core_shape += "    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n"
        self.core_shape += "    0 0 0 0 0 0 1 1 1 0 0 0 0 0 0\n"
        self.control_rod_bank  ="    D  -  A  -  D  -  C  -\n"
        self.control_rod_bank +="    -  -  -  -  - SB  -  -\n"
        self.control_rod_bank +="    A  -  C  -  -  -  B\n"
        self.control_rod_bank +="    -  -  -  A  - SC  -\n"
        self.control_rod_bank +="    D  -  -  -  D  - \n"
        self.control_rod_bank +="    - SB  - SD  - \n"
        self.control_rod_bank +="    C  -  B  -  \n"
        self.control_rod_bank +="    -  -\n"
      elif self.number_assemblies == 193:
        self.core_shape  = "    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n"
        self.core_shape += "    0 0 0 1 1 1 1 1 1 1 1 1 0 0 0\n"                 
        self.core_shape += "    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        self.core_shape += "    0 1 1 1 1 1 1 1 1 1 1 1 1 1 0\n"
        self.core_shape += "    0 0 1 1 1 1 1 1 1 1 1 1 1 0 0\n"
        self.core_shape += "    0 0 0 1 1 1 1 1 1 1 1 1 0 0 0\n"
        self.core_shape += "    0 0 0 0 1 1 1 1 1 1 1 0 0 0 0\n"
        self.control_rod_bank  ="    D  -  A  -  D  -  C  -\n"
        self.control_rod_bank +="    -  -  -  -  - SB  -  -\n"
        self.control_rod_bank +="    A  -  C  -  -  -  B  -\n"
        self.control_rod_bank +="    -  -  -  A  - SC  -  -\n"
        self.control_rod_bank +="    D  -  -  -  D  - SA \n"
        self.control_rod_bank +="    - SB  - SD  -  -  - \n"
        self.control_rod_bank +="    C  -  B  - SA  - \n"
        self.control_rod_bank +="    -  -  -  -\n"

    def _assign_from_h5(self,file_name):
      """
      Assigns values to the VERA object from an H5 file.
      """
      file_ = h5py.File(file_name,'r')
      key_list = file_.keys()
      for key in key_list:
        if key == 'CORE':
          self.assembly_pitch = file_['CORE']['apitch']
          self.rated_flow = file_['CORE']['rated_flow']
          if file_['CORE']['rated_flow_units'] == 'Kg/s':
            pass
          self.rated_power = file_['CORE']['rated_power']
        elif key == 'STATE_0001':
          state_.pressure = file_['STATE_0001']['pressure']
          state_.depletion = file_['STATE_0001']['exposure_efpds']
          state_.boron = file_['STATE_0001']['exposure_efpds']
          state_.flow = file_['STATE_0001']['flow']
          state_.tinlet = file_['STATE_0001']['core_inlet_temp']
          state_.power = file_['STATE_0001']['power']
        else:
          state_ = Depletion_State()
          state_.pressure = file_['STATE_0001']['pressure']
          state_.depletion = file_['STATE_0001']['exposure_efpds']
          state_.boron = file_['STATE_0001']['exposure_efpds']
          state_.flow = file_['STATE_0001']['flow']
          state_.tinlet = file_['STATE_0001']['core_inlet_temp']
          state_.power = file_['STATE_0001']['power']
          exposure = file_['STATE_0001']['exposure']
          self.stateList[exposure] = state_ 

class Repeating_Section(object):
  """
  Class for sections in VERA-CS files that have a large degree of repeating information.
  """
  def __init__(self):
    self.title = None
    self.npin = None
    self.stroke = None
    self.cells = {}
    self.lattices = {}
    self.axial_lattice_dict = None

class Plate(object):
    """
    Class for plates in a VERA-CS assembly.
    """
    def __init__(self):
      self.material = None
      self.thickness = None
      self.volume_fraction = None
      
class Fuel(object):
  """
  Class for designating fuel types. Right now for VERA-CS. 
  I would like to expand to Casmo-CS as well.
  """
  def __init__(self):
    self.name = None
    self.designation = None
    self.density = None
    self.theory_dense = None
    self.enrichment   = None
    self.components = []
    self.gad_material = None
    self.gad_concentration = None

class Nozzle(object):
  """
  Class for designating the nozzles within a VERA-CS Assembly
  """
  def __init__(self):
    self.material = None
    self.height = None
    self.mass = None

class Spacer_Grid(object):
  """
  Class for the spacer grids in a VERA CS assembly.
  """
  def __init__(self,key=None,
                    material=None,
                    height=None,
                    mass=None,
                    loss_coefficient=None):
    self.key = key
    self.material = material
    self.height = height
    self.mass = mass
    self.loss_coefficient = loss_coefficient

class Baffle(object):
  """
  Class for the baffle.
  """
  def __init__(self):
    self.material = None
    self.lower = None
    self.upper = None

class Library_Generator(object):
  """
  Generate a library of random VERA-CS cases based on provided settings.
  """
  def __init__(self, constant, randomness):
    self.altered_stuff = randomness
    self.constant_stuff = constant

class Axial_Grid(object):
  """
  Class for organizing the axial arrangements of lattices.
  """
  def __init__(self):
    height = None
    lattice = None

def return_triangular_string(list_,whitespace):
    """
    Returns the genome as a single triangular string
    Used for octant symmetry in PWR fuel lattices and diagonal symmetry
    in BWR fuel lattices.
    """
    triangular_string = whitespace
    column = 0
    row    = 1
    for item in list_:
        if type(item) is str:
            entry = item
        elif type(item) == list:
            print_line = "Function return_triangular_string does not accept lists as an indice in the triangle"
            raise TypeError(print_line)
        elif type(item) == set:
            print_line = "Function return_triangular_string does not accept sets as an indice in the triangle"
            raise TypeError(print_line)
        elif type(item) == dict:
            print_line = "Function return_triangular_string does not accept dictionaries as an indice in the triangle"
            raise TypeError(print_line)
        else:
            entry = str(item)
        triangular_string += entry.ljust(3)
        column +=1
        if row == column:
            triangular_string += "\n"+whitespace
            column = 0
            row +=1

    return triangular_string

def return_h5_property_as_list(file_name,state,wanted_property):
    """
    Reads data from the HDF5 File and returns it as a single list.

    Usually, VERA-CS organizes assembly pin data as row,column,height,state.
    Data value list will be returned increasing from right to left. 
    or [0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0] ...
    """
    file_ = h5py.File(file_name,'r')
    state_ = file_[state]
    print(state_)
    property_shape = state_[wanted_property].shape
    shape_list = []
    shape_count = 1
    for shape in property_shape:
      shape_list.append(0)
      shape_count *= shape
    
    property_ = [0] * shape_count

    for i in range(shape_count):
      shape_tuple = tuple(shape_list)
      property_[i] = state_[wanted_property][shape_tuple]
      iterating_shape = True
      last_val = len(property_shape) - 1
      shape_list[last_val] += 1
      while iterating_shape:
        if shape_list[last_val] >= property_shape[last_val]:
          if not last_val:
            shape_list[0] = 0
          else:
            shape_list[last_val] = 0
            last_val -= 1
            shape_list[last_val] += 1
        else:
          iterating_shape = False

    file_.close()
    return property_

def return_state_list(file_name):
  """
  Returns a list of states in the HDF5 Output File.
  """
  file_ = h5py.File(file_name,'r')
  key_list = list(file_.keys())
  file_.close()

  state_list = []
  for key in key_list:
    if 'STATE_' in key:
      state_list.append(key)

  return state_list

def return_8th_map_string(list_):
  """
  Returns a map using 8th core symmetry for a 15 x 15 core map.
  """
  if len(list_) == 31:
    str_ =  f"    {list_[0]}\n"
    str_ += f"    {list_[1]} {list_[2]}\n"
    str_ += f"    {list_[3]} {list_[4]} {list_[5]}\n"
    str_ += f"    {list_[6]} {list_[7]} {list_[8]} {list_[9]}\n"
    str_ += f"    {list_[10]} {list_[11]} {list_[12]} {list_[13]} {list_[14]}\n"
    str_ += f"    {list_[15]} {list_[16]} {list_[17]} {list_[18]} {list_[19]} {list_[20]}\n"
    str_ += f"    {list_[21]} {list_[22]} {list_[23]} {list_[24]} {list_[25]} {list_[26]}\n" 
    str_ += f"    {list_[27]} {list_[28]} {list_[29]} {list_[30]} \n"
    return str_
  elif len(list_) == 26:
    str_ =  f"    {list_[0]}\n"
    str_ += f"    {list_[1]} {list_[2]}\n"
    str_ += f"    {list_[3]} {list_[4]} {list_[5]}\n"
    str_ += f"    {list_[6]} {list_[7]} {list_[8]} {list_[9]}\n"
    str_ += f"    {list_[10]} {list_[11]} {list_[12]} {list_[13]} {list_[14]}\n"
    str_ += f"    {list_[15]} {list_[16]} {list_[17]} {list_[18]} {list_[19]} \n"
    str_ += f"    {list_[20]} {list_[21]} {list_[22]} {list_[23]} \n" 
    str_ += f"    {list_[24]} {list_[25]} \n"
    return str_

  else:
    error_ = "Map list is of length {} instead of length 31".format(len(list_))
    return ValueError(error_)

if __name__ == "__main__":
  #message1 = "The input yaml file containing the settings for the VERA-CS run."
  #message2 = "If random sampling is to occur for creating a VERA-CS data library, this yaml file structures how the random sampling is done."
#
  #parser = argparse.ArgumentParser()
  #parser.add_argument(input="--settings",required=True,help=message1)
  #parser.add_argument(input="--random",required=False,help=message2)
#
  #args = parser.parse_args()
#
  #if args.random:
  #  generator = Library_Generator(args.settings,args.random)
  #  generator.create()
  #else:
  #  pass


  foo = Core()
  foo.build_case("test.yaml")
  foo.write_file()
