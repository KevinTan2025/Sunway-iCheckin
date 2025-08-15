import threading
import tkinter as tk
from tkinter import ttk
from sunway_checkin import load_user_agents, load_users, checkin_user, save_users


# Helper: create a rounded card-like panel using Canvas
def create_rounded_card(parent, width=None, height=None, radius=16, bg="#F0EDFF", border_color="#AEA7CF", border_width=1):
    canvas = tk.Canvas(parent, bd=0, highlightthickness=0, relief='flat', bg=parent.cget('bg'))
    if width and height:
        canvas.configure(width=width, height=height)
    
    w = width or 400
    h = height or 60
    x1, y1, x2, y2 = border_width, border_width, w - border_width, h - border_width
    r = radius
    
    # Draw rounded rectangle with shadow effect
    try:
        # Shadow (offset)
        shadow_offset = 2
        canvas.create_arc(x1+shadow_offset, y1+shadow_offset, x1+shadow_offset + 2*r, y1+shadow_offset + 2*r, 
                         start=90, extent=90, fill="#E0E0E0", outline="")
        canvas.create_arc(x2+shadow_offset - 2*r, y1+shadow_offset, x2+shadow_offset, y1+shadow_offset + 2*r, 
                         start=0, extent=90, fill="#E0E0E0", outline="")
        canvas.create_arc(x1+shadow_offset, y2+shadow_offset - 2*r, x1+shadow_offset + 2*r, y2+shadow_offset, 
                         start=180, extent=90, fill="#E0E0E0", outline="")
        canvas.create_arc(x2+shadow_offset - 2*r, y2+shadow_offset - 2*r, x2+shadow_offset, y2+shadow_offset, 
                         start=270, extent=90, fill="#E0E0E0", outline="")
        canvas.create_rectangle(x1+shadow_offset + r, y1+shadow_offset, x2+shadow_offset - r, y2+shadow_offset, 
                               fill="#E0E0E0", outline="")
        canvas.create_rectangle(x1+shadow_offset, y1+shadow_offset + r, x2+shadow_offset, y2+shadow_offset - r, 
                               fill="#E0E0E0", outline="")
        
        # Main card
        canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=bg, outline=border_color, width=border_width)
        canvas.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=bg, outline=border_color, width=border_width)
        canvas.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=bg, outline=border_color, width=border_width)
        canvas.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=bg, outline=border_color, width=border_width)
        canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=bg, outline="")
        canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=bg, outline="")
        
        # Border lines
        canvas.create_line(x1 + r, y1, x2 - r, y1, fill=border_color, width=border_width)
        canvas.create_line(x1 + r, y2, x2 - r, y2, fill=border_color, width=border_width)
        canvas.create_line(x1, y1 + r, x1, y2 - r, fill=border_color, width=border_width)
        canvas.create_line(x2, y1 + r, x2, y2 - r, fill=border_color, width=border_width)
        
    except Exception:
        # Fallback
        canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline=border_color, width=border_width)

    frame = tk.Frame(canvas, bg=bg)
    canvas.create_window((w/2, h/2), window=frame, width=w - 20, height=h - 20)
    return canvas, frame


