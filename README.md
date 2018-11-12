# FileTransforms

This project started as a few basic Python functions to replace some very old Excel VBA macros that were used to reformatted client files. The original iteration had a lot of hard-coded header values, but this package can be used to generate a wide variety of outputs with relative ease.


### Warning
Some functions in the BaseTransform class had to be heavily modified to not rely upon hard-coded header values, but they have not been thoroughly tested yet. The original code was developed over several years and had to accomodate a wide variety of wild input formats, so more major refactoring of BaseTransform is to be expected.
