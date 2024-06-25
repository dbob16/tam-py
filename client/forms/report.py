import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
from ..models import ReportByBasket, ReportByName

def report_form(prefix:str, bootstyle:str, mode:str):
    if mode == "name":
        title = f"{prefix.capitalize()} Winners by Name"
        headings = ("Winner", "Preference", "Ticket #", "Basket #", "Basket Description", "Basket Donors")
        report = ReportByName(prefix)
    elif mode == "basket":
        title = f"{prefix.capitalize()} Winners by Basket #"
        headings = ("Basket #", "Basket Description", "Basket Donor", "Ticket #", "Winner", "Preference")
        report = ReportByBasket(prefix)
    
    window = ttk.Toplevel(title=title)
    v_title = ttk.StringVar(window)

    # Commands
    def cmd_update_all():
        tv_results.delete(*tv_results.get_children())
        results = report.select_all()
        for r in results:
            tv_results.insert("", "end", values=r)
        v_title.set("All Winners")

    def cmd_update_texters():
        tv_results.delete(*tv_results.get_children())
        results = report.select_filtered("preference = 'TEXT'")
        for r in results:
            tv_results.insert("", "end", values=r)
        v_title.set("Winners Preferring TEXT")
    
    def cmd_update_callers():
        tv_results.delete(*tv_results.get_children())
        results = report.select_filtered("preference = 'CALL'")
        for r in results:
            tv_results.insert("", "end", values=r)
        v_title.set("Winners Preferring CALL")

    # Frames
    frm_filters = ttk.LabelFrame(window, text="Filters")
    frm_filters.pack(padx=4, pady=4, fill="x")

    frm_title = ttk.LabelFrame(window, text="Title")
    frm_title.pack(padx=4, pady=4, fill="x")

    frm_tv = ttk.LabelFrame(window, text="Current Results")
    frm_tv.pack(padx=4, pady=4, fill="both")

    frm_save_options = ttk.LabelFrame(window, text="Save Options")
    frm_save_options.pack(side="bottom", padx=4, pady=4, fill="x")

    # Filter controls
    btn_all = ttk.Button(frm_filters, text="All", command=cmd_update_all)
    btn_all.pack(side="left", padx=4, pady=4)

    btn_text = ttk.Button(frm_filters, text="Text preference", command=cmd_update_texters)
    btn_text.pack(side="left", padx=4, pady=4)

    btn_call = ttk.Button(frm_filters, text="Call preference", command=cmd_update_callers)
    btn_call.pack(side="left", padx=4, pady=4)

    # Title controls
    lbl_title = ttk.Label(frm_title, textvariable=v_title)
    lbl_title.pack(side="left", padx=4, pady=4)

    # TV controls
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv_results = ttk.Treeview(frm_tv, show="headings", columns=headings, yscrollcommand=tv_sb.set)
    for s in headings:
        tv_results.column(s, anchor=W)
        tv_results.heading(s, text=s, anchor=W)
    tv_results.pack(padx=4, pady=4, fill="both")
    tv_sb.configure(command=tv_results.yview)

    # Save Options controls
    btn_save_open = ttk.Button(frm_save_options, text="Save and Open")
    btn_save_open.pack(side="left", padx=4, pady=4)

    # On open commands
    cmd_update_all()