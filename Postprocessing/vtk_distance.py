import os, sys, vtk, readline, statistics
import numpy as np
from vtk.util import numpy_support as ns

def compute_distance_multiple(idir, rdir, odir):
    '''
    - compute the distances between two surfaces
    - ifile is the source, rfile is used as the reference
    - outputs ifile surface with distribution of distances
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)
    
    surf_main = sorted(os.listdir(idir))
    surf_ref = sorted(os.listdir(rdir))

    for fname, rname in zip(surf_main, surf_ref):
        name = os.path.splitext(fname)[0]
        # load files
        ifile_reader = vtk.vtkPolyDataReader()
        ifile_reader.SetFileName(idir + '/' + fname)
        ifile_reader.Update()
        rfile_reader = vtk.vtkPolyDataReader()
        rfile_reader.SetFileName(rdir + '/' + rname)
        rfile_reader.Update()
        # compute distances
        dist_filter = vtk.vtkDistancePolyDataFilter()
        dist_filter.SetInputConnection(0, ifile_reader.GetOutputPort())
        dist_filter.SetInputConnection(1, rfile_reader.GetOutputPort())
        dist_filter.Update()
        distances = dist_filter.GetOutput()
        # write vtk
        writer = vtk.vtkPolyDataWriter()
        writer.SetInputData(distances)
        writer.SetFileName(odir + '/' + name + '_dist.vtk')
        writer.Write()


def compute_distance_single(ifile, rfile, ofile):
    # load files
    ifile_reader = vtk.vtkPolyDataReader()
    ifile_reader.SetFileName(ifile)
    ifile_reader.Update()
    rfile_reader = vtk.vtkPolyDataReader()
    rfile_reader.SetFileName(rfile)
    rfile_reader.Update()
    # compute distances
    dist_filter = vtk.vtkDistancePolyDataFilter()
    dist_filter.SetInputConnection(0, ifile_reader.GetOutputPort())
    dist_filter.SetInputConnection(1, rfile_reader.GetOutputPort())
    dist_filter.Update()
    distances = dist_filter.GetOutput()
    # write vtk
    writer = vtk.vtkPolyDataWriter()
    writer.SetInputData(distances)
    writer.SetFileName(ofile)
    writer.Write()


def compute_distance_custom(idir, odir):
    '''
    - save csv of average distances 
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)

    # ground truth + distance map outputted
    surf_main = sorted(os.listdir(idir))[10:]
    surf_ref = sorted(os.listdir(idir))[:10]

    average_dist = []
    for fname, rname in zip(surf_main, surf_ref):
        print(fname)
        print(rname)
        name = os.path.splitext(fname)[0]
        # load files
        ifile_reader = vtk.vtkPolyDataReader()
        ifile_reader.SetFileName(idir + '/' + fname)
        ifile_reader.Update()
        rfile_reader = vtk.vtkPolyDataReader()
        rfile_reader.SetFileName(idir + '/' + rname)
        rfile_reader.Update()
        # compute distances
        dist_filter = vtk.vtkDistancePolyDataFilter()
        dist_filter.SetInputConnection(0, ifile_reader.GetOutputPort())
        dist_filter.SetInputConnection(1, rfile_reader.GetOutputPort())
        dist_filter.Update()
        distances = dist_filter.GetOutput()        
        # write vtk
        writer = vtk.vtkImageWriter()
        writer.SetInputData(distances)
        writer.SetFileName(odir + '/' + name + '_dist.vtk')
        writer.Write()        
        # get array of data
        dist_cell_data = distances.GetCellData().GetArray("Distance")
        dist_np = ns.vtk_to_numpy(dist_cell_data)
        dist_avg = statistics.mean(abs(dist_np))
        print(dist_avg)
        average_dist.append(dist_avg)

    np.savetxt(odir + '/' + "avg_distances.csv", average_dist, delimiter=",")
    

if __name__=="__main__":
    #mode = int(input("1 = single file, 2 = multiple files in directory: "))
    #readline.set_completer_delims(" \t\n=")
    #readline.parse_and_bind("tab: complete")

    idir = "/home/endrit/Documents/Modelling/Javier/Ao_Pa/Ao_VMTK_based/Meshes_2_Clipped/"
    odir = "/home/endrit/Documents/Modelling/Javier/Ao_Pa/Ao_VMTK_based/Distances/Meshes_2/"
    compute_distance_custom(idir, odir)

    '''
    if mode == 1:
        ifile = input("Enter path to main surface file: ")
        rfile = input("Enter path to reference surface (to compute distances to): ")
        ofile = input("Enter full save location: ")
        compute_distance_single(ifile, rfile, ofile)

    if mode == 2:
        idir = input("Enter directory of main surfaces: ")
        rdir = input("Enter directory of reference surfaces (to compute distances to): ")
        odir = input("Enter directory to save files with computed distances: ")
        compute_distance_multiple(idir, rdir, odir)
    '''