#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:09:53 2019

@author: pklein

nifti.gz extractor
"""

import os
import gzip
import bz2 as bzip
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
    
    extract_gz(filepath, keep_file):
        Extract a specific gzip file. If keep_file is set to False, deletes also the old gzip file.
    """
    def extract_gz(self, filepath, keep_file=True):
        """
        Unzip a specific gzip file
        
        Parameters
        -----------        
        filepath : String
            full path to the gzip file which will be extracted
        keep_file : boolean, default=True
            If set to false, delete the old gzip file
           
        """
        with gzip.open(filepath, 'rb') as f_in:
            with open(filepath.split('.gz')[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                f_in.close()
                f_out.close()
                
        if not keep_file:
            os.remove(folder+'/'+f)
                    
    def extract_all_gz(self, folder, keep_files=True):
        """
        Unzip all gzip files in a specified folder
        
        Parameters
        -----------        
        folder : String
            path to the folder in which all gzip files will be extracted
        keep_files : boolean, default=True
            If set to false, delete the old gzip files
           
        """
        for f in os.listdir(folder):
            if '.gz' in f:
                self.extract_gz(folder+'/'+f, keep_files)