class UserCard:
    def __init__(self, parent, row, data=None):
        self.var = tk.BooleanVar(value=True)
        
        # Create individual card for each user (smaller size)
        self.card_canvas, self.card_frame = create_rounded_card(parent, width=480, height=60, 
                                                               bg="#F0EDFF", border_color="#AEA7CF")
        self.card_canvas.pack(pady=4, padx=12, fill='x')
        
        # Checkbox with purple styling (smaller)
        self.cb = tk.Checkbutton(self.card_frame, variable=self.var, bg="#F0EDFF", 
                                fg="#351ABA", selectcolor="#8A70FA", 
                                activebackground="#F0EDFF", bd=0, font=("Segoe UI", 9))
        self.cb.pack(side='left', padx=6)
        
        # Entry fields with modern styling (smaller)
        entry_style = {"bg": "#FFFFFF", "fg": "#180E47", "bd": 0, "relief": "flat",
                      "font": ("Segoe UI", 9), "insertbackground": "#8A70FA"}
        
        # Create a sub-frame for inputs
        input_frame = tk.Frame(self.card_frame, bg="#F0EDFF")
        input_frame.pack(side='left', expand=True, fill='both', padx=6)
        
        # ID field (smaller)
        id_frame = tk.Frame(input_frame, bg="#F0EDFF")
        id_frame.pack(side='left', padx=3)
        tk.Label(id_frame, text="ID:", bg="#F0EDFF", fg="#351ABA", font=("Segoe UI", 7)).pack()
        self.id_entry = tk.Entry(id_frame, width=10, **entry_style)
        self.id_entry.pack()
        
        # Password field (smaller)
        pw_frame = tk.Frame(input_frame, bg="#F0EDFF")
        pw_frame.pack(side='left', padx=3)
        tk.Label(pw_frame, text="Password:", bg="#F0EDFF", fg="#351ABA", font=("Segoe UI", 7)).pack()
        self.pw_entry = tk.Entry(pw_frame, width=10, show="*", **entry_style)
        self.pw_entry.pack()
        
        # Memo field (smaller)
        memo_frame = tk.Frame(input_frame, bg="#F0EDFF")
        memo_frame.pack(side='left', padx=3)
        tk.Label(memo_frame, text="Memo:", bg="#F0EDFF", fg="#351ABA", font=("Segoe UI", 7)).pack()
        self.memo_entry = tk.Entry(memo_frame, width=12, **entry_style)
        self.memo_entry.pack()
        
        # Status with pill-shaped background (smaller)
        self.status_label = tk.Label(self.card_frame, text="Idle", bg="#AEA7CF", fg="#180E47", 
                                    width=12, anchor="center", pady=2, 
                                    font=("Segoe UI", 8, "bold"), relief='flat')
        self.status_label.pack(side='right', padx=6)

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

    def set_status(self, state, text=None):
        """Set visual status for the row.
        state: 'success', 'already', 'error', 'invalid', 'info', 'idle'
        """
        if not text:
            if state == 'success':
                text = '✅ Checked in'
            elif state == 'already':
                text = '⚠️ Already checked in'
            elif state == 'error':
                text = '❌ Login failed'
            elif state == 'invalid':
                text = '❌ Invalid code'
            elif state == 'info':
                text = '⏳ Checking in...'
            else:
                text = 'Idle'

        color_map = {
            'success': '#8A70FA',
            'already': '#AEA7CF', 
            'error': '#351ABA',
            'invalid': '#351ABA',
            'info': '#AEA7CF',
            'idle': '#AEA7CF',
        }
        bg = color_map.get(state, '#AEA7CF')
        # Update label background and text with appropriate contrast
        text_color = '#F0EDFF' if state in ['success', 'error', 'invalid'] else '#180E47'
        try:
            self.status_label.config(bg=bg, text=text, fg=text_color)
        except Exception:
            # Fallback if theming prevents bg change
            self.status_label.config(text=text)

    def destroy(self):
        self.cb.destroy()
        self.id_entry.destroy()
        self.pw_entry.destroy()
        self.memo_entry.destroy()
        self.status_label.destroy()
        self.card_canvas.destroy()


