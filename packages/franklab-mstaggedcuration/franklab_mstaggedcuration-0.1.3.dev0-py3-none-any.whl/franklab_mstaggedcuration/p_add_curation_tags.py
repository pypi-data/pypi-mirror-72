import json
import os

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

processor_name = 'pyms.add_curation_tags'
processor_version = '0.2'


def add_curation_tags(*, metrics, metrics_tagged,
                      firing_rate_thresh=0, isolation_thresh=0,
                      noise_overlap_thresh=1, peak_snr_thresh=0,
                      mv2file='', manual_only=False):
    """Add tags to the metrics file to reflect which clusters should be
    rejected based on curation criteria.

    Based on create/apply label map by J Chung and J Magland.

    Parameters
    ----------
    metrics : str
        Input file path of metrics json file to add tags.
    metrics_tagged : str
        Output file path of metrics json to be updated with cluster tags.
    firing_rate_thresh : float64, optional
        Firing rate must be above this
    isolation_thresh : float64, optional
        Isolation must be above this
    noise_overlap_thresh : float64, optional
        `noise_overlap_thresh` must be below this
    peak_snr_thresh : float64, optional
        peak snr must be above this
    mv2file : str, optional
        If tags have already been added, update new metrics file with them
    manual_only: bool
        If True, automated tags will be overwritten by the tags in mv2
        and if mv2 file is not provided, automated tags will not be generated.
    """
    # Load json
    with open(metrics) as metrics_json:
        metrics_data = json.load(metrics_json)

    if mv2file:
        with open(mv2file) as f:
            mv2 = json.load(f)

    # Iterate through all clusters
    for cluster in metrics_data['clusters']:

        # initialize empty tags key
        if 'tags' not in cluster:
            cluster['tags'] = []

        # if the mv2 was passed in, use those tags
        if mv2file:
            cluster_label = str(cluster['label'])
            cluster['tags'] = mv2['cluster_attributes'][
                cluster_label]['tags']

        if not manual_only:
            if (cluster['metrics']['firing_rate'] < firing_rate_thresh or
                cluster['metrics']['isolation'] < isolation_thresh or
                cluster['metrics']['noise_overlap'] > noise_overlap_thresh or
                    cluster['metrics']['peak_snr'] < peak_snr_thresh):

                # Add "rejected" tag to cluster metrics (if it isn't there)
                if 'mua' not in cluster['tags']:
                    cluster['tags'] += ['mua']
                # If the cluster was formerly tagged as accepted, remove that
                if 'accepted' in cluster['tags']:
                    cluster['tags'].remove('accepted')

    # Write out updated metrics json
    with open(metrics_tagged, 'w') as f:
        json.dump(metrics_data, f, sort_keys=True, indent=4)


add_curation_tags.name = processor_name
add_curation_tags.version = processor_version
add_curation_tags.author = 'AKGillespie, SJG'
