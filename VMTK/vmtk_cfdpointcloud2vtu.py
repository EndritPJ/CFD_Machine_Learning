import os, sys, copy, readline
import vmtk
from vmtk import vmtkscripts
import numpy as np
import pandas as pd
import vtk
from vtk.vtkCommonCore import vtkObject
from vtk.util import numpy_support as ns

def csv2vtu_multiple(idir, vdir, odir):
    '''
    - take cfd point cloud arrays and add them to vtu arrays
    - save out as a vtu
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)
    idir_sort = sorted(os.listdir(idir))
    vdir_sort = sorted(os.listdir(vdir))

    for fname, vname in zip(idir_sort, vdir_sort):
        name = os.path.splitext(fname)[0]
        # read cfd csv
        cfd_csv = pd.read_csv(ifile, header=None)
        # get cfd data
        cfd_np = cfd_csv.values
        pressure_np = cfd_np[1:, 1].astype(np.float)
        velocity_np = cfd_np[1:, 3].astype(np.float)
        # cfd dict to go in mesh arr
        cfd_dict = {'PointData' : {'Pressure' : pressure_np, 'Velocity_Magnitude' : velocity_np}}
        # read vtu
        mesh_reader = vmtk.vmtkmeshreader.vmtkMeshReader()
        mesh_reader.InputFileName = vdir + '/' + vname
        mesh_reader.Execute()
        # convert vtu to np array
        mesh2np = vmtk.vmtkmeshtonumpy.vmtkMeshToNumpy()
        mesh2np.Mesh = mesh_reader.Mesh
        mesh2np.Execute()
        mesh_arr = mesh2np.ArrayDict
        # add CFD dict
        mesh_arr.update(cfd_dict)
        # convert new np array to mesh
        np2mesh = vmtk.vmtknumpytomesh.vmtkNumpyToMesh()
        np2mesh.ArrayDict = mesh_arr
        np2mesh.Execute()
        # write mesh as vtu file
        writer = vmtk.vmtkmeshwriter.vmtkMeshWriter()
        writer.Mesh = np2mesh.Mesh
        writer.OutputFileName = odir + '/' + name + '_cfd.vtu'
        writer.Execute()


def csv2vtu_single(ifile, vfile, ofile):
        # read cfd csv
        cfd_csv = pd.read_csv(ifile, header=None)
        # get cfd data
        cfd_np = cfd_csv.values
        pressure_np = cfd_np[1:, 1].astype(np.float)
        velocity_np = cfd_np[1:, 3].astype(np.float)
        # cfd dict to go in mesh arr
        cfd_dict = {'PointData' : {'Pressure' : pressure_np, 'Velocity_Magnitude' : velocity_np}}
        # read vtu
        mesh_reader = vmtk.vmtkmeshreader.vmtkMeshReader()
        mesh_reader.InputFileName = vfile
        mesh_reader.Execute()
        # convert vtu to np array
        mesh2np = vmtk.vmtkmeshtonumpy.vmtkMeshToNumpy()
        mesh2np.Mesh = mesh_reader.Mesh
        mesh2np.Execute()
        mesh_arr = mesh2np.ArrayDict
        # add CFD dict
        mesh_arr.update(cfd_dict)
        # convert new np array to mesh
        np2mesh = vmtk.vmtknumpytomesh.vmtkNumpyToMesh()
        np2mesh.ArrayDict = mesh_arr
        np2mesh.Execute()
        # write mesh as vtu file
        writer = vmtk.vmtkmeshwriter.vmtkMeshWriter()
        writer.Mesh = np2mesh.Mesh
        writer.OutputFileName = ofile
        writer.Execute()


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to cfd point cloud: ")
        vfile = input("Enter path to matching vtu mesh: ")
        ofile = input("Enter the desired output file path: ")
        csv2vtu_single(ifile, ofile)

    if mode==2:
        idir = input("Enter directory of cfd point clouds: ")
        vdir = input("Enter directory of matching vtu meshes: ")
        odir = input("Enter output directory: ")
        csv2vtu_multiple(idir, odir)