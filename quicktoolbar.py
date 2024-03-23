"""
FIXME:
-[] 以`Mode.Concurrent_Thread`执行时会跳出一个奇怪的窗口 -> 延迟解决：因为内部逻辑复杂
-[] ReturnType.Image 下的图片会丢失背景通道，导致黑色的带透明图片变成全黑
    -[] 因为使用的是win32clipboard，OS和Linux暂时不支持
TODO:
-[] 消除按钮灰色效果
-[] 图片保存功能
"""

from enum import Enum, auto
import logging
import tkinter as tk
from tkinter import font as tk_font
from PIL import Image, ImageTk
import math
from pyperclip import copy
from io import BytesIO
import win32clipboard
from concurrent.futures import ThreadPoolExecutor


class Mode(Enum):
    Api = auto()
    Concurrent_Thread = auto()
    Concurrent_Process = auto()
    Async = auto()
    # 修改，暂未实装
    Api_Repeat = auto()
    Concurrent_Thread_Endless = auto()
    Concurrent_Process_Endless = auto()
    Async_Endless = auto()
    
class ReturnType(Enum):
    String = auto()
    Image = auto()
    Auto = auto()
    
    @property
    def instance(self):
        if self == ReturnType.String:
            return str
        elif self == ReturnType.Image:
            return Image.Image
        elif self == ReturnType.Auto:
            return type(None)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class NoCreationFunction(Exception):
    def __init__(self) -> None:
        super().__init__("Without any create function buttons, the window will not be generated.")


