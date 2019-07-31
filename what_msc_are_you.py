#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: Mon Jul 29 11:39:46 2019

@mcarlisle

#  OPENING DESCRIPTION HERE
"""

# -------------------------
#  START IMPORT STATEMENTS 
# -------------------------
import pickle
from IPython.core.display import display, HTML
# -------------------------
#   END  IMPORT STATEMENTS
# -------------------------


# ------------------------
#  START GLOBAL VARIABLES 
# ------------------------
with open("../MSC/msc_2010.pickle", "rb") as f:
    msc_names_2010 = pickle.load(f)
with open('../count_rf_20190729.pickle', 'rb') as f:
    pipe = pickle.load(f)
pipe.verbose = False
# ------------------------
#   END  GLOBAL VARIABLES 
# ------------------------


# ----------------------------
#  START FUNCTION DEFINITIONS 
# ----------------------------
def msc_code_to_name(code):
    assert code < 100, "msc_code_to_name: int input only"
    return msc_names_2010.get(code, "no classification given")
    
def msc_classify_string(text):
    assert type(text) is str, "msc_classify_string: string input only"
    pipe.verbose = False  # this doesn't seem to be working
    code = pipe.predict([text])[0]
    code_str = '0'+str(code) if code < 10 else str(code)
    msc_name = msc_code_to_name(code)
    link = f"<a href=\"http://msc2010.org/mediawiki/index.php?title={code_str}-XX\""
    link = f"{link} target=\"_blank\">{msc_name}</a>"
    return f"MSC 2010: {code}: {link}"

def msc_classify_presentation():
    request = "Input a line of text, and we will classify it for you under the"
    request = request + " Mathematics Subject Classification (MSC) 2010!\n"
    request = request + "(Note: currently, most non-mathematical text "
    request = request + "will classify as Commutative Algebra.)\n"
    
    while True:
        print(request)
        some_string = input()
        print("\nYour text classifies mathematically as:")
        display(HTML(msc_classify_string(some_string)))
        print("\nWhy not try again?\n")
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

