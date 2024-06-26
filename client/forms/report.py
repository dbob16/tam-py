import ttkbootstrap as ttk 
import webbrowser
from ttkbootstrap.constants import *
from jinja2 import FileSystemLoader, Environment, select_autoescape
from ..models import ReportByBasket, ReportByName

def report_form(prefix:str, bootstyle:str, mode:str):
    if mode == "name":
        title = f"{prefix.capitalize()} Winners by Name"
        headings = ("Winner Info", "Preference", "Ticket #", "Basket #", "Description", "Donors")
        report = ReportByName(prefix)
    elif mode == "basket":
        title = f"{prefix.capitalize()} Winners by Basket #"
        headings = ("Basket #", "Description", "Donor", "Ticket #", "Winner Info", "Preference")
        report = ReportByBasket(prefix)
    
    window = ttk.Toplevel(title=title)
    v_title = ttk.StringVar(window)

    env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    template = env.get_template("report.html")

    # Commands
    def cmd_update_all():
        tv_results.delete(*tv_results.get_children())
        index = 1
        results = report.select_all()
        for r in results:
            if index % 2 != 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('oddrow',))
            elif index % 2 == 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('evenrow',))
            index += 1
        v_title.set("All Winners")

    def cmd_update_texters():
        tv_results.delete(*tv_results.get_children())
        index = 1
        results = report.select_filtered("preference = 'TEXT'")
        for r in results:
            if index % 2 != 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('oddrow',))
            elif index % 2 == 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('evenrow',))
            index += 1
        v_title.set("Winners Preferring TEXT")
    
    def cmd_update_callers():
        tv_results.delete(*tv_results.get_children())
        index = 1
        results = report.select_filtered("preference = 'CALL'")
        for r in results:
            if index % 2 != 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('oddrow',))
            elif index % 2 == 0:
                tv_results.insert("", "end", iid=index, values=r, tags=('evenrow',))
            index += 1
        v_title.set("Winners Preferring CALL")

    def cmd_save_open():
        results = []
        for c in tv_results.get_children():
            values = tuple(tv_results.item(c)["values"])
            results.append(values)
        out_file = template.render(title=title, subtitle=v_title.get(), headings=headings, rows=results)
        with open("output.html", "w") as f:
            f.write(out_file)
        webbrowser.open("output.html")

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
    btn_all = ttk.Button(frm_filters, text="All", command=cmd_update_all, bootstyle=bootstyle)
    btn_all.pack(side="left", padx=4, pady=4)

    btn_text = ttk.Button(frm_filters, text="Text preference", command=cmd_update_texters, bootstyle=bootstyle)
    btn_text.pack(side="left", padx=4, pady=4)

    btn_call = ttk.Button(frm_filters, text="Call preference", command=cmd_update_callers, bootstyle=bootstyle)
    btn_call.pack(side="left", padx=4, pady=4)

    # Title controls
    lbl_title = ttk.Label(frm_title, textvariable=v_title)
    lbl_title.pack(side="left", padx=4, pady=4)

    # TV controls
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv_results = ttk.Treeview(frm_tv, show="headings", columns=headings, yscrollcommand=tv_sb.set)
    for s in headings:
        tv_results.heading(s, text=s, anchor=W)
    tv_results.pack(padx=4, pady=4, fill="both")
    tv_sb.configure(command=tv_results.yview)
    tv_results.tag_configure('oddrow', background="#000000")
    tv_results.tag_configure('evenrow', background="#151515")

    # Save Options controls
    btn_save_open = ttk.Button(frm_save_options, text="Save and Open", bootstyle=bootstyle, command=cmd_save_open)
    btn_save_open.pack(side="left", padx=4, pady=4)

    # On open commands
    cmd_update_all()