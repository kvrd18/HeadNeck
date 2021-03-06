from sklearn.feature_extraction import image
import nrrd
import os
import getopt
import sys
import numpy as np
from scipy.ndimage import zoom

path = '../data/Training'
sliceRoot = 'slices/training/'

validation = False

options, remainder = getopt.getopt(sys.argv[1:], 'v', ['validation',])

for opt, arg in options:
    if opt in ('-v', '--validation'):
        validation = True

print 'validation   :', validation

if validation == True:
	path = '../data/Validation'
	sliceRoot = 'slices/validation/'

images = []
truths = []
folders = []

for subdir, dirs, files in os.walk(path):
	for file1 in files:
		if 'Mandible' in file1:
			truths.append(subdir + '/' + file1)
		if 'normalizedImg' in file1:
			images.append(subdir + '/' + file1)
			folders.append(subdir)

slices = np.zeros((1,200,200))
ground_truths = np.zeros((1))

for i in xrange(len(images)):

	# if i == 1:
	# 	break

	print
	print
	print '####################################################################'
	print '==> Extracting from image: ', i+1
	print '    Folder: ', folders[i]
	print '####################################################################'
	print
	print

	img, options = nrrd.read(images[i])
	try:
		truth, options = nrrd.read(folders[i]+'/structures/Mandible.nrrd')
	except:
		continue
	folder = folders[i]

	

	for j in xrange(img.shape[2]):
		# Extracting a 200x200 cross section from the center of each slice
		imgSlice = img[156:356,156:356,j]
		truthSlice = truth[:,:,j]
		imgSlice = imgSlice.reshape(1,200,200)
		slices = np.append(slices,imgSlice,axis=0)
		ground_truths = np.append(ground_truths,np.unique(truthSlice).shape[0])

	
	print 'Mandible: ', np.sum((ground_truths==2).astype(int))

	

slices = slices[1:slices.shape[0]]
ground_truths = ground_truths[1:ground_truths.shape[0]]


np.save(sliceRoot + 'slices.npy', slices)
np.save(sliceRoot + 'truths.npy', ground_truths)
