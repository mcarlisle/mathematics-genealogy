#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: Sat Jul 27 15:50:00 2019

@mcarlisle

# Assorted support functions for analysis and visualizations of 
# the Mathematics Genealogy Project database
"""

# -------------------------
#  START IMPORT STATEMENTS 
# -------------------------
import matplotlib as mpl
#import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import pickle
import pandasql as ps # sqldf
from tqdm import tqdm_notebook as tqdm

# -------------------------
#   END  IMPORT STATEMENTS
# -------------------------


# ------------------------
#  START GLOBAL VARIABLES 
# ------------------------

acad_file = "academic.pickle"
with open(acad_file, "rb") as f:
    academic = pickle.load(f)
adv_file = "advises.pickle"
with open(adv_file, "rb") as f:
    advises = pickle.load(f)

degree_grant_file = "degree_grant.pickle"
with open(degree_grant_file, "rb") as f:
    degree_grant = pickle.load(f)
school_file = "school.pickle"
with open(school_file, "rb") as f:
    school = pickle.load(f)

# ------------------------
#   END  GLOBAL VARIABLES 
# ------------------------


# ----------------------------
#  START FUNCTION DEFINITIONS 
# ----------------------------
""" build_year_ranges:
    input:  first, last, inc, over: int
    required structure: first, last are "reasonable" "years", 
                        inc(rement), over(lap) are reasonable for years
    
    output: a list of pairs (n, n + inc) corresponding 
            to the partitioning of the time frame (in years)
            [first, first + N * inc)
            where N is the min int such that 
            last >= first + N * inc.
"""
def build_year_ranges(first, last, inc=1, over=1):
    assert first < last, "build_year_ranges: first < last"
    assert inc > 0, "build_year_ranges: must increment: int > 0"
    assert over > 0, "build_year_ranges: must advance range: over > 0"

    year_ranges = []
    for n in range(first, last, over):
        year_ranges.append((n, n + inc))
    return year_ranges


""" put_data_under_year_ranges:
    input:  data:  list-like (indexable) - CURRENTLY ONLY LIST IS HANDLED
            years: list of years
            year_ranges: list of year ranges (output from build_year_ranges)
    required structure: data and years have same length
                        all entries in years are in the partition year_ranges
        
    output: a dict of 
        { key = year_range
          value = list of data that line up with years in key
        } 
            
    note: if year_ranges overlap, most of data should show up multiple times.
"""
def put_data_under_year_ranges(data, years, year_ranges):

    assert len(data) == len(years), \
        "get_content_under_ranges: data and years do not match length"

#    build a dict with keys = year_ranges, with a list for each range
    data_ranges = dict()
    for y in year_ranges:
        data_ranges[y] = []

    # bin all the data by range - each row should fall in two bins, 
    # if ranges are cleanly overlapped

    # if data is a list
    for i in range(len(data)):
        for y in year_ranges:
            if y[0] <= years[i] and years[i] < y[1]:
                data_ranges[y].append(data[i])
                # this should happen twice for every entry except 
                # the very oldest and the very newest

    # TODO if data is a pandas df
    return data_ranges


""" bin_schools_by_time_frame:
    input:  binned_degrees is the output of put_data_under_year_ranges
            for the degree_grant and school dataframes.
    required structure: Requires globals: degree_grant, school.
    
    output: binned_schools, a dict of 
        { key = year_range key from binned_degrees
          value = a dict:
              { key = degree_grant['school_id']
                value = a dict:
                    { 'lat', 'lng', 'name' (all obvious data), 
                      'count': how many degrees granted during year_range } } }
    
    NOTE: this function outputs to std out to display errors.
    NOTE: binned_schools is pickled if you don't feel like running this again.
