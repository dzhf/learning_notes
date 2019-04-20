# vim搭建python开发环境

[TOC]

## 环境

* 操作系统：mac os 10.14.4
* vim版本：系统自带的8.0、以及个人brew安装的8.1
  * 系统自带8.0版本，默认支持系统自带的python2.7
  * 个人安装的8.1版本，支持个人安装的python3.7
* python版本：系统自动的2.7，以及个人brew安装的3.7



## 安装与环境验证

* 确认vim版本以及是否支持python扩展 

  `vim --version`

  若输出包含+python或+python3，则为支持python，例如本人输出如下，说明支持python3，而不支持系统自带的python：

  ![my vim support python](/Users/zhanghaifeng/learn/learning_notes/vim/img/img1.png)

* 在vim中查看python具体版本好，进一步确认vim支持python

  `vim`

  `: python3 import sys; print(sys.version)`

  依次输入以上命令，首先vim进入vim中，然后进入命令模式输入第二条命令，如vim支持python，则会输出对应的版本号，如下：

  ![img2](/Users/zhanghaifeng/learn/learning_notes/vim/img/img2.png)

  > **注意**
  >
  > 如果你的vim是+python，-python3情况，且系统安装了2个python版本（例如系统自带的python，和个人安装的python3），那以上第二条命令需要改成python import sys，此处需要进行对应，否则会报错: "E319: 抱歉，命令在此版本中不可用", 并且下文中提到的.vimrc文件的配置中，pip和pip3、python和python3都要进行区分，要明确你的vim支持哪个版本的python，用对版本相应的指令。



## 开发环境搭建

### 安装vundle

vundle是vim用来管理插件的一个工具，安装以后只需要在.vimrc文件中添加插件名称，然后进行vim通过执行命令VundleInstall即可安装插件，需要卸载插件只需要删除配置文件中对应的行，然后执行VundleClean即可。安装vundle命令如下：

`git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim`

`touch ~/.vimrc`

将以下内容黏贴进.vimrc文件中

```
set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)


" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
```

## 分割布局

有时我们需要在一个页面打开多个窗口页面，方便进行对比与切换编辑等，很多终端支持一个页面打开多个终端窗口，例如mac的iterm2，不过我们也可以通过vim自身的命令来布局多窗口

`:sv <filename>`  纵向分割，在原窗口上方新建vim窗口

`:vs <filename>` 横行分割，在原窗口左方新建vim窗口

打开了多个vim窗口后，窗口之间的切换可以通过将以下内容加入.vimrc内之后，利用ctrl+j/k/h/l进行上下左右切换

```
"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>
```

