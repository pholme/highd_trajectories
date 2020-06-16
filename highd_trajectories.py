# Code for ploting phase space trajectories per lane of the https://www.highd-dataset.com/

import matplotlib.pyplot as plt
from pandas import read_csv

FRAME_CUTOFF = 5 # to omit super short trajectories

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

# plots trajectories for one lane
def plot_trajectories (fname,l):

	fig, ax = plt.subplots(figsize = (12.0, 4.0))
	plt.ylabel('position (m)')
	plt.xlabel('time (s)')
	for xys in l:
		x = []
		y = []
		for xy in xys:
			x.append(xy[0])
			y.append(xy[1])
		ax.plot(x,y,',k')
	plt.savefig(fname, dpi = 200)
	plt.close('all')

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

# making plots for all lanes of one data set
def analyze (name):

	df = read_csv('data/' + name + '_recordingMeta.csv')
	dt = 1.0 / float(df['frameRate'][0]) # this is the time between two frames

	df = read_csv('data/' + name + '_tracks.csv')
	xs = df['x'].values
	ys = df['y'].values

	vehicles = df.groupby(['id'], sort = False)

	lanes = {}

	for ii, vehicle in vehicles: # go over all vehicle tracks
		xs = vehicle['x'].values
		ys = vehicle['y'].values
		ts = vehicle['frame'].values
		ls = vehicle['laneId'].values

		current = []

		for i in range(len(xs)):
			if ls[i] not in lanes: # if a new lane index appears, start collecting new data
				lanes[ls[i]] = []
				lane_last = -1

			if lane_last != ls[i]: # if there is a lane change, that's the end of a trajectory
				if len(current) > FRAME_CUTOFF:
					lanes[ls[i]].append(current)
				current = []
				lane_last = ls[i]

			current.append((ts[i] * dt,xs[i]))

		if len(current) > FRAME_CUTOFF:
			lanes[ls[i]].append(current)

	for lane in lanes:
		plot_trajectories('fig/' + name + '_' + str(lane) + '.png', lanes[lane])

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##

# run the program as: python3 highd_trajectories.py
if __name__ == '__main__':

	for i in range(1,61): # the names of the HighD data files go from 01 to 60
		analyze('%02d' % i)

##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##
