### Reverse Engineering x86 Processor Microcode
~~Arithmetic Logic Unit (ALU)算术逻辑单元~~

~~ISA:指令集~~

~~COTS:现有商用~~

~~IDU:  Instruction Decode Unit指令解码单元~~

~~sequencer: 序列器~~

~~micro和macro不要弄错了。。。~~

~~链接：[]()     [链接文本](链接地址)~~

|标题|标题|标题|
|:---|:---:|---:|
|居左测试文本|居中测试文本|居右测试文本|
|居左测试文本1|居中测试文本2|居右测试文本3|

$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a}. $$

$$
x \href{why-equal.html}{=} y^2 + 1
$$

这是一个脚注的例子[^1]

[^1]: 这里是脚注

<u>下划线文本</u>
<p align="left">居左文本</p>
<p align="center">微码更新文件格式</p>
<p align="right">居右文本</p>

<font face="微软雅黑" color="red" size="6">字体及字体颜色和大小</font>
<font color="#0000ff">字体颜色</font>

``` java
// 注意java前面有空格
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
}
```
# 摘要

微码是物理层上的抽象层一个CPU的组件，并以最通用的方式存在今天的CPU。 除了促进复杂和庞大的指令集，它还提供更新机制这允许CPU在不需要的情况下就地修补任何特殊的硬件。 虽然众所周知CPU定期更新这个机制，很少知道它的内部工作原理微码和更新机制是专有的，并没有通过分析。

在本文中，我们对微代码语义进行逆向向工程以及其更新机制的内在作用COTS CPU以AMD的K8和K10微架构为例。 此外，我们证明如何开发自定义微码更新。 我们描述微代码语义并且另外呈现一组显示所提供的可能性的微程序通过这项技术。 为此，我们的微程序范围从CPU辅助仪器到微码木马甚至可以从网络浏览器中访问并启用远程代码执行和加密实现攻击。

## 1. 介绍


与复杂的软件系统类似，bugs虚拟地存在于任何商业中央处理器（CPU）并可能对系统安全造成严重后果，例如特权升级[22,36]或密码泄漏键[11]。

勘误表从嵌入到通用处理器列出不正确的行为伴随的解决方法来保护程序执行[4,29]。这些解决方法包含说明对于开发人员如何绕过这些错误或者例如借助于重新编译[40]或二进制来减轻重新翻译[26]。但是，这些临时解决方案不适合需要硬件修改的复杂设计错误[48]。专用硬件单元以防止错误是不完美的[36,49]，并涉及不可忽视的硬件成本[8]。

臭名昭着的奔腾fdiv错误[62]显示了对现场更新的明确经济需求部署后才能关闭有缺陷的部件并修补错误的行为。请注意现代处理器的实施涉及数百万行HDL代码[55]和功能正确性的验证对于这样的处理器仍然是一个未解决的问题[4,29]。

自20世纪70年代以来，x86处理器制造商已经拥有使用微码将复杂指令解码为一系列为了提高效率，简化了微指令和诊断[43]。 从高级角度来看，微码是用户可见的（CISC）指令集体系结构（ISA）和（RISC）范例[54]。 虽然微码最初是在只读内存中实现,厂商推出了更新机制,借助于一个补丁（RAM）。

一旦发现错误的CPU行为，制造商通过加载BIOS / UEFI或操作系统boot时 , 发布微码更新。 由于修补程序RAM的易变性，微码更新不是持久的，必须重新加载每个处理器复位后。 在微码的基础上更新，处理器制造商获得了灵活性减少纠正错误行为的成本。 注意英特尔和AMD都部署了微码更新机制自1995年Pentium Pro（P6）[15,30]和K7英寸1999 [2,15]。 不幸的是，CPU供应商保留有关微码秘密的信息。 公开可用文件和专利仅仅陈述模糊的主张关于真实世界的微码实际上是怎样的，但提供一点其他见解。

__目标__。 在本文中，我们专注于x86中的微代码
CPU和我们的目标是回答以下研究
问题：
1. 什么是微代码，它在x86 CPU中的作用是什么？
2. 微码更新机制如何工作？
3. 专有微码编码如何能够被结构化的，半自动地逆向？
4. 现实世界的系统如何从微码获益以及如何利用恶意微代码攻击？

为了回答问题（1），我们强调这些信息关于微码分散在众多之中来源（通常只在专利中）。因此，这是一个重要部分我们的工作致力于总结这一先决条件构成回答更多的基础的知识深入的研究问题。此外，我们还处理缺点之前对x86微代码进行的安全分析，无法对微码进行逆向工程[6,15]。我们开发一种新技术来扭转设计编码从而回答问题（2）。后我们获得了对x86微码的详细了解对于几种CPU架构，我们可以解决问题（3）。因此，我们获得了对内部工作的理解的CPU更新，甚至可以生成我们自己的更新。特别是，我们专注于潜在的应用用于防御和攻击目的的微程序回答问题（4）。我们演示一个微程序可以用来测试二进制可执行文件CPU层和我们也介绍不同种类的通过微代码更新启用的后门程序.

