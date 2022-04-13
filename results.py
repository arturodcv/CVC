#!/usr/bin/env python3
import numpy as np

from nest_values import *
from funciones   import *

with open('seed.txt') as f:
    seed = lines = int(f.readlines()[0])

########################### Results for exc/inh/total 

for num_sim, image in enumerate(images_selected):
    image = image[1:-4]
    #Total
    #print("Results for total data: ")
    path = results_path + '/data_total'; create_folder(path) ; remove_contents(path)   

    data = read_and_fix_dataframe(df_folder  + '/' + str(seed) ,'total', image, num_sim)
    times,complementary_time_list = get_times(data)
    total_eeg = get_eeg(times, complementary_time_list, 'total', '_', path)
    freqs_tot, peaks_tot, idx_tot = get_frequencies(total_eeg,'total','_', path)
    #print('Total spikes: ', np.sum(total_eeg[200:]))

    #Inhibitory
    #print("\n\nResults for inhibitory data: ")
    path = results_path + '/data_inh'; create_folder(path) ; remove_contents(path)

    data = read_and_fix_dataframe(df_folder  + '/' + str(seed) ,'inh', image, num_sim)
    times,complementary_time_list = get_times(data)
    inh_eeg = get_eeg(times, complementary_time_list, 'inh', '_', path)
    freqs, peaks, idx = get_frequencies(inh_eeg,'inh','_', path)
    #print('Inhibitory spikes: ',np.sum(inh_eeg[200:]))

    #Excitatory
    #print("\n\nResults for excitatory data: ")
    path = results_path + '/data_exc'; create_folder(path) ; remove_contents(path)
    data = read_and_fix_dataframe(df_folder  + '/' + str(seed) ,'exc', image, num_sim)
    times,complementary_time_list = get_times(data)
    exc_eeg = get_eeg(times, complementary_time_list, 'exc', '_', path)
    freqs_exc, peaks_exc, idx_exc = get_frequencies(exc_eeg,'exc','_', path)
    #print('Excitatory spikes: ',np.sum(exc_eeg[200:]))

    #Save results
    collect_data(image, exc_eeg, inh_eeg, peaks_exc,freqs_exc,
                idx_exc,peaks_tot,freqs_tot,idx_tot, seed)


#################### results for orientations

if make_image_video == True:
    pass
else:
    quit()
    
orientations = [i*180/num_orientations for i in range(0,num_orientations)]
neuron_types = ['l_exc', 'l_inh']

for orientation_to_read in orientations:
    for exc_or_inh in neuron_types:
        
        path = results_path + '/results_' + str(orientation_to_read) + '_' + str(exc_or_inh)
        create_folder(path); remove_contents(path)

        data = read_and_fix_dataframe(orientation_to_read,exc_or_inh)

        if len(data) < 2:
            continue
        times = generate_frames(data)
        frames, complementary_time_list = generate_empty_frames(times)
        img_array = read_frames(frames)
        create_video(img_array,orientation_to_read ,exc_or_inh, path)
        create_avg_img(img_array,orientation_to_read ,exc_or_inh , path)
        #eeg = get_eeg(times, complementary_time_list, orientation_to_read, exc_or_inh, path)
        #freqs = get_frequencies(eeg,orientation_to_read,exc_or_inh, path)
        

print("\n")




