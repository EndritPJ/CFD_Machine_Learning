import os, sys, readline
import vmtk
from vmtk import vmtkscripts

def remesh_multiple(idir, odir, edge, scaling, smoothing):
    '''
    - remesh, smooth, scale (m->mm) batch meshes
    - edge length
    '''
    if not os.path.exists(odir):
            os.makedirs(odir)

    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        # read surface
        reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        reader.InputFileName = idir + '/' + fname
        reader.Execute()
        # remesh
        remesher = vmtk.vmtksurfaceremeshing.vmtkSurfaceRemeshing()
        remesher.ElementSizeMode = 'edgelength'
        remesher.TargetEdgeLength = edge
        remesher.Surface = reader.Surface
        remesher.NumberOfIterations = 5
        remesher.Execute()
        # smooth
        smoother = vmtk.vmtksurfacesmoothing.vmtkSurfaceSmoothing()
        smoother.Surface = remesher.Surface
        smoother.PassBand = 0.1
        smoother.NumberOfIterations = 10
        if(smoothing=="y"):
            smoother.Execute()
        # scale from m -> mm
        scaler = vmtk.vmtksurfacescaling.vmtkSurfaceScaling()
        scaler.ScaleFactor = scaling
        scaler.Surface = smoother.Surface
        if(scaling is not 1.):
            scaler.Execute()
        # write surface as vtk
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = scaler.Surface
        writer.OutputFileName = odir + '/' + name + '_remsh.vtk'
        writer.Execute()
        

def remesh_single(ifile, ofile, edge, scaling, smoothing):
        # read surface
        reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        reader.InputFileName = ifile
        reader.Execute()
        # remesh
        remesher = vmtk.vmtksurfaceremeshing.vmtkSurfaceRemeshing()
        remesher.ElementSizeMode = 'edgelength'
        remesher.TargetEdgeLength = edge
        remesher.Surface = reader.Surface
        remesher.NumberOfIterations = 5
        remesher.Execute()
        # smooth
        smoother = vmtk.vmtksurfacesmoothing.vmtkSurfaceSmoothing()
        smoother.Surface = remesher.Surface
        smoother.PassBand = 0.1
        smoother.NumberOfIterations = 10
        if(smoothing=="y"):
            smoother.Execute()
        # scale from m -> mm
        scaler = vmtk.vmtksurfacescaling.vmtkSurfaceScaling()
        scaler.ScaleFactor = scaling
        scaler.Surface = smoother.Surface
        if(scaling is not 1.):
            scaler.Execute()
        # write surface as vtk
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = scaler.Surface
        writer.OutputFileName = ofile
        writer.Execute()

if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")
    
    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the full output path: ")
        edge = float(input("Global nominal target edge length (default=2mm):") or 2)
        scale = float(input("Scale factor (enter 1 for no scaling): ") or 1)
        smooth = input("smooth mesh (y or n): ") or "y"
        remesh_single(ifile, ofile, edge, scale, smooth)

    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        edge = float(input("Global nominal target edge length (default=2mm):") or 2)
        scale = float(input("Scale factor (enter 1 for no scaling): ") or 1)
        smooth = input("smooth mesh (y or n): ") or "y"
        remesh_multiple(idir, odir, edge, scale, smooth)