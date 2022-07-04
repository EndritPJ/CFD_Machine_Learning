from genericpath import isdir
from paraview.simple import *
# note install pv 5.8+ .tar.gz for import vtk to work:
from paraview import numpy_support as ns
from paraview import servermanager as sm
from paraview import simple
import os, sys, vtk
import numpy as np
import re

'''
sorting function
'''
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l



def resample_cfd2vtu(idir, odir):

    if not os.path.exists(odir):
        os.makedirs(odir)
    
    idir_sort = sort_nicely(os.listdir(idir))
    
    for fname in idir_sort:
        name = os.path.splitext(fname)[0]
        
        reader = simple.OpenDataFile(idir + '/' + fname)
        writer = simple.CreateWriter(odir + '/' + name + ".csv", reader)
        writer.FieldAssociation = "Point Data"
        writer.UpdatePipeline()

        '''
        # read .vtu
        print("Loading " + fname)
        vtu = XMLUnstructuredGridReader(registrationName='vtu', FileName=[idir + '/' + fname])
        UpdatePipeline(time=0.0, proxy=vtu)
        SetActiveSource(vtu)

        print("writing csv: " + name)
        print("")
        SaveData(odir + '/' + name + ".csv", proxy=vtu, ChooseArraysToWrite = 1, PointDataArrays=['Points'], Precision=8)

        Delete(vtu)
        del(vtu)
        '''

idir = "/home/endrit/Documents/Modelling/COA/pipeline_1650/Sampled_grid/new_volumes/"
odir = "/home/endrit/Documents/Modelling/COA/pipeline_1650/Sampled_grid/new_csvs/"

resample_cfd2vtu(idir, odir)