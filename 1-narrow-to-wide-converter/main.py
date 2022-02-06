"""
Created by: ITG
Date: 06/29/2021
Description: This tool converts a dataset from narrow to wide format
Notes: This utility has been tested with the following file types (add as needed):
 - Siemens HMI Log Files

"""

from master import master_frontend
import tkinter as tk


def main():
    window = tk.Tk()
    root = master_frontend.UI(window)
    window.mainloop()


if __name__ == '__main__':
    main()
