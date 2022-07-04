import os, readline
import vmtk
from vmtk import vmtkscripts


def write_msh_multi(idir, odir):

    if not os.path.exists(odir):
        os.makedirs(odir)

    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]
        # read vtu
        mesh_reader = vmtk.vmtkmeshreader.vmtkMeshReader()
        mesh_reader.InputFileName = idir + '/' + fname
        mesh_reader.Execute()
        # write mesh as fluent file
        writer = vmtk.vmtkmeshwriter.vmtkMeshWriter()
        writer.Mesh = mesh_reader.Mesh
        writer.OutputFileName = odir + '/' + name + '.msh'
        writer.Execute()


def write_msh_single(ifile, ofile):
    # read vtu
    mesh_reader = vmtk.vmtkmeshreader.vmtkMeshReader()
    mesh_reader.InputFileName = ifile
    mesh_reader.Execute()
    # write mesh as fluent file
    writer = vmtk.vmtkmeshwriter.vmtkMeshWriter()
    writer.Mesh = mesh_reader.Mesh
    writer.OutputFileName = ofile
    writer.Execute()


if __name__=="__main__":
    mode = int(input("1 = single file, 2 = multiple files in directory: "))
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")

    if mode==1:
        ifile = input("Enter path to file: ")
        ofile = input("Enter the desired output file path: ")
        write_msh_single(ifile, ofile)

    if mode==2:
        idir = input("Enter input directory: ")
        odir = input("Enter output directory: ")
        write_msh_multi(idir, odir)