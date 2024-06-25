import ttkbootstrap as ttk 
import time
from ..models import BasketTable

def basket_form(prefix:str="regular", bootstyle:str="primary"):
    basket_table = BasketTable(prefix)

    window = ttk.Toplevel(title=f"{prefix.capitalize()} Baskets")
    v_from, v_to, v_per_page = ttk.IntVar(window), ttk.IntVar(window), ttk.IntVar(window)
    v_id, v_bd, v_do = ttk.IntVar(window), ttk.StringVar(window), ttk.StringVar(window)
    copied_record = []

    # Commands
    def cmd_tv_select(_=None):
        for s in tv_results.selection():
            r = tv_results.item(s)['values']
            v_id.set(r[0]), v_bd.set(r[1]), v_do.set(r[2])

    def cmd_update():
        tv_results.delete(*tv_results.get_children())
        results = basket_table.select_range(v_from.get(), v_to.get())
        for i in range(v_from.get(), v_to.get()+1):
            d = results[i]
            tv_results.insert("", "end", iid=i, values=(i, d[0], d[1]))
        if v_id.get() > v_to.get():
            v_id.set(v_to.get())
        elif v_id.get() < v_from.get():
            v_id.set(v_from.get())
        tv_results.selection_set(v_id.get())
        txt_bd.focus()

    def cmd_save(_=None):
        if tv_results.item(v_id.get())["values"] != [v_id.get(), v_bd.get(), v_do.get()]:
            basket_table.insert(v_id.get(), v_bd.get(), v_do.get())
        cmd_update()

    def cmd_move_up(_=None):
        cmd_save()
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
            tv_results.selection_set(v_id.get())
    
    def cmd_move_down(_=None):
        cmd_save()
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            tv_results.selection_set(v_id.get())

    def cmd_copy(_=None):
        copied_record.clear()
        for c in (v_bd, v_do):
            copied_record.append(c.get())

    def cmd_paste(_=None):
        cr = copied_record
        v_bd.set(cr[0]), v_do.set(cr[1])

    def cmd_dup_up(_=None):
        cmd_copy()
        cmd_move_up()
        cmd_paste()
        cmd_save()

    def cmd_dup_down(_=None):
        cmd_copy()
        cmd_move_down()
        cmd_paste()
        cmd_save()

    def cmd_next_page():
        v_from.set(v_from.get()+v_per_page.get()), v_to.set(v_to.get()+v_per_page.get())
        cmd_update()

    def cmd_prev_page():
        v_from.set(v_from.get()-v_per_page.get()), v_to.set(v_to.get()-v_per_page.get())
        cmd_update()

    # Frames
    frm_range_select = ttk.LabelFrame(window, text="Range Select")
    frm_range_select.pack(side="top", padx=4, pady=4, fill="x")

    frm_current_record = ttk.LabelFrame(window, text="Current Record")
    frm_current_record.pack(side="top", padx=4, pady=4, fill="x")

    frm_commands = ttk.LabelFrame(window, text="Commands")
    frm_commands.pack(side="top", padx=4, pady=4, fill="x")

    frm_results = ttk.LabelFrame(window, text="Current Results")
    frm_results.pack(side="top", padx=4, pady=4, fill="both")

    # Range Select controls
    lbl_range = ttk.Label(frm_range_select, text="Range: ")
    lbl_range.pack(side="left", padx=4, pady=4)

    txt_from = ttk.Entry(frm_range_select, textvariable=v_from, width=8)
    txt_from.pack(side="left", padx=4, pady=4)

    lbl_dash = ttk.Label(frm_range_select, text=" - ")
    lbl_dash.pack(side="left", padx=4, pady=4)

    txt_to = ttk.Entry(frm_range_select, textvariable=v_to, width=8)
    txt_to.pack(side="left", padx=4, pady=4)

    btn_update = ttk.Button(frm_range_select, text="Update", bootstyle=bootstyle, command=cmd_update)
    btn_update.pack(side="left", padx=4, pady=4)

    lbl_spacer = ttk.Label(frm_range_select, text="    ")
    lbl_spacer.pack(side="left", padx=4, pady=4)

    lbl_per_page = ttk.Label(frm_range_select, text="Per Page: ")
    lbl_per_page.pack(side="left", padx=4, pady=4)

    txt_per_page = ttk.Entry(frm_range_select, textvariable=v_per_page, width=4)
    txt_per_page.pack(side="left", padx=4, pady=4)

    btn_next_page = ttk.Button(frm_range_select, text="Next Page", bootstyle=bootstyle, command=cmd_next_page)
    btn_next_page.pack(side="left", padx=4, pady=4)

    btn_prev_page = ttk.Button(frm_range_select, text="Previous Page", bootstyle=bootstyle, command=cmd_prev_page)
    btn_prev_page.pack(side="left", padx=4, pady=4)

    # Current Record controls
    lbl_id = ttk.Label(frm_current_record, text="Basket #")
    lbl_id.grid(row=0, column=0, padx=4, pady=4)

    txt_id = ttk.Entry(frm_current_record, textvariable=v_id, state="readonly", width=8)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    lbl_bd = ttk.Label(frm_current_record, text="Basket Description")
    lbl_bd.grid(row=0, column=1, padx=4, pady=4)

    txt_bd = ttk.Entry(frm_current_record, textvariable=v_bd, width=20)
    txt_bd.grid(row=1, column=1, padx=4, pady=4)

    lbl_do = ttk.Label(frm_current_record, text="Basket Donors")
    lbl_do.grid(row=0, column=2, padx=4, pady=4)

    txt_do = ttk.Entry(frm_current_record, textvariable=v_do, width=20)
    txt_do.grid(row=1, column=2, padx=4, pady=4)

    btn_save = ttk.Button(frm_current_record, text="Save - Alt S", bootstyle=bootstyle, command=cmd_save)
    btn_save.grid(row=0, column=3, padx=4, pady=4, rowspan=2, sticky="ns")
    window.bind("<Alt-s>", cmd_save)

    # Command controls
    btn_move_up = ttk.Button(frm_commands, text="Move Up - Alt O", bootstyle=bootstyle, command=cmd_move_up)
    btn_move_up.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-o>", cmd_move_up)

    btn_move_down = ttk.Button(frm_commands, text="Move Down - Alt L", bootstyle=bootstyle, command=cmd_move_down)
    btn_move_down.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-l>", cmd_move_down)

    btn_dup_up = ttk.Button(frm_commands, text="Duplicate Up - Alt U", bootstyle=bootstyle, command=cmd_dup_up)
    btn_dup_up.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-u>", cmd_dup_up)

    btn_dup_down = ttk.Button(frm_commands, text="Duplicate Down - Alt J", bootstyle=bootstyle, command=cmd_dup_down)
    btn_dup_down.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-j>", cmd_dup_down)

    btn_copy = ttk.Button(frm_commands, text="Copy - Alt C", bootstyle=bootstyle, command=cmd_copy)
    btn_copy.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-c>", cmd_copy)

    btn_paste = ttk.Button(frm_commands, text="Paste - Alt V", bootstyle=bootstyle, command=cmd_paste)
    btn_paste.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-v>", cmd_paste)

    # Results controls
    tv_sb = ttk.Scrollbar(frm_results)
    tv_sb.pack(side="right", fill="y")

    tv_results = ttk.Treeview(frm_results, show="headings", columns=("id", "bd", "do"), yscrollcommand=tv_sb.set, height=30)
    tv_results.heading("id", text="Basket #")
    tv_results.heading("bd", text="Basket Description")
    tv_results.heading("do", text="Basket Donors")
    tv_results.pack(padx=4, pady=4, fill="both")
    tv_results.bind("<<TreeviewSelect>>", cmd_tv_select)

    tv_sb.configure(command=tv_results.yview)

    v_per_page.set(20)