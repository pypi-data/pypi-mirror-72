import os, sys
import requests
import warnings
import Bio
from Bio.PDB import PDBList, PDBParser
from Bio.Data.IUPACData import protein_letters_3to1
from Bio.pairwise2 import format_alignment
from Bio import pairwise2
import json

warnings.filterwarnings("ignore")

def GeneToUniprotMapper(gene_id, specie="HUMAN"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the Reviewed Entries Uniprot ID value. Returns \"\" if the identifier is not found or not has structure.
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - Uniprot Reviewed id (list)
    """

    response = requests.get("https://www.uniprot.org/uniprot/?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=id")
    first_identifier = response.content.decode('utf-8')
    if first_identifier == "":
        return ""
    else:
        return first_identifier.split("\n")[1].split(";")[0]

def GeneToPDBMapper(gene_id, specie="HUMAN"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the first PDB mapped in Uniprot. Returns \"\" if the identifier is not found or not has structure.
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - PDB id (str)
    """

    response = requests.get("https://www.uniprot.org/uniprot/?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=database(PDB)")
    first_identifier = response.content.decode('utf-8')
    if first_identifier == "":
        return ""
    else:
        identifiers = first_identifier.split("\n")[1].split(";")
        return identifiers

def PDBIDtoFile(pdb_id_list):   
    """
    This function takes a PDB ID list (Can be obtained with function GeneToPDBMapper) and downloads the PDB into the working directory. 
    @ input - pdb_id_list (list) 
    @ output - Path to PDB file. (str)
    """
    pdbl=PDBList()

    for identifier in pdb_id_list:
        filename = pdbl.retrieve_pdb_file(identifier, pdir=".", file_format="pdb")
        
        if os.path.isfile(filename):
            return filename
        else:
            continue
    print ("All PDB entries are obsoleted and cannot be downloaded.")
    return None

def ExtractPDBSequence(pdb_file):   
    
    """
    This function takes a path to a PDB file and extract its fasta. 
    @ input - pdb_file (str) : Path to PDB file
    @ output - fasta (str) : Fasta of the PDB file
    """

    def _residue_parser(res):   
        """
        Internal Helper function for the parsing of residues of the PDB file
        """
        if res.get_resname().title() == "Hoh":
            return ""
        try:
            return protein_letters_3to1[res.get_resname().title()]
        except :
            return "X"

    parser = PDBParser(PERMISSIVE=1)
    residues = parser.get_structure('X', pdb_file).get_residues()
    resid_1_letter = map(lambda res: _residue_parser(res) , residues)

    return "".join(resid_1_letter)

def GeneToFasta(gene_id, specie="Human"):   
    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the Fasta sequence stored in Uniprot. Returns \"\" if the identifier is not found or not has structure.
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - Fasta string (str)
    """
    response = requests.get("https://www.uniprot.org/uniprot/?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=sequence")
    str_response = response.content.decode('utf-8')
    if str_response != "":
        sequence = str_response.split("\n")[1]
        return sequence
    else:
        return ""

def ObtainActiveCenterResidues(uniprot_id): 

    """
    This function takes an Uniprot ID (str) and returns a list of residue numbers of the active site.
    @ input - uniprot_id (str)
    @ output - ActiveSiteResidues (list)
    """

    response = requests.get("https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?entries.proteins.sequences.uniprot_ids=" + uniprot_id)
    json_data = json.loads(response.text)
    if json_data['results'] == []:
        return None
    return list(map( lambda residue: residue['residue_chains'][0]['resid'], json_data['results'][0]['residues']))

def MapUniprotToPDB(uniprot_sequence, pdb_sequence, res_mut): 

    """
    This function takes the sequence of uniprot, the sequence of PDB and a list of residue numbers of uniprot, and check if these residue have structure in the PDB file
    @ input - uniprot_sequence (str) - Uniprot Fasta sequence
    @ input - pdb_sequence (str) - PDB Fasta Sequence
    @ input - res_mut_num_list - List of residues of Uniprot Sequence
    @ output - list - List of residues with structure in PDB Sequence. If "-" means, no structure.
    """

    PDB_residues = list()
    alignments = pairwise2.align.globalms(uniprot_sequence, pdb_sequence, 2, -1, -5, -.1)

    if isinstance(res_mut, int):
        res_mut = [res_mut]
    
    for mutation in res_mut:
        if alignments[0].seqB[int(mutation)-1] != "-":
            subsequence = alignments[0].seqB[:int(mutation)]
            GAPnum = subsequence.count("-")
            PDBresidue = int(mutation) - int(GAPnum)
            PDB_residues.append(int(PDBresidue))
        else:
            continue
    
    return PDB_residues

def CheckDistances(res_id_1, ActiveSiteResidues, pdb_file):
    """
    This function takes the number of a residue inside a PDB file, the number of ActiveSiteResidues in a PDB file, and a PDB file, and returns 
    the list of distances from res_id_1 to each of the Active Site Residues in Amstrongs.
    @ input - res_id_1 (int) - Residue number of the mutation
    @ input - ActiveSiteResidues (list) - List of the active site residue numbers (List of int)
    @ input - pdb_file (str) - Path to PDB file

    @ output - List of floats: List of distances from res_id_1 to each of the ActiveSiteResidues in Amstrongs.
    """

    parser = PDBParser()
    structure = parser.get_structure("X", pdb_file)

    mutation_CA = list(structure.get_residues())[int(res_id_1)-1]['CA']

    if len(ActiveSiteResidues) == 0:
        print ("Active Site residues are not in the structure. Halting execution")
        return None
        
    return list(map(lambda res: (str(list(structure.get_residues())[int(res)-1].get_resname()) + str(int(res)) , round(float(list(structure.get_residues())[int(res_id_1)-1]['CA'] - list(structure.get_residues())[int(res)-1]['CA']), 2))       , ActiveSiteResidues))


def CheckDistanceToActiveSite(gene, res_number):
    """
    Main function of the package. It takes a GENE ID and a Residue Number and computes the physical distances between the residue to the active site.
    @ input - Gene (str) - Gene identifier
    @ input - res_number (int) - Number of the mutation in Uniprot
    @ output - List of floats: List of distances from res_number to each of the residues of the active site in Amstrongs.
    """

    # Obtain the Active Site residues for the gene.
    ActiveResidues = ObtainActiveCenterResidues(GeneToUniprotMapper(gene))

    if ActiveResidues is None: 
        return "The gene " + gene + " has not an active site mapped in EBI database."

    # Obtain the PDF file
    PDBfile = PDBIDtoFile(GeneToPDBMapper(gene))

    # Check if the active site residues have structure
    PDB_Residues = MapUniprotToPDB (GeneToFasta(gene), ExtractPDBSequence(PDBfile), [res_number] + ActiveResidues)
    
    Mutation = PDB_Residues[0]
    PDBActiveSite = PDB_Residues[1:]

    distances = CheckDistances(Mutation, PDBActiveSite, PDBfile)
    os.remove(PDBfile)
    return distances


if __name__ == "__main__":
    
    print (CheckDistanceToActiveSite(sys.argv[1], sys.argv[2]))