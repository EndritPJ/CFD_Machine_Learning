from genericpath import isdir
from paraview.simple import *
# note install pv 5.8+ .tar.gz for import vtk to work:
from paraview import numpy_support as ns
from paraview import servermanager as sm
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

def resample_cfd2vtu(idir, vdir, odir):
    '''
    - For each case in directory:
        - load cfd .csv and deformed .vtu
        - resample dataset (source is .csv), target is vtu
        - save out file as csv (ideally)
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)
    
    idir_sort = sort_nicely(os.listdir(idir))
    vdir_sort = sort_nicely(os.listdir(vdir))
    
    for fname, vname in zip(idir_sort, vdir_sort):
        name = os.path.splitext(fname)[0]

        
        # read .csv
        print("Loading " + fname)
        cfd_csv = CSVReader(registrationName='cfd_csv', FileName = idir + '/' + fname)
        UpdatePipeline(time=0.0, proxy=cfd_csv)

        # read target mesh .vtu
        print("Loading " + vname)
        vtu = XMLUnstructuredGridReader(registrationName='vtu', FileName = [vdir + '/' + vname])
        UpdatePipeline(time=0.0, proxy=vtu)
        
        # csv to point cloud
        tableToPoints = TableToPoints(registrationName='tableToPoints', Input=cfd_csv)
        tableToPoints.XColumn = '    x-coordinate'
        tableToPoints.YColumn = '    y-coordinate'
        tableToPoints.ZColumn = '    z-coordinate'
        UpdatePipeline(time=0.0, proxy=tableToPoints)

        pointVolumeInterpolator = PointVolumeInterpolator(registrationName='PointVolumeInterpolator', Input=tableToPoints, Source='Bounded Volume')
        pointVolumeInterpolator.Kernel = 'VoronoiKernel'
        pointVolumeInterpolator.Locator = 'Static Point Locator'
        pointVolumeInterpolator.Source.Padding = 5
        UpdatePipeline(time=0.0, proxy=pointVolumeInterpolator)
        
        # resample filter
        resampleWithDataset = ResampleWithDataset(registrationName='resampleWithDataset', 
                                                    SourceDataArrays=pointVolumeInterpolator,
                                                    DestinationMesh=vtu)
        UpdatePipeline(time=0.0, proxy=resampleWithDataset)
        
        # clear and save
        print("writing interpolated cfd data: " + name)
        print("")
        SaveData(odir + '/' + name + ".csv", proxy=resampleWithDataset, PointDataArrays=['        pressure', 'velocity-magnitude'], Precision=8)


        Delete(resampleWithDataset)
        Delete(pointVolumeInterpolator)
        Delete(tableToPoints)
        Delete(cfd_csv)
        Delete(vtu)
        del(resampleWithDataset)
        del(pointVolumeInterpolator)
        del(tableToPoints)
        del(cfd_csv)
        del(vtu)

'''
idir = "/home/endrit/Documents/Modelling/COA/67_subjects/Results_CFD/Results_csv/Synthetic/"
vdir = "/home/endrit/Documents/Modelling/COA/SSM_67_subj/SSM/new_shapes_deformed_vtus/edge_0.27/"
odir = "/home/endrit/Documents/Modelling/COA/67_subjects/Results_CFD/Results_Interpolated/"
'''

idir = "/home/endrit/Documents/Modelling/Post_Repair_COA/Pipeline/Results_CFD_2/Point_Cloud/"
vdir = "/home/endrit/Documents/Modelling/Post_Repair_COA/Pipeline/Vtu_SSM/"
odir = "/home/endrit/Documents/Modelling/Post_Repair_COA/Pipeline/Results_CFD_2/Point_Cloud_Interpolated/"

resample_cfd2vtu(idir, vdir, odir)