import os
import ray
import multiprocessing as mp
import modin.pandas as mpd
import pandas as pd
import sys
import csv
import numpy as np
from datetime import date
import re
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


def days_since(date_string):
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    d0 = date(2014,1,1)
    d1 = date(year,month,day)
    return(d1 - d0).days

def is_date(lnput):
    return len(lnput) == 10 and re.match(r"(?<![\w-])20\d\d-\d\d-\d\d(?![\w-])",lnput) != None

def bin_num(date_string):
	days = days_since(date_string)
	if days < 244:
		return 0
	elif days < 359:
		return 1
	elif days < 607:
		return 2
	elif days < 919:
		return 3
	elif days < 2338:
		return 4
	elif days < 2410:
		return 5
	else:
		return 6


# Sorts the data into bins while handling glitches created by newline entries. Very sluggish still.

def sort_csv(split_file, num_bins = 7, sorting = True):
	if not sorting:
		num_bins = 1
	with open(split_file, 'r') as f:
		iterator = csv.reader(f)
		i = 1
		row = next(iterator)
		after = next(iterator)
		last_date = None
		last_bin = -1
		template = pd.DataFrame(columns = ['id', 'name', 'body','date'])
		bins = list()
		for _ in range(num_bins):
			thisbin = template.copy()
			bins.append(thisbin)
		while True:
			if is_date(row[-1]) and len(row) == 4:
				if sorting:
					j = -1
					if (row[-1] == last_date):
						j = last_bin
					else:
						j = bin_num(row[-1])
						last_bin = j
						last_date = row[-1]
					cur_bin = bins[j]
					bins[j] = cur_bin.append(row)
					print(f"Bin {j} at len {len(bins[j])}")
				else:
					bins[0] = bins[0].append(row)
					print(f"Bin {0} at len {len(bins[0])}")
				row = after
				try:
					after = next(iterator)
				except StopIteration:
					print(f"CSV cleaning complete, {i} rows generated.")
					return bins
				i += 1
			elif is_date(row[-1]):
				raise ValueError(f"Row input mishandled at row {i} with row length {len(row)}. Text: \n\n{str(row)}")
			else:
				print(f"Error at row {i}. Stitching now. {len(after)}")
				if len(after) == 0:
					after = next(iterator)
				if len(after) == 1:
					if(is_date(after[0])):
						row.append(after[0])
						try:
							after = next(iterator)
						except StopIteration:
							after = None
					else:
						row[-1] += after[0]
						try:
							after = next(iterator)
						except StopIteration:
							after = None
				if len(after) == 2:
					row[-1] += after[0]
					row.append(after[1])
					try:
						after = next(iterator)
					except StopIteration:
						after = None


# Cleans CSV files somewhat quickly and converts them into pandas dataframes saved into json.
#	csv_file: a strong containing the filepath to relevant twitter data
# -- Returns a clean pandas dataframe.
def clean_csv(csv_file):
	num_lines = sum(1 for line in open(csv_file))
	with open(csv_file, 'r') as f:
		iterator = csv.reader(f)
		i = 1
		row = next(iterator)
		after = next(iterator)
		output = pd.DataFrame(columns = ['id', 'name', 'body','date'])
		while True:
			if is_date(row[-1]) and len(row) == 4:
				output.loc[len(output)] = row
				row = after
				print(f"Row {i} added, {str(100 * (i / num_lines))[:5]}% complete.")
				try:
					after = next(iterator)
				except StopIteration:
					print(f"CSV cleaning complete, {i} rows generated.")
					output.to_json(csv_file[:-4] + "_clean.json", orient='records')
					return output
				i += 1
			elif is_date(row[-1]):
				raise ValueError(f"Row input mishandled at row {i} with row length {len(row)}. Text: \n\n{str(row)}")
			else:
				print(f"Error at row {i}. Stitching now. {len(after)}")
				if len(after) == 0:
					after = next(iterator)
				if len(after) == 1:
					if(is_date(after[0])):
						row.append(after[0])
						try:
							after = next(iterator)
						except StopIteration:
							after = None
					else:
						row[-1] += after[0]
						try:
							after = next(iterator)
						except StopIteration:
							after = None
				if len(after) == 2:
					row[-1] += after[0]
					row.append(after[1])
					try:
						after = next(iterator)
					except StopIteration:
						after = None

clean_csv(sys.argv[1])