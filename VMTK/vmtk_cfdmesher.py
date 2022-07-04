import os, sys, readline


def cfdmesher_multiple(idir, odir, edge, bl):
    '''
    - vascular volume meshing
    - uses vmtk in shell, script fails with python classes
    - option for boundary layer (bl)
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)

    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        if os.path.exists(odir+'/'+name+".vtu"):
            continue
        # meshing with inflation layers
        if(bl=="y"):
            arg = (
                f" vmtksurfacereader -ifile {idir+'/'+fname} "
                f" --pipe vmtkcenterlines -seedselector profileidlist -sourceids 0 -targetids 1 -endpoints 1 "
                f" --pipe vmtkdistancetocenterlines -useradius 1 "
                f" --pipe vmtkmeshgenerator -elementsizemode edgelengtharray -edgelengtharray DistanceToCenterlines "
                f" -edgelengthfactor {edge} -boundarylayer 1 -thicknessfactor 0.5 -sublayers 3 -sublayerratio 0.5 "
                f" -boundarylayeroncaps 0 -tetrahedralize 1 -ofile {odir+'/'+name}.vtu"
            )
            os.system(arg)
        else:
            arg = (
                f" vmtkmeshgenerator -ifile {idir+'/'+fname} -edgelength {edge} "
                f" -ofile {odir+'/'+name}.vtu"
            )
            os.system(arg)


def cfdmesher_single(ifile, ofile, edge, bl):
    # meshing with inflation layers
    if(bl=="y"):
        arg = (
            f" vmtksurfacereader -ifile {ifile} "
            f" --pipe vmtkcenterlines -endpoints 1 -seedselector profileidlist -sourceids 0 -targetids 1 "
            f" --pipe vmtkdistancetocenterlines -useradius 1 "
            f" --pipe vmtkmeshgenerator -elementsizemode edgelengtharray -edgelengtharray DistanceToCenterlines "
            f" -edgelengthfactor {edge} -boundarylayer 1 -thicknessfactor 0.5 -sublayers 3 -sublayerratio 0.8 "
            f" -boundarylayeroncaps 0 -tetrahedralize 1 -ofile {ofile}"
        )
        os.system(arg)
    else:
        arg = (
            f" vmtkmeshgenerator -ifile {ifile} -edgelength {edge} -ofile {ofile}"
        )
        os.system(arg)


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")
    
    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the full output path: ")
        edge = input("Element edge length factor (default=0.2): ") or "0.2"
        bl = input("Inflation layers (y or n): ") or "y"
        cfdmesher_single(ifile, ofile, edge, bl)

    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        edge = input("Element edge length factor (default=0.2): ") or "0.2"
        bl = input("Inflation layers (y or n): ") or "y"
        cfdmesher_multiple(idir, odir, edge, bl)