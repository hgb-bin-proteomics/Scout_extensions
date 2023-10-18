# Scout Extensions

Extensions to use [Scout](https://github.com/diogobor/Scout) with other software.

## Requirements

Python 3.7+ and the following packages are required:
- Install [pandas](https://pandas.pydata.org/): `pip install pandas`
- Install [xlsxwriter](https://xlsxwriter.readthedocs.io/): `pip install xlsxwriter`

## Scout to [IMP-X-FDR](https://github.com/fstanek/imp-x-fdr) converter

The main purpose of this script is to convert Scout output files to MS Annika format - which are usable with the [IMP-X-FDR](https://github.com/fstanek/imp-x-fdr) tool. This way Scout can be benchmarked on synthetic peptide libraries.

```
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
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of the output file.
  -xl CROSSLINKER, --crosslinker CROSSLINKER
                        Name of the Crosslinker e.g. DSSO.
  -xlmod CROSSLINKER_MODIFICATION, --crosslinker-modification CROSSLINKER_MODIFICATION
                        Residue that the Crosslinker binds to e.g. K for DSSO.
  --version             show program's version number and exit
```

Example Usage:

```
python scoutToIMPXFDR.py my_scout_results.csv -o my_scout_results_converted -xl DSSO -xlmod K
```

## License

[MIT License](https://github.com/hgb-bin-proteomics/MaXLinker_extensions/blob/master/LICENSE)

## Contact

[micha.birklbauer@fh-hagenberg.at](mailto:micha.birklbauer@fh-hagenberg.at)