class QuickToolBar:
    # region 变量/错误
    # 窗口对象
    root = None  # 根窗口
    __manageWindow, __manageWindow_mainFrame = None, None  # 管理窗口
    
    # 窗口数据
    __window_height, __window_length = -1, -1  # 根窗口高度，长度 （位于基本数据变量设置）
    
    # 创建内容存储
    __root_content_dataset = dict()  # 创建内容数据集
    __manager_content_dataset = []  # 管理内容数据集
    executor = None # 线程池
    
    # 颜色设计
    __colors = {'bg': 'white', 'fg': 'black', 'bg2': "gray"}  # 颜色设计

    class __DuplicateButtonName(NameError):  # 命名重复错误
        def __init__(self, name):
            super().__init__(f"You created a button with a name that already exists \"{name}\", please check the name.")

    # endregion

    # 初始化
    def __init__(self):
        # 创建主屏幕
        self.root = tk.Tk()
        
        # 开启线程池
        self.__threading_init()
        # 把线程池关闭加入到关闭动作中
        self.root.protocol('WM_DELETE_WINDOW',self.__threading_close)
        
        # region 基本数据变量设置（如窗口宽度……）
        # 设置窗口的高度为屏幕分辨率较短的那一边的1/20，初始长度与高度相同
        screen_size = min(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.__window_height = int(screen_size / 20)
        # 将主窗口的长度设置为0
        self.__window_length = 0
        # endregion

        # 标准窗口创建：命名，将其设置为最上层，禁止改变窗口大小，移除标题栏，移动和关闭，置于屏幕中央位置
        self.__DefaultWindowSetting(self.root)
        # 设置窗口尺寸
        self.root.geometry(str(self.__window_length) + "x" + str(self.__window_height))
    
    # 多线程_线程池创建
    def __threading_init(self):
        logging.debug("Thread pool has been opened.")
        self.executor = ThreadPoolExecutor(max_workers=None)
    # 多线程_线程池关闭
    def __threading_close(self):
        logging.debug("Thread pool has been closed.")
        self.executor.shutdown(wait=False)
    # 多线程_上交一个任务
    def __threading_submit(self, function):
        self.executor.submit(function)
    # *运行系统*
    def run(self):
        # 如果没有添加任何的按钮，则返回错误并不启动窗口
        if(self.__window_length == 0):
            raise NoCreationFunction()
        self.root.mainloop()
        logging.info("The basic window has been created successfully.")
        
    # 管理窗口
    def ManageWindow_test(self):
        self.__ManageWindow("add")
    # TODO:
    def __ManageWindow(self, action:str) -> None:
        if not (action in ["add"]):
            raise ValueError("内部错误：在调用__ManageWindow方法时，使用了错误的action字符串。")
        # 若不存在管理窗口，则创建
        if self.__manageWindow is None:
            # 创建管理窗口
            self.__manageWindow = tk.Toplevel(self.root)
            # 进行基本设置
            basicFrame = self.__DefaultWindowSetting(self.__manageWindow)
            # 创建另一个区域用于显示内容
            self.__manageWindow_mainFrame = tk.Frame(self.__manageWindow)
            self.__manageWindow_mainFrame.pack(side="left", expand=True, fill="both")
       
        # 添加一个空白块，用于刷新提示
        reflashcall = tk.Label(self.__manageWindow_mainFrame,text='R')
        
        # 计算字符串长度和高度，并设置
        stringLengthPx = tk_font.nametofont(reflashcall.cget("font")).measure('R')
        stringHeightPx = tk_font.nametofont(reflashcall.cget("font")).metrics("linespace")
        
        # 计算行数，并设置
        rowIndex = len(self.__manager_content_dataset)
        reflashcall.grid(row=rowIndex,column=0,ipadx=int((stringHeightPx-stringLengthPx)/2))
        
        
        
        #self.__manager_content_dataset.append
        pass
    # 跳出屏幕信息显示视窗
    def __LoggingWindow(self, text: str, level: str, followMouse = True) -> None:
        # 根据状态，设置数据
        if level == "succeed":
            color = "green"
            stayTime = 1500
        elif level == "error":
            color = "red"
            stayTime = 3000
        else:
            raise ValueError("内部错误：在调用__Loggingwindow方法时，使用了错误的level字符串。")

        # 跳出窗口完成执行提示
        window = tk.Toplevel(self.root)

        # 设置窗口基础设置

        # 设置窗口标题
        window.title("QuickToolBar")
        # 使窗口保持在最上层
        window.attributes("-topmost", True)
        # 禁止改变窗口大小
        window.resizable(False, False)
        # 移除标题栏
        window.overrideredirect(True)
        # 使窗口背景透明
        window.config(bg='#add123')
        window.wm_attributes('-transparentcolor', '#add123')
        # 创建文字Label，并设置
        showText = tk.Label(window, text="", bg=color, fg="white")
        showText.pack(side="left", expand=False)
        # 设置窗口大小
        stringLengthPx = tk_font.nametofont(showText.cget("font")).measure(text) + 10
        stringHeightPx = tk_font.nametofont(showText.cget("font")).metrics("linespace")
        showText.pack(side="left", expand=False)
        
        # 根据要不要跟随鼠标决定位置
        if (followMouse):
        # 获取鼠标位置，并生成在鼠标位置
            mouseX, mouseY = self.root.winfo_pointerxy()
            window.geometry(
                str(stringLengthPx) + 'x' + str(stringHeightPx)
                + f"+{mouseX}+{mouseY}")
        else:
            # 这是固定位置生成
            window.geometry(
                str(stringLengthPx) + 'x' + str(stringHeightPx)
                + "+0+"
                + str(int(window.winfo_screenheight() / 2)))
            
        # 在一定时间后自动关闭
        window.after(stayTime, window.destroy)
        
        # 添加鼠标点击时关闭效果
        def on_click(event):
            window.destroy()
        window.bind("<Button-1>", on_click)

        # 添加文字逐字显示效果
        def reveal_text(label, text, idx=0):
            if idx < len(text):
                # 显示下一个字符
                next_text = text[:idx + 1]
                label.config(text=next_text)
                # 安排下一次调用自身，以显示下一个字符
                label.after(int(0.1 * 2000 / len(text)), reveal_text, label, text, idx + 1)

        reveal_text(showText, text)
    # 创建按钮 - 快速单次执行
    def createButtonVersionB(self, name:str,command ,mode:Mode,returnType:ReturnType = None,icon:str=None):
        self.__create_instant_checkError(name, command, mode, returnType, icon)
        self.__create_dataset_space(name)
        button = self.__create_button(name,icon)
        self.__assign_buttonEvent(name, button, command, mode, returnType)

    # 创建按钮 - 快速单次执行 (错误检查)
    def __create_instant_checkError(self,name:str,command,mode,returnType = None,icon=None):
        # name
        if type(name) is not str:  
            logging.warning(
                f"When importing the button named \"{name}\", you attempted to import data of type \'{type(name)}\' "
                f"for name. The name will be automatically converted to the string \"{str(name)}\""
                f", but it is not recommended to use non-string objects for the name parameter.")
            name = str(name)
        if name in self.__root_content_dataset:
            raise QuickToolBar.__DuplicateButtonName(name)
        
        # mode
        if type(mode) is not Mode: 
            raise TypeError(
                "mode is not an instance of \'Mode\', Please define using the \'Mode\' enum type.")
        
        # command
        if command is None:  # 检查command是否为空或非方法对象
            raise ValueError("command cannot be None")
        elif not callable(command):
            raise TypeError("The passed data to command is not a callable data")
            
        # returnType
        if not ((returnType is None) or (isinstance(returnType,ReturnType))): 
            raise TypeError(f"You are using {returnType} as an argument for returnType, which is not supported. "
                            "Only `ReturnType` enum values can be passed as arguments for returnType.")
            
        # icon
        if not ((icon is None) or (type(icon) is str)):
            raise TypeError("Please use None to indicate the absence of an Icon, "
                            "or use a string to specify the file path for the Icon image.")
    
    # 通用 - 创建内容存储
    def __create_dataset_space(self, name:str):
        self.__root_content_dataset[name] = dict()

    # 通用 - 创建按钮
    def __create_button(self,name,icon:str):
        # 有icon传入的情况
        if icon is not None: 
            button = tk.Button()
            button.config(bg=self.__colors['bg'], borderwidth=0, highlightthickness=0,
                            activebackground=self.__colors['bg'],
                            activeforeground=self.__colors['fg'])
            
            # 处理Icon，使其符合主窗口的大小
            icon = Image.open(icon)
            width, height = icon.size
            width, height = math.floor(width / height * self.__window_height), self.__window_height
            icon = icon.resize((int(width * 4 / 5), int(height * 4 / 5)), Image.Resampling.NEAREST)
            icon_tk = ImageTk.PhotoImage(icon)
            
            # 在数据集中，创建icon数据
            self.__root_content_dataset[name]["icon"] = icon_tk
            
            # 将按钮的图片设置为输入的icon，并增加主窗口的大小
            button.config(image=self.__root_content_dataset[name]["icon"], width=width,
                          height=self.__window_height)
            self.__window_length += width
            self.root.geometry(f"{self.__window_length}x{self.__window_height}")
            button.pack(side="left")
            return button
        
        # 无icon传入的情况
        else:
            frame = tk.Frame(self.root, height=self.__window_height, width=self.__window_height)
            frame.pack_propagate(False)
            frame.pack(side="left")
            button = tk.Button(frame)
            # 设置基本特征
            button.config(bg=self.__colors['bg'], borderwidth=0, highlightthickness=0,
                          activebackground=self.__colors['bg'],
                          activeforeground=self.__colors['bg'])
            # 在没有设置按钮图像的情况下，将添加一个正方形的按钮并将第一个字母作为标识，并调整其大小为按钮大小
            button.config(text=name[0], height=self.__window_height, width=self.__window_height,
                          font=("Arial", int(self.__window_height * 0.5)))
            # 增加主窗口的大小
            self.__window_length += self.__window_height
            self.root.geometry(f"{self.__window_length}x{self.__window_height}")
            button.pack()
            return button
    
    # 通用？ - 创建按钮事件 #TODO:这真的可以通用吗？如果是多线程的情况下还能正常运行吗？
    def __assign_buttonEvent(self,name , button, command, mode, returnType:ReturnType):
        def ButtonFunction():
            # 错误捕获
            try:
                returnData = command()
            except:
                self.__LoggingWindow(f"{name}..............An error occurred while executing. "
                                    f"See the console for detailed information.", "error")
                logging.error(f"An error occurred while executing {name}:")
                raise
            else: 
                # 没有出现错误：
                # 若返回类型不符合需求:
                
                isReturnCorrect, theType = QuickToolBar.__isReturnCorrect(returnData,returnType)
                if not isReturnCorrect:
                    if mode is Mode.Api:
                        self.__LoggingWindow(f"{name}..............The returned data type is incorrect. "
                                                    f"See the console for detailed information. ", "error")
                    else:
                        self.__LoggingWindow(f"{name}..............The returned data type is incorrect. "
                                                f"See the console for detailed information. ", "error" , False)
                    if returnType is ReturnType.Auto:
                        typeslist = []
                        for types in ReturnType:
                            typeslist.append(types.instance)
                        logging.error(f"While invoking the method named \'{name}\', "
                              f"the returned data type is {type(returnData)}. "
                              f"However, the return type is not supported. "
                              f"The return types supported in Auto mode include {typeslist}"
                              )
                        return
                    logging.error(f"While invoking the method named \'{name}\', "
                                    f"the returned data type is {type(returnData)} instead "
                                    f"of {returnType.instance}. Please confirm whether the method is returning data "
                                    f"of the str Image.")
                    return
                if theType is ReturnType.String:
                    pass
                    self.__createWindow_String(returnData)
                elif theType is ReturnType.Image:
                    pass
                    self.__createWindow_Image(returnData)
                # 输出正常运行日志
                if mode is Mode.Api:
                    self.__LoggingWindow(f"{name}..............has successfully completed running", "succeed")
                else:
                    self.__LoggingWindow(f"{name}..............has successfully completed running", "succeed", False)
                logging.debug(f"{name}..............has been executed successfully.")
        def ButtonFunction_submitThreading():
            self.__threading_submit(ButtonFunction)
            self.__LoggingWindow(f"{name}..............Success runs in the background.", "succeed")
        if mode is Mode.Api:
            button.config(command = ButtonFunction)
        elif mode is Mode.Concurrent_Process:
            button.config(command = ButtonFunction_submitThreading)
    
    # 返回窗口创建：字符串 ReturnType.String
    def __createWindow_String(self, returnData):
        # 创建窗口
        window = tk.Toplevel(self.root)
        window.withdraw()
        
        # 创建复制功能
        def copyCommand():
            copy(returnData)
            self.__LoggingWindow("The content has been copied to the clipboard.", "succeed")
        
        # 设定窗口
        self.__DefaultWindowSetting(window,menu_copy=copyCommand)
        
        # 创建窗口
        textLabel = tk.Label(window, text=returnData, bg=self.__colors['bg'], fg=self.__colors['fg'], justify="left")
        textLabel.pack(side="left", expand=False)
        self.__CenterWindow(window)
        window.deiconify()
        
    # 返回窗口创建：图片 ReturnType.Image
    def __createWindow_Image(self,returnData):
        window = tk.Toplevel(self.root)
        window.withdraw()
        # 创建复制按钮命令
        window.returnData = returnData
        
        def copyCommand():
            self.__send_to_clipboard(window.returnData)
            self.__LoggingWindow("The content has been copied to the clipboard.", "succeed")
        self.__DefaultWindowSetting(window,menu_copy=copyCommand)
        
        # 创建保存按钮
        if returnData.size[0]>self.root.winfo_screenwidth()/3:
            wx = self.root.winfo_screenwidth()/3
            wy = wx*returnData.size[1]/returnData.size[0]
            wx, wy = int(wx), int(wy)
            returnData = returnData.resize((wx, wy), Image.Resampling.BILINEAR)
            logging.info(
                "The image has been scaled down to within one-third of the screen for better display.")
        if returnData.size[1]>self.root.winfo_screenheight()/3:
            wy = self.root.winfo_screenheight()/3
            wx = wy*returnData.size[0]/returnData.size[1]
            wx, wy = int(wx), int(wy)
            returnData = returnData.resize((wx, wy), Image.Resampling.BILINEAR)
            logging.info(
                "The image has been scaled down to within one-third of the screen for better display.")
        
        # 创建显示的图片
        window.tkImage = ImageTk.PhotoImage(returnData)
        imageLabel = tk.Label(window, image=window.tkImage, bg=self.__colors['bg'], fg=self.__colors['fg'])
        imageLabel.pack(side="left", expand=False)
        self.__CenterWindow(window)
        window.deiconify()
        
        positionx = int((window.winfo_screenwidth() - window.tkImage.width())/2)
        positiony = int((window.winfo_screenheight() - window.tkImage.height())/2)
        window.geometry(f"+{positionx}+{positiony}")
        
    
    # 返回值判断
    @staticmethod
    def __isReturnCorrect(returnData, returnType) -> bool:
        if returnType is ReturnType.Auto:
            for theType in ReturnType:
                if isinstance(returnData,theType.instance):
                    return True, theType
            return False, returnType
        if returnType is None:
            return (returnData is None), None
        return isinstance(returnData,returnType.instance), returnType
            
    # 标准窗口设置：命名，将其设置为最上层，禁止改变窗口大小，移除标题栏，移动和关闭，置于屏幕中央位置 {将会返回basicTools_frame用于添加部件}
    def __DefaultWindowSetting(self, window, menu_copy=None, menu_save=None):
        """
        # 设置窗口的透明度为50%
        self.root.attributes("-alpha", 0.5)
        # 背景透明设置
        root.config(bg = '#add123')
        root.wm_attributes('-transparentcolor','#add123')
        """
        window.title("QuickToolBar")
        # 使窗口保持在最上层
        window.attributes("-topmost", True)
        # 禁止改变窗口大小
        window.resizable(False, False)
        # 移除标题栏
        window.overrideredirect(True)
        # 创建一个用于放置移动和关闭的区域
        
        # 创建一个移动窗口用的label
        # region 随意位置拖动即可移动窗口功能
        window.dragging = False
        window.start_x = None
        window.start_y = None
        window.pre_x = None
        window.pre_y = None
        
        # 在拖动时禁用所有的组件
        def DisableAllWidgets(widget):
            if isinstance(widget, tk.Button):
                widget['state'] = 'disabled'
            for child in widget.winfo_children():
                DisableAllWidgets(child)
        # 结束时启用所有的组件
        def EnableAllWidgets(widget):
            if isinstance(widget, tk.Button):
                widget['state'] = 'normal'
            for child in widget.winfo_children():
                EnableAllWidgets(child)
        def start_move(event):
            window.dragging = True
            window.start_x = event.x
            window.start_y = event.y
            window.pre_x, window.pre_y = 0,0
        def EnableAllWidgets_trigger():
            EnableAllWidgets(window)
        def stop_move(event):
            window.dragging = False
            window.after(32,EnableAllWidgets_trigger)
        def on_move(event):
            if window.dragging:
                deltax = event.x - window.start_x
                deltay = event.y - window.start_y
                window.pre_x += event.x
                window.pre_y += event.y
                if(window.pre_x + window.pre_x > 128):
                    DisableAllWidgets(window)
                x = window.winfo_x() + deltax
                y = window.winfo_y() + deltay
                window.geometry(f"+{x}+{y}")
        
        window.bind("<Button-1>", start_move)
        window.bind("<ButtonRelease-1>", stop_move)
        window.bind("<B1-Motion>", on_move)
        # endregion
        
        # region 创建右键面板
        menu = tk.Menu(window,tearoff=0)
        
        def show_menu(e):
            menu.post(e.x_root, e.y_root)  # 在点击的位置显示菜单
            
        # 若不为主窗口则增加一些如复制，保存的功能
        if menu_copy is not None:
            menu.add_command(label="Copy", command=menu_copy)
        if menu_save is not None:
            menu.add_command(label="Copy", command=menu_save) 
        if (menu_copy is not None) or (menu_save is not None): 
            menu.add_separator()
        
        menu.add_command(label="Exit", command=window.destroy) 
        # 绑定
        window.bind("<Button-3>", show_menu)
        # endregion
        
        # 将窗口置于屏幕中央
        self.__CenterWindow(window)

    # 使窗口置于屏幕中央
    @staticmethod
    def __CenterWindow(window):
        window.update_idletasks()
        window.geometry(f"+{int((window.winfo_screenwidth() - window.winfo_width()) / 2)}"
                        f"+{int((window.winfo_screenheight() - window.winfo_height()) / 2)}")
        return
    
    # Copy image to Clipboard method from https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
    @staticmethod
    def __send_to_clipboard(image):
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()  

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()


# region 快速接入系统
root = QuickToolBar()


# 执行产生窗口，进入内部循环
def run():
    root.run()
    return


# 添加按钮方法
def createButton(name:str,command,mode, returnType = None,icon=None):
    root.createButtonVersionB(name, command, mode,returnType, icon)
    return
# endregion