# 配置用户名、邮件信息

$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"

以上配置的用户名和邮箱将会出现在远程库上，例如github。每个库可以设置不同的值，只需要把--global参数去除


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

场景：本地已经有一个git库，需要将其放入到github远程库上进行维护，步骤如下：

    git init：本地初始化一个git库
    github上创建一个git库：注意创建时不要勾选生成readme.md文件，否则关联本地库和远程库时会报冲突
    git remote add origin git@github.com:dzhf/learning_notes.git：本地库关联到远程库origin
    git push -u origin master：把本地库的内容推送到远程，用git push命令，实际上是把当前分支master推送到远程。由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令
    
# 从远程库克隆

场景：github有个他人的库，需要将其库拷贝到个人计算机上并与之关联

    git clone <addr>：直接拷贝即可

# 创建与合并分支

因为创建、合并和删除分支非常快（只是修改指针指向），所以Git鼓励你使用分支完成某个任务，合并后再删掉分支，这和直接在master分支上工作效果是一样的，但过程更安全

    git branch：查看分支

    git branch <name>：创建分支

    git checkout <name>：切换分支

    git checkout -b <name>：创建+切换分支，-b应该是branch的缩写

    git merge <name>：合并某分支到当前分支，使用fast forward模式，这种模式下，删除分支后，会丢掉分支信息
    git merge --no-ff -m "merge with no-ff" <name>：不使用fast forward模式合并
    
    git log --graph --pretty=oneline --abbrev-commit：查看分支合并情况

    git branch -d <name>：删除已经被合并了的分支
    git branch -D <name>：删除还未被合并过的分支

# 解决冲突

场景：你在feature分支修改了文件test.log的第一行后commit到git库；然后切回master分支又对test.log的第一行进行了不同的修改；最后想要将feature分支合并到master时，会导致冲突

解决方案：

    手动对冲突文件进行处理，对冲突区域的内容进行选择
    对处理后的文件git add/commit，此时feature和master分支一致
    删除feature分支
    

# 分支管理策略

在实际开发中，我们应该按照几个基本原则进行分支管理：

    首先，master分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；

    干活都在dev分支上，也就是说，dev分支是不稳定的，到某个时候，比如1.0版本发布时，再把dev分支合并到master上，在master分支发布1.0版本；

    你和你的小伙伴们每个人都在dev分支上干活，每个人都有自己的分支，时不时地往dev分支上合并就可以了。
    
    debug分支一般取名为issue_debug_num, 新功能开发分支一般取名为feature_function
    
# bug分支

场景：你正在dev分支上开发，开发到一半时，发现一个bug需要紧急修复上线，此时你不可以在当前dev上修复bug，也不能在当前的dev上开分支，因为你当前的工作进行到一半，如果在dev上修复bug并合并到master上，那么会把开发到一半的代码合并进去，显然是不行的。你也不能直接切换到master分支上去开分支修复bug，因为你在dev分支上开发一半的所有工作内容都没有commit过就切到master分支上了（如果commit了，那是没问题到，但是我们的前提就是dev工作到一半，不想commit），这样会导致dev上未commit的开发工作内容在master上也会被看到（包括在dev开发一半过程中新建的文件，还没有git add的留存在工作区的文件，以及git add过的留存在暂存区的文件。需要注意的是，工作区和暂存区是所有分支公用的，未commit的话，即使切换其它分支，也能看到，只有commit后，才是分支私有的），这样肯定就没法在此基础上进行修复bug了。

解决方案：

    在切换到master分支之前，留在dev分支上做好切换分支前的准备：将在dev分支上新建的文件都进行git add，然后用git status确保没有未untracked的文件后，执行git stash命令，保存当前工作环境，再用git status查看工作区就是干净的了
    切换到master分支，并在master分支上开一个issue-bug_num分支，然后就可以在该分支下进行bug修复，修复后合并到master分支上并删除issue-bug_num分支
    切回dev分支，执行git stash list查看保存的工作环境，若只有一个，可以通过git stash pop(或者git stash apply + git stash drop)命令恢复之前保存的工作环境，继续dev未完成的开发工作即可；若有多个工作环境，可以用git stash apply <name>来指定恢复到某个工作环境




