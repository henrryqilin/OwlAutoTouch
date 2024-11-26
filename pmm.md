# Program Maintenance Manual(程序维护手册)

该手册用于解释项目原理以及项目的使用方法

## Crossing Index(交叉索引目录)
 00 - [Front Matter](#00)<br>
 01 - [快速开始](#02)<br>
 02 - [项目基本结构]<br>
 03 - 任务管理器
 
 10 - [模板匹配](#10)
 11 - OCR

<a name = '00'></a>

## Front Matter

### Index
 [Introduction](#00-00)
 [How To Use Index](#00-01)
 [Reference Projects](#00-03)
 [Effect Pages](#00-04)

<a name = '00-00'></a>

### Introduction

本手册是一个对本项目的简单介绍以及对实现形式(代码)的详细解析,当然也有可能是我不是很爱写注释

<a name = '00-01'></a>

### How To Use Index



<a name = '00-02'></a>

### Reference Project

<a name = '00-03'></a>

### Effect Pages

 有效性
 

<a name = '01'></a>

## 快速开始

<a name = '02'></a>

## 项目基本结构




<a name = '00'></a>

## 模板匹配

### Introduction

 模版匹配全部使用opencv-python实现,该模块截止目前(v0.5.1)有两个文件:<br>
 templat.py:模版匹配功能的主体,可以用self.temp来调用<br>
 button.py:temp模块的内部类,主要功能是通过temp模块传入的参数判断模版是否注册,是否只用检测按钮出现区域

### template.py(v0.5.1)
 
 template文件中共有1个类:Template
 
 #### Template

```
__init__(self,Config_Input):
```
 简单来看该函数分为上下两部分<br>
 上半部分是处理luncher传来的参数,这些会在[luncher.py](#luncher)部分说明<br>
 下半部分就是简单的变量初始化<br>
 其中:<br>
 self.templates(dict,key:(模板名称)(颜色模式),value:Matrix(模板图片))<br>
 用来存储部分最近读取的模板,目的是让在短时间内多次被匹配的模板可重复使用,<br>
 减少文件的读取次数,该字典长度大于10时会在调用工作函数开始时被清除<br>
 self.last_result(list,[True/False,[-1,-1]/[123,456]])<br>
 用来储存上次的识别结果,在函数外也可以通过self.temp.last_result获取上次识别结果

```
_match(self,Image,Template):
```
 该函数的目的是将模版匹配的核心功能与传参解析的功能解耦<br>
 该函数内部使用的全部都是opencv函数

```
_location_calculate(self,Result,Forward_Mode):
```
 该函数的设计目的与match函数类似,如果还是将这部分塞入主程序则会过于臃肿<br>
 该函数主要是解析_match的返回值<br>
 内部主要分三种情况<br>
 1.匹配置信度不满足设置要求,返回false<br>
 2.置信度满足但为全屏匹配(button返回模版未注册)<br>
 3.置信度满足,且button返回模版注册

```
get_xy(self,Template,Image = '',Colour_Mode = 1,Forward_Mode = 0):
```
 该函数是目前Templat的主要功能函数<br>
 第一部分功能是模板储存内容过多时删除<br>
 具体来讲就是模板名字加颜色代码最为key,模板本身最为value<br>
 可以参考上面初始化函数的介绍<br>
 第二部分是模板的导入目前简单分为注册模板导入和自由模板导入<br>
 其中注册模板为template文件夹及其子文件夹中出现并且在注册列表中有具体预期出现位置的模板<br>
 自由模板为矩阵类型的图片(从文件中使用类似于cv2方法读取的)<br>
 第三部分为图片的导入,目前基本分为四种情况<br>
 为空字符串:直接从上次截图返回颜色或灰度图<br>
 为绝对地址:直接读取<br>
 在img文件夹中:加后缀读取<br>
 非字符串:直接导入<br>
 **至此传入参数处理部分完成**<br>
 第四部分功能实现部分<br>
 大体上分成两个方向<br>
 如果button返回False则全屏识别<br>
 反之则需要先进行一次预期区域识别,如果出现则正常继续<br>
 若未出现,需要进行全屏识别,来判断预期区域是否有误<br>

### button.py

