#!/usr/bin/env python3
import json
import os
notebooks_to_test = [['cat_access', 'LSST%20Catalog%20Access%20Tutorial', '120', 'medium'],
                     ['cluster', 'cluster', '30', 'medium'],
                     ['firefly', 'Firefly', '300', 'medium'],
                     ['sg', 'star_galaxy', '30', 'medium'],
                     ['soda', 'LSST%20SODA%20Tutorial', '30', 'medium'],
                     ['token', 'token-info', '30', 'medium'],
                     ['tutorial', '2017_tutorial', '1800', 'large'],
                     ['efd_access', 'efd_examples/Accessing_EFD_data', '120', 'medium'],
                     ['correlate_telemetry', 'efd_examples/Correlate%20Exposure%20and%20telemetry', '120', 'medium'],
                     ['efd_latency', 'efd_examples/EFD_latency_characterization', '120', 'medium'],
                     ['hich_cadence', 'efd_examples/High_cadence_EFD_data', '120', 'medium'],
                     ['wise_cc', 'wise_color_color', '120', 'medium'],
                     ['gaia_rv', 'experiments/DASK-notebooks/rv_gaia', '1800', 'large'],
                     ['gaia_all_sky', 'experiments/DASK-notebooks/gaia_all_sky', '1800', 'large'],]
image_name = os.environ['JUPYTER_IMAGE']
cmd = os.getenv('HOME') + "/scripts/runner.sh"
extracted=os.getenv('JUPYTERHUB_API_URL').split('/')[2]
ns=extracted.split('.')[1].split(':')[0]
prefix=extracted.split('.')[0][:-4]
wf_url="http://{}-wf-api.{}:8080".format(prefix,ns)
testname = image_name.split(':')[1]
shname = 'run_%s_wf.sh'%(testname)
with open(shname, 'w') as rfh:
    rfh.write("#!/usr/bin/env sh\n")
    for short_name, base_notebook_name, timeout, size in notebooks_to_test:
        fname = '%s_%s_wf.json'%(short_name, testname)
        with open(fname, 'w') as fh:
            d = { "type": "cmd",
                     "command": [ "{}".format(cmd), "{}".format(base_notebook_name), "{}".format(timeout)],
                     "image": "{}".format(image_name),
                     "size": "{}".format(size) }
            outstr = json.dumps(d)
            fh.write(outstr)
        rfh.write(f'workflow-api-client create -u {wf_url} -j {fname} > {fname[:-4]}log\n')
os.chmod(shname,0o755)
