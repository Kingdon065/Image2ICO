#! python3
# _*_ coding:utf-8 _*_

import os
import subprocess
import PythonMagick
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk


class Image2Ico:
    def __init__(self):
        self.win = Tk()
        self.win.title('图标制作2.0')
        self.win.iconbitmap('icon/ico-32.ico')
        self.window_center(self.win, 600, 360)  # 窗口居中
        self.win.resizable(0, 0)

        lf = LabelFrame(self.win, text='图标制作', bd=2, font='楷体 16')
        lf.pack(pady=20, ipadx=5, ipady=5)

        # 打开图片
        openLabel = Label(lf, text='打开图片: ', bg='#FFA500', width=10, anchor='e')
        openLabel.grid(row=0, column=0, padx=20, pady=10)

        self.imgFile = StringVar()
        Entry(lf, width=50, textvariable=self.imgFile).grid(row=0, column=1, sticky=W)

        Button(lf, text=' 预览 ', command=self.open_file).grid(row=0, column=2, padx=10)

        # 保存结果
        saveLabel = Label(lf, text='保存为: ', bg='#FFA500', width=10, anchor='e')
        saveLabel.grid(row=1, column=0, padx=20, pady=10)

        self.icoFile = StringVar()
        Entry(lf, width=50, textvariable=self.icoFile).grid(row=1, column=1, sticky=W)

        Button(lf, text=' 预览 ', command=self.set_save_filename).grid(row=1, column=2, padx=5)

        # 选择分辨率
        sizeLabel = Label(lf, text='ICO大小: ', bg='#FFA500', width=10, anchor='e')
        sizeLabel.grid(row=2, column=0, padx=20, pady=10)

        self.size = StringVar()
        # 组合框
        cb = Combobox(lf, textvariable=self.size, width=10, state='readonly')
        cb['value'] = ('16x16', '32x32', '64x64', '128x128', '256x256')
        cb.current(4)
        cb.grid(row=2, column=1)

        # 约束比例
        scaleLabel = Label(lf, text='约束比例: ', bg='#FFA500', width=10, anchor='e')
        scaleLabel.grid(row=3, column=0, pady=10)

        self.scale = IntVar()
        self.scale.set(1)

        frame = Frame(lf)
        frame.grid(row=3, column=1)

        yesRButton = Radiobutton(frame, text='是', variable=self.scale, value=1)
        yesRButton.grid(row=0, column=0, padx=3)

        noRButton = Radiobutton(frame, text='否', variable=self.scale, value=0)
        noRButton.grid(row=0, column=1, padx=3)

        startButton = Button(self.win, text=' 开始转换 ', bg='#FFA500', command=self.translate)
        startButton.config(relief=SOLID, height=2)
        startButton.config(font=('黑体', 12))
        startButton.pack(pady=5)

        dirButton = Button(self.win, text='保存文件夹', command=self.open_explorer)
        dirButton.pack(side=LEFT, padx=20, pady=10)

        previewButton = Button(self.win, text='预览图标', command=self.preview_ico)
        previewButton.pack(side=RIGHT, padx=20)

        self.win.mainloop()

    def window_center(self, window, width, height):
        win_width = window.winfo_screenwidth()
        win_height = window.winfo_screenheight()
        x = int((win_width - width) / 2)
        y = int((win_height - height) / 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def preview_ico(self):
        path = self.icoFile.get()
        if not os.path.exists(path):
            messagebox.showwarning(title='转换未进行', message='没有可预览的ico文件!')
            return

        height = self.size.get().split('x')[0]
        y = (300 - int(height)) / 2

        top = Toplevel()
        top.title('预览')
        self.window_center(top, 300, 300)
        top.iconbitmap('icon/img2ico.ico')

        image = Image.open(path)
        tk_image = ImageTk.PhotoImage(image)

        Label(top, image=tk_image).pack(pady=y)

        top.mainloop()     # 添加此行，程序就不会离开这个函数，局部变量tk_image就不会被销毁， 子窗口中的图片才能正常显示

    def open_explorer(self):
        path = os.path.dirname(self.icoFile.get())
        if not path:
            messagebox.showwarning(title='ico文件路径未指定', message='没有可打开的ico文件夹!')
            return
        command = f'explorer "{path}"'
        # 路径中有'/'，命令无法运行
        command = command.replace('/', '\\')
        #os.system(command)     # 运行时会弹出dos窗口
        subprocess.run(command)     # 不会弹出dos窗口

    def open_file(self):
        filename = askopenfilename(filetypes=[('所有支持的文件', '*.png;*.jpg;*.ico'),
            ('PNG文件', '*.png'),('JPG文件', '*.jpg'), ('ICO文件', '*.ico')]
        )
        self.imgFile.set(filename)

    def set_save_filename(self):
        filename = asksaveasfilename(filetypes=[('ICO文件', '*.ico')])
        # 如果文件名中没有扩展名.ico, 且不为空，则为其添加扩展名.ico
        if not filename.endswith('.ico') and filename:
                filename += '.ico'
        self.icoFile.set(filename)

    def translate(self):
        imgFileVar = self.imgFile.get()
        if not os.path.exists(imgFileVar):
            messagebox.showerror(title='路径错误', message='图片路径未指定或不存在!')
            return
        icoFileVar = self.icoFile.get()
        if not icoFileVar:
            messagebox.showerror(title='路径错误', message='存储路径未指定!')
            return

        # 确保保存的文件的扩展名为.ico
        if not icoFileVar.endswith('.ico'):
            icoFileVar += '.ico'

        try:
            img = PythonMagick.Image(imgFileVar)

            size = self.size.get()
            if not self.scale.get():
                size = self.size.get() + '!'
            img.sample(size)
            img.write(icoFileVar)
            messagebox.showinfo(title='转换完成', message=f'文件保存于{icoFileVar}.')
        except RuntimeError:
            messagebox.showerror(title='打开文件错误', message=f'无法打开 {imgFileVar} 文件')


if __name__ == '__main__':
    Image2Ico()