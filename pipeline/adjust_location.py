# script to adjust lng and lat such that the points dont overlap

import sys
import pandas as pd
import math
import time

start_time = time.time()

def get_closest(df, idx_current):
	if idx_current == 0:
		closest_idx = 1
	else:
		closest_idx = 0
	closest_distance = get_distance(df, idx_current, closest_idx)
	for i in range(0, len(df['idx'])):
		val = get_distance(df, idx_current, i)
		if val < closest_distance and val != 0:
			closest_idx = i
			closest_distance = val
	return closest_idx

def get_distance(df, idx1, idx2):
	return round(math.sqrt((df.iloc[idx1]['lat'] - df.iloc[idx2]['lat']) ** 2 +
			 (df.iloc[idx1]['lng'] - df.iloc[idx2]['lng']) ** 2), 6)

def move(og_df, df, idx_current, idx_closest, tether_dist, move_dist):

	def norm(lat, lng):
		return round(math.sqrt(lat ** 2 + lng ** 2), 6)

	def check_tether(og_df, idx_current, lat_new, lng_new):
		dist = round(math.sqrt((og_df.iloc[idx_current]['lat'] - lat_new) ** 2 +
			 (og_df.iloc[idx_current]['lng'] - lng_new) ** 2), 6)
		if dist <= tether_dist:
			return True 
		else:
			return False 

	lat0 = df.iloc[idx_closest]['lat']
	lng0 = df.iloc[idx_closest]['lng']
	lat1 = df.iloc[idx_current]['lat']
	lng1 = df.iloc[idx_current]['lng']
	
	lat_v = (lat1 - lat0)
	lng_v = (lng1 - lng0)
	
	lat_u = lat_v / norm(lat_v, lng_v)
	lng_u = lng_v / norm(lat_v, lng_v)

	lat_new = lat1 + move_dist * lat_u
	lng_new = lng1 + move_dist * lng_u

	if check_tether(original_df, idx_current, lat_new, lng_new):
		df_copy = df.copy()
		df_copy.at[idx_current, 'lat'] = lat_new
		df_copy.at[idx_current, 'lng'] = lng_new
		print('checking tether: ')
		print(df_copy.at[idx_current, 'lat'])
		print(df_copy.at[idx_current, 'lng'])
		return df_copy, True
	else:
		return df, False



input_file = sys.argv[1]
output_file = sys.argv[2]

original_df = pd.read_csv(input_file)
# print(list(df.columns))

MAX_MOVES = 100
_DISTANCE = 0.0002
TETHER_DISTANCE = 0.0002
_MOVE = 0.000015

df = original_df.copy()
for idx_current in df['idx']:
	print('working on this idx: ', idx_current)
	idx_closest = get_closest(df, idx_current)
	dist_closest = get_distance(df, idx_current, idx_closest)
	print('first idx closest: ', idx_closest)
	print('first dist closest: ', dist_closest)
	moves = 0
	while moves < MAX_MOVES and dist_closest < _DISTANCE:
		df, stop = move(original_df, df, idx_current, idx_closest, TETHER_DISTANCE, _DISTANCE)
		idx_closest = get_closest(df, idx_current)
		dist_closest = get_distance(df, idx_current, idx_closest)
		#print(idx_closest)
		moves = moves + 1
		if stop == False:
			break
	print('moves: ', moves)
	print('final idx closest: ', idx_closest)
	print('final dist closest: ', dist_closest)
	print('+======================+')

print('======lat=====')
print(original_df['lat'])
print(df['lat'])
print('======lng=====')
print(original_df['lng'])
print(df['lng'])
df.to_csv(output_file)

print('time elapsed: ' , time.time() - start_time)