#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:09:53 2019

@author: pklein

nifti.gz extractor
"""

import os
import gzip
import bzip
import pickle
import shutil
import numpy as np

class ZipUtils:
    """
    Set of zip/unzip functionalities
    
    
    Methods:
    --------    
    extract_all_gz(folder, keep_files)
        Extract all gzip files in a folder. If keep_files is set to False, deletes also the old gzip files.
    
            
    """

    def extract_all_gz(self, folder, keep_files=True):
        """
        Generates a graph with the p-value annotations on it.
        
        Parameters
        -----------        
        folder : String
            path to the folder in which all gzip files will be extracted
        keep_files : boolean, default=True
            If set to false, delete the old gzip files
           
        """
        for f in os.listdir(folder):
            if '.gz' in f:
                with gzip.open(folder+'/'+f, 'rb') as f_in:
                    with open(folder+'/'+f.split('.gz')[0], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                f_in.close()
                f_out.close()
                
                if not keep_files:
                    os.remove(folder+'/'+f)