# FilesDSSAT

This was an exercise I made to extract data from an `excel`/`csv` file and organize it into a `.CST` file (DSSAT specific format). It can also extract data from a `.CST` file to a pandas dataframe.

## Overview

The source file contains field data from cassava experiments.

The `.CST` is where we inform real data for DSSAT. With a `.CST` we are able to compare this results against simulations.
That is used for model **calibration** and **validation** purposes.

## How to use

#### From `excel`/`csv` to `.CST`

```python
from main import sourceFile, targetFile

# Create the source instance
source = sourceFile('excelFileDirectory')

# Choose the variables to extract and the cultivar name
source.choose_variables(var_list = ["MASSA SECA DE RAÍZ", 
                                    "MASSA SECA DE FOLHAS", 
                                    "MASSA SECA DE CAULE", 
                                    "MASSA SECA TOTAL", 
                                    "IAF"],
                        cultivar = "EUCALIPTO")

# Create the target instance
target = targetFile(filename = "EBCZ1802.CST")  # the filename can be of a nonexistent one

# Set the var list with the same sequence as the 'source' above 
target.set_variables(var_list = ["HWAD", "LWAD", "SWAD", "TWAD", "LAID"])

# and Go!
source.write_file(target)
```
Of course, the source file must follow the same structure as the `exampleSource.xlsx`.

<br>

#### From `.CST` to `pd.DataFrame`

```python
# That time, must be an existent one
target = targetFile("yourFile.CST")

# and Go!
df = target.read_file()
```

## Further Reading

[Working with dynamic crop models](https://www.elsevier.com/books/working-with-dynamic-crop-models/wallach/978-0-12-811756-9)

[The DSSAT crop modeling ecosystem](https://shop.bdspublishing.com/store/bds/detail/product/3-190-9781786765185)
