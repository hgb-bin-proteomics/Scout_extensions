#!/usr/bin/env python3

# Scout Result file to MS Annika Result file converter
# 2022 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

import argparse
import pandas as pd
import traceback as tb

__version = "1.0.0"
__date = "2023-10-17"

"""
DESCRIPTION:
A script to convert Scout *.csv result files to MS Annika format as
Microsoft Excel worksheets for usage with IMP-X-FDR (v1.1.0).

USAGE:
scoutToIMPXFDR.py f [f ...]
                    [-o OUTPUT]
                    [-xl CROSSLINKER]
                    [-xlmod CROSSLINKER_MODIFICATION]
                    [-h]
                    [--version]

positional arguments:
  f                     Scout result file to process, if second filename
                        is given it will be used as the output name!

optional arguments:
  -h, --help            show this help message and exit.
  -o OUTPUT, --output OUTPUT
                        Name of the output file.
  -xl CROSSLINKER, --crosslinker CROSSLINKER
                        Name of the Crosslinker e.g. DSSO.
  -xlmod CROSSLINKER_MODIFICATION, --crosslinker-modification CROSSLINKER_MODIFICATION
                        Residue that the Crosslinker binds to e.g. K for DSSO.
  --version             show program's version number and exit.
"""

#### MS Annika Result columns mapping ####
# Checked: (bool) TRUE | FALSE                             -> create with FALSE
# Crosslinker:  (string) e.g. DSSO                         -> create with crosslinker name
# Crosslink Type: (string selection) Intra | Inter         -> mapped "Link-Type"
# # CSMs: (int)                                            -> mapped "CSM count"
# # Proteins: (int)                                        -> create with zeros
# Sequence A: (string) e.g. [K]SSAAR                       -> mapped "Alpha peptide"
# Accession A: (string) e.g. P0A7X3                        -> mapped "Alpha protein mapping(s)"
# Position A: int                                          -> mapped "Alpha peptide position"
# Sequence B: (string)                                     -> ^
# Accession B: (string)                                    -> ^
# Position B: (int)                                        -> ^
# Protein Descriptions A: (string)                         -> mapped "Alpha protein mapping(s)"
# Protein Descriptions B: (string)                         -> ^
# Best CSM Score: (double)                                 -> mapped "Score"
# In protein A: (int)                                      -> create with zeros
# In protein B: (int)                                      -> create with zeros
# Decoy: (bool) TRUE | FALSE                               -> create with FALSE
# Modifications A: (string) e.g. K1(DSSO);M1(Oxidation)    -> create with xl name and modification
# Modifications B: (string)                                -> create with xl name and modification
# Confidence: (string selection) High | Medium | Low       -> create with High

# function that returns pandas dataframe in annika format
def create_annika_result(scout_filename: str, crosslinker: str = "DSSO", crosslinker_aa: str = "K") -> pd.DataFrame:

    if len(crosslinker_aa) != 1:
        raise Exception("Crosslinker modifications that affect more than one amino acid are not supported! Exiting...")

    # load file
    scout_df = pd.read_csv(scout_filename)
    nrows = scout_df.shape[0]

    # columns
    Checked = ["FALSE" for i in range(nrows)]
    Crosslinker = [crosslinker for i in range(nrows)]
    Crosslink_Type = scout_df["Link-Type"].apply(lambda x: "Intra" if "intra" in x.lower() else "Inter").tolist()
    CSMs = scout_df["CSM count"].tolist()
    Proteins = [0 for i in range(nrows)]
    Sequence_A = scout_df["Alpha peptide"].apply(lambda x: x.replace(" ", "")).tolist()
    Accession_A = scout_df["Alpha protein mapping(s)"].tolist()
    Position_A = scout_df["Alpha peptide position"].tolist()
    Sequence_B = scout_df["Beta peptide"].apply(lambda x: x.replace(" ", "")).tolist()
    Accession_B = scout_df["Beta protein mapping(s)"].tolist()
    Position_B = scout_df["Beta peptide position"].tolist()
    Protein_Descriptions_A = scout_df["Alpha protein mapping(s)"].tolist()
    Protein_Descriptions_B = scout_df["Beta protein mapping(s)"].tolist()
    Best_CSM_Score = scout_df["Score"].tolist()
    In_protein_A = [0 for i in range(nrows)]
    In_protein_B = [0 for i in range(nrows)]
    Decoy = ["FALSE" for i in range(nrows)]
    Modifications_A = scout_df["Alpha peptide position"].apply(lambda x: crosslinker_aa + str(x) + "(" + crosslinker + ")").tolist()
    Modifications_B = scout_df["Beta peptide position"].apply(lambda x: crosslinker_aa + str(x) + "(" + crosslinker + ")").tolist()
    Confidence = ["High" for i in range(nrows)]

    # create annika dataframe
    annika_df = pd.DataFrame({"Checked": Checked,
                              "Crosslinker": Crosslinker,
                              "Crosslink Type": Crosslink_Type,
                              "# CSMs": CSMs,
                              "# Proteins": Proteins,
                              "Sequence A": Sequence_A,
                              "Accession A": Accession_A,
                              "Position A": Position_A,
                              "Sequence B": Sequence_B,
                              "Accession B": Accession_B,
                              "Position B": Position_B,
                              "Protein Descriptions A": Protein_Descriptions_A,
                              "Protein Descriptions B": Protein_Descriptions_B,
                              "Best CSM Score": Best_CSM_Score,
                              "In protein A": In_protein_A,
                              "In protein B": In_protein_B,
                              "Decoy": Decoy,
                              "Modifications A": Modifications_A,
                              "Modifications B": Modifications_B,
                              "Confidence": Confidence})

    return annika_df

# read Scout result and write MS Annika result (in xlsx format)
def main() -> pd.DataFrame:

    parser = argparse.ArgumentParser()
    parser.add_argument(metavar = "f",
                        dest = "files",
                        help = "Scout result file to process, if second filename is given it will be used as the output name!",
                        type = str,
                        nargs = "+")
    parser.add_argument("-o", "--output",
                        dest = "output",
                        default = None,
                        help = "Name of the output file.",
                        type = str)
    parser.add_argument("-xl", "--crosslinker",
                        dest = "crosslinker",
                        default = "DSSO",
                        help = "Name of the Crosslinker e.g. DSSO.",
                        type = str)
    parser.add_argument("-xlmod", "--crosslinker-modification",
                        dest = "crosslinker_modification",
                        default = "K",
                        help = "Residue that the Crosslinker binds to e.g. K for DSSO.",
                        type = str)
    parser.add_argument("--version",
                        action = "version",
                        version = __version)
    args = parser.parse_args()

    input_file = args.files[0]
    output_file = args.files[0].split(".csv")[0] + ".xlsx"

    if len(args.files) > 1:
        output_file = args.files[1].split(".xlsx")[0] + ".xlsx"

    if args.output is not None:
        output_file = args.output.split(".xlsx")[0] + ".xlsx"

    scout_resultdf = create_annika_result(input_file, args.crosslinker, args.crosslinker_modification)
    scout_resultdf.to_excel(output_file, sheet_name = "Crosslinks", index = False, engine = "xlsxwriter")

    return scout_resultdf

if __name__ == "__main__":

    scout_df = main()
