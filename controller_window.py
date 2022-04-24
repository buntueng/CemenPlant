from json.tool import main
import tkinter as tk
import tkinter.font as font

# main program
main_window = tk.Tk()
main_window.wm_title("Cement Plant")
main_window.geometry('1024x768')


main_font = font.Font(family='TH Niramit AS',size=14,weight="bold")
main_frame = tk.Frame(main_window)
top_frame = tk.Frame(main_frame)
left_frame = tk.Frame(main_frame)
right_frame = tk.Frame(main_frame)
bottom_frame = tk.Frame(main_frame)

top_frame.grid(row=0,column=0,columnspan=2,padx=50,sticky='w')
left_frame.grid(row=1,column=0,padx=(10,10),pady=5)
right_frame.grid(row=1,column=1,padx =(30,0),pady=10,sticky='ne')
bottom_frame.grid(row=2,column=0,columnspan=2,padx=(0,0),sticky='w')
main_window.mainloop()