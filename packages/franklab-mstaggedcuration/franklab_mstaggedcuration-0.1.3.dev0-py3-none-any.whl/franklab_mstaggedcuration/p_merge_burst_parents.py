import json
from logging import getLogger

import numpy as np

from pyms.mlpy import readmda, writemda64

processor_name = 'pyms.merge_burst_parents'
processor_version = '0.11'

logger = getLogger(__name__)


def merge_burst_parents(*, firings, metrics, firings_out):
    """
    Identify clusters labeled as merge parents in the metrics file, perform
    the merge, and save the new firings.mda

    Based on p_create_label_map / apply_label_map by JFM and JC

    Parameters
    ----------
    firings : str
        Input file path of input firings mda file
    metrics : str
        Input file path of metrics json file to be used for generating the
        merge map
    firings_out : str
        Output file path of the updated firings, post-merge.


    """

    merge_map = []
    firings = readmda(firings)

    # Load json
    with open(metrics) as metrics_json:
        metrics_data = json.load(metrics_json)

    # Iterate through all clusters and identify clusters to merge
    for cluster in metrics_data['clusters']:

        # Check if burst parent exists
        if cluster['metrics']['bursting_parent']:
            merge_map.append(
                [cluster['metrics']['bursting_parent'], cluster['label']])
        else:
            # otherwise, map to itself!
            merge_map.append([cluster['label'], cluster['label']])

    merge_map = np.reshape(merge_map, (-1, 2))
    # Assure input is sorted
    merge_map = merge_map[np.argsort(merge_map[:, 0])]
    logger.debug(merge_map)

    # Propagate merge pairs to lowest label number
    for idx, label in enumerate(merge_map[:, 1]):
        logger.debug(label)
        merge_map[np.where(merge_map[:, 0] == label)[0],
                  0] = merge_map[idx, 0]  # Input should be sorted

    # Apply label map
    logger.debug(range(merge_map.shape[0]))
    for merge_pair in range(merge_map.shape[0]):
        logger.debug(merge_pair)
        firings[2, np.where(firings[2, :] == merge_map[merge_pair, 1])[
            0]] = merge_map[merge_pair, 0]

    # Write remapped firings
    return writemda64(firings, firings_out)


merge_burst_parents.name = processor_name
merge_burst_parents.version = processor_version
merge_burst_parents.author = 'AKGillespie'
