"""This module performs the actual parsing of the PDB file, though it does not
process the values that it extracts."""

import datetime
import math
from .pdbfile import PdbRecord, PdbFile

class PdbDataFile:
    """This object is essentially a list of values extracted from a PDB file. It
    functions as a data sheet.

    :param PdbFile pdb_file: The PDB file to extract information from."""

    def __init__(self):
        
        self._classification = None
        self._deposition_date = None
        self._pdb_code = None
        self._is_obsolete = False
        self._obsolete_date = None
        self._replacement_code = None
        self._title = None
        self._split_codes = []
        self._caveat = None
        self._compounds = []
        self._sources = []
        self._keywords = []
        self._experimental_techniques = []
        self._model_count = 1
        self._model_annotations = []
        self._authors = []
        self._revisions = []
        self._supercedes = []
        self._supercede_date = None
        self._journal = None
        self._remarks = []

        self._dbreferences = []
        self._sequence_differences = []
        self._residue_sequences = []
        self._modified_residues = []

        self._hets = []
        self._het_names = {}
        self._het_synonyms = {}
        self._formulae = {}

        self._helices = []
        self._sheets = []

        self._ss_bonds = []
        self._links = []
        self._cis_peptides = []

        self._sites = []

        self._crystal = None
        self._origix = None
        self._scale = None
        self._matrix = None

        self._models = [{"model_id": 1, "start_record": -1, "end_record": -1}]
        self._atoms = []
        self._anisou = []
        self._termini = []
        self._heteroatoms = []

        self._connections = []

        self._master = None


    def __repr__(self):
        return "<PdbDataFile (%s)>" % (self.pdb_code() if self.pdb_code() else "????")


    def classification(self, classification=None):
        if classification:
            if not isinstance(classification, str):
                raise TypeError(
                 "classification must be str, not '%s'" % str(classification)
                )
            if len(classification) > 40:
                raise ValueError(
                 "classification must be <40 chars, not '%s'" % classification
                )
            self._classification = classification
        else:
            return self._classification


    def deposition_date(self, deposition_date=None):
        if deposition_date:
            if not isinstance(deposition_date, datetime.date):
                raise TypeError(
                 "deposition_date must be date, not '%s'" % str(deposition_date)
                )
            self._deposition_date = deposition_date
        else:
            return self._deposition_date


    def pdb_code(self, pdb_code=None):
        if pdb_code:
            if not isinstance(pdb_code, str):
                raise TypeError(
                 "pdb_code must be str, not '%s'" % str(pdb_code)
                )
            if len(pdb_code) != 4:
                raise ValueError(
                 "pdb_code must be 4 chars, not '%s'" % pdb_code
                )
            self._pdb_code = pdb_code
        else:
            return self._pdb_code


    def is_obsolete(self, is_obsolete=None):
        if is_obsolete is not None:
            if not isinstance(is_obsolete, bool):
                raise TypeError(
                 "is_obsolete must be bool, not '%s'" % str(is_obsolete)
                )
            self._is_obsolete = is_obsolete
        else:
            return self._is_obsolete


    def obsolete_date(self, obsolete_date=None):
        if obsolete_date:
            if not isinstance(obsolete_date, datetime.date):
                raise TypeError(
                 "obsolete_date must be date, not '%s'" % str(obsolete_date)
                )
            self._obsolete_date = obsolete_date
        else:
            return self._obsolete_date


    def replacement_code(self, replacement_code=None):
        if replacement_code:
            if not isinstance(replacement_code, str):
                raise TypeError(
                 "replacement_code must be str, not '%s'" % str(replacement_code)
                )
            if len(replacement_code) != 4:
                raise ValueError(
                 "replacement_code must be 4 chars, not '%s'" % replacement_code
                )
            self._replacement_code = replacement_code
        else:
            return self._replacement_code


    def title(self, title=None):
        if title:
            if not isinstance(title, str):
                raise TypeError("title must be str, not '%s'" % str(title))
            self._title = title
        else:
            return self._title


    def split_codes(self):
        return self._split_codes


    def caveat(self, caveat=None):
        if caveat:
            if not isinstance(caveat, str):
                raise TypeError("caveat must be str, not '%s'" % str(caveat))
            self._caveat = caveat
        else:
            return self._caveat


    def compounds(self):
        return self._compounds


    def sources(self):
        return self._sources


    def keywords(self):
        return self._keywords


    def experimental_techniques(self):
        return self._experimental_techniques


    def model_count(self, model_count=None):
        if model_count:
            if not isinstance(model_count, int):
                raise TypeError(
                 "model_count must be int, not '%s'" % str(model_count)
                )
            self._model_count = model_count
        else:
            return self._model_count


    def model_annotations(self):
        return self._model_annotations


    def authors(self):
        return self._authors


    def revisions(self):
        return self._revisions


    def supercedes(self):
        return self._supercedes


    def supercede_date(self, supercede_date=None):
        if supercede_date:
            if not isinstance(supercede_date, datetime.date):
                raise TypeError(
                 "supercede_date must be date, not '%s'" % str(supercede_date)
                )
            self._supercede_date = supercede_date
        else:
            return self._supercede_date


    def journal(self, journal=None):
        if journal:
            if not isinstance(journal, dict):
                raise TypeError(
                 "journal must be dict, not '%s'" % str(journal)
                )
            self._journal = journal
        else:
            return self._journal


    def remarks(self):
        return self._remarks


    def get_remark_by_number(self, number):
        for remark in self.remarks():
            if remark["number"] == number:
                return remark


    def dbreferences(self):
        return self._dbreferences


    def sequence_differences(self):
        return self._sequence_differences


    def residue_sequences(self):
        return self._residue_sequences


    def modified_residues(self):
        return self._modified_residues


    def hets(self):
        return self._hets


    def het_names(self):
        return self._het_names


    def het_synonyms(self):
        return self._het_synonyms


    def formulae(self):
        return self._formulae


    def helices(self):
        return self._helices


    def sheets(self):
        return self._sheets


    def ss_bonds(self):
        return self._ss_bonds


    def links(self):
        return self._links


    def cis_peptides(self):
        return self._cis_peptides


    def sites(self):
        return self._sites


    def crystal_a(self, crystal_a=None):
        if crystal_a is not None:
            if not isinstance(crystal_a, float):
                raise TypeError(
                 "crystal_a must be float, not '%s'" % str(crystal_a)
                )
            self._crystal_a = crystal_a
        else:
            return self._crystal_a


    def crystal_b(self, crystal_b=None):
        if crystal_b is not None:
            if not isinstance(crystal_b, float):
                raise TypeError(
                 "crystal_b must be float, not '%s'" % str(crystal_b)
                )
            self._crystal_b = crystal_b
        else:
            return self._crystal_b


    def crystal_c(self, crystal_c=None):
        if crystal_c is not None:
            if not isinstance(crystal_c, float):
                raise TypeError(
                 "crystal_c must be float, not '%s'" % str(crystal_c)
                )
            self._crystal_c = crystal_c
        else:
            return self._crystal_c


    def crystal_alpha(self, crystal_alpha=None):
        if crystal_alpha is not None:
            if not isinstance(crystal_alpha, float):
                raise TypeError(
                 "crystal_alpha must be float, not '%s'" % str(crystal_alpha)
                )
            self._crystal_alpha = crystal_alpha
        else:
            return self._crystal_alpha


    def crystal_beta(self, crystal_beta=None):
        if crystal_beta is not None:
            if not isinstance(crystal_beta, float):
                raise TypeError(
                 "crystal_beta must be float, not '%s'" % str(crystal_beta)
                )
            self._crystal_beta = crystal_beta
        else:
            return self._crystal_beta


    def crystal_gamma(self, crystal_gamma=None):
        if crystal_gamma is not None:
            if not isinstance(crystal_gamma, float):
                raise TypeError(
                 "crystal_gamma must be float, not '%s'" % str(crystal_gamma)
                )
            self._crystal_gamma = crystal_gamma
        else:
            return self._crystal_gamma


    def crystal_s_group(self, crystal_s_group=None):
        if crystal_s_group is not None:
            if not isinstance(crystal_s_group, str):
                raise TypeError(
                 "crystal_s_group must be str, not '%s'" % str(crystal_s_group)
                )
            self._crystal_s_group = crystal_s_group
        else:
            return self._crystal_s_group


    def crystal_z(self, crystal_z=None):
        if crystal_z is not None:
            if not isinstance(crystal_z, int):
                raise TypeError(
                 "crystal_z must be int, not '%s'" % str(crystal_z)
                )
            self._crystal_z = crystal_z
        else:
            return self._crystal_z


    def origx_o11(self, origx_o11=None):
        if origx_o11 is not None:
            if not isinstance(origx_o11, float):
                raise TypeError("origx_o11 must be float, not '%s'" % str(origx_o11))
            self._origx_o11 = origx_o11
        else:
            return self._origx_o11


    def origx_o12(self, origx_o12=None):
        if origx_o12 is not None:
            if not isinstance(origx_o12, float):
                raise TypeError("origx_o12 must be float, not '%s'" % str(origx_o12))
            self._origx_o12 = origx_o12
        else:
            return self._origx_o12


    def origx_o13(self, origx_o13=None):
        if origx_o13 is not None:
            if not isinstance(origx_o13, float):
                raise TypeError("origx_o13 must be float, not '%s'" % str(origx_o13))
            self._origx_o13 = origx_o13
        else:
            return self._origx_o13


    def origx_t1(self, origx_t1=None):
        if origx_t1 is not None:
            if not isinstance(origx_t1, float):
                raise TypeError("origx_t1 must be float, not '%s'" % str(origx_t1))
            self._origx_t1 = origx_t1
        else:
            return self._origx_t1


    def origx_o21(self, origx_o21=None):
        if origx_o21 is not None:
            if not isinstance(origx_o21, float):
                raise TypeError("origx_o21 must be float, not '%s'" % str(origx_o21))
            self._origx_o21 = origx_o21
        else:
            return self._origx_o21


    def origx_o22(self, origx_o22=None):
        if origx_o22 is not None:
            if not isinstance(origx_o22, float):
                raise TypeError("origx_o22 must be float, not '%s'" % str(origx_o22))
            self._origx_o22 = origx_o22
        else:
            return self._origx_o22


    def origx_o23(self, origx_o23=None):
        if origx_o23 is not None:
            if not isinstance(origx_o23, float):
                raise TypeError("origx_o23 must be float, not '%s'" % str(origx_o23))
            self._origx_o23 = origx_o23
        else:
            return self._origx_o23


    def origx_t2(self, origx_t2=None):
        if origx_t2 is not None:
            if not isinstance(origx_t2, float):
                raise TypeError("origx_t2 must be float, not '%s'" % str(origx_t2))
            self._origx_t2 = origx_t2
        else:
            return self._origx_t2


    def origx_o31(self, origx_o31=None):
        if origx_o31 is not None:
            if not isinstance(origx_o31, float):
                raise TypeError("origx_o31 must be float, not '%s'" % str(origx_o31))
            self._origx_o31 = origx_o31
        else:
            return self._origx_o31


    def origx_o32(self, origx_o32=None):
        if origx_o32 is not None:
            if not isinstance(origx_o32, float):
                raise TypeError("origx_o32 must be float, not '%s'" % str(origx_o32))
            self._origx_o32 = origx_o32
        else:
            return self._origx_o32


    def origx_o33(self, origx_o33=None):
        if origx_o33 is not None:
            if not isinstance(origx_o33, float):
                raise TypeError("origx_o33 must be float, not '%s'" % str(origx_o33))
            self._origx_o33 = origx_o33
        else:
            return self._origx_o33


    def origx_t3(self, origx_t3=None):
        if origx_t3 is not None:
            if not isinstance(origx_t3, float):
                raise TypeError("origx_t3 must be float, not '%s'" % str(origx_t3))
            self._origx_t3 = origx_t3
        else:
            return self._origx_t3


    def scale_s11(self, scale_s11=None):
        if scale_s11 is not None:
            if not isinstance(scale_s11, float):
                raise TypeError("scale_s11 must be float, not '%s'" % str(scale_s11))
            self._scale_s11 = scale_s11
        else:
            return self._scale_s11


    def scale_s12(self, scale_s12=None):
        if scale_s12 is not None:
            if not isinstance(scale_s12, float):
                raise TypeError("scale_s12 must be float, not '%s'" % str(scale_s12))
            self._scale_s12 = scale_s12
        else:
            return self._scale_s12


    def scale_s13(self, scale_s13=None):
        if scale_s13 is not None:
            if not isinstance(scale_s13, float):
                raise TypeError("scale_s13 must be float, not '%s'" % str(scale_s13))
            self._scale_s13 = scale_s13
        else:
            return self._scale_s13


    def scale_u1(self, scale_u1=None):
        if scale_u1 is not None:
            if not isinstance(scale_u1, float):
                raise TypeError("scale_u1 must be float, not '%s'" % str(scale_u1))
            self._scale_u1 = scale_u1
        else:
            return self._scale_u1


    def scale_s21(self, scale_s21=None):
        if scale_s21 is not None:
            if not isinstance(scale_s21, float):
                raise TypeError("scale_s21 must be float, not '%s'" % str(scale_s21))
            self._scale_s21 = scale_s21
        else:
            return self._scale_s21


    def scale_s22(self, scale_s22=None):
        if scale_s22 is not None:
            if not isinstance(scale_s22, float):
                raise TypeError("scale_s22 must be float, not '%s'" % str(scale_s22))
            self._scale_s22 = scale_s22
        else:
            return self._scale_s22


    def scale_s23(self, scale_s23=None):
        if scale_s23 is not None:
            if not isinstance(scale_s23, float):
                raise TypeError("scale_s23 must be float, not '%s'" % str(scale_s23))
            self._scale_s23 = scale_s23
        else:
            return self._scale_s23


    def scale_u2(self, scale_u2=None):
        if scale_u2 is not None:
            if not isinstance(scale_u2, float):
                raise TypeError("scale_u2 must be float, not '%s'" % str(scale_u2))
            self._scale_u2 = scale_u2
        else:
            return self._scale_u2


    def scale_s31(self, scale_s31=None):
        if scale_s31 is not None:
            if not isinstance(scale_s31, float):
                raise TypeError("scale_s31 must be float, not '%s'" % str(scale_s31))
            self._scale_s31 = scale_s31
        else:
            return self._scale_s31


    def scale_s32(self, scale_s32=None):
        if scale_s32 is not None:
            if not isinstance(scale_s32, float):
                raise TypeError("scale_s32 must be float, not '%s'" % str(scale_s32))
            self._scale_s32 = scale_s32
        else:
            return self._scale_s32


    def scale_s33(self, scale_s33=None):
        if scale_s33 is not None:
            if not isinstance(scale_s33, float):
                raise TypeError("scale_s33 must be float, not '%s'" % str(scale_s33))
            self._scale_s33 = scale_s33
        else:
            return self._scale_s33


    def scale_u3(self, scale_u3=None):
        if scale_u3 is not None:
            if not isinstance(scale_u3, float):
                raise TypeError("scale_u3 must be float, not '%s'" % str(scale_u3))
            self._scale_u3 = scale_u3
        else:
            return self._scale_u3


    def matrix_serial_1(self, matrix_serial_1=None):
        if matrix_serial_1 is not None:
            if not isinstance(matrix_serial_1, int):
                raise TypeError("matrix_serial_1 must be int, not '%s'" % str(matrix_serial_1))
            self._matrix_serial_1 = matrix_serial_1
        else:
            return self._matrix_serial_1


    def matrix_m11(self, matrix_m11=None):
        if matrix_m11 is not None:
            if not isinstance(matrix_m11, float):
                raise TypeError("matrix_m11 must be float, not '%s'" % str(matrix_m11))
            self._matrix_m11 = matrix_m11
        else:
            return self._matrix_m11


    def matrix_m12(self, matrix_m12=None):
        if matrix_m12 is not None:
            if not isinstance(matrix_m12, float):
                raise TypeError("matrix_m12 must be float, not '%s'" % str(matrix_m12))
            self._matrix_m12 = matrix_m12
        else:
            return self._matrix_m12


    def matrix_m13(self, matrix_m13=None):
        if matrix_m13 is not None:
            if not isinstance(matrix_m13, float):
                raise TypeError("matrix_m13 must be float, not '%s'" % str(matrix_m13))
            self._matrix_m13 = matrix_m13
        else:
            return self._matrix_m13


    def matrix_v1(self, matrix_v1=None):
        if matrix_v1 is not None:
            if not isinstance(matrix_v1, float):
                raise TypeError("matrix_v1 must be float, not '%s'" % str(matrix_v1))
            self._matrix_v1 = matrix_v1
        else:
            return self._matrix_v1


    def matrix_i_given_1(self, matrix_i_given_1=None):
        if matrix_i_given_1 is not None:
            if not isinstance(matrix_i_given_1, bool):
                raise TypeError("matrix_i_given_1 must be bool, not '%s'" % str(matrix_i_given_1))
            self._matrix_i_given_1 = matrix_i_given_1
        else:
            return self._matrix_i_given_1


    def matrix_serial_2(self, matrix_serial_2=None):
        if matrix_serial_2 is not None:
            if not isinstance(matrix_serial_2, int):
                raise TypeError("matrix_serial_2 must be int, not '%s'" % str(matrix_serial_2))
            self._matrix_serial_2 = matrix_serial_2
        else:
            return self._matrix_serial_2


    def matrix_m21(self, matrix_m21=None):
        if matrix_m21 is not None:
            if not isinstance(matrix_m21, float):
                raise TypeError("matrix_m21 must be float, not '%s'" % str(matrix_m21))
            self._matrix_m21 = matrix_m21
        else:
            return self._matrix_m21


    def matrix_m22(self, matrix_m22=None):
        if matrix_m22 is not None:
            if not isinstance(matrix_m22, float):
                raise TypeError("matrix_m22 must be float, not '%s'" % str(matrix_m22))
            self._matrix_m22 = matrix_m22
        else:
            return self._matrix_m22


    def matrix_m23(self, matrix_m23=None):
        if matrix_m23 is not None:
            if not isinstance(matrix_m23, float):
                raise TypeError("matrix_m23 must be float, not '%s'" % str(matrix_m23))
            self._matrix_m23 = matrix_m23
        else:
            return self._matrix_m23


    def matrix_v2(self, matrix_v2=None):
        if matrix_v2 is not None:
            if not isinstance(matrix_v2, float):
                raise TypeError("matrix_v2 must be float, not '%s'" % str(matrix_v2))
            self._matrix_v2 = matrix_v2
        else:
            return self._matrix_v2


    def matrix_i_given_2(self, matrix_i_given_2=None):
        if matrix_i_given_2 is not None:
            if not isinstance(matrix_i_given_2, bool):
                raise TypeError("matrix_i_given_2 must be bool, not '%s'" % str(matrix_i_given_2))
            self._matrix_i_given_2 = matrix_i_given_2
        else:
            return self._matrix_i_given_2


    def matrix_serial_3(self, matrix_serial_3=None):
        if matrix_serial_3 is not None:
            if not isinstance(matrix_serial_3, int):
                raise TypeError("matrix_serial_3 must be int, not '%s'" % str(matrix_serial_3))
            self._matrix_serial_3 = matrix_serial_3
        else:
            return self._matrix_serial_3


    def matrix_m31(self, matrix_m31=None):
        if matrix_m31 is not None:
            if not isinstance(matrix_m31, float):
                raise TypeError("matrix_m31 must be float, not '%s'" % str(matrix_m31))
            self._matrix_m31 = matrix_m31
        else:
            return self._matrix_m31


    def matrix_m32(self, matrix_m32=None):
        if matrix_m32 is not None:
            if not isinstance(matrix_m32, float):
                raise TypeError("matrix_m32 must be float, not '%s'" % str(matrix_m32))
            self._matrix_m32 = matrix_m32
        else:
            return self._matrix_m32


    def matrix_m33(self, matrix_m33=None):
        if matrix_m33 is not None:
            if not isinstance(matrix_m33, float):
                raise TypeError("matrix_m33 must be float, not '%s'" % str(matrix_m33))
            self._matrix_m33 = matrix_m33
        else:
            return self._matrix_m33


    def matrix_v3(self, matrix_v3=None):
        if matrix_v3 is not None:
            if not isinstance(matrix_v3, float):
                raise TypeError("matrix_v3 must be float, not '%s'" % str(matrix_v3))
            self._matrix_v3 = matrix_v3
        else:
            return self._matrix_v3


    def matrix_i_given_3(self, matrix_i_given_3=None):
        if matrix_i_given_3 is not None:
            if not isinstance(matrix_i_given_3, bool):
                raise TypeError("matrix_i_given_3 must be bool, not '%s'" % str(matrix_i_given_3))
            self._matrix_i_given_3 = matrix_i_given_3
        else:
            return self._matrix_i_given_3


    def models(self):
        return self._models


    def atoms(self):
        return self._atoms


    def anisou(self):
        return self._anisou


    def termini(self):
        return self._termini


    def heteroatoms(self):
        return self._heteroatoms


    def connections(self):
        return self._connections


    def master(self, master=None):
        if master:
            if not isinstance(master, dict):
                raise TypeError(
                 "master must be dict, not '%s'" % str(master)
                )
            self._master = master
        else:
            return self._master
