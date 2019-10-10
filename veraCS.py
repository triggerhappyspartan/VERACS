import os
import sys
import copy
import yaml
import numpy
import random
import h5py

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
    print(self.stateList)
    file_ = open(self.title+".inp",'w')
    file_.write("[CASEID] \n")
    file_.write('  title {}\n'.format(self.caseID))
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
      print(i,height,layer)
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
              position = elems.index['power']
              current_state.power = float(elems[position+2])
            else:
              current_state.power = base_state.power
            if 'flow' in line:
              position = elems.index['flow']
              current_state.flow = float(elems[position+2])
            else:
              current_state.flow = base_state.flow
            if 'tinlet' in line:
              position = elems.index['tinlet']
              current_state.tinlet = float(elems[position+2])
            else:
              current_state.tinlet = base_state.tinlet
            if 'pressure' in line:
              position = elems.index['pressure']
              current_state.pressure = float(elems[position+2])
            else:
              current_state.pressure = base_state.pressure
            if 'boron' in line:
              position = elems.index['boron']
              current_state.boron = float(elems[position+2])
            else:
              current_state.boron = base_state.boron
            if 'deplete' in line:
              position = elems.index['boron']
              current_state.boron = float(elems[position+2])
            else:
              current_state.boron = base_state.boron
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
         # fuel_instance.gad_material =
         # fuel_instance.gad_concentration
        elif elems[0] == 'cell':
          self.cells[elems[1]] = {}
          self.cells[elems[1]]['radius'] = []
          slash = elems.index('/')
          self.cells[elems[1]]['radius'].extend[elems[2:slash]]
          self.cells[elems[1]]['material'] = []
          self.cells[elems[1]]['material'].extend[elems[(slash+1):]]
        elif elems[0] == 'lattice':
          current_lattice = elems[1]
          self.lattices[current_lattice] = []
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
            self.end_spacer_grid.mass = float(elems[4])
            loss = elems[6].replace("loss=","")
            self.end_spacer_grid.loss_coefficient = loss
          elif elems[1] == 'MID':
            self.mid_spacer_grid.material = elems[2]
            self.mid_spacer_grid.height = float(elems[3])
            self.mid_spacer_grid.mass = float(elems[4])
            loss = elems[6].replace("loss=","")
            self.mid_spacer_grid.loss_coefficient = loss
        elif elems[0] == 'grid_axial':
          searching_grid_axial = True
          self.spacer_grid_locations['order'] = []
          self.spacer_grid_locations['height'] = []
        elif elems[0] == 'lower_nozzle':
          searching_grid_axial = False
          self.lower_nozzle.material = elems[1]
          self.lower_nozzle.height = float(elems[2])
          self.lower_nozzle.mass = float(elems[3])
        elif elems[0] == 'upper_nozzle':
          self.lower_nozzle.material = elems[1]
          self.lower_nozzle.height = float(elems[2])
          self.lower_nozzle.mass = float(elems[3])
        elif elems[0] == 'axial_edit_bounds':
          searching_axial_edits = True
        elif elems[0] == '[MPACT]':
          searching_mpact = True
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
            self.material[material][elems[0]] = float(elems[1])
        if searching_fuel_lattice:
          if elems[0] == 'lattice':
            pass
          else:
            self.lattices[current_lattice].extend(elems)
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
          self.MPACT[elems[0]] = elems[1]
        if searching_cobra:
          self.COBRA[elems[0]] = elems[1]
        if searching_shift:
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
               criticality=None
              ):

    self.depletion = depletion
    self.power = power
    self.boron = boron
    self.flow = flow
    self.tinlet = inlet
    self.pressure = pressure
    self.criticality = criticality

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
    property_shape = state_[wanted_property].shape
    shape_list = []
    shape_count = 1
    for shape in property_shape:
      shape_list.append(0)
      shape_count *= shape
    
    property_ = []

    while len(property_) < shape_count:
      shape_tuple = tuple(shape_list)
      property_.append(state_[wanted_property][shape_tuple])
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

if __name__ == "__main__":
  pass