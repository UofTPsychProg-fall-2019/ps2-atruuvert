#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
from shutil import copyfile

destination = "/Users/Annie/Desktop/Master's/PSY1210/GitHub/ps2-atruuvert/rawdata"
testingrooms = ['A','B','C']
for room in testingrooms:
    source = "/Users/Annie/Desktop/Master's/PSY1210/GitHub/ps2-atruuvert/testingroom" + room
    new_filename = 'experiment_data_' + room + '.csv'
    copyfile(source + '/experiment_data.csv', destination + '/' + new_filename)

#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#

path = "/Users/Annie/Desktop/Master's/PSY1210/GitHub/ps2-atruuvert/rawdata/"
data = np.empty((0,5))
for room in testingrooms:
    tmp = sp.loadtxt(path + 'experiment_data_' + room + '.csv', delimiter=',')
    data = np.vstack([data,tmp])

#%%
# calculate overall average accuracy and average median RT
#

# finding average of the accuracy column
acc_avg = np.mean(data[:,3])   # 91.48%
# finding average of the median RT column
mrt_avg = np.mean(data[:,4])   # 477.3ms

# turning the average accuracy value into a percentage
acc_in_percentage = acc_avg * 100

#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms 
# 1 = words, 2 = faces

# counting how many data points in each condition
word_sum = 0
face_sum = 0

# adding up all of the data points in each condition
word_accuracy_total = 0
face_accuracy_total = 0
word_RT_total = 0
face_RT_total = 0

for array in data:
    if array[1] == 1: # finding word conditions
        word_sum += 1
        word_accuracy_total += array[3]
        word_RT_total += array[4]
    elif array[1] == 2: # finding face conditions
        face_sum += 1
        face_accuracy_total += array[3]
        face_RT_total += array[4]

# using arithmetic to calculate the averages
word_accuracy_average = word_accuracy_total / word_sum
word_RT_average = word_RT_total / word_sum
face_accuracy_average = face_accuracy_total/ face_sum
face_RT_average = face_RT_total / face_sum

# turning the accuracy values into percentages
word_acc_percentage = word_accuracy_average * 100
face_acc_percentage = face_accuracy_average * 100

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
# 1 = white/pleasant, 2 = black/pleasant

# indexing into the white/pleasant condition and averaging the accuracy values
acc_wp = np.mean(data[data[:,2]==1,3])  # 94.0%
# indexing into the black/pleasant condition and averaging the accuracy values
acc_bp = np.mean(data[data[:,2]==2,3])  # 88.9%
# indexing into the white/pleasant condition and averaging the median RT values
mrt_wp = np.mean(data[data[:,2]==1,4])  # 469.6ms
# indexing into the black/pleasant condition and averaging the median RT values
mrt_bp = np.mean(data[data[:,2]==2,4])  # 485.1ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#

# making a list for each condition divided by stimulus
word_wp_mrt = []
word_bp_mrt = []
face_wp_mrt = []
face_bp_mrt = []

# appending each median RT to corresponding list
for array in data:
    if array[1] == 1:  # words
        if array[2] == 1:  # white/pleasant
            word_wp_mrt.append(array[4])
        elif array[2] == 2:  # black/pleasant
            word_bp_mrt.append(array[4])
    elif array[1] == 2:  # faces
        if array[2] == 1:  # white/pleasant
            face_wp_mrt.append(array[4])
        elif array[2] == 2:  # black/pleasant
            face_bp_mrt.append(array[4])

# finding the average median RT in each list created
words_wp_avg = np.mean(word_wp_mrt)
words_bp_avg = np.mean(word_bp_mrt)
face_wp_avg = np.mean(face_wp_mrt)
face_bp_avg = np.mean(face_bp_mrt)

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

word_ttest = scipy.stats.ttest_rel(word_wp_mrt, word_bp_mrt)
face_ttest = scipy.stats.ttest_rel(face_wp_mrt, face_bp_mrt)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))

# Averages by stimulus
print("\nAVERAGES FOR WORDS: {:.2f}%, {:.1f} ms".format(word_acc_percentage, word_RT_average))
print("\nAVERAGES FOR FACES: {:.2f}%, {:.1f} ms".format(face_acc_percentage, face_RT_average))

# Averages by congruency
print("\nAVERAGES FOR WHITE/PLEASANT: {:.2f}%, {:.1f} ms".format(acc_wp*100, mrt_wp))
print("\nAVERAGES FOR BLACK/PLEASANT: {:.2f}%, {:.1f} ms".format(acc_bp*100, mrt_bp))

# Average RT for each condition
print("\nWORDS WHITE/PLEASANT AVG MEDIAN RT: {:.1f} ms".format(words_wp_avg))
print("\nWORDS BLACK/PLEASANT AVG MEDIAN RT: {:.1f} ms".format(words_bp_avg))
print("\nFACES WHITE/PLEASANT AVG MEDIAN RT: {:.1f} ms".format(face_wp_avg))
print("\nFACES BLACK/PLEASANT AVG MEDIAN RT: {:.1f} ms".format(face_bp_avg))

# T test results
print('\nWORD PAIRING EFFECT ON RT T-TEST: t={:.2f}, p={}'.format(word_ttest.statistic, word_ttest.pvalue))
print('\nFACE PAIRING EFFECT ON RT T-TEST: t={:.2f}, p={}'.format(face_ttest.statistic, face_ttest.pvalue))
