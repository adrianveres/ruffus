#!/usr/bin/env python
"""

    test_transform_with_no_re_matches.py
    
        test messages with no regular expression matches
        
"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

from optparse import OptionParser
import sys, os
import os.path
import io
import re,time

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))
if __name__ == '__main__':
    module_name = os.path.split(sys.argv[0])[1]
    module_name = os.path.splitext(module_name)[0];
else:
    module_name = __name__



import ruffus
print("\tRuffus Version = ", ruffus.__version__)
parser = OptionParser(version="%%prog v1.0, ruffus v%s" % ruffus.ruffus_version.__version)
parser.add_option("-t", "--target_tasks", dest="target_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME", 
                  type="string",
                  help="Target task(s) of pipeline.")
parser.add_option("-f", "--forced_tasks", dest="forced_tasks",
                  action="append",
                  default = list(),
                  metavar="JOBNAME", 
                  type="string",
                  help="Pipeline task(s) which will be included even if they are up to date.")
parser.add_option("-j", "--jobs", dest="jobs",
                  default=1,
                  metavar="jobs", 
                  type="int",
                  help="Specifies  the number of jobs (commands) to run simultaneously.")
parser.add_option("-v", "--verbose", dest = "verbose",
                  action="count", default=0,
                  help="Print more verbose messages for each additional verbose level.")
parser.add_option("-d", "--dependency", dest="dependency_file",
                  #default="simple.svg",
                  metavar="FILE", 
                  type="string",
                  help="Print a dependency graph of the pipeline that would be executed "
                        "to FILE, but do not execute it.")
parser.add_option("-F", "--dependency_graph_format", dest="dependency_graph_format",
                  metavar="FORMAT", 
                  type="string",
                  default = 'svg',
                  help="format of dependency graph file. Can be 'ps' (PostScript), "+
                  "'svg' 'svgz' (Structured Vector Graphics), " +
                  "'png' 'gif' (bitmap  graphics) etc ")
parser.add_option("-n", "--just_print", dest="just_print",
                    action="store_true", default=False,
                    help="Print a description of the jobs that would be executed, "
                        "but do not execute them.")
parser.add_option("-M", "--minimal_rebuild_mode", dest="minimal_rebuild_mode",
                    action="store_true", default=False,
                    help="Rebuild a minimum of tasks necessary for the target. "
                    "Ignore upstream out of date tasks if intervening tasks are fine.")
parser.add_option("-K", "--no_key_legend_in_graph", dest="no_key_legend_in_graph",
                    action="store_true", default=False,
                    help="Do not print out legend and key for dependency graph.")
parser.add_option("-H", "--draw_graph_horizontally", dest="draw_horizontally",
                    action="store_true", default=False,
                    help="Draw horizontal dependency graph.")

parameters = [  
                ]







#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import io
import re
import operator
import sys,os
from collections import defaultdict
import random

sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Main logic


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





# get help string
f =io.StringIO()
parser.print_help(f)
helpstr = f.getvalue()
(options, remaining_args) = parser.parse_args()


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
@files(None, "a")
def task_1 (i, o):
    for f in o:
        open(f, 'w')

@transform(task_1, regex("b"), "task_2.output")
def task_2 (i, o):
    for f in o:
        open(f, 'w')

import unittest

class Test_task_mkdir(unittest.TestCase):

    def setUp (self):
        """
        """
        pass
        
    def tearDown (self):
        """
        """
        for d in ['a']:
            fullpath = os.path.join(exe_path, d)
            os.unlink(fullpath)


    def test_no_re_match (self):
        class t_save_to_str_logger:
            """
            Everything to stderr
            """
            def __init__ (self):
                self.info_str = ""
                self.warning_str = ""
                self.debug_str = ""
            def info (self, message):
                self.info_str += message
            def warning (self, message):
                self.warning_str += message
            def debug (self, message):
                self.debug_str += message

        save_to_str_logger = t_save_to_str_logger()
        pipeline_run([task_2], options.forced_tasks, multiprocess = options.jobs,
                            logger = save_to_str_logger,
                            gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                            verbose = 1)

        self.assert_("no files names matched" in save_to_str_logger.warning_str)
        print("\n    Warning printed out correctly", file=sys.stderr)
        

if __name__ == '__main__':
    if options.just_print:
        pipeline_printout(sys.stdout, options.target_tasks, options.forced_tasks,
                            verbose = options.verbose,
                            gnu_make_maximal_rebuild_mode = not options.minimal_rebuild_mode)

    elif options.dependency_file:
        pipeline_printout_graph (     open(options.dependency_file, "w"),
                             options.dependency_graph_format,
                             options.target_tasks,
                             options.forced_tasks,
                             draw_vertically = not options.draw_horizontally,
                             gnu_make_maximal_rebuild_mode  = not options.minimal_rebuild_mode,
                             no_key_legend  = options.no_key_legend_in_graph)
    else:
        sys.argv= sys.argv[0:1]
        unittest.main()        

