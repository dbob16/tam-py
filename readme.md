# Introduction

TAM-PY is the Python version of the Ticket Auction Manager application I originally developed in Microsoft Access. It also uses MariaDB for the backend database.

# System Requirements

- Server
    - Windows or Linux
    - MariaDB installed and set up
    - 2GB of RAM (Command-line Linux), 4GB (Windows or Linux with a Desktop Environment)
    - At least 4GB of storage
- Client
    - Any OS that can run Python with ttkbootstrap, mariadb, and jinja2 pip modules
    - 4GB of RAM
    - At least 2GB of storage
    - A Desktop Environment or Window Manager if on Linux

# Prerequisites

- Server
    - A MariaDB Server instance with a root-level user
    - The ability to download and run the install script in the server directory
- Client
    - Python with the following pip packages
        - ttkbootstrap
        - mariadb
        - jinja2

# How to use

Setup virtual environment and install the above pip packages using the guide [here](https://docs.python.org/3/library/venv.html), and run server-init.py on the server machine which has MariaDB installed.

Launch using the "python run_client.py" with the venv activated.

When the main menu comes up, click the Edit Session in the corner. Then specify the server's hostname or IP, port, username, password, and database. I'd recommend using the admin on the first one. Click Save. Then click Refresh to the right of the dropdown, which should bring in the new credentials.

Then click Edit on the right of the dropdown. Using this dialog you'll specify the ticket/item types, its bootstyle, laid out below (ttkbootstrap theme I selected), and then click Add Prefix. So for instance, if your event has "regular" tickets/items, and "specialty" tickets/items, you will specify one for regular, one for specialty, whichever bootstyle you want for each.

![ttkbootstrap cyborg theme cardlet](https://ttkbootstrap.readthedocs.io/en/latest/assets/themes/cyborg.png)

Keep in mind, creating a prefix generates an isolated tableset which can't cross reference from other tablesets/prefixes.

Once that is setup, you can click close. Then click Refresh again. The prefixes you created should be available on the dropdown. Click the dropdown and select the Prefix you want to edit.

From then on out, it's just a matter of changing the prefix when you need to, and then clicking what you want to edit in the Forms section.

- **Tickets**: Edits the First Name, Last Name, Phone Number, and contact preference of ticket buyers.
- **Baskets**: Edits the Basket Description and Donors of the baskets/items.
- **Drawing**: Edits the winning ticket number of the baskets/items, and shows you the winner if one is found.

After all the ticket buyers and winning numbers are entered, reports can be generated using the buttons in the Reports section. The dialog that comes up after can be used to filter by contact preference. Click Save and Open to generate the report in HTML format, and open it in your default web browser. Then you can print or save it using your default web browser.