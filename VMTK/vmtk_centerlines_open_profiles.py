import os, sys, readline
import vmtk
from vmtk import vmtkscripts

def centerlines_multiple(idir, odir):
    '''
    - calculate new centerlines (openprofiles)
    - profileidlist is automatic without renderer
    - subdivide into 99 segments (100 nodes)
    - divide by 99.1 (not 99) to ensure 100 nodes
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)

    for fname in sorted(os.listdir(idir)):
        
        name = os.path.splitext(fname)[0]
        print(name)
        output_name = odir + '/' + name + '_centerline.vtk'
        if os.path.isfile(output_name):
            continue
        # read surface
        reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
        reader.InputFileName = idir + '/' + fname
        reader.Execute()
        # compute centerline
        centerline = vmtk.vmtkcenterlines.vmtkCenterlines()
        centerline.SeedSelectorName = "profileidlist"
        centerline.SourceIds = [0]
        centerline.TargetIds = [1]
        #centerline.SeedSelectorName = "openprofiles"
        centerline.Surface = reader.Surface
        centerline.AppendEndPoints = 1
        centerline.Execute()
        # resample centerline to 100 points
        cent_geom = vmtk.vmtkcenterlinegeometry.vmtkCenterlineGeometry()
        cent_geom.Centerlines = centerline.Centerlines
        cent_geom.Execute()
        cent2np = vmtk.vmtkcenterlinestonumpy.vmtkCenterlinesToNumpy()
        cent2np.Centerlines = cent_geom.Centerlines
        cent2np.Execute()
        cent_length = cent2np.ArrayDict['CellData']['Length']
        resampler = vmtk.vmtkcenterlineresampling.vmtkCenterlineResampling()
        resampler.Centerlines = centerline.Centerlines
        resampler.Length = cent_length / 99.1
        resampler.Execute()
        # write centerline
        writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
        writer.Input = resampler.Centerlines
        writer.OutputFileName = odir + '/' + name + '_centerline.vtk'
        writer.Execute()


def centerlines_single(ifile, ofile):
    # read surface
    reader = vmtk.vmtksurfacereader.vmtkSurfaceReader()
    reader.InputFileName = ifile
    reader.Execute()
    # compute centerline
    centerline = vmtk.vmtkcenterlines.vmtkCenterlines()
    #centreline.SeedSelectorName = "profileidlist"
    #centreline.SourceIds = [0]
    #centreline.TargetIds = [1]
    centerline.SeedSelectorName = "openprofiles"
    centerline.Surface = reader.Surface
    centerline.AppendEndPoints = 1
    centerline.Execute()
    # resample centerline to 100 points
    cent_geom = vmtk.vmtkcenterlinegeometry.vmtkCenterlineGeometry()
    cent_geom.Centerlines = centerline.Centerlines
    cent_geom.Execute()
    cent2np = vmtk.vmtkcenterlinestonumpy.vmtkCenterlinesToNumpy()
    cent2np.Centerlines = cent_geom.Centerlines
    cent2np.Execute()
    cent_length = cent2np.ArrayDict['CellData']['Length']   
    resampler = vmtk.vmtkcenterlineresampling.vmtkCenterlineResampling()
    resampler.Centerlines = centerline.Centerlines
    resampler.Length = cent_length / 99.1
    resampler.Execute()
    # write centerline
    writer = vmtk.vmtksurfacewriter.vmtkSurfaceWriter()
    writer.Input = resampler.Centerlines
    writer.OutputFileName = ofile
    writer.Execute()
    

if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the full output path: ")
        centerlines_single(ifile, ofile)

    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        centerlines_multiple(idir, odir)