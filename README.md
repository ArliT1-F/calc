# Euro → Lek Conversion Board

A native Linux desktop GUI showing fixed conversions for **€5, €10, €20, €50, €100 and €200**. The initial exchange rate is **1 EUR = 88 ALL**.

## Run

Install Python 3 and Tkinter (on Debian/Ubuntu: `sudo apt install python3 python3-tk`), then run:

```bash
python3 app.py
```

Click the **⚙ gear** to change the lek-per-euro rate (for example, `86`), then click **Save rate** or press Enter. The board only updates when you save; cancelling or closing settings leaves it unchanged. The saved rate is remembered across launches in `$XDG_CONFIG_HOME/euro-lek-board/settings.json` (or `~/.config/euro-lek-board/settings.json`). No network connection or third-party Python packages are needed.

Run the headless logic tests with `python3 -m unittest discover -s tests`.

## Start automatically when you log in

From this repository directory, run:

```bash
python3 startup.py
```

This installs a launcher in your application menu and an XDG autostart entry for your **user account**. The board opens at your next graphical desktop login (GNOME, KDE, Xfce, and other desktops that support XDG autostart). You can also launch it from the application menu as **Euro to Lek Board**. Keep this repository at the same location: the launcher points to its `app.py` file. This does not run the app as a system service or before graphical login.

To stop automatic startup and remove the menu entry:

```bash
python3 startup.py --uninstall
```

Uninstalling the launcher leaves your saved exchange rate intact. No `sudo` is needed for the startup setup.
