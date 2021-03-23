import pytest, os
from .. import ScriptSamplingTorsion

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
forcefield_dir = os.path.join(cur_dir, '../forcefield/amber14')

class TestScriptSamplingTorsion:
    def setup(self):
        self.script = ScriptSamplingTorsion(
            save_dir=os.path.join(cur_dir, 'output'), 
            forcefield_file=os.path.join(forcefield_dir, 'nonbonded.xml'),
            pdb_file=os.path.join(cur_dir, 'data/testPDBManipulator.pdb'),
            model_name='alpha helix validation', cuda_id=0
        )

    def teardown(self):
        self.script = None

    def test_attributes(self):
        pass

    def test_exceptions(self):
        pass

    def test_writeFile(self):
        self.script.writeFile()