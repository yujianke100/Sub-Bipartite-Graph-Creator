# Sub-Bipartite-Graph-Creator

## Guide

### This program need [Python3](https://www.python.org/downloads/). We recommend using [Anaconda](https://www.anaconda.com/products/individual#Downloads) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

### 1. Install environment.

pip install -r ./requirements.txt --user -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

### 2. Run the program.
python ./main.py

## 项目介绍(Chinses)
在当今的数据时代，图作为大数据的一个重要表示结构，得到了很大关注。比如，已经影响到我们日常生活各个方面的电子商务平台和社交网络，我们可以把它们建模为图。因此，随着图数据的日益增加，许多研究工作都致力于挖掘图数据结构中有价值的信息。通常情况下，有两类图。一类是简单图，其中的连接可以连接任何一对实体。另一类是多部图，其中顶点被分为不同的互不相干的类别，而边只存在于不同类别的顶点之间。

### 二部图
**定义：** 二部图有两个相互独立的不同类别的顶点集，边只存在于不同类别的顶点之间。

**举例：** 二部图在各个领域无处不在。例如，对于维基词典的用户和页面之间的关系，可以用边表示用户在页面上的编辑行为，构成一个二部图。在图中，可以有多个用户合作编辑同一个页面，也可以由一个用户编辑多个页面，但没有用户-用户或页面-页面的联系。下图展示了一个用户-页面关系的二部图的例子。Bob(s1)和Lisa(s3)合作编辑B(t1)页，而Jack(s2)、Lisa(s3)和Sam(s4)合作编辑A(t1)和C(t3)页。

<div align=center>
   <img src="./fig/intro.png" width="50%" alt="bipartite example"/><br/>
</div>

### 二部图分类应用举例

1. 不同语言的用户和他们编写的维基词典页面可以组成不同类别的二部图。对这些数据进一步挖掘，可以实现对用户的分类，或是得到不同母语的用户的使用习惯。

2. 二部图分类还可用于洗钱检测。考虑到亚马逊等电子商务平台中已知的洗钱周期之间的有向边，我们可以学习这些二部图的特征表示，并进一步利用它们来检测其他潜在的洗钱周期。

3. 在描述蛋白质结构时，将二级结构之间的相互作用表示为二部图是可行的。而且，二部图的分类可以作为寻找蛋白质中常见亚结构的基础。因此，在寻找具有类似结构的蛋白质时，二部图分类也可以发挥重要作用。

### 问题描述
1. 定义：利用某一时序二部图的时序信息，从二部图中截出大小符合要求的连通图，可获得一组同类型的二部图数据集。利用该思想，可生成获得多类型二部图数据集。

2. 输入：
    - 同一张图的节点出现的相对时间间隔（Gap）
    - 生成的图的最小节点数（Min）
    - 生成的图的最大节点数（Max）

3. 输出：

    - 多类型二部图数据集的邻接矩阵
    - 每个节点对应的图序号
    - 每个图的类别标签
    - 新数据集各信息的统计表格

4. 痛点：

    - 少有公开的多类型二部图数据集
    - 难以筛选、批量下载时序二部图数据集
    - 对原始数据集的处理过程较为繁杂
    - 根据时序信息进行分割，可能获得实验中无法使用的非连通图
    - 难以直接获取新生成的数据集的各类信息，如总点数、边数等

### 功能描述

1. 启动爬虫爬取数据集，并对这些数据集进行筛选，只保留时序二部图数据集。整个过程大约需要十五秒。

<div align=center>
<figure>
   <img src="./fig/prepare1.png" width="45%" alt="main"/>
   <img src="./fig/prepare2.png" width="45%" alt="main"/>
   <img src="./fig/prepare3.png" width="45%" alt="main"/>
   <img src="./fig/prepare4.png" width="45%" alt="main"/>
   <img src="./fig/main_ui.jpg" width="80%" alt="main"/>
</figure>
</div>
<br/>

2. 选择需要处理的数据。利用左上角“Deselect all”按钮可取消所有已选数据集。当前已选数据集的数量会显示在右下角“generate”按钮上。当选择的数据集数量大于等于2时，单击“generate”按钮会弹出选中的数据集的确认界面。按下确定后将会开始生成由这些数据集为原始数据的多类型二部图数据集。

<div align=center>
   <img src="./fig/data_check.jpeg" width="80%" alt="main"/><br/>
</div>
<br/>

3. 下载器下载并获取数据集源文件。
<div align=center>
   <img src="./fig/datas_tar.jpeg" width="80%" alt="main"/><br/>
</div>
<br/>

4. 解压器解压所需的数据集。

<div align=center>
   <img src="./fig/datas_origin.jpeg" width="80%" alt="main"/><br/>
</div>

5. 根据设定进行裁剪，获得各数据集的无时序连通子图，并将结果存于以当前时间命名的文件夹中。

<div align=center>
   <img src="./fig/raw.jpeg" width="80%" alt="main"/><br/>
</div>
<br/>

6. 数据统计，包括每种类型的二部图中的所有S节点数量，所有T节点数量，总边数以及该类型的图的总数。

<div align=center>
   <img src="./fig/data_exccel.jpeg" width="80%" alt="main"/><br/>
</div>
<br/>

### 功能优化：

1. 初始化时提供加载界面，并显示加载过程。

2. UI界面提供信息展示窗口，实时展示当前步骤，并在得到数据集时打印“伪统计表”。

<div align=center>
   <img src="./fig/data_ui.jpeg" width="80%" alt="main"/><br/>
</div>
<br/>

3. 利用QT5组件，界面可自适应拖拽，超参输入框可手动输入规定范围内的数值，也可鼠标滚轮调节。

4. 下载器于下载前会检查本地是否已有目标数据集，避免重复下载。

5. 数据表格保持对齐（name与data）

6. 表格中上下相邻的选项组用统一的底色区分

7. 生成一次数据集后，可直接回到主界面继续选择生成其他数据集，并提供“一键全不选”功能按钮。


