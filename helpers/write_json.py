#!/usr/bin/env python3
import json
import urllib.parse

notebooks_to_test = [['cat_access', 'LSST Catalog Access Tutorial', '120', 'medium'],
                     ['cluster', 'cluster', '30', 'medium'],
                     ['firefly', 'Firefly', '300', 'medium'],
                     ['sg', 'star_galaxy', '30', 'medium'],
                     ['soda', 'LSST SODA Tutorial', '30', 'medium'],
                     ['token', 'token-info', '30', 'medium'],
                     ['tutorial', '2017_tutorial', '1800', 'large'],
                     ['efd_access', 'efd_examples/Accessing_EFD_data', '120', 'medium'],
                     ['correlate_telemetry',
                         'efd_examples/Correlate Exposure and telemetry', '120', 'medium'],
                     ['efd_latency', 'efd_examples/EFD_latency_characterization',
                         '120', 'medium'],
                     ['hich_cadence', 'efd_examples/High_cadence_EFD_data',
                         '120', 'medium'],
                     ['wise_cc', 'wise_color_color', '120', 'medium'],
                     ['gaia_rv', 'experiments/DASK-notebooks/rv_gaia', '1800', 'large'],
                     ['gaia_all_sky', 'experiments/DASK-notebooks/gaia_all_sky', '1800', 'large'], ]

nd = {}
for n in notebooks_to_test:
    name = n[0]
    nd[name] = {"name": name,
                "path": urllib.parse.quote(n[1]),
                "timeout": n[2],
                "size": n[3]}

with open("notebooks_to_test.json", "w") as f:
    json.dump(nd, f, indent=4)
