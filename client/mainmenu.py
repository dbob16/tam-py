import ttkbootstrap as ttk 
from .forms import ticket_form, basket_form, drawing_form, report_form
from .db import session_writer
from .editprefixes import edit_form
from .models import PrefixTable, PermChecker

def mainmenu():
    root = ttk.Window(title="Ticket Auction Manager", themename="cyborg")
    current_prefix = {}
    prefix_table = PrefixTable()
    v_status = ttk.StringVar(root)

    # Commands
    def cmd_check_perms():
        try:
            perm_checker = PermChecker()
            is_admin = perm_checker.check_admin()
            if is_admin > 0:
                btn_edit.configure(state="normal")
            else:
                btn_edit.configure(state="disabled")
        except:
            pass

    def cmd_update():
        try:
            results = prefix_table.select_all()
            l = [r[0].capitalize() for r in results]
            cmb_prefixselect.configure(values=l)
            if len(l) > 0:
                cmb_prefixselect.set(l[0])
            v_status.set("Online")
            lbl_status.configure(bootstyle="success")
        except:
            cmb_prefixselect.set("No Valid DB config")
            v_status.set("Offline: Check config <")
            lbl_status.configure(bootstyle="danger")

    def cmd_style_set(_=None):
        try:
            result = prefix_table.select(cmb_prefixselect.get().lower())
            if len(result) == 2:
                current_prefix["prefix"], current_prefix["bootstyle"] = result[0], result[1]
                for e in stl_elements:
                    e.configure(bootstyle=current_prefix["bootstyle"])
        except:
            pass

    def cmd_edit_prefixes():
        edit_form()

    def cmd_edit_session():
        session_writer()

    def cmd_ticket_form():
        ticket_form(current_prefix["prefix"], current_prefix["bootstyle"])

    def cmd_basket_form():
        basket_form(current_prefix["prefix"], current_prefix["bootstyle"])

    def cmd_drawing_form():
        drawing_form(current_prefix["prefix"], current_prefix["bootstyle"])
    
    def cmd_name_report():
        report_form(current_prefix["prefix"], current_prefix["bootstyle"], "name")

    def cmd_basket_report():
        report_form(current_prefix["prefix"], current_prefix["bootstyle"], "basket")

    # Frames
    frm_prefixes = ttk.LabelFrame(root, text="Prefixes")
    frm_prefixes.pack(side="top", padx=4, pady=4, fill="x")

    frm_forms = ttk.LabelFrame(root, text="Forms")
    frm_forms.pack(side="top", padx=4, pady=4, fill="x")

    frm_reports = ttk.LabelFrame(root, text="Reports")
    frm_reports.pack(side="top", padx=4, pady=4, fill="x")

    frm_statusbar = ttk.Frame(root)
    frm_statusbar.pack(side="bottom", padx=4, pady=4, fill="x")

    # Prefix controls
    cmb_prefixselect = ttk.Combobox(frm_prefixes, state="readonly")
    cmb_prefixselect.grid(row=0, column=0, padx=4, pady=4)

    btn_refresh = ttk.Button(frm_prefixes, text="Refresh", command=cmd_update)
    btn_refresh.grid(row=0, column=1, padx=4, pady=4)

    btn_edit = ttk.Button(frm_prefixes, text="Edit", command=edit_form)
    btn_edit.grid(row=0, column=2, padx=4, pady=4)

    # Forms controls
    btn_tickets = ttk.Button(frm_forms, text="Tickets", width=25, command=cmd_ticket_form)
    btn_tickets.grid(row=0, column=0, padx=4, pady=4)

    btn_baskets = ttk.Button(frm_forms, text="Baskets", width=25, command=cmd_basket_form)
    btn_baskets.grid(row=0, column=1, padx=4, pady=4)

    btn_drawing = ttk.Button(frm_forms, text="Drawing", command=cmd_drawing_form)
    btn_drawing.grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

    # Reports controls
    btn_r_lastname = ttk.Button(frm_reports, text="Winners by Last Name", width=25, command=cmd_name_report)
    btn_r_lastname.grid(row=0, column=0, padx=4, pady=4)

    btn_r_sequence = ttk.Button(frm_reports, text="Winners by Basket #", width=25, command=cmd_basket_report)
    btn_r_sequence.grid(row=0, column=1, padx=4, pady=4)

    # Statusbar Controls
    btn_edit_session = ttk.Button(frm_statusbar, text="Edit Session", command=cmd_edit_session)
    btn_edit_session.pack(side="left", padx=4, pady=4)

    lbl_status = ttk.Label(frm_statusbar, textvariable=v_status)
    lbl_status.pack(side="left", padx=4, pady=4)

    lbl_attr = ttk.Label(frm_statusbar, text="TAM by Dilan Gilluly")
    lbl_attr.pack(side="right", padx=4, pady=4)

    # Automation jobs
    cmd_update()

    stl_elements = (btn_baskets, btn_drawing, btn_r_lastname, btn_r_sequence, btn_tickets)
    cmb_prefixselect.bind("<<ComboboxSelected>>", cmd_style_set)
    cmd_style_set()

    cmd_check_perms()

    root.mainloop()

if __name__ == "__main__":
    mainmenu()