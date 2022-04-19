#!/bin/env python

import nest
import nest.topology as tp
nest.Install('mymodule')

import numpy as np
import time
from glob import glob

from nest_values import *
from funciones   import *

files = glob('spike_detector-*')
for file in files:
    os.remove(file)

images_to_simulate = [input_images_path + image for image in images_selected ]  
num_images_to_simulate = len(images_to_simulate)

########################################################### Nest ###################################################################

nest.ResetKernel()
nest.SetKernelStatus({'local_num_threads':local_num_threads})
nest.SetKernelStatus({'print_time':True})
nest.SetKernelStatus({'overwrite_files':True})
nest.SetKernelStatus({"resolution": resolution})

nest.CopyModel("izhikevich","exc", RS_dict)
nest.CopyModel("izhikevich","inh", FS_dict) 

msd = int(sys.argv[1])


N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
pyrngs = [np.random.RandomState(s) for s in range(msd, msd+N_vp)]
nest.SetKernelStatus({'grng_seed' : msd+N_vp})
nest.SetKernelStatus({'rng_seeds' : range(msd+N_vp+1, msd+2*N_vp+1)})

with open('seed.txt', 'w') as f:
    f.write(str(msd))

    
########################################################### Image processing ####################################################################

create_folder(gabor_folder); remove_contents(gabor_folder)
create_folder(sd_path); remove_contents(sd_path)
create_folder(df_folder); remove_contents(df_folder)
create_folder(positions_path); remove_contents(positions_path)
create_folder(df_folder + '/' + str(msd))

t = time.time()
gabors_to_nest = full_img_filtering(images_to_simulate,num_orientations)
gabors_time = time.time() - t


save_gabors(gabors_to_nest, images_to_simulate,num_orientations);   
if get_output_gabors:
    quit()


############################################################  Connectivity ######################################################################

t = time.time()
layers, poiss_layers = main_all_orientations(num_orientations)
conn_time = time.time() - t
print("All layers succesfully connected!")

#############################################################

layers_to_record = {}
spike_detectors = {}
for i in layers:
    layers_to_record.update(dict(list(layers[i].items())[:2]))
    spike_detectors.update(dict(list(layers[i].items())[2:]))

#save_dict(layers_to_record,'to_record_layer')
#save_dict(spike_detectors,'to_record_sd')

##################################################### Positions ###############################

for layer,j in zip(layers_to_record,range(0,len(layers_to_record))):
    tp.DumpLayerNodes(layers_to_record[layer],positions_path + '/positions-'+str(layer))

positions = get_positions()

#positions.to_csv('positions_df.txt', index = False, sep = ' ')

############################################################## Simulation #######################################################################

t = time.time()

null_images_dict = {}
for i in range(num_orientations):
    null_images_dict['orientation_' + str(i*180/num_orientations)] = [0.0] * cortex_size

for i in range(num_images_to_simulate):
    set_poisson_values(gabors_to_nest['image_' + str(i)], poiss_layers, num_orientations)
    nest.Simulate(ms_per_stimuli)
    set_poisson_values(null_images_dict, poiss_layers, num_orientations)
    nest.Simulate(ms_rest)

sim_time = time.time() - t

######################################################### Data Treatment #################################################################

data_to_df(images_selected, positions, spike_detectors, layers_to_record, msd)

files = glob('spike_detector-*')
for file in files:
    os.remove(file)
    
print("Times: \n\n     Building architecture: " + str(np.around(conn_time/60,2)) +"m")
print("\n     Image processing: " + str(np.around(gabors_time,2)) +"s")
print("\n     Simulation: " + str(np.around(sim_time/60,2))+"m")
print("\n")


