#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:15:29 2020

@author: ele
"""

import logging 
import json
import shutil
import glob
import pickle
import itertools

class IOUtils:
    
    logger = logging.getLogger(__name__)
    
    
    @classmethod
    def _expand_user(cls,path):
        """
        Expand ~ and ~user constructions.  If user or $HOME is unknown, do nothing.
        """
        
        return glob.os.path.expanduser(path)
    
    @classmethod
    def _rm_trailing_slash(cls,path):
        """
        Remove ending path separator if present
        """
        if path[-1] == glob.os.sep:
            path = path[:-1]
        
        return path
        
    
    @classmethod
    def chunkize(cls,iterable, size=10):
        """
        Split iterable into chunks of size `size`.
        
        args:
            iterable (iterable) : to be split
            size (int) : chunk size
        
        return:
            generator
        """
        iterator = iter(iterable)
        for first in iterator:
            yield itertools.chain([first], itertools.islice(iterator, size - 1))

    
    @classmethod
    def mkdir(cls,path):
        """
        Create directory (with subdirectories). Equivalent to bash `mkdir -p`.
        
        args:
            path (str) : system path
        """
        
        path = cls._expand_user(path)
        
        if not glob.os.path.exists(path):
            glob.os.makedirs(path)
            cls.logger.debug("Created `{}`".format(path))

    @classmethod
    def rm(cls,path):
        """
        Remove directory/file. Equivalent to bash `rm -r`.
        
        args:
            path (str) : system path
        """
        
        path = cls._expand_user(path)
        
        if glob.os.path.exists(path):
            if glob.os.path.isdir(path):
                shutil.rmtree(path)
            else:
                glob.os.remove(path)
            cls.logger.debug("Deleted `{}`".format(path))
    
    @classmethod
    def exists(cls,path):
        """
        Check if directory/file exists.
        
        args:
            path (str) : system path
        
        return:
            res (bool) : response
            
        >>> IOUtils.exists('.')
        True
        """
        
        path = cls._expand_user(path)
        
        res = glob.os.path.exists(path)
        
        return res
    
    @classmethod
    def join_paths(cls,paths):
        """
        Create system paths from elements.
        
        args:
            paths (list) : elements to create path
        
        return:
            path (str) : system path
        
        >>> IOUtils.join_paths(['new','path','to','be','created'])
        'new/path/to/be/created'
        """
        
        path = glob.os.path.join(*paths)
        return path
    
    @classmethod
    def dname(cls,path):
        """
        Return name of main directory.
        
        args:
            path (str) : system path
        
        return:
            name (str) : directory name
        
        >>> IOUtils.dname('/path/to/file.txt')
        '/path/to'
        """
        
        name = glob.os.path.dirname(path)
        
        return name
    
    @classmethod
    def fname(cls,path):
        """
        Return name of file in system path.
        
        args:
            path (str) : system path
        
        return:
            name (str) : file name
        
        >>> IOUtils.fname('/path/to/file.txt')
        'file.txt'
        """
        path = cls._rm_trailing_slash(path)
            
        name = glob.os.path.basename(path)
        return name
    
    @classmethod
    def load_json(cls,path):
        """
        Load JSON file into dict.
        
         args:
            path (str) : system path
        
        return:
            json_file (dict) : file content
        """
        
        path = cls._expand_user(path)
        
        with open(str(path)) as infile:
            json_file = json.load(infile)
        return json_file
    
    @classmethod
    def save_json(cls,path,item):
        """
        Save dict into JSON file .
        
         args:
            path (str) : system path
            item (dict) : dictionary
        
        return:
            json_file (dict) : file content
        """
        
        path = cls._expand_user(path)
        
        with open(str(path),'w') as outfile:
            json.dump(item, outfile)
            
    @classmethod
    def load_pickle(cls,path):
        """
        Load pickled python object.
        
         args:
            path (str) : system path
        
        return:
            item (object) : python object
        """
        
        path = cls._expand_user(path)
        
        with open(str(path), mode = "rb") as infile:
            item = pickle.load(infile)
        return item
      
    @classmethod
    def save_pickle(cls,item,path):
        """
        Save python object to pickle file .
        
         args:
            path (str) : system path
            item (dict) : python object 
        
        return:
            json_file (dict) : file content
        """
        
        path = cls._expand_user(path)
        
        with open(str(path), mode = "wb") as outfile:
            pickle.dump(item, outfile)        
        
    @classmethod
    def ioglob(cls, path, ext = None, recursive = False):
        """
        Backward compatibility.
        """
        
        for p in cls.iglob(path, ext = ext, recursive = recursive, ordered = True):
            yield p
            
    @classmethod
    def iuglob(cls, path, ext = None, recursive = False):
        """
        Backward compatibility.
        """
        
        for p in cls.iglob(path, ext = ext, recursive = recursive):
            yield p

    
    @classmethod
    def iglob(cls, path, ext = None, recursive = False, ordered = False):
        """
        Iterator yielding paths matching a path pattern.
        If the extension is not provided all files are returned. 
        
        Note: if `ordered=True` all paths will be load into memory, otherwise lazy loading is used. 
        
        args:
            path (str) : system path
            ext (str) : file extension
            recursive (bool) : check subfolder
            
        >>> list(IOUtils.iglob(path = '.', ext = 'py', ordered = True))
        ['./__init__.py', './ieaiaio.py', './setup.py']
        """
        
        path = cls._expand_user(path)
        
        ext = "*.{}".format(ext) if ext is not None else "*"
        
        splits = [path,ext] 
        
        if recursive:
            splits.insert(1,"**")
        
        pregex = glob.os.path.join(*splits)
                
        path_gen = sorted(glob.iglob(pregex)) if ordered else glob.iglob(pregex)
        
        for p in path_gen:
            yield p
    
if __name__ == "__main__": 
    import doctest
    doctest.testmod()


