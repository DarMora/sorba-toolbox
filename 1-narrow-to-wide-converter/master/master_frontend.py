from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
from narrow2wide import narrow2wide_frontend


class UI:
    def __init__(self, win: Tk):
        self.win = win
        self.win.title("SORBA Toolkit")
        # self.win.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.lbl_source_file = Label(self.win, text='SORBA Toolkit is a group of apps to support applications. \n'
                                                    'This is not a SORBA product!!! \n'
                                                    'No support is available!!!')
        self.lbl_source_file.grid(row=0, columnspan=3, pady=10)  # padx=10,

        self.btn_narrow_to_wide_converter = Button(self.win,
                                                   text='Narrow to Wide Converter',
                                                   command=self.narrow_to_wide_converter)
        self.btn_narrow_to_wide_converter.grid(row=1, column=0, columnspan=3, pady=10)

    def clear_widgets(self):
        for item in self.win.grid_slaves():
            item.destroy()

    def narrow_to_wide_converter(self):
        self.clear_widgets()
        app = narrow2wide_frontend.UI(self.win)