我们的分析侧重于AMD K8 / K10微架构因为这些CPU不使用加密签名验证微码的完整性和真实性更新。 请注意，英特尔开始加密签名微代码更新于1995年[15]，AMD开始部署2011年强大的密码保护[15]。 我们假设底层的微码更新机制是类似的，但不能分析微码更新我们无法解密它们。

__贡献__。 总之，我们的主要贡献在本文如下：

**微码的深入分析**。 我们在现代CPU中提供一个深入了解微码的不透明作用。 我们特别提出了由供应商部署的微码更新修补CPU缺陷和错误的基本原则

**新颖的逆向技术**。 我们介绍第一个半自动反向工程技术来披露通用CPU的微码编码。 此外，我们描述设计和实现允许我们执行此操作逆向工程的框架。

**综合评估**。 我们在几种（COTS）AMD x86 CPU架构展示了我们的技术上。 我们提供微码编码格式和报告AMD x86 CPU内部新颖见解。 另外，我们介绍我们的基于消除实际CPU的硬件逆向工程的结果。

**概念验证微程序**。 我们是首先为x86提供完整的微程序的CPU的人。 我们精心挑选的微程序突出显示好处以及揭露的微码对真实世界的系统严重后果。

## 2. 相关工作

在介绍我们的分析过程的结果之前，我们简要回顾关于微编程的现有文献和相关主题。

**微程序**。 自从威尔克斯的开创性工作1951年[61]，在学术界和工业界的许多作品采用先进的微程序CPU设计。 与微程序相关的不同研究分支包括更高级别的微码语言，微码编译器和工具以及微码验证[5,43,56]。 其他主要研究领域关注微码的优化，如最小化执行时间和内存空间[32]。 另外还有几个微程序的应用的发展[27]如诊断[41]。

由于今天的x86 CPU的微代码还没有公开记录，有几个项目尝试了高等级来自英特尔和英特尔的CPU的安全分析AMD [6,15]。 即使这些项目报道了微码更新机制的运作，微代码更新头中的字段目的，以及其他元数据的存在，没有任何项目是能够对基本的微码编码进行逆向工程。因此，他们无法构建他们自己的微码更新。

我们想要注意的是Arrigo Triulzi在TROOPERS'15届和'16届介绍的, 他已经能够修补AMD K8微架构的微代码[59,60]。但是，他没有公布他的逆向工程细节或微码编码。

**不完美的CPU设计**。 虽然微码更新可以利用它来纠正一些错误的行为 , 但它不是万能的。 微码更新由于额外的条件检查能够降低性能; 他们的表现不能在所有情况下应用。 一个臭名昭著的例子是AMD的K7，微码更新机制本身有缺陷[2,15]。

为了解决这些缺点，已经提出了多种技术，包括动态指令流编辑[16]，现场可编程硬件[49]和硬件检查[8,36]。

__可信硬件__。 应用程序和安全性操作系统建立在底层安全之上硬件。 通常软件不是为了设计在不可信的或潜在的恶意硬件上执行[11,20,22]。 一旦硬件行为错误（无论是否故意），软件安全性机制可以失效。 众多安全处理器多年来一直如此被建议18,23,37]。商业上可用的例子包括技术如英特尔SGX [17]和AMD Pacifica [3]。然而，安全关键故障的周期性[4，29]和封闭源中的无文档调试功能[22]CPU架构挑战其可信度[17,45]。

