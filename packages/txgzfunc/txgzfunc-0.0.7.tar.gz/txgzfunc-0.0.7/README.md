# txgz_func
工具方法集合

----------------------------------------------------------------------------------------------------------------------


- #### generation - 更新库

_Make sure you installed setuptools and wheel._

_Important: You must modify the version of the package in setup.py and delete folders (build, dist, egg-info)_

> python setup.py sdist bdist_wheel

- #### upload - 上传代码

Install twine before doing this
> twine upload dist/*

------------------------------------------------------------

- #### install - 安装
> pip install txgzfunc

- #### find the latest package of txgzfunc - 发现最新版本
> pip list --outdated

- #### upgrade - 升级到最新包
> pip install txgzfunc --upgrade