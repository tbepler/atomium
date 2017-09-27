from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from atomium.files.pdbstring2pdbdict import *

class PdbStringToPdbDictTests(TestCase):

    @patch("atomium.files.pdbstring2pdbdict.pdb_string_to_lines")
    @patch("atomium.files.pdbstring2pdbdict.extract_header")
    @patch("atomium.files.pdbstring2pdbdict.extract_structure")
    def test_can_convert_pdb_string_to_dict(self, mock_struc, mock_head, mock_lines):
        mock_lines.return_value = ["line1", "line2"]
        pdb_dict = pdb_string_to_pdb_dict("filestring")
        mock_lines.assert_called_with("filestring")
        mock_head.assert_called_with({}, ["line1", "line2"])
        mock_struc.assert_called_with({}, ["line1", "line2"])
        self.assertEqual(pdb_dict, {})



class StringToLinesTests(TestCase):

    def test_can_convert_filestring_to_lines(self):
        filestring = "line1\nline2"
        lines = pdb_string_to_lines(filestring)
        self.assertEqual(lines, ["line1".ljust(80), "line2".ljust(80)])


    def test_can_handle_windows_line_endings(self):
        filestring = "line1\r\nline2"
        lines = pdb_string_to_lines(filestring)
        self.assertEqual(lines, ["line1".ljust(80), "line2".ljust(80)])


    def test_can_remove_empty_lines(self):
        filestring = "line1\n\nline2\n"
        lines = pdb_string_to_lines(filestring)
        self.assertEqual(lines, ["line1".ljust(80), "line2".ljust(80)])



class HeaderExtractionTests(TestCase):

    def setUp(self):
        self.pdb_dict = {}
        self.lines = ["line1", "line2", "line3"]
        self.header_line = (
         "HEADER    UNKNOWN FUNCTION" + " " * 24 + "21-AUG-17   6AR7" + " " * 14
        )
        self.title_lines = ["TITLE     L1".ljust(80), "TITLE    2 L2".ljust(80)]


    @patch("atomium.files.pdbstring2pdbdict.get_line")
    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    @patch("atomium.files.pdbstring2pdbdict.merge_lines")
    def test_can_extract_header(self, mock_merge, mock_lines, mock_line):
        mock_line.return_value = self.header_line
        mock_lines.return_value = self.title_lines
        mock_merge.return_value = "MERGED TEXT"
        extract_header(self.pdb_dict, self.lines)
        mock_line.assert_called_with("HEADER", self.lines)
        mock_lines.assert_called_with("TITLE", self.lines)
        mock_merge.assert_called_with(self.title_lines, 10)
        self.assertEqual(
         self.pdb_dict["deposition_date"], datetime(2017, 8, 21).date()
        )
        self.assertEqual(self.pdb_dict["code"], "6AR7")
        self.assertEqual(self.pdb_dict["title"], "MERGED TEXT")


    @patch("atomium.files.pdbstring2pdbdict.get_line")
    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    @patch("atomium.files.pdbstring2pdbdict.merge_lines")
    def test_empty_header_extraction(self, mock_merge, mock_lines, mock_line):
        mock_line.return_value = "HEADER".ljust(80)
        mock_lines.return_value = self.title_lines
        mock_merge.return_value = "MERGED TEXT"
        extract_header(self.pdb_dict, self.lines)
        mock_line.assert_called_with("HEADER", self.lines)
        self.assertEqual(self.pdb_dict["deposition_date"], None)
        self.assertEqual(self.pdb_dict["code"], None)


    @patch("atomium.files.pdbstring2pdbdict.get_line")
    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    @patch("atomium.files.pdbstring2pdbdict.merge_lines")
    def test_missing_header_extraction(self, mock_merge, mock_lines, mock_line):
        mock_line.return_value = None
        mock_lines.return_value = self.title_lines
        mock_merge.return_value = "MERGED TEXT"
        extract_header(self.pdb_dict, self.lines)
        mock_line.assert_called_with("HEADER", self.lines)
        self.assertEqual(self.pdb_dict["deposition_date"], None)
        self.assertEqual(self.pdb_dict["code"], None)


    @patch("atomium.files.pdbstring2pdbdict.get_line")
    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    def test_missing_title_extraction(self, mock_lines, mock_line):
        mock_line.return_value = self.header_line
        mock_lines.return_value = []
        extract_header(self.pdb_dict, self.lines)
        mock_lines.assert_called_with("TITLE", self.lines)
        self.assertEqual(self.pdb_dict["title"], None)



