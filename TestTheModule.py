import quicktoolbar
from PIL import Image

#quicktoolbar.root.ManageWindow_test()

def test():
    b = Image.open("Icons\\close.png")
    return b

quicktoolbar.createButton(
    name = "1",
    command=test,
    returnType=quicktoolbar.ReturnType.Auto,
    mode = quicktoolbar.Mode.Api
    )
quicktoolbar
quicktoolbar.run()
# 整理变量,创建测试文件，推进
"""
TODO:
    -[] 测试returnType枚举值是否可用的isinstance方法是否能正常运行
    -[] 当照片传入的地址错误时，是否会正常报错
"""