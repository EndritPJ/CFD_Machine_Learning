# Deep Neural Networks for Fast Aortic CFD
Pipeline and code for building deep neural networks (DNNs) to predict computational fluid dynamics (CFD) pressure and velocity point clouds in aortas. Uses VMTK, Deformetrica (v4.3), Ansys Fluent (v19.0), Paraview and Keras. The code in this repo enables users to build DNNs with a collection of their own aortic surfaces (or other single inlet/outlet vessels).  

### Setup

Clone the github repo:

    $ git clone https://github.com/EndritPJ/CFD_Machine_Learning

Enter the Envs/ directory. You will need to build 3 separate environments (VMTK, DFCA, Keras). 

    $ conda env create -f env_DFCA.yml

### Overview
The process is split up into different stages:
1) Statistical shape modelling (SSM) which is used for expressing aortas using lower-dimensional latent vectors. This also allows for the generation of synthetic aortas through random sampling. Built using Deformetrica 4.3 and original code written by Raphael Sivera (https://github.com/ClinicalCardiovascEngGroup/SSM/tree/master/python)
2) Meshing of surfaces to create volume meshes for CFD. The package used primarily for mesh editing is VMTK.
3) Computational Fluid Dynamics is performed on a large train/test dataset of synthetic aortic meshes. In this case the commercial platform Ansys Fluent was used. Post-processing of data with the platform Paraview is necessary.
4) Finally, DNN model training and testing can commence. This is conducted using the package Keras and Tensorflow 2.0. It is recommended to have a high performance GPU (GTX1080 or higher) to speed up training.

### Initial Aortic Surface Preprocessing
1) Create an empty project directory (e.g. CFD_ML_Aortas/).
2) Create a subfolder containing your aortic surface meshes (in .vtk format). **If custom scaling has been applied to your aortic images/surface meshes please revert it**. Additionally, surface aortas should **be in millimetres**.
3) Enter the VMTK conda env.
4) Remesh and smooth your surfaces: `$ python vmtk_remesher.py`
5) Clip inlets and outlets manually: `$ python vmtk_clipper.py` . Ensure that clipping is consistent between subjects (e.g. STJ and diaphragm). Try to preserve curvature of aorta (no awkward angles in cuts).
6) Register all meshes using `$ python vmtk_registration.py` (some initial manual repositioning may be necessary)

### Statistical Shape Modelling
1. Create a new folder SSM/
2. Grab the necessary code that manages the SSM estimation and more:  
`$ git clone ClinicalCardiovascEngGroup/SSM/tree/master/python`
3. You will need an initial "template" subject. This is an initial guess which is used as a reference for building the shape model. Ideally an aorta from another dataset or a simplified aortic shape.
4. Enter the deformetrica conda environment.
5. Run: `$ ssm_estimation.ipynb` (update the directory variables). By the end you should have a SSM/r2/output/ directory containing your final template, momenta and surface reconstructions.
6. Run: `$ ssm_new_shape_generation.ipynb` (update the directory variables). By the end, you should have generated synthetic surface/volume meshes and a pca_u_new_shapes_concat.csv file which has the shape scores for each synthetic subject.

### Meshing and CFD
1. Enter the VMTK conda environment.
2. Compute centerlines for each synthetic aortic surface: `$ python vmtk_centerlines_open_profiles.py`
3. Add flow extensions to the inlets of each surface: `$ python vmtk_extension.py`
4. Compute the meshes (.vtu) of each extended aorta: `$ python vmtk_cfdmesher.py`
5. Assign .vtu mesh boundary ids using previously computed centerlines: `$ python vmtk_idfix_inlet.py`
6. Convert new .vtu files to Fluent meshes (.msh): `$ python vmtk_vtu2msh.py`
7. Enter the Fluent/ directory and run: `$ python cfd_prepare.py`. This will output a Fluent journal file which will manage the CFD loop. Enter this file and edit it to select/change boundary conditions.
8. Run the Fluent CFD simulations in batch mode in the terminal.
9. After all simulations are completed, you should have a Point_Cloud directory in the results folder. The next step is to interpolate all the CFD results back on the volume meshes (computed by SSM) which have point-point correspondence. To do this run: `$ pvbatch pview_resample_cfd2vtu` (make sure you edit the directories in the code first).

### Neural Network Building
1. Enter the Keras conda environment.
2. The training/testing data consists of the aortic shape scores computed from SSM when creating the new surfaces (pca_u_new_shapes_concat.csv) and the synthetic simulations in point correspondence (interpolated point clouds).
3. Run: `$ cfd_dnn_training.ipynb` (update directories).
4. Run: `$ cfd_dnn_testing.ipynb` (update directories).
