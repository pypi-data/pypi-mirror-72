## Install package

```bash
pip install objmpp-classification
```

## Run package

### Run in Python script 

```python
from objmpp_classification import organoid_classification

organoid_classification.organoid_classification(path_data, path_images)
```

### Run with command line

```bash
objmpp-classification organoid /home/path_data /home/path_images
```

Show options:

```bash
objmpp-classification --help
```

## Install for development

If you want to develop on the package, this will update the package locally automatically when the files changes:

```bash
pip install -e .
```

