"""
A Class for plotting brains (still experimental)
"""
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from visbrain.objects import BrainObj, ColorbarObj, SceneObj, SourceObj
from visbrain.io import download_file, read_stc

from sklearn import preprocessing

class PlotBrain:        
    
    def __init__(self):
        pass
    
    def create_scene(self, bgcolor='white', size=(4000, 3000)):
        # Scene creation
        self.sc = SceneObj(bgcolor=bgcolor, size=size)
        # Colorbar default arguments. See `visbrain.objects.ColorbarObj`
        self.CBAR_STATE = dict(cbtxtsz=60, txtsz=60., width=1, cbtxtsh=60.,
                          rect=(-3, -2., 10., 4.), txtcolor="black")
        self.KW = dict(title_size=60., zoom=2, title_color="black")


    def parcellize_brain(self, path_to_file1 = None, path_to_file2=None, cmap="videen_style"):
        # Here, we parcellize the brain (using all parcellated included in the file).
        # Note that those parcellates files comes from MNE-python.

        # Download the annotation file of the left hemisphere lh.aparc.a2009s.annot
        if path_to_file1 == None:
            path_to_file1 = download_file('lh.aparc.annot', astype='example_data')
        # Define the brain object (now you should know how to do it)
        b_obj_parl = BrainObj('inflated', hemisphere='left', translucent=False)
        # From the list of printed parcellates, we only select a few of them
        select_par = [b for b in b_obj_parl.get_parcellates(path_to_file1)['Labels'].values if b not in ["unknown", "corpuscallosum", "FreeSurfer_Defined_Medial_Wall"]]
        print("Selected parcelations:", select_par)
        # Now we define some data for each parcellates (one value per pacellate)
        #data_par = self.data[0:34]
        data_par = self.data[0:7]
        
 
        # Finally, parcellize the brain and add the brain to the scene
        b_obj_parl.parcellize(path_to_file1, select=select_par, hemisphere='left',
                              cmap=cmap, data=data_par, clim=[self.min_ji, self.max_ji], 
                              #cmap='videen_style', data=data_par, clim=[self.min_ji, self.max_ji],
                              vmin=self.min_ji, vmax=self.max_ji, under='lightgray',
                              over='darkred')
        self.sc.add_to_subplot(b_obj_parl, row=0, col=0, col_span=3, rotate='left',
                          title='Left Hemisphere', **self.KW)

        
        # Again, we download an annotation file, but this time for the right hemisphere
        
        # Download the annotation file of the right hemisphere rh.aparc.annot
        if path_to_file2 == None:
            path_to_file2 = download_file('rh.aparc.annot', astype='example_data')
        # Define the brain object (again... I know, this is redundant)
        b_obj_parr = BrainObj('inflated', hemisphere='right', translucent=False)
        print(b_obj_parr)
        
        select_par = [b for b in b_obj_parr.get_parcellates(path_to_file2)['Labels'].values if b not in ["unknown", "corpuscallosum", "FreeSurfer_Defined_Medial_Wall"]]
        print("Selected parcelations:", select_par)
        #data_par = self.data[49:-1]
        data_par = self.data[7:]
        
        b_obj_parr.parcellize(path_to_file2, select=select_par, hemisphere='right',
                              cmap=cmap, data=data_par, clim=[self.min_ji, self.max_ji], 
                              #cmap='videen_style', data=data_par, clim=[self.min_ji, self.max_ji], 
                              vmin=self.min_ji, vmax=self.max_ji, under='lightgray',
                              over='darkred')
        
        # Add the brain object to the scene
        self.sc.add_to_subplot(b_obj_parr, row=0, col=4, col_span=3, rotate='right',
                          title='Right Hemisphere', **self.KW)
        # Get the colorbar of the brain object and add it to the scene
        cb_parr = ColorbarObj(b_obj_parl, cblabel='Feedback Inhibitory Synaptic Coupling', **self.CBAR_STATE)
        #self.sc.add_to_subplot(cb_parr, row=0, col=3, width_max=2000)
        self.b_obj_parl = b_obj_parl
        self.path_to_file1 = path_to_file1
        self.b_obj_parr = b_obj_parr
        self.path_to_file2 = path_to_file2
        

    def plot(self, data, path_to_file1=None, path_to_file2=None, cmap="videen_style"):
        self.data = data
        # self.min_ji = np.min(self.data)
        # self.max_ji = np.max(self.data)
        self.min_ji = 0
        self.max_ji = 2
        self.create_scene()
        self.parcellize_brain(path_to_file1, path_to_file2, cmap=cmap)
        self.sc.preview()
        
        return(self.b_obj_parl, self.path_to_file1, self.b_obj_parr, self.path_to_file1, self.path_to_file2)