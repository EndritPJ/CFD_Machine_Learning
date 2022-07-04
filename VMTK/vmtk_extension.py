import os, sys, readline
import vmtk
from vmtk import vmtkscripts
import custom_vmtkflowextensions

def extension_boundary_multi(idir, odir):
    '''
    - add flow extensions for all meshes in directory
    - uses boundary normals as extension direction
    - surface normals recomputed after extension
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)

    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        print(name)
        # read surface
        surf_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        surf_reader.InputFileName = idir + '/' + fname
        surf_reader.Execute()
        # extensions
        extender = custom_vmtkflowextensions.vmtkFlowExtensions()
        extender.Surface = surf_reader.Surface
        extender.ExtensionMode = "boundarynormal"
        extender.Interactive = 0
        # 30mm
        extender.ExtensionLength = 40
        extender.Execute()
        # recompute normals
        normals = vmtk.vmtksurfacenormals.vmtkSurfaceNormals()
        normals.Surface = extender.Surface
        normals.Execute()
        # write surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = normals.Surface
        writer.OutputFileName = odir + '/' + name + '_ext.vtk'
        writer.Execute()


def extension_boundary_single(ifile, ofile):
        # read surface
        surf_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        surf_reader.InputFileName = ifile
        surf_reader.Execute()
        # extensions
        extender = vmtk.vmtkflowextensions.vmtkFlowExtensions()
        extender.Surface = surf_reader.Surface
        extender.ExtensionMode = "boundarynormal"
        extender.Interactive = 0
        extender.ExtensionLength = 30
        extender.Execute()
        # recompute normals
        normals = vmtk.vmtksurfacenormals.vmtkSurfaceNormals()
        normals.Surface = extender.Surface
        normals.Execute()
        # write surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = normals.Surface
        writer.OutputFileName = ofile
        writer.Execute()


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the full output path: ")
        extension_boundary_single(ifile, ofile)
    
    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        extension_boundary_multi(idir, odir)