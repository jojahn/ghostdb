# GhostDB

![Static Badge](https://img.shields.io/badge/lang-python-blue)

![GhostDB](assets/GhostDB.png)

> Simple SQL Engine using OpenDocument spreadsheets as storage

## Usage

```python
import ghostdb

# connect to a local file
con = ghostdb.connect("test.ods")

# execute SQL statements
con.execute("CREATE TABLE peoples (id, name, age)")
```