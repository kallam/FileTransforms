# FileTransforms

This project started as a few basic Python functions to replace some very old Excel VBA macros that were used to reformatted client files. The original iteration had a lot of hard-coded header values, but this package can be used to generate a wide variety of outputs with relative ease.

### Converting Excel Workbooks

This package originally included a function that would automatically convert Excel files to CSVs automatically, but it was removed because it was kind of hacky and might not have been reliably invoked. If `pandas` is available, this conversion can be done with `convert_xlsx_to_csv()` in `csv_utils.py`. 

### Warning
Some functions in the BaseTransform class had to be heavily modified to not rely upon hard-coded header values, but they have not been thoroughly tested yet. The original code was developed over several years and had to accommodate a wide variety of wild input formats, so more major refactoring of BaseTransform is to be expected.
