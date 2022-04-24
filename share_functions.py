def center_screen(top_level_window):
    top_level_window.update_idletasks()
    width = top_level_window.winfo_width()
    frm_width = top_level_window.winfo_rootx() - top_level_window.winfo_x()
    win_width = width + 2 * frm_width
    height = top_level_window.winfo_height()
    titlebar_height = top_level_window.winfo_rooty() - top_level_window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = top_level_window.winfo_screenwidth() // 2 - win_width // 2
    y = top_level_window.winfo_screenheight() // 2 - win_height // 2
    top_level_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    top_level_window.deiconify()