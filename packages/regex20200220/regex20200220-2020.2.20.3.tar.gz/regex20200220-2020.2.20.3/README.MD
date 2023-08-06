
# regex20200220

- regex的20200220版本安装包

## 安装方式

- 下载此项目，进入项目根目录，执行如下命令安装：

~~~shell
python setup.py install
~~~

- 使用pip进行安装

~~~shell
pip install regex20200220
pip install -U git+https://github.com/q759729997/regex20200220.git@master  # 使用git安装
~~~

## Python包操作

- 当前用户根目录下创建`.pypirc`，配置pypi信息

~~~shell
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: name
password: xxxx
~~~

- 打包上传

~~~shell
python setup.py sdist bdist_wheel  # 打包
twine upload dist/*.whl --verbose  # 将打包后的whl上传
# Linux下文件改为：manylinux2010
~~~
