import threading
import tkinter as tk
from tkinter import ttk
from sunway_checkin import load_user_agents, load_users, checkin_user, save_users


class UserRow:
    def __init__(self, parent, row, data=None):
        self.var = tk.BooleanVar(value=True)
        self.cb = ttk.Checkbutton(parent, variable=self.var)
        self.cb.grid(row=row, column=0, padx=2, pady=2)
        self.id_entry = ttk.Entry(parent, width=15)
        self.id_entry.grid(row=row, column=1, padx=2, pady=2)
        self.pw_entry = ttk.Entry(parent, width=15, show="*")
        self.pw_entry.grid(row=row, column=2, padx=2, pady=2)
        self.memo_entry = ttk.Entry(parent, width=20)
        self.memo_entry.grid(row=row, column=3, padx=2, pady=2)
        if data:
            self.id_entry.insert(0, data.get('id', ''))
            self.pw_entry.insert(0, data.get('password', ''))
            self.memo_entry.insert(0, data.get('memo', ''))

    def get_user(self):
        return {
            'id': self.id_entry.get(),
            'password': self.pw_entry.get(),
            'memo': self.memo_entry.get(),
        }

    def destroy(self):
        self.cb.destroy()
        self.id_entry.destroy()
        self.pw_entry.destroy()
        self.memo_entry.destroy()


class App:
    def __init__(self, master):
        self.master = master
        master.title("Sunway iCheckIn")

        style = ttk.Style(master)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        ttk.Label(master, text="Check-in Code:").grid(row=0, column=0, sticky="e")
        self.code_entry = ttk.Entry(master, width=20)
        self.code_entry.grid(row=0, column=1, sticky="w")
        self.code_entry.focus_set()

        self.table_frame = ttk.Frame(master)
        self.table_frame.grid(row=1, column=0, columnspan=4, pady=10)

        headers = ["Select", "Username", "Password", "Memo"]
        for idx, h in enumerate(headers):
            ttk.Label(self.table_frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=idx)

        self.rows = []
        for user in load_users():
            self.add_row(user)

        self.btn_frame = ttk.Frame(master)
        self.btn_frame.grid(row=2, column=0, columnspan=4, pady=5)
        ttk.Button(self.btn_frame, text="Add Row", command=self.add_row).pack(side="left", padx=5)
        ttk.Button(self.btn_frame, text="Remove Row", command=self.remove_rows).pack(side="left", padx=5)
        ttk.Button(self.btn_frame, text="Save Users", command=self.save_users_file).pack(side="left", padx=5)
        ttk.Button(self.btn_frame, text="Start Check-In", command=self.start_checkin).pack(side="left", padx=5)

        self.log_text = tk.Text(master, height=15, width=60)
        self.log_text.grid(row=3, column=0, columnspan=4, pady=10)
        self.log_text.config(state=tk.DISABLED)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(master, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=4, sticky="w", padx=5, pady=(0,5))

        self.user_agents = load_user_agents()

    def add_row(self, data=None):
        row_index = len(self.rows) + 1
        row = UserRow(self.table_frame, row_index, data)
        self.rows.append(row)

    def remove_rows(self):
        for row in reversed(self.rows):
            if row.var.get():
                row.destroy()
                self.rows.remove(row)
        self.refresh_rows()

    def refresh_rows(self):
        for idx, row in enumerate(self.rows, start=1):
            row.cb.grid(row=idx, column=0)
            row.id_entry.grid(row=idx, column=1)
            row.pw_entry.grid(row=idx, column=2)
            row.memo_entry.grid(row=idx, column=3)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(message)

    def save_users_file(self):
        users = [row.get_user() for row in self.rows]
        save_users(users)
        self.status_var.set("Users saved")

    def start_checkin(self):
        selected_users = [row.get_user() for row in self.rows if row.var.get()]
        code = self.code_entry.get().strip()
        if not selected_users or not code:
            self.log("No users selected or code is empty")
            return
        self.status_var.set("Checking in...")
        threading.Thread(target=self._run_checkin, args=(selected_users, code), daemon=True).start()

    def _run_checkin(self, users, code):
        for user in users:
            checkin_user(user, code, self.user_agents, log=self.log)
        self.status_var.set("Done")

    def on_close(self):
        self.save_users_file()
        self.master.destroy()


def main():
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