class StructureExtractionTests(TestCase):

    def setUp(self):
        self.pdb_dict = {}
        self.lines = [
         "model1", "atom1", "hetam1", "model2", "atom2", "hetam2", "con1", "con2"
        ]


    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    @patch("atomium.files.pdbstring2pdbdict.extract_connections")
    @patch("atomium.files.pdbstring2pdbdict.lines_to_model")
    def test_can_extract_structure_one_model(self, mock_model, mock_con, mock_lines):
        mock_lines.side_effect = [
         [], ["atom1", "atom2"], ["hetatm1", "hetatm2"], ["con1", "con2"]
        ]
        mock_model.return_value = {"model": "1"}
        extract_structure(self.pdb_dict, self.lines)
        mock_lines.assert_any_call("MODEL", self.lines)
        mock_lines.assert_any_call("ATOM", self.lines)
        mock_lines.assert_any_call("HETATM", self.lines)
        mock_lines.assert_any_call("CONECT", self.lines)
        mock_model.assert_called_with(["atom1", "atom2"], ["hetatm1", "hetatm2"])
        mock_con.assert_called_with(self.pdb_dict, ["con1", "con2"])
        self.assertEqual(self.pdb_dict["models"], [{"model": "1"}])


    @patch("atomium.files.pdbstring2pdbdict.get_lines")
    @patch("atomium.files.pdbstring2pdbdict.extract_connections")
    @patch("atomium.files.pdbstring2pdbdict.lines_to_model")
    def test_can_extract_structure_multiple_models(self, mock_model, mock_con, mock_lines):
        mock_lines.side_effect = [
         [self.lines[0], self.lines[3]], [self.lines[1], self.lines[4]],
         [self.lines[2], self.lines[5]], [self.lines[6], self.lines[7]],
        ]
        mock_model.side_effect = [{"model": "1"}, {"model": "2"}]
        extract_structure(self.pdb_dict, self.lines)
        mock_lines.assert_any_call("MODEL", self.lines)
        mock_lines.assert_any_call("ATOM", self.lines)
        mock_lines.assert_any_call("HETATM", self.lines)
        mock_lines.assert_any_call("CONECT", self.lines)
        mock_model.assert_any_call([self.lines[1]], [self.lines[2]])
        mock_model.assert_any_call([self.lines[4]], [self.lines[5]])
        mock_con.assert_called_with(self.pdb_dict, self.lines[6:8])
        self.assertEqual(self.pdb_dict["models"], [{"model": "1"}, {"model": "2"}])



class LinesToModelTests(TestCase):

    @patch("atomium.files.pdbstring2pdbdict.atom_line_to_atom_dict")
    @patch("atomium.files.pdbstring2pdbdict.atoms_to_residues")
    @patch("atomium.files.pdbstring2pdbdict.atoms_to_chains")
    def test_can_convert_lines_to_model(self, mock_chain, mock_res, mock_dict):
        mock_dict.side_effect = [
         {"a": 1}, {"a": 2}, {"a": 3}, {"a": 4},
         {"h": 1}, {"h": 2}, {"h": 3}, {"h": 4}
        ]
        mock_res.return_value = [{"m": 1}, {"m": 2}]
        mock_chain.return_value = [{"c": 1}, {"c": 2}]
        model = lines_to_model(["a1", "a2", "a3", "a4"], ["h1", "h2", "h3", "h4"])
        for char in ["a", "h"]:
            for num in ["1", "2", "3", "4"]:
                mock_dict.assert_any_call(char + num)
        mock_res.assert_called_with([{"h": 1}, {"h": 2}, {"h": 3}, {"h": 4}])
        mock_chain.assert_called_with([{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}])
        self.assertEqual(model, {
         "molecules": [{"m": 1}, {"m": 2}], "chains": [{"c": 1}, {"c": 2}]
        })



class AtomLineToAtomDictTests(TestCase):

    def test_can_convert_empty_line_to_atom(self):
        atom = atom_line_to_atom_dict("ATOM".ljust(80))
        self.assertEqual(atom, {
         "atom_id": None, "atom_name": None,
         "alt_loc": None, "residue_name": None,
         "chain_id": "", "residue_id": None, "insert_code": "", "full_id": "",
         "x": None, "y": None, "z": None,
         "occupancy": 1, "temp_factor": None,
         "element": None, "charge": 0
        })


    def test_can_convert_full_line_to_atom(self):
        atom = atom_line_to_atom_dict(
         "ATOM    107  N1 AGLY B  13C     " +
         "12.681  37.302 -25.211 0.70  15.56           N2-"
        )
        self.assertEqual(atom, {
         "atom_id": 107, "atom_name": "N1",
         "alt_loc": "A", "residue_name": "GLY",
         "chain_id": "B", "residue_id": 13, "insert_code": "C", "full_id": "B13C",
         "x": 12.681, "y": 37.302, "z": -25.211,
         "occupancy": 0.7, "temp_factor": 15.56,
         "element": "N", "charge": -2
        })



