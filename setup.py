#!/usr/bin/env python
#import ez_setup
#ez_setup.use_setuptools()

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

import sys, os
if not sys.version_info[0:2] >= (2,4):
    sys.stderr.write("Requires Python later than 2.4\n")
    sys.exit(1)
    
# quickly import the latest version of ruffus
sys.path.insert(0, os.path.abspath("."))
#import ruffus.ruffus_version
sys.path.pop(0)
    
    
if sys.version_info[0:2] >= (2,6):
    module_dependencies = []
else:
    module_dependencies = ['multiprocessing>=2.6', 'simplejson']


#from setuptools import setup, find_packages
setup(
        name='ruffus',
        #version=ruffus.ruffus_version.__version, #major.minor[.patch[.sub]]
        version='2.4b1',
        description='Light-weight Python Computational Pipeline Management',
        long_description=\
"""     
***************************************
Overview
***************************************


    The ruffus module is a lightweight way to add support 
    for running computational pipelines.
    
    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate **tasks**.
    
    Each stage or **task** in a computational pipeline is represented by a python function
    Each python function can be called in parallel to run multiple **jobs**.
    
    Ruffus was originally designed for use in bioinformatics to analyse multiple genome
    data sets.

***************************************
Documentation
***************************************
    
    Ruffus documentation can be found `here <http://wwwfgu.anat.ox.ac.uk/~lg/oss/ruffus/index.html>`_ ,
    with an `download notes <http://wwwfgu.anat.ox.ac.uk/~lg/oss/ruffus/installation.html>`_ ,
    a `short tutorial <http://wwwfgu.anat.ox.ac.uk/~lg/oss/ruffus/tutorials/simple_tutorial/simple_tutorial.html>`_ and
    an `in-depth tutorial <http://wwwfgu.anat.ox.ac.uk/~lg/oss/ruffus/tutorials/manual/manual_introduction.html>`_ .


***************************************
Background
***************************************

    The purpose of a pipeline is to determine automatically which parts of a multi-stage 
    process needs to be run and in what order in order to reach an objective ("targets")

    Computational pipelines, especially for analysing large scientific datasets are
    in widespread use. 
    However, even a conceptually simple series of steps can be difficult to set up and
    to maintain, perhaps because the right tools are not available.

***************************************
Design
***************************************
    The ruffus module has the following design goals:

        * Simplicity. Can be picked up in 10 minutes
        * Elegance
        * Lightweight
        * Unintrusive
        * Flexible/Powerful

***************************************
Features
***************************************

    Automatic support for

        * Managing dependencies
        * Parallel jobs                         
        * Re-starting from arbitrary points, especially after errors
        * Display of the pipeline as a flowchart
        * Reporting


***************************************
A Simple example
***************************************

        Use the **@follows(...)** python decorator before the function definitions::

            from ruffus import *
            import sys

            def first_task():
                print "First task"

            @follows(first_task)
            def second_task():
                print "Second task"

            @follows(second_task)
            def final_task():
                print "Final task"




        the ``@follows`` decorator indicate that the ``first_task`` function precedes ``second_task`` in 
        the pipeline.

********
Usage
********

    Each stage or **task** in a computational pipeline is represented by a python function
    Each python function can be called in parallel to run multiple **jobs**.
    
    1. Import module::
            
            import ruffus
    

    1. Annotate functions with python decorators

    2. Print dependency graph if you necessary

        - For a graphical flowchart in ``jpg``, ``svg``, ``dot``, ``png``, ``ps``, ``gif`` formats::

            graph_printout ( open("flowchart.svg", "w"),
                             "svg",
                             list_of_target_tasks)

        This requires ``dot`` to be installed

        - For a text printout of all jobs ::

            pipeline_printout(sys.stdout, list_of_target_tasks)


    3. Run the pipeline::

        pipeline_run(list_of_target_tasks, [list_of_tasks_forced_to_rerun, multiprocess = N_PARALLEL_JOBS])


""",
        author='Leo Goodstadt',
        author_email='ruffus@llew.org.uk',
        url='http://ruffus.googlecode.com',
        #download_url = "http://http://code.google.com/p/ruffus/download",
    
        install_requires = module_dependencies, #['multiprocessing>=1.0', 'json' ], #, 'python>=2.5'],
        setup_requires   = module_dependencies, #['multiprocessing>=1.0', 'json'],    #, 'python>=2.5'],

        
        classifiers=[
                    'Intended Audience :: End Users/Desktop',
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python',
                    'Topic :: Scientific/Engineering',
                    'Topic :: Scientific/Engineering :: Bio-Informatics',
                    'Topic :: System :: Distributed Computing',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development :: Libraries',
                    'Environment :: Console',
                    ],
        license = "MIT",
        keywords = "make task pipeline parallel bioinformatics science",


        #packages = find_packages('src'),    # include all packages under src
        #package_dir = {'':'src'},           #packages are under src
        packages=['ruffus'],
        package_dir={'ruffus': 'ruffus'},
        include_package_data = True,    # include everything in source control
        # use_2to3=True
        #package_data = {
        #    # If any package contains *.txt files, include them:
        #    '': ['*.TXT'],                                \
        #}


     )

#
#  http://pypi.python.org/pypi
#  http://docs.python.org/distutils/packageindex.html
#   
# 
# 
# python setup.py register
# python setup.py sdist --format=gztar upload
