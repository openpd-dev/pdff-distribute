import pytest, os
import numpy as np
from .. import PDBManipulator

cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(cur_dir, '../template')

class TestPDBManipulator:
    def setup(self):
        self.manipulator = PDBManipulator(os.path.join(cur_dir, 'data/testPDBManipulator.pdb'), 'END')

    def teardown(self):
        self.manipulator = None

    def test_attributes(self):
        assert self.manipulator.patches['NTER']['ParentAtom'] == 'N'
        assert self.manipulator.atom_id[0] == 0
        assert self.manipulator.res_id[0] == 0

    def test_exceptions(self):
        with pytest.raises(KeyError):
            self.manipulator._getMass('Z')

        with pytest.raises(KeyError):
            self.manipulator.addPatch(0, 'NT')

    def test_sortAtomId(self):
        self.manipulator.sortAtomId()
        for i, atom_id in enumerate(self.manipulator.atom_id):
            assert atom_id == i

    def test_sortResId(self):
        cur_res = self.manipulator.res_id[0]
        cur_order = 0
        sorted_id = []
        for res_id in self.manipulator.res_id:
            if res_id == cur_res:
                sorted_id.append(cur_order)
            else:
                cur_res = res_id
                cur_order += 1
                sorted_id.append(cur_order)
        self.manipulator.sortResId()
        for i, j in zip(sorted_id, self.manipulator.res_id):
            assert i == j

    def test_writeNewFile(self):
        self.manipulator.writeNewFile(os.path.join(cur_dir, 'output/sorted.pdb'))

    def test_addPatch(self):
        self.manipulator.addPatch(0, 'NH3')
        self.manipulator.addPatch(1, 'COOH')
        self.manipulator.writeNewFile(os.path.join(cur_dir, 'output/patched.pdb'))

    def test_moveBy(self):
        origin_coord = np.array(self.manipulator.coord[1, :])
        self.manipulator.moveBy([5, 5, 5])
        cur_coord = self.manipulator.coord[1, :]
        self.manipulator.writeNewFile(os.path.join(cur_dir, 'output/moved.pdb'))
        for i, j in zip(origin_coord, cur_coord):
            assert i + 5 == j

    def test_getCenterOfMass(self):
        origin_com = np.array(self.manipulator.getCenterOfMass())
        self.manipulator.moveBy([5, 5, 5])
        cur_com = np.array(self.manipulator.getCenterOfMass())
        for i, j in zip(origin_com, cur_com):
            assert i + 5 == pytest.approx(j)

    def test_setChainNameByResId(self):
        self.manipulator.setChainNameByResId(0, 'B')
        assert self.manipulator.chain_name[0] == 'B'
        assert self.manipulator.line_ATOM[0].startswith('ATOM      0  N   LYS B')

    def test_setResIdByResId(self):
        self.manipulator.setResIdByResId(0, 30)
        assert self.manipulator.res_id[0] == 30
        assert self.manipulator.line_ATOM[0].startswith('ATOM      0  N   LYS A  30')

    def test_setAtomIdByAtomId(self):
        self.manipulator.setAtomIdByAtomId(0, 10)
        assert self.manipulator.atom_id[0] == 10
        assert self.manipulator.line_ATOM[0].startswith('ATOM     10')

    def test_catManipulator(self):
        manipulator = PDBManipulator(os.path.join(cur_dir, 'data/testPDBManipulator.pdb'), 'END')
        self.manipulator._catManipulator(manipulator)
        self.manipulator.writeNewFile(os.path.join(cur_dir, 'output/cat1.pdb'))

    def test_catManipulators(self):
        asn = PDBManipulator(os.path.join(template_dir, 'peptide/ASN.pdb'), end_label='ENDMDL')
        leu = PDBManipulator(os.path.join(template_dir, 'peptide/LEU.pdb'), end_label='ENDMDL')
        solution = PDBManipulator(os.path.join(template_dir, 'solution/nacl_0.15mol.pdb'), end_label='ENDMDL')

        leu.setResIdByResId(0, 1)
        leu.moveBy([4, 4, 4])
        asn.catManipulators(leu, solution)
        asn.writeNewFile(os.path.join(cur_dir, 'output/cat2.pdb'))
