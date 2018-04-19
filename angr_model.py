from angr import *
import logging
imoprt claripy
file=''
found_list=[]
avoid_list=[]
p=angr.factory(file,load_options={'auto_load_libs':False})

st=p.factory.blank_state(addr=0x401284)
st.regs.rbp=0xfffffffd80000000
st.regs.rsp=st.regs.rbp-0x1000
flag=claripy.BVS('flag',26*8)

def myhook(state):
    state.regs.rax=0
    pass
for i in flag.chop(8):  # 每8位看成一个整体
    st.add_constraints(i>=0x20)
    st.add_constraints(i<=0x7f)
st.memory.store(st.regs.ebp+0x100,flag)
p.hook(0x8888888 , USER_HOOK(myhook,length=5))
proj.hook(0x40130E,angr.SIM_PROCEDURES['libc']['strcmp']() , length=5)
sm=p.factory.simgr(st)
sm.explore(found=found_list , avoid=avoid_list )

found_state = sm.found[0].state
p1 = found_state.se.eval(flag,cast_to=str)
print(p1)

