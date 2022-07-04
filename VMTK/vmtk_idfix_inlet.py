import os, sys, copy, readline
import vmtk
from vmtk import vmtkscripts
import numpy as np
import vtk
from vtk.vtkCommonCore import vtkObject
from vtk.util import numpy_support as ns

def id_fix_multiple(idir, cdir, odir):
    '''
    - get inlet point from centerline
    - get ids of boundaries (in/out) from .vtu
    - get dist of outlet-id3 and outlet-id2
    - outlet-id2 should be smaller since no outlet extension
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)
    idir_sort = sorted(os.listdir(idir))
    cdir_sort = sorted(os.listdir(cdir))

    for fname, cname in zip(idir_sort, cdir_sort):
        name = os.path.splitext(fname)[0]
        # read centerlines
        cent_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        cent_reader.InputFileName = cdir + '/' + cname
        cent_reader.Execute()
        # convert centerlines to np array
        cent2np = vmtk.vmtkcenterlinestonumpy.vmtkCenterlinesToNumpy()
        cent2np.Centerlines = cent_reader.Surface
        cent2np.Execute()
        cent_arr = cent2np.ArrayDict
        # outlet centerline point
        ao_outlet = cent_arr['Points'][-1]
        # read vtu
        mesh_reader = vmtk.vmtkmeshreader.vmtkMeshReader()
        mesh_reader.InputFileName = idir + '/' + fname
        mesh_reader.Execute()
        # convert vtu to np array
        mesh2np = vmtk.vmtkmeshtonumpy.vmtkMeshToNumpy()
        mesh2np.Mesh = mesh_reader.Mesh
        mesh2np.Execute()
        mesh_arr = mesh2np.ArrayDict
        # read vtu with vtk
        vtk_reader = vtk.vtkXMLUnstructuredGridReader()
        vtk_reader.SetFileName(idir + '/' + fname)
        vtk_reader.Update()
        ugrid = vtk_reader.GetOutput()
        # get indices of two triangles (id=2, id=3)
        cell_id2 = np.where(mesh_arr['CellData']['CellEntityIds']==2)[0][0]
        cell_id3 = np.where(mesh_arr['CellData']['CellEntityIds']==3)[0][0]
        # get triangle verts
        points_id2 = copy.deepcopy(ns.vtk_to_numpy(ugrid.GetCell(cell_id2).GetPoints().GetData()))
        points_id3 = copy.deepcopy(ns.vtk_to_numpy(ugrid.GetCell(cell_id3).GetPoints().GetData()))
        # euclidean distances for centerline_inlet - boundaries
        dist_outlet_id2 = np.linalg.norm(ao_outlet - points_id2[0])
        dist_outlet_id3 = np.linalg.norm(ao_outlet - points_id3[0])                
        '''
        if outlet->id2 is smaller, then outlet is id2 (incorrect). Therefore switch:
        '''
        if dist_outlet_id2 < dist_outlet_id3:
            print("switching CellEntityIds for " + fname + "...")
            for i, cell_id in enumerate(mesh_arr['CellData']['CellEntityIds']):
                if cell_id == 2:
                    mesh_arr['CellData']['CellEntityIds'][i] = 3
                elif cell_id == 3:
                    mesh_arr['CellData']['CellEntityIds'][i] = 2

        # convert new np array to mesh
        np2mesh = vmtk.vmtknumpytomesh.vmtkNumpyToMesh()
        np2mesh.ArrayDict = mesh_arr
        np2mesh.Execute()
        # write mesh as vtu file
        writer = vmtk.vmtkmeshwriter.vmtkMeshWriter()
        writer.Mesh = np2mesh.Mesh
        writer.OutputFileName = odir + '/' + name + '.vtu'
        writer.Execute()

if __name__=="__main__":
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    idir = input("Enter vtu directory: ")
    cdir = input("Enter centerlines directory: ")
    odir = input("Enter output directory: ")
    id_fix_multiple(idir, cdir, odir)