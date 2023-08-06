# winney
![pypi](https://img.shields.io/pypi/v/winney?color=blue) ![Codacy Badge](https://app.codacy.com/project/badge/Grade/6e1a16da7b3747e0b69440fd3826e8f3)

## Install
> pip install winney

## Tutorial
``` python
from winney import Winney

wy = Winney(host="www.baidu.com")
wy.register(method="get", uri="/", function_name="download")
wy.download()
t = wy.get_bytes()
print(t)
```
