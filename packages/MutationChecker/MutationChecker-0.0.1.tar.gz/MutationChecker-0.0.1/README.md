# Mutation_Checker

Python package for checking the distance of a mutation from an active center of a protein.

## Installation

Run the following to install:

```python
pip install MutationChecker
```

## Usage

Several function exists in this package, the main ones are

### GeneToUniprotMapper

This function takes the name of a gene and maps it into a Uniprot Reviewed ID. By default uses the human
specie. 

@ input - gene (str) Name of Gene
@ input - specie (str) Name of the Specie. Default: Human
@ output - Uniprot ID (str) - Uniprot ID Code

Example: Generate info for EIF2B5 gene

```python
from MutationChecker import GeneToUniprotMapper
GeneToPDBMapper("EIF2B5")
```

### GeneToPDBMapper

This function takes the name of a gene and maps it into a PDB ID. 
By default uses the human specie. 

@ input - gene (str) Name of Gene
@ input - specie (str) Name of the Specie. Default: Human
@ output - PDB ID (str) - PDB ID Code

Example: Generate PDB Code for EIF2B5 gene

```python
from MutationChecker import GeneToPDBMapper
GeneToPDBMapper("EIF2B5")
```

### PDBIDtoFile

This function takes a PDB Code and downloads the file into the working folder.
It accepts a list of PDB to download the first available. 

@ input - List of Strings - Code of PDBs
@ output - PDB ID (str) - Path of the downloaded file.

Example: Download 1UBQ

```python
from MutationChecker import PDBIDtoFile
PDBIDtoFile("1UBQ")
```

### ExtractPDBSequence

This function takes a PDB file and extracts the sequence of the structure.

@ input - PDB File path (str)
@ output - Fasta Sequence (str) - Sequence of the structure.

Example: Get sequence for 1UBQ file

```python
from MutationChecker import ExtractPDBSequence
ExtractPDBSequence(["./1UBQ"])
```

### GeneToFasta

This function takes the name of a gene, and extract its sequence from Uniprot.

@ input - gene (str) Name of Gene
@ input - specie (str) Name of the Specie. Default: Human
@ output - Uniprot Fasta (str)

Example: Generate Fasta for EIF2B5 gene

```python
from MutationChecker import GeneToFasta
GeneToFasta("EIF2B5")
```

### ObtainActiveCenterResidues

This function takes the Uniprot ID of a protein, and returns a list of
residue numbers that conforms the active site based on EMBL-EBI

@ input - gene (str) Name of Gene
@ output - List of Strings - Active Site residue numbers.

If the protein has not an active site mapped on EMBL-EBI it returns None.

Example: Get Active Site residues for LTA4H

```python
from MutationChecker import GeneToUniprotMapper, GeneToFasta
UniprotID = GeneToUniprotMapper("LTA4H")
ObtainActiveCenterResidues(UniprotID)
```

### CheckDistanceToActiveSite

This function takes a name of the Gene, and a residue number, and
computes the physical distance in amstrongs between the residue number and the
active site residues.

@ input - gene (str) Name of the gene
@ input - residue number (int) - Number of residue to check
@ output - List of tupples (Name of active site residue, number)

Example: Get distances to the Active site from ASN488 in LTA4H

```python
from MutationChecker import CheckDistanceToActiveSite
CheckDistanceToActiveSite("LTA4H")
```