import os, sys, readline
import vmtk
from vmtk import vmtkscripts

def clipper_multiple(idir, cdir, odir):
    '''
    - use existing centerlines to clip ends of aortas
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)    
    idir_sort = sorted(os.listdir(idir))
    cdir_sort = sorted(os.listdir(cdir))

    for fname, cname in zip(idir_sort, cdir_sort):
        name = os.path.splitext(fname)[0]
        # read centerline
        reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        reader.InputFileName = cdir + '/' + cname
        reader.Execute()
        # get end points of centerline
        endpoints = vmtk.vmtkendpointextractor.vmtkEndpointExtractor()
        endpoints.NumberOfEndpointSpheres = 1
        endpoints.Centerlines = reader.Surface
        endpoints.Execute()
        # read surface
        reader.InputFileName = idir + '/' + fname
        reader.Execute()
        # clip mesh ends
        branchclipper = vmtk.vmtkbranchclipper.vmtkBranchClipper()
        branchclipper.Surface = reader.Surface
        branchclipper.Centerlines = endpoints.Centerlines
        branchclipper.Execute()
        # re-triangulate
        connect = vmtk.vmtksurfaceconnectivity.vmtkSurfaceConnectivity()
        connect.Surface = branchclipper.Surface
        connect.CleanOutput = 1
        connect.Execute()
        # write surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = connect.Surface
        writer.OutputFileName = odir + '/' + name + '_clip.vtk'
        writer.Execute()


def clipper_single(ifile, ofile):
        # read surface
        reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        reader.InputFileName = ifile
        reader.Execute()
        # calculate centerlines
        centerline = vmtk.vmtkcenterlines.vmtkCenterlines()
        centerline.Surface = reader.Surface
        centerline.Execute()
        # get end points of centerline
        endpoints = vmtk.vmtkendpointextractor.vmtkEndpointExtractor()
        endpoints.NumberOfEndpointSpheres = 1
        endpoints.Centerlines = centerline.Centerlines
        endpoints.Execute()
        # clip mesh ends
        branchclipper = vmtk.vmtkbranchclipper.vmtkBranchClipper()
        branchclipper.Surface = reader.Surface
        branchclipper.Centerlines = endpoints.Centerlines
        branchclipper.Execute()
        # re-triangulate
        connect = vmtk.vmtksurfaceconnectivity.vmtkSurfaceConnectivity()
        connect.Surface = branchclipper.Surface
        connect.CleanOutput = 1
        connect.Execute()
        # write surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = connect.Surface
        writer.OutputFileName = ofile
        writer.Execute()


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the full output path: ")
        clipper_single(ifile, ofile)

    if mode==2:
        idir = input("Enter input directory: ")
        cdir = input("Enter centerline directory: ")
        odir = input("Enter output directory: ")
        clipper_multiple(idir, cdir, odir)
    