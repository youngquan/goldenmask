# Goldenmask

Goldenmask 直译为金色的罩子，是我对中国的一种武功“金钟罩”的“意译”😝。下面是百度百科里关于金钟罩的一个词条的介绍：

> 【金钟罩】为【少林四大神功】之一，是一代武学宗师【达摩】感到之前所创的【童子功】未臻于【圆满极境】而创出的第二套绝世武学。
>
> 【金钟罩】为一套内外兼修的无上神功，共分为十二关，每一关都比前一关练起来更为艰难，修练者若能闯过十二关，必定天下无敌!
>
> 【金钟罩】，号称天下防御第一，第十二关圆满之后，不仅【金刚不坏】，而且不怕【水火毒药】，更能【不眠不休】，功力【源源不尽】，堪称神奇至极。即使未达元满之境，金钟罩具备受攻击时反震的能力，越是关数高，同样的护体能力就越是强悍，对敌时，对敌方攻击的反震力也越强。

因为 Goldenmask 是一个用来对 Python 源码进行加密保护的工具，因此用了金钟罩这个名字。同时，还引入了一个选项叫做 layer，代表着武功的层数。目前，Goldenmask 只有两层功力，一层用的是 Python 自带的 **Compileall**，一层用的是 **Cython**。

Goldenmask 支持对 Python 文件、Python Wheel 包、Python 源码包以及 Python 模块文件夹进行加密，可以选择替换原始的文件，也可以将保护后的文件放到临时的编译文件夹 `__goldenmask__` 。此外，每一次保护，还会生成一个叫做 `.goldenmask` 的文件，里面记录了编译 Python 文件使用的 Python 版本和操作系统信息。

## 小试牛刀

```bash
$ pip install goldenmask
# 默认方法是使用 Compileall 编译为 pyc
$ goldenmask yourpythonfile.py
$ tree -a .
.
├── __goldenmask__
│   ├── .goldenmask
│   └── yourpythonfile.pyc
└── yourpythonfile.py

1 directory, 3 files
# 用生成的 pyc 文件替换原始的 py 文件
$ goldenmask -i yourpythonfile.py
$ tree -a .
.
├── .goldenmask
└── yourpythonfile.pyc

0 directories, 2 files
# 对包含 py 的模块文件夹进行加密
$ goldenmask yourpythonmoduledir
# 对 wheel 包进行加密
$ goldenmask goldenmask-0.1.2-py3-none-any.whl
# 对源码包进行加密
$ goldenmask goldenmask-0.1.2.tar.gz
```

## 安装方法

可以直接通过 pip 进行安装：

```bash
$ pip install -U goldenmask
```

当然更推荐使用虚拟环境，使用 Python 自带的 vevn 模块或者第三方的 vitrualenv：

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

## 使用方法

直接查看 goldenmask 的帮助文档即可。

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

## 滴水之恩

- [如何加密你的 Python 代码](https://prodesire.cn/2019/01/06/%E5%A6%82%E4%BD%95%E5%8A%A0%E5%AF%86%E4%BD%A0%E7%9A%84-Python-%E4%BB%A3%E7%A0%81-%E2%80%94%E2%80%94-%E8%AE%B0-PyCon-China-2018-%E7%9A%84%E4%B8%80%E6%AC%A1%E5%88%86%E4%BA%AB/)