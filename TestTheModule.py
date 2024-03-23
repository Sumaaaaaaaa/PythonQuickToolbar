import quicktoolbar
from PIL import Image
import time

#quicktoolbar.root.ManageWindow_test()

def test():
    time.sleep(1)
    b = Image.open("Icons\\close.png")
    return b

quicktoolbar.createButton(
    name = "1",
    command=test,
    returnType=quicktoolbar.ReturnType.Auto,
    mode = quicktoolbar.Mode.Concurrent_Process
    )
quicktoolbar
quicktoolbar.run()
# 整理变量,创建测试文件，推进