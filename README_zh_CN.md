# Goldenmask

Goldenmask 直译为金色的罩子，是我对中国的一种武功“金钟罩”的“意译”。下面是百度百科里关于金钟罩的介绍：

> 【金钟罩】为【少林四大神功】之一，是一代武学宗师【达摩】感到之前所创的【童子功】未臻于【圆满极境】而创出的第二套绝世武学。
> 【金钟罩】为一套内外兼修的无上神功，共分为十二关，每一关都比前一关练起来更为艰难，修练者若能闯过十二关，必定天下无敌!
> 【金钟罩】，号称天下防御第一，第十二关圆满之后，不仅【金刚不坏】，而且不怕【水火毒药】，更能【不眠不休】，功力【源源不尽】，堪称神奇至极。即使未达元满之境，金钟罩具备受攻击时反震的能力，越是关数高，同样的护体能力就越是强悍，对敌时，对敌方攻击的反震力也越强。

因为 goldenmask 是一个用来对 Python 源码进行加密保护的工具，因此用了金钟罩这个名字。

## 安装

可以直接通过 pip 进行安装：

```bash
$ pip install -U goldenmask
```

因为 Goldenmask 依赖了 Cython 这个项目，因此你还需要确保你的机子上安装了一个正确的C代码编译器，你可以查看 Cython 的文档进行安装，也可以点击这里查看详细的安装方法。总的来说，根据不同的操作系统有以下三种方法：

1. 在 Linux 系统上，通过使用 `sudo apt-get install build-essential` 或者 `yum install ` 完成依赖的安装。
2. 在 Macosx 系统上，安装 XCode。
3. 在 Windows操作系统上，安装 MinGW 或者 Visual 。

## 使用

```bash
$ goldenmask file1.py
$ goldenmask dir1

$ goldenmask -l 2 file1.py
$ goldenmask -l 2 dir1

$ goldenmask --help
```

## 相关链接

- 详细文档