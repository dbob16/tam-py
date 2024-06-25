import ttkbootstrap as ttk
from .models import PrefixTable

def edit_form():
    window = ttk.Toplevel(title="Edit Prefixes")

    v_prefix = ttk.StringVar(window)

    prefix_table = PrefixTable()

    # Commands
    def cmd_update():
        tv_results.delete(*tv_results.get_children())
        results = prefix_table.select_all()
        for row in results:
            tv_results.insert("", "end", iid=row[0], values=(row[0], row[1]))

    def cmd_add():
        prefix_table.create(v_prefix.get(), cmb_bootstyle.get())
        cmd_update()

    def cmd_tv_select(_=None):
        r = tv_results.item(tv_results.focus())
        r = r["values"]
        v_prefix.set(r[0])
        cmb_bootstyle.set(r[1])

    def cmd_edit():
        prefix_table.edit_bootstyle(v_prefix.get(), cmb_bootstyle.get())
        cmd_update()
    
    def cmd_drop():
        prefix_table.drop(v_prefix.get())
        cmd_update()

    frm_add = ttk.LabelFrame(window, text="Add/Edit Prefix")
    frm_add.pack(side="top", padx=4, pady=4, fill="x")

    frm_tv = ttk.LabelFrame(window, text="All Prefixes")
    frm_tv.pack(side="top", padx=4, pady=4, fill="x")

    # Add controls
    lbl_prefix = ttk.Label(frm_add, text="Prefix Name")
    lbl_prefix.grid(row=0, column=0, padx=4, pady=4)

    txt_prefix = ttk.Entry(frm_add, width=12, textvariable=v_prefix)
    txt_prefix.grid(row=1, column=0, padx=4, pady=4)

    lbl_bootstyle = ttk.Label(frm_add, text="Bootstyle")
    lbl_bootstyle.grid(row=0, column=1, padx=4, pady=4)

    cmb_bootstyle = ttk.Combobox(frm_add, state="readonly", values=("primary", "secondary", "success", "info", "warning", "danger"))
    cmb_bootstyle.grid(row=1, column=1, padx=4, pady=4)

    btn_add = ttk.Button(frm_add, text="Add Prefix", command=cmd_add)
    btn_add.grid(row=0, column=2, padx=4, pady=4, rowspan=2, sticky="ns")

    btn_change = ttk.Button(frm_add, text="Edit Bootstyle", command=cmd_edit)
    btn_change.grid(row=0, column=3, padx=4, pady=4, rowspan=2, sticky="ns")

    btn_delete = ttk.Button(frm_add, text="Delete Prefix", command=cmd_drop, bootstyle="danger")
    btn_delete.grid(row=0, column=4, padx=4, pady=4, rowspan=2, sticky="ns")

    # Edit TV controls
    sb_tv = ttk.Scrollbar(frm_tv, orient="vertical")
    sb_tv.pack(side="right", fill="y")

    tv_results = ttk.Treeview(frm_tv, show="headings", columns=("prefix", "bootstyle"), yscrollcommand=sb_tv.set)
    tv_results.heading("prefix", text="Prefix Name")
    tv_results.heading("bootstyle", text="Bootstyle")
    tv_results.pack(padx=4, pady=4, fill="both")

    sb_tv.configure(command=tv_results.yview)

    tv_results.bind("<<TreeviewSelect>>", cmd_tv_select)

    cmd_update()