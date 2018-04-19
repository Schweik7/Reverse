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
6. 不安全的反序列化:



