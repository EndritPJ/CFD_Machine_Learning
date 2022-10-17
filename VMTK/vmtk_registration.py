import os, sys, readline
import vmtk
from vmtk import vmtkscripts

def registration_multiple(idir, rfile, odir):
    if not os.path.exists(odir):
        os.makedirs(odir)

    # read reference surface
    reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
    reader.InputFileName = rfile
    reader.Execute()
    # set as registration target
    register = vmtk.vmtkicpregistration.vmtkICPRegistration()
    register.ReferenceSurface = reader.Surface

    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        # read surface + register
        reader.InputFileName = idir + '/' + fname
        reader.Execute()
        register.Surface = reader.Surface
        register.Execute()
        # write registered surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = register.Surface
        writer.OutputFileName = odir + '/' + name + '_reg.vtk'
        writer.Execute()

def registration_single(ifile, rfile, ofile):
    # read reference surface
    reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
    reader.InputFileName = rfile
    reader.Execute()
    # read input surface
    surf_reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
    surf_reader.InputFileName = ifile
    surf_reader.Execute()
    # registration
    register = vmtk.vmtkicpregistration.vmtkICPRegistration()
    register.ReferenceSurface = reader.Surface
    register.Surface = surf_reader.Surface
    register.Execute()
    # write registered surface
    writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
    writer.Surface = register.Surface
    writer.OutputFileName = ofile
    writer.Execute()

if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")
    
    if mode==1:
        ifile = input("Enter path to file: ")
        rfile = input("Enter path to registration target: ")
        ofile = input("Enter the full output path: ")
        registration_single(ifile, rfile, ofile)

    if mode==2:
        idir = input("Enter input directory: ")
        rfile = input("Enter path to registration target: ")
        odir = input("Enter output directory: ")
        registration_multiple(idir, rfile, odir)