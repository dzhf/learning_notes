# 配置用户名、邮件信息

$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"


# 创建仓库

git init：初始化一个Git仓库，使用git init命令。

添加文件到Git仓库，分两步：

git add <file>：使用命令git add <file>，注意，可反复多次使用，添加多个文件；
git commit -m <message>：使用命令git commit -m <message>，完成。
    

# 查看仓库状态

git status：要随时掌握工作区的状态，使用git status命令。
git diff <file>：如果git status告诉你有文件被修改过，用git diff可以查看修改内容。
    

# 版本回退

git log：git log命令显示从最近到最远的提交日志，如果嫌输出信息太多，看得眼花缭乱的，可以试试加上--pretty=oneline参数；回退前，用git log可以查看提交历史，以便确定要回退到哪个版本

git reset --hard <version>：版本重置（包括现在回退到历史版本，以及历史回退到现在），version是能够表示具体版本的参数：HEAD(当前版本)、HEAD^(上一个版本)、HEAD^^(上上个版本)、HEAD~100(上100个版本)、commit id(git commit提交时对应的id，一般填前几位即可)
    
git reflog：用来记录你的每一次命令。例如，当你用git reset命令回退到历史版本version1后，再使用git log是查不到version1之后的commit记录的，也就查不到commit id用来将版本回退到version1之后的版本，此时可用git reflog来查看


# 工作区、版本库、暂存区

工作区：就是你在电脑里能看到的目录
版本库：工作区有一个隐藏目录.git，这个不算工作区，而是Git的版本库
暂存区：Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支master，以及指向master的一个指针叫HEAD。

git add：把文件从工作区添加到暂存区

git commit：提交更改，把暂存区的所有内容提交到当前分支

因为我们创建Git版本库时，Git自动为我们创建了唯一一个master分支，所以，现在，git commit就是往master分支上提交更改。

你可以简单理解为，需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

# 管理修改

为什么Git比其他版本控制系统设计得优秀，因为Git跟踪并管理的是修改，而非文件

为什么说Git管理的是修改，而不是文件呢？
实例：修改一个文件-->git add-->再修改该文件-->git commit，此时工作区和版本库里的文件不一致，版本库只存里第一次修改的结果，可以说明git add只是把文件的修改加入了暂存区而非文件，因此之后的修改除非再次git add，否则不会影响暂存区的版本，自然commit后的分支版本也不会收到影响

git diff HEAD -- <file>：可以查看工作区和版本库里面最新版本的区别，HEAD版本库最新版本，--代表工作区
    

# 撤销修改

场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时（只在工作区修改了，还没有git add），用命令git checkout -- file
    
    git checkout -- <file>：意思就是，把文件在工作区的修改全部撤销(其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还原”)，这里有两种情况：

        一种是<file>自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；

        一种是<file>已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。

    总之，就是让这个文件回到最近一次git commit或git add时的状态。git checkout -- file命令中的--很重要，没有--，就变成了“切换到另一个分支”的命令

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时（git add了，但没有commit），想丢弃修改，分两步，第一步用命令git reset HEAD <file>，就回到了场景1，第二步按场景1操作
    
    git reset HEAD <file>：可以把暂存区的修改撤销掉（unstage），重新放回工作区
    
场景3：已经提交了不合适的修改到版本库时（commit到本地版本库了），想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库

# 删除文件

本地工作区删除文件后，有2种选择操作
$ rm test.txt

选择1: 确实是需要删除该文件，那么执行git rm， git commit命令删除本地git库的文件
$ git rm test.txt
$ git commit -m "remove test.txt"

选择2: 误删除本地文件，可用git库最新版本恢复工作区被删除的文件
$ git checkout -- test.txt

# 远程仓库

Git的杀手级功能之一。找一台电脑充当服务器的角色，每天24小时开机，其他每个人都从这个“服务器”仓库克隆一份到自己的电脑上，并且各自把各自的提交推送到服务器仓库里，也从服务器仓库中拉取别人的提交。在这个世界上有个叫GitHub的神奇的网站，从名字就可以看出，这个网站就是提供Git仓库托管服务的

# 添加远程库

场景：本地已经有一个git库，需要将其放入到github远程库上进行维护





