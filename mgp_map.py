#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: Sat Jul 27 16:44:41 2019

@michael

#  OPENING DESCRIPTION HERE
"""

# -------------------------
#  START IMPORT STATEMENTS 
# -------------------------
# https://gist.github.com/graydon/11198540
from country_bounding_boxes import country_bounding_boxes
from mgp_functions import *
import pickle
# -------------------------
#   END  IMPORT STATEMENTS
# -------------------------


# ------------------------
#  START GLOBAL VARIABLES 
# ------------------------
degree_file = "degree.pickle"
with open(degree_file, "rb") as f:
    degree = pickle.load(f)
degree_grant_file = "degree_grant.pickle"
with open(degree_grant_file, "rb") as f:
    degree_grant = pickle.load(f)
school_file = "school.pickle"
with open(school_file, "rb") as f:
    school = pickle.load(f)
    
degree_with_year = degree[degree['year']>-1].copy()

""" box coordinates for Basemap to isolate portions of the globe 
    corresponding to (lllon,lllat,urlon,urlat) in generate_mgp_map
"""
world  = (-180, -90, 180, 90)
# to get all of Europe, we use th lower left corner of Portugal 
# and the upper right corner of Finland
Europe = (-9.52657060387, 36.838268541, 31.5160921567, 70.1641930203)


""" 
"""
ten_year_ranges_agg = build_year_ranges(first=1290, last=2019, inc=9, over=10)
binned_degrees_agg  = put_data_under_year_ranges(list(degree_with_year['degree_id']), 
                                                 list(degree_with_year['year']), 
                                                 ten_year_ranges_agg)
# ------------------------
#   END  GLOBAL VARIABLES 
# ------------------------


# ----------------------------
#  START FUNCTION DEFINITIONS 
# ----------------------------

""" aggs:
    input:  
        
    output: 
"""
def aggs(degree_with_year, f=1290, l=2019, i=9, o=10):

    year_ranges_agg = build_year_ranges(first=f, last=l, inc=i, over=o)
    binned_degrees_agg  = put_data_under_year_ranges(list(degree_with_year['degree_id']), 
                                                     list(degree_with_year['year']), 
                                                     year_ranges_agg)
    
    binned_schools_agg = bin_schools_by_time_frame(binned_degrees_agg)
    # NOTE: this dictionary does NOT have aggregated counts!
    # We need to do that now.
    
    binned_schools_map_all_agg = {}
    aggregates = {}

    # TODO check to see if this agrees with restructure_schools_for_map()
    # with modifications
    for k, v in binned_schools_agg.items():
    #    print(k)
        binned_schools_map_all_agg[k] = {}
        # NOTE: this assumes our iterations are IN CHRONOLOGICAL ORDER
        for s, w in v.items():  
    #        print(s)
            # build the sums for EVERY school up to this time period
            # NOTE: This ONLY makes sense for overlap = 0!! otherwise, you're double-counting.
            aggregates[(w['lng'], w['lat'])] = aggregates.get((w['lng'], w['lat']), 0) + w['count']
    
        for loc, count in aggregates.items():
            binned_schools_map_all_agg[k][loc] = count

    return binned_schools_map_all_agg


def generate_aggregate_world(degree_with_year):
    
    binned_schools_map_all_agg = aggs(degree_with_year)
    generate_mgp_map(school_freq_dict=binned_schools_map_all_agg,
                folder="mgp_img/", fileprefix="all_mgp_year_agg", 
                title_prefix="All MGP dissertations (aggregate): ", 
                max_size=3000)


def generate_aggregate_USA(degree_with_year):
    
    binned_schools_map_all_agg = aggs(degree_with_year)
    generate_mgp_map(school_freq_dict=binned_schools_map_all_agg,
                     folder="mgp_img/", fileprefix="all_mgp_year_agg_USA", 
                     title_prefix="All MGP dissertations (aggregate, USA): ", 
                     max_size=3000,
                     lllon=-171.791110603,lllat=18.91619,
                     urlon=-66.96466,urlat=71.3577635769)  # USA
    return None


def generate_aggregate_Europe(degree_with_year):
    # Let's zoom in on Europe in the aggregate map and watch the evolution over all time.
    # lower-left: 'PT': ('Portugal', (-9.52657060387, 36.838268541, -6.3890876937, 42.280468655)),
    # upper-right: 'FI': ('Finland', (20.6455928891, 59.846373196, 31.5160921567, 70.1641930203)),
    binned_schools_map_all_agg = aggs(degree_with_year)
    generate_mgp_map(school_freq_dict=binned_schools_map_all_agg,
                     folder="mgp_img/", fileprefix="all_mgp_year_agg_Europe", 
                     title_prefix="All MGP dissertations (aggregate, Europe): ", 
                     max_size=1000,
                     lllon=-9.52657060387,lllat=36.838268541,
                     urlon=31.5160921567,urlat=70.1641930203)   # Europe
    return None

# ----------------------------
#   END  FUNCTION DEFINITIONS 
# ----------------------------


# ------------
#  BEGIN MAIN 
# ------------

if __name__ == "__main__":

    # Let's map everyone in ten-year increments with five-year overlap
    ten_year_ranges = build_year_ranges(first=1290, last=2019, inc=10, over=5)
    binned_degrees  = put_data_under_year_ranges(list(degree_with_year['degree_id']), 
                                                 list(degree_with_year['year']), 
                                                 ten_year_ranges)    
    # The key to recognize here is" we feed degrees into bins.
    # Then, we bin schools from those degrees.
    
    binned_schools = bin_schools_by_time_frame(binned_degrees)
    binned_schools_map_all = restructure_schools_for_map(binned_schools)
    generate_mgp_map(school_freq_dict=binned_schools_map_all,
                     folder="mgp_img/", fileprefix="all_mgp_year", 
                     title_prefix="All MGP dissertations: ", max_size=100)
    

# ------------
#   END  MAIN 
# ------------

