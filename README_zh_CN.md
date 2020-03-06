# Goldenmask - 一键化保护你的 Python 源码

Goldenmask 直译为金色的罩子，灵感来自“金钟罩”的“翻译”。因为 Goldenmask 是一个用来对 Python 源码进行加密保护的工具，有点像金钟罩这种防御性武功的意思，因此用了金钟罩这个名字。同时，还引入了一个选项叫做 layer，对应着武功的层数，实际上则代表了不同层级的 Python 源码保护方法。当前，Goldenmask 只有两层功力，一层用的是 Python 自带的 **Compileall** 这个库，一层用的是 **Cython** 这个库，还需要继续修炼。

目前，Goldenmask 支持对 Python 文件、Python Wheel 包、Python 源码包以及 Python 模块文件夹进行加密，你可以选择替换原始的文件，也可以将加密保护后的文件放到临时的编译文件夹 `__goldenmask__`里去 。此外，每一次保护，还会生成一个叫做 `.goldenmask` 的文件，里面记录了编译 Python 文件使用的 Python 版本（ `sys.version`）和操作系统信息（`platform.uname()`）。因为考虑到源代码一般会通过 git 或者 svn 进行源码管理，不适合直接替换，因此保护 Python 源码的默认方式是会生成  `__goldenmask__` 这个文件夹的。此外，默认的保护方法是 Compileall，Cython 因为自身的限制，以及其实际的用途，有时加密效果并不是很理想。

## 小试牛刀

```bash
$ pip install goldenmask

# 默认方法是使用 Compileall 编译为 pyc
$ goldenmask yourpythonfile.py
All done! ✨ 🍰 ✨

$ tree -a .
.
├── __goldenmask__
│   ├── .goldenmask
│   └── yourpythonfile.pyc
└── yourpythonfile.py

1 directory, 3 files

# 用生成的 .so 文件替换原始的 py 文件
$ goldenmask -i -l 2 yourpythonfile.py
All done! ✨ 🍰 ✨

$ tree -a .
.
├── .goldenmask
└── yourpythonfile.so

0 directories, 2 files
```

## 安装方法

可以直接使用 pip 进行安装：

```bash
$ pip install -U goldenmask
```

当然更推荐使用虚拟环境，可以使用 Python 自带的 vevn 模块或者第三方的 virtualenv：

```bash
$ python -m venv env
# On Windows:
$ .\venv\Scripts\activate
# On Linux:
$ source env/bin/activate
$ pip install goldenmask --upgrade
```

因为 Goldenmask 依赖了 Cython 这个项目，因此你还需要确保你的机子上安装了合适的 C 代码编译器。你可以查看 Cython 的 [文档 ](https://cython.readthedocs.io/en/latest/src/quickstart/install.html)获得详细的安装方法。总的来说，根据不同的操作系统有以下三种方法：

1. 在 Linux 系统上，可以使用 `sudo apt-get install build-essential` 或者 `yum groupinstall "Development Tools"` 完成 C 编译器及其依赖的安装。
2. 在 Macosx 系统上，安装 XCode。
3. 在 Windows操作系统上，安装 MinGW 或者 Microsoft’s Visual C。

## 使用说明

Goldenmask 的帮助文档有详细的说明，可以直接使用 `help` 选项查看。

```bash
$ goldenmask --help
Usage: goldenmask [OPTIONS] [FILES_OR_DIRS]...

  Goldenmask is a tool to protect your python source code easily.

  FILES_OR_DIRS can be python files, wheel packages,source packages or dirs
  contain python files.

Options:
  -l, --layer <int>  Level of protection: 1 - compileall; 2 - cython.
  -i, --inplace      Whether compile python files in place.
  --no_smart         This will copy and compile everything you specified.
  --help             Show this message and exit.
```

对 wheel 包进行保护：

```bash
$ goldenmask goldenmask-0.2.1-py3-none-any.whl 
All done! ✨ 🍰 ✨
$ tree -a .
.
├── __goldenmask__
│   ├── .goldenmask
│   └── goldenmask-0.2.1-py3-none-any.whl
├── .goldenmask
└── goldenmask-0.2.1-py3-none-any.whl

1 directory, 4 files
```

对源码包进行加密：

```bash
$ goldenmask -l 2 --inplace goldenmask-0.1.2.tar.gz  
running build_ext
building 'goldenmask.cli' extension
...
All done! ✨ 🍰 ✨
$ tree -a .
.
├── .goldenmask
└── goldenmask-0.1.2.tar.gz
```

对包含 Python 代码的模块文件夹进行保护：

```bash
$ goldenmask pip-download/
All done! ✨ 🍰 ✨
```

## 参与其中

Goldenmask 的开发采用了 Python 项目管理工具 [**Poetry**](https://python-poetry.org/)，它是 [Sébastien Eustace](https://github.com/sdispater) 开发的一个用来管理 Python 打包和项目依赖的工具，使用起来非常方便，下面是参与 Goldenmask 这个项目的步骤：

1. 在 github 上 fork 项目 goldenmask
2. 克隆 fork 后的工程到本地
3. 安装 Poetry
4.   执行 `poetry install` 安装依赖，修改代码，并通过测试，便可以提交 Pull Requests

## 滴水之恩

- 感谢知乎用户 [prodesire](https://www.zhihu.com/people/prodesire) 的分享：[如何加密你的 Python 代码](https://prodesire.cn/2019/01/06/%E5%A6%82%E4%BD%95%E5%8A%A0%E5%AF%86%E4%BD%A0%E7%9A%84-Python-%E4%BB%A3%E7%A0%81-%E2%80%94%E2%80%94-%E8%AE%B0-PyCon-China-2018-%E7%9A%84%E4%B8%80%E6%AC%A1%E5%88%86%E4%BA%AB/)
- [黄玉郎创作武侠漫画《龙虎门》中武功](https://baike.baidu.com/item/%E9%87%91%E9%92%9F%E7%BD%A9/16964796#viewPageContent)