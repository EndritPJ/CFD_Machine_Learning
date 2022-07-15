import os, sys, readline
from shutil import copyfile

def prepare_cfd(idir, odir, jpath):
    '''
    - copies journal template to jou_path
    - populates it with the mesh filenames in idir
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)

    template_dir = os.path.join(os.getcwd(), 'autofluent_template.jou')
    copyfile(template_dir, jpath + 'autofluent.jou')

    if not os.path.exists(odir + 'CGNS/'):
        os.makedirs(odir + 'CGNS/')
    if not os.path.exists(odir + 'Point_Cloud/'):
        os.makedirs(odir + 'Point_Cloud/')

    jou = open(jpath + 'autofluent.jou', 'r')
    lines = jou.readlines()
    jou.close()

    fnames = sorted(os.listdir(idir))
    for i, fname in enumerate(fnames):
        fnames[i] = fname.replace('.msh','')
    # add filepaths and filenames
    for i in range(0, len(lines)):
        if 'define filedir' in lines[i]:
            lines[i] = '(define filedir ' + '"' + idir + '")\n'
        if 'define cgnsdir' in lines[i]:
            lines[i] = '(define cgnsdir ' + '"' + odir + 'CGNS/")\n'
        if 'define csvdir' in lines[i]:
            lines[i] = '(define csvdir ' + '"' + odir + 'Point_Cloud/")\n'
        if '(list' in lines[i]:
            for j, fname in enumerate(fnames):
                lines.insert(i+j+1, ' "' + fname + '"\n')
            break

    jou = open(jpath + '/autofluent.jou', 'w')
    jou.writelines(lines)
    jou.close()

if __name__=="__main__":
    readline.set_completer_delims(" \t\n=")
    readline.parse_and_bind("tab: complete")
    idir = input("Enter Fluent meshes directory: ")
    odir = input("Enter the desired CFD results directory: ")
    jpath = input("Enter directory where journal file will be saved: ")
    prepare_cfd(idir, odir, jpath)