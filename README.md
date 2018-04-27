# this is a rep for reverse:
+ -f to force push
+ angr
+ z3
+ unicorn
+ ODscript

### angr
1. 使用blank_state 进行函数的执行
2. 设定ebp,esp之后, 将符号化的输入,存放到ebp-xx中
3. 

### 这里将会存放 https://firmianay.gitbooks.io/ctf-all-in-one 的笔记.
#### linux
1. C-l  C-a  C-d
2. l : owner, group, others ;  r:4 , w:2 , x:1
3. 是little endian
4. 0: stdin , 1:stdout , 2:stderr
5. ulimit -c  unlimited  开启核心转储
6. 修改 /etc/profile ,PATH=... export PATH ; source 使其生效
7. LD_PRELOAD=/path/to/libc.so ./binary 设置优先加载的动态链接库
8. /proc/[pid] ; /proc/[pid]/maps 内存映射 ; /proc/[pid]/stack 内核调用栈 ; /proc/[pid]/fd 文件打开情况 ; /proc/[pid]/syscall  正在执行的系统调用
9. man stdlib.h; man printf
10. ldd hello.out 打印依赖库
#### web
1. 
    region{
    xss:<script>，定义客户端脚本
    <img src=>，规定显示图像的 URL
    <body background=>，规定文档背景图像URL
    <body onload=>，body标签的事件属性
    <input onfocus= autofocus>，form表单的事件属性
    <button onclick=>，击键的事件属性
    <link href=>，定义外部资源链接
    <object data=>，定义引用对象数据的 URL
    <svg onload=>，定义SVG资源引用
    }region

##### server
1. Nginx文件后缀解析特性:cgi.fix_pathinfo = 1 
2. IIS 短文件名爆破;6.0解析时忽略分号;存在1的CGI解析特性
3. 通过http头识别;目录;后缀;会话令牌 得到服务器指纹
##### OWASP TOP 10
1. 注入:sql;系统命令;表达式语言(java);服务端模板
2. 失效的身份认证;敏感数据泄露(github搜索口令或关键字);失效的访问控制(及用户权限跨越)
3. XML外部实体  
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><c>&xxe</c>
4. 安全配置错误(intitle:index of)
5. XSS:反射型;存储型;DOM型
    <script>alert(document.cookie)</script>
6. 不安全的反序列化;使用含有已知漏洞的组件

#### 逆向工程基础
##### C语言基础
1. 预编译->编译->汇编->链接
2. 预编译:处理#指令;删除注释;添加行号,文件标号
3. 编译: gcc -S
4. 汇编: gcc -c
5. 链接: 分配地址,空间;符号决议;重定向
6. gcc -save-temps hello.c 保存中间文件
7. gcc --verbose 输出详细工作流程
8. 在 libcdb.com 搜索泄露的函数地址
9. Signed和Unsigned 编译时指令不同:idiv,imul,sal,sar,movsx,jl,jg是有符号的; div,mul,shl,shr,movzx,jb,ja是无符号的
10. 格式化输出: %p void*型; %n 将成功输出的字符个数输入到变量中;%%字面值; n$ 指定第几个参数

##### X86 汇编
1. 未初始化的变量放在.bss段;未运行前不存在
2. readelf -l hello.out
3. LD_PRELOAD重载库函数
    gcc -shared -o hack.so hack.c
    LD_PRELOAD="./hack.so" ./a.out
4. 
##### 内存管理

#### 密码学基础
1. 初等数论
2. 近世代数
3. 流密码
4. 分组密码
5. 公钥密码
6. 哈希函数
7. 数字签名