"""
def bin_schools_by_time_frame(binned_degrees):
    
    # binned_degree now contains degree_ids binned by year.
    # we want these converted to counts per school, 
    # so they can be plotted on a world map.

    binned_schools = {}  # empty dict
    total_degrees, error_count = 0, 0 
    # will be roughly double on each, since overlap doubles up almost everyone
    for k, v in tqdm(binned_degrees.items()):
    #    print(f"years: {k}")
        binned_schools[k] = dict()
        for d in v: # for degree in this year range's list
            total_degrees += 1
            # find this degree in the degree_grant df, and take its school
            l = degree_grant.index[degree_grant['degree']==d].tolist()
            if len(l) > 0:
                i = l[0]
                s = degree_grant['school'].iloc[i]
    #            print(f"{s}: placing school: ", end="")
                # add this school to the binned_schools[k] dict
                if s in binned_schools[k]: # if s is in there, increment the count
                    binned_schools[k][s]['count'] = binned_schools[k][s]['count'] + 1
    #                print(f"total count now {binned_schools[k][s]['count']}.")
                else: # add the lat, long, and a count of 1
                    s_idx = school.index[school['school_id']==s].tolist()[0] 
                    # index in school table
                    school_name = school['school_name'].iloc[s_idx] # school name!                
                    binned_schools[k][s] = { 'lat': school['lat'].iloc[s_idx], 
                                             'lng': school['lng'].iloc[s_idx],
                                             'count': 1,
                                             'name': school_name }
    #                print(f"added {school_name} at ({binned_schools[k][s]['lat']}, \
    # {binned_schools[k][s]['lng']}).")
            else:
    #            print(f"{d}: degree_id does not have degree_grant index!")
                error_count += 1
    print(f"total number of errors: {error_count} out of {total_degrees} placed.")
    return binned_schools


""" restructure_schools_for_map:
    input:  binned_schools, output from bin_schools_by_time_frame
        
    output: an easier-to-read dict for plotting on a map by year range: 
        { key = key from binned_schools (year_range)
          value = a dict:
              { key = ('lng', 'lat')
                value = 'count' }
              for the schools present in that year_range }
"""
def restructure_schools_for_map(binned_schools):
    binned_schools_map_all = {}
    # make the new keys the long/lat, and the new values the counts.
    # then we can more easily plot these objects.
    for k, v in binned_schools.items():
    #    print(k)
        binned_schools_map_all[k] = {}
        for s, w in v.items():
    #        print(s)
            binned_schools_map_all[k][(w['lng'], w['lat'])] = w['count']
    return binned_schools_map_all


""" generate_mgp_map:
    input:  folder: relative path in which to store map images
            fileprefix: prefix of name for map image files (augment with years)
            school_freq_dict: output of restructure_schools_for_map
            title_prefix: title for individual map images (augment with years)
            max_size: max for colormap (min is hard-coded to 0)
            lllon, lllat, urlon, urlat: lower-left, upper-right corners 
                    long/lat for BaseMap to restrict map to
                    
    output: 
