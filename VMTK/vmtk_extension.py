import os, sys, readline
import vmtk
from vmtk import vmtkscripts
import vmtkflowextensions_custom

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
        extender = vmtkflowextensions_custom.vmtkFlowExtensions()
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


def extension_centerline_multi(idir, cdir, odir):
    '''
    - add flow extensions for all meshes in directory
    - uses centerlines as extension direction
    - surface normals recomputed after extension
    '''
    idir_sort = sorted(os.listdir(idir))
    cdir_sort = sorted(os.listdir(cdir))
    if not os.path.exists(odir):
        os.makedirs(odir)

    for fname, cname in zip(idir_sort, cdir_sort):
        name = os.path.splitext(fname)[0]
        print(name)
        # read surface
        surf_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        surf_reader.InputFileName = idir + '/' + fname
        surf_reader.Execute()
        # read centerline
        cent_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        cent_reader.InputFileName = cdir + '/' + cname
        cent_reader.Execute()
        # extensions
        extender = vmtk.vmtkflowextensions.vmtkFlowExtensions()
        extender.Surface = surf_reader.Surface
        extender.Centerlines = cent_reader.Surface
        extender.ExtensionMode = "centerlinedirection"
        extender.Interactive = 0
        # 30mm
        extender.ExtensionLength = 30
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


def extension_centerline_single(ifile, cfile, ofile):
        # read surface
        surf_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        surf_reader.InputFileName = ifile
        surf_reader.Execute()
        # read centerline
        cent_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        cent_reader.InputFileName = cfile
        cent_reader.Execute()
        # extensions
        extender = vmtk.vmtkflowextensions.vmtkFlowExtensions()
        extender.Surface = surf_reader.Surface
        extender.Centerlines = cent_reader.Surface
        extender.ExtensionMode = "centerlinedirection"
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
        mode = int(input("1 = use boundary normals, 2 = use centerlines: "))
        if mode==1:
            ifile = input("Enter path to file: ")
            ofile = input("Enter the full output path: ")
            extension_boundary_single(ifile, ofile)
        if mode==2:
            ifile = input("Enter path to file: ")
            cfile = input("Enter path to centerline: ")
            ofile = input("Enter the full output path: ")
            extension_centerline_single(ifile, cfile, ofile)

    if mode==2:
        mode = int(input("1 = use boundary normals, 2 = use centerlines: "))
        if mode==1:
            idir = input("Enter input directory: ")
            odir = input("Enter output directory: ")
            extension_boundary_multi(idir, odir)
        if mode==2:
            idir = input("Enter input directory: ")
            cdir = input("Enter centerlines directory: ")
            odir = input("Enter output directory: ")
            extension_centerline_multi(idir, cdir, odir)