class App:
    def __init__(self, master):
        self.master = master
        master.title("Sunway iCheckIn - Modern Edition")

        # Modern font and spacing with purple theme (smaller)
        default_font = ("Segoe UI", 10)
        master.option_add("*Font", default_font)

        # Set main window background to gradient-like purple (smaller padding)
        master.configure(padx=16, pady=16, bg="#180E47")

        # Main container with scrollable area
        main_frame = tk.Frame(master, bg="#180E47")
        main_frame.pack(fill='both', expand=True)

        # Header section with modern design (smaller)
        header_frame = tk.Frame(main_frame, bg="#180E47")
        header_frame.pack(fill='x', pady=(0, 12))
        
        title_label = tk.Label(header_frame, text="Sunway iCheckIn", 
                              font=("Segoe UI", 18, "bold"), 
                              fg="#F0EDFF", bg="#180E47")
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(header_frame, text="Modern bulk check-in management", 
                                 font=("Segoe UI", 10), 
                                 fg="#AEA7CF", bg="#180E47")
        subtitle_label.pack(anchor='w', pady=(2, 0))

        # Code input section with card design (smaller)
        code_section = tk.Frame(main_frame, bg="#180E47")
        code_section.pack(fill='x', pady=(0, 16))
        
        code_card_canvas, code_card_frame = create_rounded_card(code_section, width=320, height=60, 
                                                               bg="#F0EDFF", border_color="#8A70FA")
        code_card_canvas.pack(anchor='w')
        
        tk.Label(code_card_frame, text="Check-in Code", bg="#F0EDFF", fg="#351ABA", 
                font=("Segoe UI", 10, "bold")).pack(pady=(6, 2))
        
        self.code_entry = tk.Entry(code_card_frame, width=20, bg="#FFFFFF", fg="#180E47", 
                                  font=("Segoe UI", 12), bd=0, relief='flat', 
                                  insertbackground="#8A70FA")
        self.code_entry.pack(pady=(0, 6))
        self.code_entry.focus_set()

        # Users section (smaller)
        users_frame = tk.Frame(main_frame, bg="#180E47")
        users_frame.pack(fill='both', expand=True, pady=(0, 12))
        
        # Users header (smaller)
        users_header = tk.Frame(users_frame, bg="#180E47")
        users_header.pack(fill='x', pady=(0, 10))
        
        tk.Label(users_header, text="User Accounts", 
                font=("Segoe UI", 13, "bold"), 
                fg="#F0EDFF", bg="#180E47").pack(side='left')

        # Scrollable users area
        self.users_canvas = tk.Canvas(users_frame, bg="#180E47", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(users_frame, orient="vertical", command=self.users_canvas.yview)
        self.scrollable_frame = tk.Frame(self.users_canvas, bg="#180E47")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all"))
        )

        self.users_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.users_canvas.configure(yscrollcommand=scrollbar.set)

        self.users_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.rows = []
        for user in load_users():
            self.add_row(user)

        # Controls section with modern buttons (smaller)
        controls_frame = tk.Frame(main_frame, bg="#180E47")
        controls_frame.pack(fill='x', pady=(0, 12))
        
        # Button styling (smaller)
        btn_style = {"bg": "#8A70FA", "fg": "#F0EDFF", "font": ("Segoe UI", 9, "bold"),
                     "bd": 0, "relief": "flat", "padx": 15, "pady": 6, "cursor": "hand2"}
        
        btn_frame_left = tk.Frame(controls_frame, bg="#180E47")
        btn_frame_left.pack(side='left')
        
        self.add_btn = tk.Button(btn_frame_left, text="➕ Add User", command=self.add_row, **btn_style)
        self.add_btn.pack(side="left", padx=(0, 8))
        
        self.remove_btn = tk.Button(btn_frame_left, text="🗑️ Remove Selected", command=self.remove_rows, **btn_style)
        self.remove_btn.pack(side="left", padx=(0, 8))
        
        self.save_btn = tk.Button(btn_frame_left, text="💾 Save Users", command=self.save_users_file, **btn_style)
        self.save_btn.pack(side="left", padx=(0, 8))
        
        # Start button with special styling (smaller)
        start_btn_style = btn_style.copy()
        start_btn_style.update({"bg": "#351ABA", "fg": "#F0EDFF"})
        self.start_btn = tk.Button(btn_frame_left, text="🚀 Start Check-In", command=self.start_checkin, **start_btn_style)
        self.start_btn.pack(side="left", padx=(8, 0))

        # Log section with card design (smaller)
        log_section = tk.Frame(main_frame, bg="#180E47")
        log_section.pack(fill='both', expand=True)
        
        tk.Label(log_section, text="Activity Log", 
                font=("Segoe UI", 12, "bold"), 
                fg="#F0EDFF", bg="#180E47").pack(anchor='w', pady=(0, 8))
        
        log_card_canvas, log_card_frame = create_rounded_card(log_section, width=600, height=150, 
                                                             bg="#F0EDFF", border_color="#AEA7CF")
        log_card_canvas.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_card_frame, bd=0, highlightthickness=0,
                               bg="#FFFFFF", fg="#180E47", font=("Consolas", 9))
        self.log_text.pack(fill='both', expand=True, padx=6, pady=6)
        self.log_text.config(state=tk.DISABLED)
        self._configure_log_tags()

        # Status bar (smaller)
        status_frame = tk.Frame(main_frame, bg="#180E47")
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready to check in")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, bg="#180E47", 
                                    fg="#AEA7CF", font=("Segoe UI", 9))
        self.status_label.pack(side='left')

        # Legend (smaller)
        legend_frame = tk.Frame(status_frame, bg="#180E47")
        legend_frame.pack(side='right')
        self._create_legend(legend_frame)

        self.user_agents = load_user_agents()

    def _configure_log_tags(self):
        # Create text tags for colored log messages using the purple color palette
        self.log_text.tag_config('info', foreground='#8A70FA')
        self.log_text.tag_config('success', foreground='#351ABA')
        self.log_text.tag_config('warning', foreground='#AEA7CF')
        self.log_text.tag_config('error', foreground='#180E47')
        self.log_text.tag_config('default', foreground='#180E47')

    def _create_legend(self, parent):
        # Modern legend using the purple color palette
        legends = [('#8A70FA', 'Success'), ('#AEA7CF', 'Already'), ('#351ABA', 'Error')]
        for color, label in legends:
            # Create small colored indicators
            indicator = tk.Label(parent, bg=color, width=3, height=1, relief='flat')
            indicator.pack(side='left', padx=(8, 2))
            legend_label = tk.Label(parent, text=label, bg="#180E47", fg="#AEA7CF", 
                                  font=("Segoe UI", 9))
            legend_label.pack(side='left', padx=(0, 8))

    def add_row(self, data=None):
        row = UserCard(self.scrollable_frame, len(self.rows), data)
        self.rows.append(row)

    def remove_rows(self):
        for row in reversed(self.rows):
            if row.var.get():
                row.destroy()
                self.rows.remove(row)

    def refresh_rows(self):
        # Not needed with the new card layout - they auto-arrange
        pass

    def _insert_log(self, message, level='default'):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert('end', message + '\n', level)
        self.log_text.see('end')
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(message)

    def log(self, message):
        # Determine tag by content
        msg = message.lower()
        if 'error' in msg or 'failed' in msg or 'not valid' in msg:
            tag = 'error'
        elif 'already checked in' in msg or 'have already checked in' in msg:
            tag = 'warning'
        elif 'checked in successfully' in msg or 'checked in' in msg and 'failed' not in msg:
            tag = 'success'
        elif 'checking in' in msg or 'trying to login' in msg:
            tag = 'info'
        else:
            tag = 'default'
        self._insert_log(message, tag)

    def save_users_file(self):
        users = [row.get_user() for row in self.rows]
        save_users(users)
        self.status_var.set("Users saved successfully")

    def start_checkin(self):
        selected_rows = [row for row in self.rows if row.var.get()]
        selected_users = [row.get_user() for row in selected_rows]
        code = self.code_entry.get().strip()
        if not selected_users or not code:
            self.log("❌ No users selected or check-in code is empty")
            return
        # Disable UI while running
        self._set_controls_state('disabled')
        self.status_var.set("⏳ Starting check-in process...")
        threading.Thread(target=self._run_checkin, args=(selected_rows, selected_users, code), daemon=True).start()

    def _set_controls_state(self, state):
        for widget in (self.add_btn, self.remove_btn, self.save_btn, self.start_btn, self.code_entry):
            try:
                widget.config(state=state)
            except Exception:
                pass

    def _run_checkin(self, rows, users, code):
        for row, user in zip(rows, users):
            # mark row as in-progress
            row.set_status('info', '⏳ Checking in...')

            # Create a per-row logger to parse messages and update status label
            def make_logger(r):
                def _logger(msg):
                    self.log(msg)
                    m = msg.lower()
                    if 'checked in successfully' in m:
                        r.set_status('success', None)
                    elif 'has already checked in' in m or 'have already checked in' in m:
                        r.set_status('already', None)
                    elif 'login failed' in m or 'may have failed to login' in m or ('invalid' in m and 'login' in m):
                        r.set_status('error', None)
                    elif 'not valid' in m or 'not in this class' in m or ('check-in failed' in m and 'not' in m):
                        r.set_status('invalid', None)
                return _logger

            logger = make_logger(row)
            try:
                checkin_user(user, code, self.user_agents, log=logger)
            except Exception as e:
                logger(f"❌ Unexpected error for {user.get('id')}: {e}")
                row.set_status('error', '❌ Error')

        self.status_var.set("✅ Check-in process completed")
        self._set_controls_state('normal')

    def on_close(self):
        self.save_users_file()
        self.master.destroy()


def main():
    root = tk.Tk()
    
    # Set smaller window size and center it
    window_width = 650
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Modern window styling
    try:
        root.attributes('-transparentcolor', '')  # Remove any transparency
    except Exception:
        pass
    
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
