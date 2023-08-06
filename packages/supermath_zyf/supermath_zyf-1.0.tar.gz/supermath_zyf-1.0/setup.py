#encoding=utf-8
from distutils.core import setup

setup(
    name='supermath_zyf',       #对外我们的模块名字
    version='1.0',          #版本号
    description='这是第一个对外发布的模块，测试',#描述
    author='zyf',            #作者
    author_email='',
    py_modules=['supermath.a1','supermath.a2']  #要发布的模块
)
