import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
import random
from ..models import TicketTable
try:
    import names
except:
    pass

def ticket_form(prefix:str="regular", bootstyle:str="primary"):
    ticket_table = TicketTable(prefix)

    window = ttk.Toplevel(title=f"{prefix.capitalize()} Tickets")
    v_from, v_to = ttk.IntVar(window), ttk.IntVar(window)
    v_id, v_fn, v_ln, v_pn, v_pr = ttk.IntVar(window), ttk.StringVar(window), ttk.StringVar(window), ttk.StringVar(window), ttk.StringVar(window)
    copied_record = []

    # Commands
    def cmd_tv_select(_=None):
        for s in tv_results.selection():
            r = tv_results.item(s)['values']
            v_id.set(r[0]), v_fn.set(r[1]), v_ln.set(r[2]), v_pn.set(r[3]), v_pr.set(r[4])

    def cmd_update():
        tv_results.delete(*tv_results.get_children())
        results = ticket_table.select_range(v_from.get(), v_to.get())
        for i in range(v_from.get(), v_to.get()+1):
            d = results[i]
            if i % 2 != 0:
                tv_results.insert("", "end", iid=i, values=(i, d[0], d[1], d[2], d[3]), tags=('oddrow',))
            elif i % 2 == 0:
                tv_results.insert("", "end", iid=i, values=(i, d[0], d[1], d[2], d[3]), tags=('evenrow',))
        if v_id.get() > v_to.get():
            v_id.set(v_to.get())
        elif v_id.get() < v_from.get():
            v_id.set(v_from.get())
        tv_results.selection_set(v_id.get())
        txt_fn.focus()

    def cmd_save(_=None):
        if tv_results.item(v_id.get())["values"] != [v_id.get(), v_fn.get(), v_ln.get(), v_pn.get(), v_pr.get()]:
            ticket_table.insert(v_id.get(), v_fn.get(), v_ln.get(), v_pn.get(), v_pr.get())
            tv_results.item(v_id.get(), values=[v_id.get(), v_fn.get(), v_ln.get(), v_pn.get(), v_pr.get()])

    def cmd_move_up(_=None):
        cmd_save()
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
            tv_results.selection_set(v_id.get())
        window.update()
        txt_fn.focus()
    
    def cmd_move_down(_=None):
        cmd_save()
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            tv_results.selection_set(v_id.get())
        txt_fn.focus()

    def cmd_copy(_=None):
        copied_record.clear()
        for c in (v_fn, v_ln, v_pn, v_pr):
            copied_record.append(c.get())

    def cmd_paste(_=None):
        cr = copied_record
        v_fn.set(cr[0]), v_ln.set(cr[1]), v_pn.set(cr[2]), v_pr.set(cr[3])

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

    def cmd_next_page(_=None):
        diff = v_to.get() - v_from.get() + 1
        v_from.set(v_from.get()+diff), v_to.set(v_to.get()+diff)
        cmd_update()

    def cmd_prev_page(_=None):
        diff = v_to.get() - v_from.get() + 1
        v_from.set(v_from.get()-diff), v_to.set(v_to.get()-diff)
        cmd_update()

    def cmd_random(_=None):
        def d0():
            return random.randint(0, 1)
        def d():
            return random.randint(0, 9)
        pref_list = ["TEXT", "CALL"]
        fname, lname = names.get_first_name(), names.get_last_name()
        pnum = f"{d0()}{d()}{d()}-{d()}{d()}{d()}-{d()}{d()}{d()}{d()}"
        pref = random.choice(pref_list)
        v_fn.set(fname), v_ln.set(lname), v_pn.set(pnum), v_pr.set(pref)

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

    lbl_pages = ttk.Label(frm_range_select, text="Pages: ")
    lbl_pages.pack(side="left", padx=4, pady=4)

    btn_next_page = ttk.Button(frm_range_select, text="Next Page - Alt N", bootstyle=bootstyle, command=cmd_next_page)
    btn_next_page.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-n>", cmd_next_page)

    btn_prev_page = ttk.Button(frm_range_select, text="Previous Page - Alt B", bootstyle=bootstyle, command=cmd_prev_page)
    btn_prev_page.pack(side="left", padx=4, pady=4)
    window.bind("<Alt-b>", cmd_prev_page)

    # Current Record controls
    lbl_id = ttk.Label(frm_current_record, text="Ticket #")
    lbl_id.grid(row=0, column=0, padx=4, pady=4)

    txt_id = ttk.Entry(frm_current_record, textvariable=v_id, state="readonly", width=8)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    lbl_fn = ttk.Label(frm_current_record, text="First Name")
    lbl_fn.grid(row=0, column=1, padx=4, pady=4)

    txt_fn = ttk.Entry(frm_current_record, textvariable=v_fn, width=20)
    txt_fn.grid(row=1, column=1, padx=4, pady=4)
    txt_fn.bind("<Return>", cmd_save)

    lbl_ln = ttk.Label(frm_current_record, text="Last Name")
    lbl_ln.grid(row=0, column=2, padx=4, pady=4)

    txt_ln = ttk.Entry(frm_current_record, textvariable=v_ln, width=20)
    txt_ln.grid(row=1, column=2, padx=4, pady=4)
    txt_ln.bind("<Return>", cmd_save)

    lbl_pn = ttk.Label(frm_current_record, text="Phone Number")
    lbl_pn.grid(row=0, column=3, padx=4, pady=4)

    txt_pn = ttk.Entry(frm_current_record, textvariable=v_pn, width=20)
    txt_pn.grid(row=1, column=3, padx=4, pady=4)
    txt_pn.bind("<Return>", cmd_save)

    lbl_pr = ttk.Label(frm_current_record, text="Preference")
    lbl_pr.grid(row=0, column=4, padx=4, pady=4)

    chk_pr = ttk.Checkbutton(frm_current_record, textvariable=v_pr, variable=v_pr, onvalue="TEXT", offvalue="CALL", width=5, bootstyle=f"{bootstyle}-outline-toolbutton")
    chk_pr.grid(row=1, column=4, padx=4, pady=4)
    chk_pr.bind("<Return>", cmd_save)

    btn_save = ttk.Button(frm_current_record, text="Save - Alt S", bootstyle=bootstyle, command=cmd_save)
    btn_save.grid(row=0, column=5, padx=4, pady=4, rowspan=2, sticky="ns")
    window.bind("<Alt-s>", cmd_save)
    window.bind("<Alt-r>", cmd_random)

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

    tv_results = ttk.Treeview(frm_results, show="headings", columns=("id", "fn", "ln", "pn", "pr"), yscrollcommand=tv_sb.set, height=30)
    tv_results.heading("id", text="Ticket #", anchor=W)
    tv_results.heading("fn", text="First Name", anchor=W)
    tv_results.heading("ln", text="Last Name", anchor=W)
    tv_results.heading("pn", text="Phone Number", anchor=W)
    tv_results.heading("pr", text="Preference", anchor=W)
    tv_results.pack(padx=4, pady=4, fill="both")
    tv_results.bind("<<TreeviewSelect>>", cmd_tv_select)
    tv_results.tag_configure('oddrow', background="#000000")
    tv_results.tag_configure('evenrow', background="#151515")

    tv_sb.configure(command=tv_results.yview)