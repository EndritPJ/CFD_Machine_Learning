from paraview.simple import *
# note install pv 5.8+ .tar.gz for import vtk to work:
from paraview import numpy_support as ns
from paraview import servermanager as sm
import os, sys, vtk
import numpy as np

def slice_cfd_data(idir, cdir, odir, param):
    '''
    - For each case in directory:
        - load cfd .cas (.dat needed) and centerline (care with naming)
            - for each point in centerline (0->len-1)
                - place slice: origin = point, normal = vector (point->point+1)
                - clip slice with sphere: origin = point, radius = centerlineMaxInscribedSphere
                - integrate variables: on clip to get avg pressure
                - concat and export .csv array of avg pressures
    '''
    if not os.path.exists(odir):
        os.makedirs(odir)
    
    for fname in sorted(os.listdir(idir)):
        name = os.path.splitext(fname)[0]       
        
        #pv_file = odir + '/' + name + '_pv.csv'
        #if os.path.exists(pv_file) == False:

        if fname.__contains__(".encas"):
            cname = fname.replace(".encas", "_centerline.vtk") # depends on naming convention

            # read .cas
            print("Loading " + fname)
            # deleted: renderView = GetActiveViewOrCreate('RenderView')
            cfd_cas = EnSightReader(registrationName='cfd_cas', CaseFileName = idir + '/' +fname)
            UpdatePipeline(time=0.0, proxy=cfd_cas)
            
            # read centerline .vtk
            print("Loading " + cname)
            reader = vtk.vtkPolyDataReader()
            reader.SetFileName(cdir + '/' + cname)
            reader.Update()
            points = ns.vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
            radii = ns.vtk_to_numpy(reader.GetOutput().GetPointData().GetArray("MaximumInscribedSphereRadius"))
            
            # initialise vtk filters
            slice_ = Slice(Input=cfd_cas)
            slice_.SliceType = 'Plane'
            clip_ = Clip(Input=slice_)
            clip_.ClipType = 'Sphere'
            clip_.Invert = 1
            integrateVariables_ = IntegrateVariables(registrationName='IntegrateVariables', Input=clip_)

            pressures = []
            # compute 99 slices
            for i in range(0, len(radii)-1):
                point_1 = points[i]
                point_2 = points[i+1]
                normal = np.subtract(point_2, point_1)

                # slice
                slice_.SliceType.Origin = point_2
                slice_.SliceType.Normal = normal
                UpdatePipeline(time=0.0, proxy=slice_)

                # clip
                '''
                CARE: centerlines must have been computed after surface scaling (m->mm).
                scaling centerline leaves stored radii values unscaled!
                '''
                clip_.ClipType.Center = point_2
                clip_.ClipType.Radius = radii[i+1] * 1.3
                UpdatePipeline(time=0.0, proxy=clip_)

                # total pressure on slice
                UpdatePipeline(time=0.0, proxy=integrateVariables_)
                
                # avg_P = total_P / slice area
                integrate_data = sm.Fetch(integrateVariables_)
                param_arr = ns.vtk_to_numpy(integrate_data.GetPointData().GetArray(param))
                area_arr = ns.vtk_to_numpy(integrate_data.GetCellData().GetArray('Area'))
                avg_param = param_arr[0] / area_arr[0]
                # to save x-sectional area
                if odir.__contains__("Area/"):
                    avg_param = area_arr[0]

                '''
                for max values instead of average
                '''
                # clip_data = sm.Fetch(clip_)
                # max_P = max(ns.vtk_to_numpy(clip_data.GetBlock(0).GetPointData().GetArray('pressure')))
                pressures.append(avg_param)
            
            # clear and save
            Delete(integrateVariables_)
            Delete(clip_)
            Delete(slice_)
            Delete(cfd_cas)
            del(integrateVariables_)
            del(clip_)
            del(slice_)
            del(cfd_cas)
            print("writing in " + odir)
            print("")
            np.savetxt(odir + '/' + name + '_' + param + ".csv", pressures, delimiter=",")


idir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Results_CFD/Ensight/"
cdir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Centerline_Branches/LPA/"
odir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Results_Pv/LPA/"

slice_cfd_data(idir, cdir, odir + "/Avg_Pressure/", "pressure")
slice_cfd_data(idir, cdir, odir + "/Avg_Velocity/", "velocity_magnitude")
slice_cfd_data(idir, cdir, odir + "/Area/", "velocity_magnitude")

idir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Results_CFD/Ensight/"
cdir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Centerline_Branches/RPA/"
odir = "/home/endrit/Documents/Modelling/Javier/New_Sims/PA_Vivek/Results_Pv/RPA/"

slice_cfd_data(idir, cdir, odir + "/Avg_Pressure/", "pressure")
slice_cfd_data(idir, cdir, odir + "/Avg_Velocity/", "velocity_magnitude")
slice_cfd_data(idir, cdir, odir + "/Area/", "velocity_magnitude")