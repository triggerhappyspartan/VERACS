import os
import sys
import json
import numpy
import random
import pickle
from multiprocessing import Pool
import keras
from keras import layers
from keras import models
from keras import optimizers
from matplotlib import pyplot 
import h5py 

class Neural_Network(object):
    """
    Class for keras neural network.
    """ 
    def __init__(self, training_data = None,
                validation_data = None,
                training_target = None,
                validation_target = None,
                number_layers = None,
                number_nodes = None,
                learning_rate = None,
                minibatch_size = None,
                training_epochs = None,
                name = None   
                ):

        self.name = name
        self.training_data = training_data
        self.validation_data = validation_data
        self.training_targets = training_target
        self.validation_target = validation_target
        self.nodes_per_layer = number_nodes
        self.number_layers = number_layers
        self.learning_rate = learning_rate
        self.number_training_epochs = training_epochs
        self.minibatch_size = minibatch_size

        self.model = None
        self.mean_training_error      = None
        self.mean_validation_error    = None
        self.deviation_training_error = None
        self.deviation_validation_error = None
        self.max_training_error   = None
        self.max_validation_error = None
        
        def initialize_network(self):
            """
            Initialize the neural network for the model. 
            """
            self.model = models.Sequential()
            for i in range(self.number_layers):
                if(i==0):
                    self.model.add(layers.Dense(self.nodes_per_layer,
                                        activation='relu',
                                        input_shape=(self.training_data.shape[1])))
                else:
                    self.model.add(layers.Dense(self.nodes_per_layer,
                                                activation='relu'))
            self.model.add(layers.Dense(1))
            keras.optimizers.RMSprop(lr=self.learning_rate)
            self.model.compile(optimizer='rmsprop',loss='mse',metrics=['mae'])

    def train_network(self):
        """
        Trains the weights and biases of the neural network.
        """
        self.model.fit(self.training_data,
                        self.training_targets,
                        epochs=self.number_training_epochs,
                        batch_size=self.minibatch_size,verbose=0)

    def evaluate_error(self):
        """
        Evaluates the training and validation error of the model. 
        """
        training_predictions = self.model.predict(self.training_data)
        validation_predictions = self.model.predict(self.validation_data)

        training_error = training_predictions - self.training_targets
        validation_error = validation_predictions - self.validation_target

        self.mean_training_error = numpy.mean(training_error)
        self.mean_validation_error = numpy.mean(validation_error)
        self.deviation_training_error = numpy.std(training_error)
        self.deviation_validation_error = numpy.std(validation_error)
        self.max_training_error = numpy.max(training_error)
        self.min_training_error = numpy.min(validation_error)

def evaluate(network):
    """
    Initializes trains and evaluates the neural network. 
    """
    network.initialize_network()
    network.train_network()
    network.evaluate_error()

    return network

def compile_data_library(library_name,output_property,number_files):
    """
    Read all data from the VERA input and output files and turn them into a neural network
    library that can be easily shared or transfered. 
    """
    main_h5_properties = ('average_flux','b10','b10_depl','bank_labels','bank_pos','boron','bypass','comp_ids','coolden',
                          'exposure','exposure_efpd','exposure_hours','feedback','flow','from_matids','hours','kcrit','keff',
                          'mat_units','modden','op_date','outer_timer','outers','pin_cladtemps','pin_exposures','pin_fueltemps',
                          'pin_moddens','pin_modtemps','pin_powers','power','pressure','reaction_rates','reset_sol','rlx_xesm',
                          'samopt','search','search_bank','tfuel','thexp_tclad','thexp_tfuel','thexp_tmod','time_units','tinlet',
                          'title','to_matids','total_power','trans_amounts','trans_on','void','xenopt')
    ctf_h5_properties = ('channel_liquid_temps','cool_max_liquid_temp','core_avg_linear_heatrate','liquid_density','mixture_massflux',
                         'pin_fueltemps','pin_max_clad_surface_temp','pin_max_clad_temp','pin_max_linear_power','pin_max_temp','pin_powers',
                         'pin_steamrate','pressure','vapor_void')

    library = {}
    usable_file_list = []
    for i in range(number_files):
        file_name = "full_assembly_library/workdir.{}/p6.inp".format(i)
        if os.path.isfile(file_name):
            file_name = "full_assembly_library/workdir.{}/p6.h5".format(i)
            if os.path.isfile(file_name):
                file_name = file_name = "full_assembly_library/workdir.{}/p6.ctf.h5".format(i)
                if os.path.isfile(file_name):
                    file_name = "workdir.{}".format(i)
                    usable_file_list.append(file_name)

    for directory in usable_file_list:
        library[directory] = {}

def main():
    """
    Main function for analyzing the numerous neural networks I plan to investigate.
    """
    neural_network_list = []
    usable_directory_list = []

    for i in range(2000):
        if os.path.exists("workdir.{}/p6.inp".format(i)):
            if os.path.exists("workdir.{}/p6.h5".format(i)):
                usable_directory_list.append("workdir.{}".format(i))

    for directory in usable_directory_list:
        pass







