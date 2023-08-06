import os
import sys

from franklab_mstaggedcuration.p_add_curation_tags import add_curation_tags
from franklab_mstaggedcuration.p_merge_burst_parents import merge_burst_parents
from pyms.mlpy import ProcessorManager

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PM = ProcessorManager()

PM.registerProcessor(add_curation_tags)
PM.registerProcessor(merge_burst_parents)

if not PM.run(sys.argv):
    exit(-1)