## 3. 微码
如前所述，微码可以被看作是一种位于CPU的物理组件之上的抽象层。 在本节中，我们提供了在微代码幕后的机制的总体概述，并且还涵盖了有关的细节微码结构和更新机制。
### 3.1 概览
ISA为软件提供一致的界面定义指令，寄存器，存储器访问，I / O和中断处理。本文重点介绍x86 ISA，为避免混淆，我们将x86指令称为宏指令。微架构描述了制造商如何利用处理器设计技术以实现ISA，如高速缓存大小，流水线数量和单元模具的放置。从高尺度来看，处理器的内部组件可以细分为数据路径和控制单元。数据路径是功能单元的集合，例如寄存器，数据总线和算术逻辑单元（ALU）。控制单元包含程序计数器（PC），指令寄存器（IR）和指令解码单元（IDU）。控制单元依次运行各种功能单元驱动程序执行。更确切地说，是控制单元将每个宏指令转换为一个序列动作，即从寄存器检索数据，执行一定的ALU操作，然后写回结果。该控制信号是控制单元在一个时钟周期将其发送给不同的功能单元电脉冲的集合。功能单元产生状态信号指示它们的当前状态，如最后的ALU操作是否等于零，并将此反馈报告给控制单元。根据状态信号，控制单元可以改变程序执行，如如果零标志被设置,采取条件跳转。  
IDU在控制单元内起着核心作用并根据指令的内容生成控制信号寄存器。 我们区分两种IDU实施概念：（1）硬连线和（2）微编码。  
**硬连线解码单元**。 硬连线解码单元是通过时序逻辑实现，通常是有限状态机（FSM），以生成指令特定的一系列行动。 因此，它提供了在速度方面高效率。 但是，对于复杂的ISA而言,在设计和测试阶段, 则缺乏在FSM中的层次结构并且状态爆炸是具有挑战性的问题[50]。硬连线解码单元抑制了后期设计过程中灵活的变化，如在测试和验证期间纠正发生的错误，因为之前的阶段必须重复。 此外，后制造更改（纠正错误）需要修改硬件，这不是（经济上）可行的部署CPU [62]。 因此，硬连线解码单元适合于简单的ISA，如RISC处理器如SPARC和MIPS。  
**微码解码单元**。与硬连线相反方法，微编码的IDU不会生成即时控制信号，而是重新预先计算控制字。我们将一个控制字称为 ***微指令*** 。一个微指令包含一个时钟周期内所有的控制操作所有相关功能所需的控制信息。我们指的是多个微指令作为微码。微指令是从微码存储中提取，通常被实现为片上只读存储器（ROM）。操作码字节的当前解码的宏指令被利用生成一个起始地址，作为入口指向微码存储。每个微指令后跟一个序列字，其中包含到下一个微指令的地址。序列词也可能表明当前的宏指令的解码过程已经完成。应当指出的是一个宏指令通常会发出一个以上的微指令。微码序列器操作整个解码过程，连续选择微指令直到解码完成指示符出现。一些微架构支持的话, 微码定序器还处理条件微码的分支。预先计算并存储控制字引入了灵活性：更改，修补程序和添加新的说明可以转移到设计过程的后期阶段。该设计过程被简化，因为解码逻辑的改变只需要适应微码ROM的内容。然而不利的一面是，由于ROM取数据和多级解码逻辑,解码延迟将增加获取。微码IDU是商业CISC处理器的普遍选择。
### 3.2 微码结构
存在两种常见的原则来包装控制信号变成微指令。 这个选择很大地影响整个微架构和微码程序的大小。  
**水平编码**。 水平编码指定每个控制的微指令中的一位位置所有功能单元的信号。 为了逻辑和速度的简单起见，不再进行编码或压缩。这产生了广泛的控制字，即使是小的处理器。 历史上的IBM System / 360 M50处理器使用水平编码的85位微码控制字[53]。 水平微码的本质允许程序员明确地寻址几个功能单元同时发起并行计算，从而有效地使用这些单元。 一个缺点是由于长期的控制，微码ROM相当大。  
**垂直编码**。 垂直编码的微码可以看起来像一个常见的RISC指令集。 微指令通常包含一个操作码字段来选择要执行的操作和附加操作数字段。操作数字段的数量和大小可能在操作码和特定标志字段上有所不同。 位的位置可以有效地重用，因此微指令更加紧凑。 缺乏显式并行性可以简化微码程序的实施，但可能会影响性能。 一个编码操作可能会激活可能具有多种功能单位多个控制信号。 因此，需要另一个级别的解码。微码应该选择小心保持第二级解码开销最小的微码指令集和编码。

### 3.3 微码更新
微码微体系结构的一个特殊好处是在设计过程后期安装更改和错误修复的能力。这一优势可以进一步扩展：随着微码更新的推出，人们甚至可以在生产之后改变处理器行为 . 制造商利用微码补丁进行调试并修复处理器勘误。众所周知的fdiv bug [62]，在1994年影响英特尔奔腾处理器，让我们认识到与软件类似，复杂的硬件是也容易出错。这可以说是制造商推动微码更新的发展机制的动机。通常，由主板固件（例如BIOS）提供给CPU或UEFI）或boot开始的时候操作系统处理上传微码补丁。微码更新存储在低延迟，不稳定的片上RAM。因此，微码补丁并不持久。通常，微码补丁RAM与微码ROM相比尺寸相当有限。微码补丁包含许多微指令，序列词和触发器。触发器代表微码ROM修补RAM控制权转移的条件。在典型的用例中，微码片段拦截ROM的入口点宏观指令。如果需要的话在指令解码期间，微码的sequencer检查触发器并重定向控制到补丁RAM。一个典型的微码程序驻留在补丁RAM中，然后可以，例如，清理操作数中的输入数据并传输控制回到微码ROM。

