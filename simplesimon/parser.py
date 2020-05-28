#!/usr/bin/env python3
import os
import pathlib

notebooks_to_test = [['cat_access', 'LSST%20Catalog%20Access%20Tutorial', '120', 'medium'],
                     ['cluster', 'cluster', '30', 'medium'],
                     ['firefly', 'Firefly', '300', 'medium'],
                     ['sg', 'star_galaxy', '30', 'medium'],
                     ['soda', 'LSST%20SODA%20Tutorial', '30', 'medium'],
                     ['token', 'token-info', '30', 'medium'],
                     ['tutorial', '2017_tutorial', '1800', 'large'],
                     ['efd_access', 'efd_examples/Accessing_EFD_data', '120', 'medium'],
                     ['correlate_telemetry',
                         'efd_examples/Correlate%20Exposure%20and%20telemetry', '120', 'medium'],
                     ['efd_latency', 'efd_examples/EFD_latency_characterization',
                         '120', 'medium'],
                     ['hich_cadence', 'efd_examples/High_cadence_EFD_data',
                         '120', 'medium'],
                     ['wise_cc', 'wise_color_color', '120', 'medium'],
                     ['gaia_rv', 'experiments/DASK-notebooks/rv_gaia', '1800', 'large'],
                     ['gaia_all_sky', 'experiments/DASK-notebooks/gaia_all_sky', '1800', 'large'], ]

image_name = os.environ['JUPYTER_IMAGE']
homedir = os.environ['HOME']
script = homedir + "/scripts/runner.sh"
path = pathlib.Path(script)
path.parent.mkdir(parents=True, exist_ok=True)
shname = 'run_%s_wf.sh' % (image_name.split(':')[1])
hub_fqdn = os.environ['JUPYTERHUB_API_URL'].split('/')[2].split(':')[0]
wf_namespace = hub_fqdn.split('.')[1]
wf_prefix = hub_fqdn.split('.')[0][:-4]  # Ends in "-hub"
with open(shname, 'w') as rfh:
    rfh.write('#!/usr/bin/env bash\n')
    for short_name, base_notebook_name, timeout, size in notebooks_to_test:
        fname = '%s_%s_wf.json' % (short_name, image_name.split(':')[1])
        with open(fname, 'w') as fh:
            outstr = f"""{{ "type": "cmd",
  "command": [ "{path}", "{base_notebook_name}", "{timeout}" ],
  "image": "{image_name}", "size": "{size}"
}}
"""
            fh.write(outstr)
        rfh.write(
            f'workflow-api-client create -u http://{wf_prefix}-wf-api.{wf_namespace}:8080/ -j {fname} > {fname[:-4]}log\n')
os.chmod(shname, 0o755)
