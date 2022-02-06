from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
from narrow2wide.narrow2wide_backend import *


class UI:
    def __init__(self, win: Tk):
        self.win = win
        self.win.title("Narrow2WideConverter")
        # self.win.geometry('300x320')
        # self.win.resizable(False, False)

        self.lbl_source_file = Label(self.win, text='The following app has been tested with:\n'
                                                    ' - Siemens HMI log files')
        self.lbl_source_file.grid(row=0, padx=40, pady=10)  # padx=10, pady=20, columnspan=10

        self.running = False

        self.var_src_file_name = StringVar()
        self.var_src_file_name.set("Choose source file...")

        self.var_dst_file_name = StringVar()
        self.var_dst_file_name.set("Choose destination file...")

        self.var_convert_stat = StringVar()
        self.var_convert_stat.set("Waiting to convert...")

        self.btn_choose_src_file = Button(self.win, text='Choose Source File', command=self.choose_src_file)
        self.btn_choose_src_file.grid(row=1, pady=10)   # column=0, columnspan=10, pady=10

        self.lbl_source_file = Label(self.win, textvariable=self.var_src_file_name)
        self.lbl_source_file.grid(row=2, pady=10)  # padx=10, pady=20, columnspan=10

        self.btn_choose_dst_file = Button(self.win, text='Choose Destination File', command=self.choose_dst_file)
        self.btn_choose_dst_file.grid(row=3, pady=10)  # , column=0, columnspan=10, pady=10, padx=10

        self.lbl_destination_file = Label(self.win, textvariable=self.var_dst_file_name)
        self.lbl_destination_file.grid(row=4, pady=10)  # column=0, padx=10, columnspan=10, pady=10

        self.btn_convert_file = Button(self.win, text='Convert file', command=self.convert_file)
        self.btn_convert_file.grid(row=5, pady=10)  # column=1, padx=10, columnspan=10, pady=10

        self.lbl_convert_stat = Label(self.win, textvariable=self.var_convert_stat)
        self.lbl_convert_stat.grid(row=6, pady=10)  # column=0, padx=10 , columnspan=10, pady=10

    def choose_src_file(self):
        if not self.running:
            file_path = filedialog.askopenfilename(
                title="Choose source file",
                filetypes=[('Text Document', '*txt'), ('Text Document', '*csv',)])

            if file_path != '':
                self.var_src_file_name.set(file_path)
                self.var_dst_file_name.set(file_path[:-4]+'-wide'+file_path[-4:])

    def choose_dst_file(self):
        if not self.running:
            file_path = filedialog.asksaveasfilename(title="Choose destination file",
                                                     filetypes=[('Text Document', '*txt'), ('Text Document', '*csv',)])

            if file_path != '':
                self.var_dst_file_name.set(file_path)

    def convert_file(self):
        if not self.running:
            if self.var_src_file_name.get()[-4:] == ".txt" or self.var_src_file_name.get()[-4:] == ".csv":
                try:
                    self.running = True
                    self.var_convert_stat.set('Converting...')
                    fmt_narrow_to_wide_s7_hmi_to_sdc(self.var_src_file_name.get(), self.var_dst_file_name.get())
                    self.running = False
                    self.var_convert_stat.set('Conversion Finished Successfully!')
                except:
                    self.running = False
                    self.var_convert_stat.set('Failed to convert file!')
            else:
                self.var_convert_stat.set("Filename must be a .txt or .csv")