"""
def generate_mgp_map(school_freq_dict,
                     folder="mgp_img/", fileprefix="all_mgp_year", 
                     title_prefix="All MGP dissertations: ",
                     max_size=100,
                     lllon=-180,lllat=-90,urlon=180,urlat=90):

    fig, ax  = plt.subplots()

    for k, v in tqdm(school_freq_dict.items()):
        x = [a[0] for a in list(v.keys())]
        y = [a[1] for a in list(v.keys())]
        c = list(v.values())
        # only bad points will be (0.0, 0.0)
        fig = plt.figure(figsize=(20,10)) # inches, at 72dpi
        ax  = Basemap(projection='cyl', #lat_0 = 0, lon_0 = 0,
                     llcrnrlon=lllon,llcrnrlat=lllat,
                     urcrnrlon=urlon,urcrnrlat=urlat)
        ax.drawcountries()
        ax.drawmapboundary()
        ax.drawcoastlines()
        ax.drawmeridians(np.arange(-180, 180, 30))
        ax.drawparallels(np.arange(-90, 90, 30))

        # normalize colorbar so it doesn't bounce range through the centuries
        norm = mpl.colors.Normalize(vmin=0,vmax=max_size)

#        x, y = map(x, y)
        ax.scatter(x, y, marker='D', c=c, norm=norm, cmap='plasma') 
        # use brighter colors?
        # TODO: add a paramter to switch this to ax.plot for chrono w/ line?
        plt.colorbar()
        plt.title(f"{title_prefix} {k}")
        plt.savefig(f"{folder}{fileprefix}_{k[0]}_{k[1]}.png", format="png")

    return None


""" LINEAGE FUNCTIONS """



def get_academic_degree_info(list_of_academics):
    # simple. go into the degree_grant table and pull all that info out.
    assert isinstance(list_of_academics, list)
    info_dict = {}
    if len(list_of_academics) == 0:
        results = pd.DataFrame()
    elif len(list_of_academics) == 1:
        results = ps.sqldf(f"select * from degree where academic = {list_of_academics[0]}")
    else:
        results = ps.sqldf(f"select * from degree where academic in {tuple(list_of_academics)}")
    return results



""" get_immediate_advice:
    input:  academic_id: int
            get_advisors: boolean: if True, get advisors (back in time);
                                if False, get advisees (forward in time).
        required: advises dataframe
    output: dict of advisors/advisees one generation back:
        { key = academic_id
          value = list of dict: [
                  { 'degree', 'year', 'school', 'lng', 'lat' } ] }
"""
def get_immediate_advice(academic_id, get_advisors=True):
    who,whom = ('advisee','advisor') if get_advisors else ('advisor','advisee')
    people = advises[advises[who]==academic_id]
    return list(people[whom])



def build_lineage_academic_list(academic_id, get_advisors=True):
    # The first part to the large function below.
    # Make this easy: get all the academic_ids of the lineage.
    
    # First, get all of this academic's line (in the direction of get_advisors).
    line_exists = True
    # only count self on way back
    academic_id_lineage = [academic_id] if get_advisors else [] 
    while line_exists:
        immediate = get_immediate_advice(academic_id, get_advisors)
#        print(f"{academic_id}: immediate {immediate}")
        if len(immediate) > 0:
            for a in immediate:
                academic_id_lineage.extend(build_lineage_academic_list(a, get_advisors))
        line_exists = False
#        print(f" {academic_id}: finished a branch.")
    return list(set(academic_id_lineage))


""" build_lineage:
    input:  academic_id is the id of an academic in the MGP.
            back: boolean: if True, get advisors (back in time);
                            if False, get advisees (forward in time).
    output: a df from the degree table.
    
    NOT YET: dict of all academics before and up to this academic, 
        who predate this academic on their lineage
        { key = academic_id
          value = a dict:
              { academic_name, school, lng, lat, thesis, year, msc } }
"""
def build_lineage(academic_id):
    # Start with a master dataframe in which to put this academic's lineage.
    # It should have the same structure as other maps: 
    # We do not plot PEOPLE; we plot CLASSIFIED DEGREES from SCHOOLS in a YEAR.
    # Thus, the end result to feed into put_data_under_year_ranges
    # is degree IDs.
            
    # Then, pull the dataframe from degree containing ALL their data.

    # First, get the list of academic_ids of advisors for this academic_id.
    academic_id_advisors = build_lineage_academic_list(academic_id, get_advisors=True)
    # Then, get the dataframe containing these advisors' info.
    advisors_df = get_academic_degree_info(academic_id_advisors)
    
    # Then, get all of this academic's descendants' academic_ids.
    academic_id_students = build_lineage_academic_list(academic_id, get_advisors=False)
    # Then, get the dataframe containing these advisors' info.
    students_df = get_academic_degree_info(academic_id_students)

    # Put them all together.
    lineage_df = pd.concat([advisors_df, students_df], ignore_index=True)
    return lineage_df


    
# ----------------------------
#   END  FUNCTION DEFINITIONS 
# ----------------------------


# ------------
#  BEGIN MAIN 
# ------------

if __name__ == "__main__":

    pass
    
# ------------
#   END  MAIN 
# ------------

