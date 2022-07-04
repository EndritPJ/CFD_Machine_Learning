import os, sys, readline
import vmtk
from vmtk import vmtkscripts

def marchingcubes_multiple(idir, odir):
    '''
    - batch mask to surface conversion
    - marching level indicates threshold
    '''
    if not os.path.exists(odir):
            os.makedirs(odir)
    
    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        # read image
        reader = vmtk.vmtkimagereader.vmtkImageReader()
        reader.InputFileName = idir + '/' + fname
        reader.Execute()
        # marching cubes img -> mesh
        march = vmtk.vmtkmarchingcubes.vmtkMarchingCubes()
        march.Image = reader.Image
        march.Level = 0.5
        march.Execute()
        # write surface
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Surface = march.Surface
        writer.OutputFileName = odir + '/' + name + '.vtk'
        writer.Execute()


def marchingcubes_single(ifile, ofile):
    # read image
    reader = vmtk.vmtkimagereader.vmtkImageReader()
    reader.InputFileName = ifile
    reader.Execute()
    # marching cubes img -> mesh
    march = vmtk.vmtkmarchingcubes.vmtkMarchingCubes()
    march.Image = reader.Image
    march.Level = 0.5
    march.Execute()
    # write surface
    writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
    writer.Surface = march.Surface
    writer.OutputFileName = ofile
    writer.Execute()


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to image: ")
        ofile = input("Enter the full output path: ")
        marchingcubes_single(ifile, ofile)

    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        marchingcubes_multiple(idir, odir)