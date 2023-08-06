# **MClipp docs**
MClipp is a easy library, where you can create big or small files.
You can do it using **Memory** class. 

## How does it working?

MClipp creates a file, that has custom file size. It multiplies a unit by custom **file size in bytes**.
As it known, the unit is a simple zero (0). 

## Create

Using "**create**" method you can create files width custom file size.

**Example:**
```python
from mclipp import *

clipper = Memory()
clipper.create('filename', 1024)
```
It creates a file, that has name **"filename"** and size 1024 bytes.

**Pattern:**
```python
from mclipp import *

clipper = Memory()
clipper.create(filename, byte)
```

... where **filename** is a filename and **byte** is a file_size.

## Delete

Using **delete** you can delete large or simple files without recovery.

**Example:**
```python
from mclipp import *

clipper = Memory()
clipper.delete(r'C:/Users/user/Desktop', 'filename')
```

Here you can delete file **"filename"**, that is in *"C:/Users/user/Desktop"*.
You can successful delete this file if it isn't in use.

**Pattern:**
```python
from mclipp import *

clipper = Memory()
clipper.delete(path, filename)
```


## Bonus: get **unit**

To get a unit you must to use property **unit**.

Example:
```python
from mclipp import *

clipper = Memory()
print(clipper.unit)
```

In current version the unit is **"0"**.