class AtomsToResiduesTests(TestCase):

    def test_can_convert_heteroatoms_to_molecules(self):
        heteroatoms = [
         {"full_id": "A10", "residue_name": "GLY"},
         {"full_id": "A10", "residue_name": "GLY"},
         {"full_id": "B10", "residue_name": "VAL"},
         {"full_id": "B10", "residue_name": "VAL"},
         {"full_id": "B10", "residue_name": "VAL"},
        ]
        molecules = atoms_to_residues(heteroatoms)
        self.assertEqual(molecules, [{
         "id": "A10", "name": "GLY", "atoms": heteroatoms[:2]
        }, {
         "id": "B10", "name": "VAL", "atoms": heteroatoms[2:]
        }])



class AtomsToChainsTests(TestCase):

    @patch("atomium.files.pdbstring2pdbdict.atoms_to_residues")
    def test_can_convert_atoms_to_chains(self, mock_res):
        atoms = [
         {"full_id": "A10", "residue_name": "GLY", "chain_id": "A"},
         {"full_id": "A11", "residue_name": "PRO", "chain_id": "A"},
         {"full_id": "B10", "residue_name": "VAL", "chain_id": "B"},
         {"full_id": "B10", "residue_name": "VAL", "chain_id": "B"},
         {"full_id": "B11", "residue_name": "LYS", "chain_id": "B"},
        ]
        mock_res.side_effect = [[{"r": 1}, {"r": 2}], [{"r": 3}, {"r": 4}]]
        chains = atoms_to_chains(atoms)
        mock_res.assert_any_call(atoms[:2])
        mock_res.assert_any_call(atoms[2:])
        self.assertEqual(chains, [{
         "chain_id": "A", "residues": [{"r": 1}, {"r": 2}]
        }, {
         "chain_id": "B", "residues": [{"r": 3}, {"r": 4}]
        }])



class ConnectionExtractionTests(TestCase):

    def test_extract_connections(self):
        pdb_dict = {}
        conect_lines = [
         "CONECT 1179  746 1184 1195 1203".ljust(80),
         "CONECT 1179 1211 1222".ljust(80),
         "CONECT 1221  544 1017 1020 1022".ljust(80)
        ]
        extract_connections(pdb_dict, conect_lines)
        self.assertEqual(pdb_dict, {"connections": [
         {"atom": 1179, "bond_to": [746, 1184, 1195, 1203, 1211, 1222]},
         {"atom": 1221, "bond_to": [544, 1017, 1020, 1022]}
        ]})




class GetLineTests(TestCase):

    def setUp(self):
        self.lines = ["AAA   X", "AAA   Y", "BBBBBBX"]


    def test_can_get_line(self):
        self.assertEqual(get_line("BBBBBB", self.lines), "BBBBBBX")


    def test_can_get_stripped_line(self):
        self.assertEqual(get_line("AAA", self.lines), "AAA   X")


    def test_can_get_none(self):
        self.assertIsNone(get_line("AA", self.lines))



class GetLinesTests(TestCase):

    def setUp(self):
        self.lines = ["AAA   X", "AAA   Y", "BBBBBBX"]


    def test_can_get_lines(self):
        self.assertEqual(get_lines("BBBBBB", self.lines), ["BBBBBBX"])


    def test_can_get_stripped_lines(self):
        self.assertEqual(get_lines("AAA", self.lines), ["AAA   X", "AAA   Y"])


    def test_can_get_no_lines(self):
        self.assertEqual(get_lines("AA", self.lines), [])



class LineMergingTests(TestCase):

    def setUp(self):
        self.lines = ["0123456789 ", "abcdefghij ", "0123456789 "]
        self.punc_lines = ["0123, 456789 ", "abcd  efghij ", "0123; 456789 "]


    def test_can_merge_lines(self):
        self.assertEqual(
         merge_lines(self.lines, 5),
         "56789 fghij 56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8),
         "89 ij 89"
        )


    def test_can_vary_join(self):
        self.assertEqual(
         merge_lines(self.lines, 5, join=""),
         "56789fghij56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8, join="."),
         "89.ij.89"
        )