## 4. 对微代码进行逆向工程
在本节中，我们将概述AMD K8和K10微架构家族，并描述我们的逆向工程方法。此外，我们提出我们的分析设置和框架，包括实现我们的概念和支持我们的逆向以半自动化的方式进行工程设计的原型。我们的分析主要涵盖AMD K8和K10处理器因为 - 尽我们所知，他们是市场上唯一缺乏强大的密码保护微码补丁的现代x86微架构。
### 4.1 AMD K8和K10
AMD从2003年到2008年和2008年到2013年发布了K8和K10处理器的新版本。 注意实际生产日期可能会有所不同，仅在2013年两款采用K10架构的低端CPU型号发行。 K9是K8的双核继任者，因此从我们的角度来看，差异是微不足道的。 家庭11h和12h是适用于移动平台和APU的K10微架构。  
所有这些微架构都包含一个微码IDU。 x86指令集被细分为直接路径和矢量路径的微指令。 前者主要表现为常用的，性能至关重要的宏指令（例如，算术和逻辑运算）由硬件解码成最多三个微指令。 后者不常见或复杂，并要求微码序列器进行解码微码ROM。 矢量路径的微指令可能会产生许多微指令。 在微码序列器的执行过程中，硬件解码会暂停。微代码由三个64位微指令和一个32位序列字构成[15]。 一个例子是来自2002的RISC86的AMD的专利描述了微指令集 [24]。序列字可以包含下一个三元组的地址或指示解码已经完成。
微代码ROM的长度是三元组的步长（The microcode ROM is addressed in steps whose length is a triad）。 一个例子是地址空间从0x0到0xbff包含3,072个三元组。该微码负责矢量路径宏指令的解码和异常处理，例如页面错误和除0错误。
### 4.2 更新机制
1999年发布的K7是AMD第一款支持微码更新的微架构。 更新机制并没有应用到12h家庭版。AMD保持着更新功能的秘密，直到2004年它暴露有三个K8微码补丁。补丁和更新机制被从BIOS更新中逆向[6]。 微码更新被存储在专有文件格式中，尽管有些信息已被逆向工程[6,15]。 从K10微架构开始，AMD公开发布微代码更新，这有利于Linux开源微码更新驱动程序。 我们对文件格式的看法是如表1所示，包括带校验和的标题和三元组数量，匹配注册字段和三元组。应该指出，处于道德考量, 微码更新中的三元组被我们没有进一步指明的算法混淆了.  


<table style="border-collapse:collapse;border-spacing:0;table-layout: fixed; width: 652px"><colgroup><col style="width: 73px"><col style="width: 104px"><col style="width: 98px"><col style="width: 113px"><col style="width: 264px"></colgroup><tr><th style="font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">B↓Bit→</th><th style="font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top" colspan="3">0               ------&gt;             31</th><th style="font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">32      -------&gt;          63</th></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">0</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top" colspan="3">date</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">patch ID</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">8</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">patch block</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">len</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">init</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">checksum</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">16</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top" colspan="3">northbridge ID </td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:inherit;text-align:center;vertical-align:top">southbridge ID</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">24</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">CPUID</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">magic value</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">32</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">match register 0</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">match register 1</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">40</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">match register 2</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">match register 3</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">48</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">match register 4</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">match register 5</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">54</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">match register 6</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">match register 7</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">64</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="4">triad 0, microinstruction 0</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">72</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="4">triad 0, microinstruction 1</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">80</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="4">triad 0, microinstruction 2</td></tr><tr><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">88</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top" colspan="3">triad 0, sequence word</td><td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;text-align:center;vertical-align:top">triad 1....</td></tr></table>

<p align="center"> 表1-微码更新文件格式 </p>

**微码更新程序**。 微码更新二进制文件以下列方式上传到CPU：首先，补丁必须放置在可访问的虚拟地址中空间。 然后64位虚拟地址必须是写入型号专用寄存器（MSR）0xc0010020。根据更新大小和微架构，发起更新的wrmsr指令可能会占用大约5,000个周期完成。 拒绝修补程序会导致一般保护错误。 内部, 更新机制会验证校验和，将三元组复制到微码的补丁RAM，并将匹配寄存器字段存储在实际匹配寄存器。 补丁内存映射到微码ROM的地址空间，由此补丁三元组直接跟随只读三元组。


关于我的故事:
1. 首先从我的名字说起。我叫钟敬。为什么叫这个名字呢？因为我的父母希望我xxx。我从小就生活在一个xxx的家庭。我被什么样的书籍环绕呢：《教会史》《戴德生传》《天路历程》《创世纪

---
关于公众号的开发