#### Android
##### Dalvik指令集
1. 寄存器: V命名法,P命名法
2. 基本类型,引用类型(对象和数组)
    V  Void
    Z  Boolean
    B  Byte
    S  Short
    C  Char
    I  Int
    J  Long
    F  Float
    D  Double
    L  对象
    [  数组
3. Lpackage/name/ObjectName;->MethodName(III)Z  方法名、类型参数和返回值来描述一个方法
4. 一个字母表示4位;基本指令:
    nop 00
    move
    return
    const 数据定义
    monitor-enter vAA 获取锁
    monitor-exit  vAA 释放锁
    array
    instance
    chec-cast
    goto / switch / if
    cmp vAA,vBB,vCC
    invoke
    unop / binop



#### 工具
##### gdb
1. 原理是使用ptrace接管一个进程的执行
2. b xxx if <cond>
3. info reg/ threads / frame / proc / breakpoints list
4. clear/delete/disable/enable [b] [list...]  (dis  d)
5. tbreak 临时断点
6. watch [-l] <expr> 带参数则内存所指的值改变即停
7. step / reverse-step  (s)
8. next / reverse-next  (n)
9. return <expr> 直接以其值返回
10. finish   (fin)
11. until    (u)
12. continur (c)
13. print    (p)
14. x/nfu <addr>  检查内存 n:次数,f(x,d):格式,u:单位大小(b,h,w,g)
15. display <expr> 每次停止时打印 ;undisplay 编号 ; info display 看编号
16. disas <begin> <end>
17. help (h)
18. run [set args]
19. backtrace (bt)
#### peda
1. aslr
2. asmsearch "add esp,?" libc
3. assemble $pc  (NASM语法)
4. context code/registe/stack 展示
5. crashdump 
6. deactive (chdir sleep )跳过函数 
7. distance addr1 addr2
8. dumpargs 显示参数
9. dumpmem libc.mem libc 
10. dumprop binary "pop"
11. elfsymbol printf 获取符号信息 plt,got
12. gennop 500 "\x90"
13. goto 
14. help
15. hexdump $sp 64 显示堆栈
16. hexprint $sp 64 用字符串格式显示
17. jmpcall (eax/ esp libc) 搜索跳转的指令
18. loadmem
19. lookup 查找引用 lookup address stack libc ; lookup pointer stack ld-2
20. nearpc [addr] 反汇编附近的信息
21. nextcall / nextjmp 执行到 call / jmp
22. patch $esp 0xdeadbeef / "a long str"
23. pattern
    pattern_arg ; pattern_create ; pattern_env ; pattern_offset ; pattern_patch ; pattern_search ;
24. payload 使用ret2plt生成ROPpayload; payload copybytes target "/bin/sh"
25. procinfo
26. profile
27. readelf libc .text
28. refsearch "/bin/sh"搜索值的所有引用
29. ropgadget (libc)
30. ropsearch "pop eax" (libc)
31. session save/restore 保存会话
32. sgrep 索索字串
33. shellcode (x86/linux exec) 生成下载shellcode
34. skeleton argv exploit.py 生成脚本模板
35. snapshot save / restore 生成/读取快照!!
36. stepuntil (cmp / xor) 执行到指令
37. tracecall "cpy , printf " 追踪
38. traceinst "cmp,xor" 追踪指令
39. vmmap 获取段的虚拟映射地址范围
40. xormem [begin] [end] "key" 对内存进行异或
41. http://ropshell.com/peda/ python使用peda
42. GEF/pwndbg 查看堆

#### Radare2
1. r2 -c=H a.out 开启web视图
#### IDA插件
1. FLIRT 识别库函数
2. find crypt 寻找加密算法的常数
3. IDA signsrch 寻找算法
4. ponce 污点分析,符号执行
5. snowman 不知道和HexRay反编译哪个好
6. auto re 函数重命名,不知道好不好用
7. idaemu 模拟代码执行,不知道什么用
8. diaphora 补丁比对
9. keypatch  patch文件;像OD那样改
10. friend  哪里不会点哪里
11. simplifyGraph 简化幻术流程图
12. bincat 静态分析包
13. hexrayspytools alt+f8 建立结构;alt+f1 建立类
####
1. binwalk -Me firmware.bin 递归扫描文件
2. 

