import json
import tempfile


class SimpleSimon:
    """SimpleSimon provides the mechanism necessary to execute LSST test
    notebooks under a CI framework.
    """

    def __init__(self, test_definition_json="./notebooks_to_test.json",
                 workdir=None):
        if workdir:
            self.workdir = workdir
        else:

        self.load_test_definitions(test_definition_json)

    def load_test_definitions(self, test_definition_json):
        self.test_definition_json = test_definition_json
        with open(self.test_definition_json, "r") as f:
            self.test_definition = json.load(f)

    def write_wf_inputs(self, workdir):
