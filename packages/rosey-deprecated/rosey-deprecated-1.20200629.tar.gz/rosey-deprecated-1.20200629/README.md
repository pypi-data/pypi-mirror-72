# Rosey (Deprecated)

Quickly mark things are deprecated

```python
from rosey_deprecated import deprecated  # Decorate a function to raise an error
from rosey_deprecated import Deprecated  # Decorate a class or function to throw a warning


@deprecated
def funfunfunction():
    pass

@Deprecated('Please use BlahClass instead')
class MerpClass:
    pass
```
