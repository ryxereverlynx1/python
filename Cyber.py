

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import datetime
import os
import re
import random
import string



LOG_FILE = "security_audit_log.txt"
PASSWORD_FILE = "encrypted_credentials.txt"


FONT_MAIN = ("Helvetica", 11)
FONT_H1 = ("Helvetica", 20, "bold")
FONT_H2 = ("Helvetica", 14, "bold")
FONT_BOLD = ("Helvetica", 11, "bold")
FONT_MONO = ("Consolas", 11)
FONT_SMALL = ("Helvetica", 10)


DARK_THEME = {
    "bg":         "#1e1e1e",
    "panel":      "#252526",
    "card":       "#2d2d30",
    "border":     "#3e3e42",
    "accent":     "#007acc",
    "accent2":    "#4CAF50",
    "warning":    "#d32f2f",
    "text":       "#cccccc",
    "subtext":    "#9e9e9e",
    "input_bg":   "#3c3c3c",
}

LIGHT_THEME = {
    "bg":         "#f3f3f3",
    "panel":      "#ffffff",
    "card":       "#ffffff",
    "border":     "#e0e0e0",
    "accent":     "#005a9e",
    "accent2":    "#2e7d32",
    "warning":    "#c62828",
    "text":       "#333333",
    "subtext":    "#666666",
    "input_bg":   "#f9f9f9",
}

T = dict(DARK_THEME)



SAFETY_TIPS = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■  ENTERPRISE SAFE BROWSING PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Ensure TLS/SSL (HTTPS) is active before transmitting confidential data.
• Scrutinize domain spelling to prevent Typosquatting attacks.
• Utilize enterprise-approved ad-blocking and anti-tracking extensions.
• Restrict software downloads to approved, official vendor repositories.
• Routinely clear session tokens and cache on shared workstations.
• Utilize isolated browsing instances (Incognito/Private) for unverified sites.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■  IDENTIFYING SOCIAL ENGINEERING & PHISHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ARTIFICIAL URGENCY: Malicious actors manufacture deadlines to force errors.
• FALSE AUTHORITY: Verify requests from executives or IT via out-of-band channels.
• GENERIC SALUTATIONS: Legitimate vendors typically utilize personalized data.
• OBFUSCATED URIS: Hover over hyperlinks to verify the exact destination domain.
• CREDENTIAL HARVESTING: IT will never request your password or MFA tokens.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■  DATA PRIVACY & CREDENTIAL HYGIENE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Enforce complex, unique passwords for every active service.
• Mandate Multi-Factor Authentication (MFA) across all external accounts.
• Audit application permissions regularly (Camera, Microphone, Location).
• Monitor breached credential databases for compromised enterprise addresses.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■  THREAT LANDSCAPE OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• PHISHING: Deceptive communications designed to harvest authentication tokens.
• RANSOMWARE: Cryptovirology attacks that encrypt assets for extortion.
• MITM (Man-in-the-Middle): Interception of unencrypted network traffic.
• SOCIAL ENGINEERING: Psychological manipulation to bypass technical controls.
"""



SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".scr", ".vbs", ".cmd", ".com", ".pif", ".msi", ".ps1", ".jar", ".wsf"]
DOUBLE_EXTENSION_PATTERN = re.compile(r'\.(jpg|jpeg|png|gif|pdf|doc|docx|txt|mp3|mp4|csv)\.(exe|bat|scr|vbs|cmd|com|pif)$', re.IGNORECASE)



BADGES = {
    "phishing_expert":  ("🛡️ Threat Analyst",      "Conducted a message threat analysis"),
    "strong_password":  ("🔐 Credential Auditor",  "Evaluated a high-entropy password"),
    "password_creator": ("🔑 Vault Administrator", "Generated a secure credential"),
    "file_detective":   ("📁 Integrity Specialist","Executed a local file integrity scan"),
    "tips_reader":      ("📘 Policy Reviewer",     "Reviewed enterprise security protocols"),
}

def log_activity(entry: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {entry}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except IOError:
        pass 



class CyberShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberShield Enterprise — Security & Awareness Platform")
        self.geometry("1150x750")
        self.minsize(950, 650)
        self.configure(bg=T["bg"])

        self.dark_mode = True
        self.earned_badges = set()

        self._build_layout()
        self.show_page("dashboard")
        log_activity("System initialization complete. Session started.")

    def _build_layout(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(self, bg=T["panel"], width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.content = tk.Frame(self, bg=T["bg"])
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self._build_sidebar()
        self.pages: dict[str, tk.Frame] = {}
        self._register_pages()

    def _build_sidebar(self):
        sb = self.sidebar

        logo_frame = tk.Frame(sb, bg=T["accent"], height=70)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="CyberShield", font=("Helvetica", 16, "bold"),
                 bg=T["accent"], fg="#ffffff").pack(pady=(15, 0))
        tk.Label(logo_frame, text="ENTERPRISE EDITION", font=("Helvetica", 8, "bold"),
                 bg=T["accent"], fg="#e0e0e0").pack()

        tk.Frame(sb, bg=T["border"], height=1).pack(fill="x")

        nav_items = [
            ("■  System Dashboard",       "dashboard"),
            ("■  Message Analyzer",        "phishing"),
            ("■  Credential Security",     "password"),
            ("■  File Integrity Scan",     "file_detect"),
            ("■  Security Protocols",      "tips"),
            ("■  Audit Logs",              "log"),
            ("■  Compliance Metrics",      "badges"),
        ]

        self.nav_buttons = {}
        tk.Frame(sb, bg=T["panel"], height=10).pack() 
        
        for label, page_id in nav_items:
            btn = tk.Button(
                sb, text=label, anchor="w", padx=25, pady=8,
                font=FONT_MAIN, relief="flat", cursor="hand2",
                bg=T["panel"], fg=T["text"], activebackground=T["border"],
                activeforeground=T["text"],
                command=lambda pid=page_id: self.show_page(pid)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[page_id] = btn

        tk.Frame(sb, bg=T["panel"]).pack(fill="both", expand=True)

        tk.Frame(sb, bg=T["border"], height=1).pack(fill="x")
        self.theme_btn = tk.Button(
            sb, text="Toggle UI Theme", font=FONT_SMALL,
            relief="flat", cursor="hand2", bg=T["panel"], fg=T["subtext"],
            pady=15, command=self.toggle_theme
        )
        self.theme_btn.pack(fill="x")

    def _register_pages(self):
        page_classes = {
            "dashboard":   DashboardPage,
            "phishing":    PhishingDetectorPage,
            "password":    PasswordPage,
            "file_detect": FileDetectPage,
            "tips":        TipsPage,
            "log":         LogPage,
            "badges":      BadgesPage,
        }
        for pid, cls in page_classes.items():
            page = cls(self.content, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[pid] = page

    def show_page(self, page_id: str):
        page = self.pages.get(page_id)
        if page:
            page.tkraise()
            page.on_show()
        for pid, btn in self.nav_buttons.items():
            if pid == page_id:
                btn.config(bg=T["card"], fg=T["accent"], font=FONT_BOLD)
            else:
                btn.config(bg=T["panel"], fg=T["text"], font=FONT_MAIN)

    def toggle_theme(self):
        global T
        self.dark_mode = not self.dark_mode
        T.update(DARK_THEME if self.dark_mode else LIGHT_THEME)
        self._apply_theme_recursive(self)
        for page in self.pages.values():
            page.apply_theme()

    def _apply_theme_recursive(self, widget):
        try:
            wclass = widget.winfo_class()
            if wclass in ("Frame", "Toplevel", "Tk"):
                widget.config(bg=T["bg"])
            elif wclass == "Label":
                widget.config(bg=widget.master.cget("bg") if widget.master else T["bg"], fg=T["text"])
            elif wclass == "Button":
                if widget.cget("text") != "CyberShield": 
                    widget.config(bg=T["panel"], fg=T["text"])
            elif wclass == "Text":
                widget.config(bg=T["input_bg"], fg=T["text"], insertbackground=T["text"])
            elif wclass == "Entry":
                widget.config(bg=T["input_bg"], fg=T["text"], insertbackground=T["text"])
        except Exception:
            pass
        for child in widget.winfo_children():
            self._apply_theme_recursive(child)

    def award_badge(self, badge_id: str):
        if badge_id not in self.earned_badges:
            self.earned_badges.add(badge_id)
            name, desc = BADGES[badge_id]
            log_activity(f"Compliance metric recorded: {name}")
            self._show_toast(f"System Notification\nMilestone Recorded: {name}")

    def _show_toast(self, message: str):
        toast = tk.Toplevel(self)
        toast.overrideredirect(True)
        toast.configure(bg=T["border"])
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width() - 320
        y = self.winfo_y() + self.winfo_height() - 90
        toast.geometry(f"300x70+{x}+{y}")
        
        inner = tk.Frame(toast, bg=T["panel"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        
        tk.Label(inner, text=message, font=FONT_SMALL,
                 bg=T["panel"], fg=T["text"], justify="left",
                 padx=15, pady=15).pack(fill="both", expand=True)
        self.after(3500, toast.destroy)

class BasePage(tk.Frame):
    def __init__(self, parent, app: CyberShieldApp):
        super().__init__(parent, bg=T["bg"])
        self.app = app

    def on_show(self):
        pass

    def apply_theme(self):
        self.config(bg=T["bg"])

    def _section_header(self, parent, text: str) -> tk.Frame:
        frame = tk.Frame(parent, bg=T["bg"])
        tk.Label(frame, text=text, font=FONT_H1, bg=T["bg"], fg=T["text"]).pack(side="left", pady=10)
        return frame

    def _card(self, parent, **kwargs) -> tk.Frame:
        return tk.Frame(parent, bg=T["card"],
                        highlightbackground=T["border"], highlightthickness=1, **kwargs)

    def _button(self, parent, text, command, primary=True) -> tk.Button:
        bg_color = T["accent"] if primary else T["border"]
        fg_color = "#ffffff" if primary else T["text"]
        return tk.Button(
            parent, text=text, command=command,
            font=FONT_BOLD, relief="flat", cursor="hand2",
            bg=bg_color, fg=fg_color,
            activebackground=T["text"] if primary else T["subtext"], 
            activeforeground=T["bg"],
            padx=20, pady=8
        )



class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        header.pack(fill="x")
        tk.Label(header, text="System Dashboard", font=FONT_H1, bg=T["bg"], fg=T["text"]).pack(anchor="w")
        tk.Label(header, text="Unified Security and Threat Awareness Control Center",
                 font=FONT_MAIN, bg=T["bg"], fg=T["subtext"]).pack(anchor="w", pady=(5, 0))

        grid = tk.Frame(self, bg=T["bg"], padx=35, pady=10)
        grid.pack(fill="both", expand=True)

        tiles = [
            ("Message Analyzer",     "Scan internal & external\ncommunications for phishing\nand social engineering.", "phishing"),
            ("Credential Security",  "Evaluate entropy and generate\ncryptographically secure\nauthentication tokens.", "password"),
            ("File Integrity Scan",  "Analyze local directory assets\nfor structural anomalies\nand hidden executables.", "file_detect"),
            ("Security Protocols",   "Review corporate IT policies,\nsafe browsing standards,\nand privacy protocols.", "tips"),
            ("Audit Logs",           "Export and review local\nsession actions and\nsecurity event history.", "log"),
            ("Compliance Metrics",   "Track user adherence to\nsecurity milestones and\nplatform engagement.", "badges"),
        ]

        for i, (title, desc, pid) in enumerate(tiles):
            row, col = divmod(i, 3)
            card = tk.Frame(grid, bg=T["card"], cursor="hand2",
                            highlightbackground=T["border"], highlightthickness=1)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            grid.columnconfigure(col, weight=1)
            grid.rowconfigure(row, weight=1)

            inner = tk.Frame(card, bg=T["card"], padx=20, pady=25)
            inner.pack(fill="both", expand=True)

            tk.Label(inner, text=title, font=FONT_H2, bg=T["card"], fg=T["text"]).pack(anchor="w", pady=(0, 10))
            tk.Label(inner, text=desc, font=FONT_MAIN, bg=T["card"], fg=T["subtext"], justify="left").pack(anchor="w")

            for w in [card, inner] + inner.winfo_children():
                w.bind("<Button-1>", lambda e, p=pid: self.app.show_page(p))
                w.bind("<Enter>", lambda e, c=card: c.config(bg=T["border"]))
                w.bind("<Leave>", lambda e, c=card: c.config(bg=T["card"]))



class PhishingDetectorPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        self._section_header(container, "Message Threat Analyzer").pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Input communication text (email, SMS, or URI) for semantic threat analysis:",
                 font=FONT_MAIN, bg=T["bg"], fg=T["text"]).pack(anchor="w", pady=(0, 10))

        self.text_area = scrolledtext.ScrolledText(
            container, font=FONT_MONO, height=8,
            bg=T["input_bg"], fg=T["text"], insertbackground=T["text"],
            relief="flat", bd=1, highlightthickness=1, highlightbackground=T["border"]
        )
        self.text_area.pack(fill="x", pady=5)

        btn_frame = tk.Frame(container, bg=T["bg"])
        btn_frame.pack(fill="x", pady=15)
        self._button(btn_frame, "Execute Analysis", self._scan_text).pack(side="left")
        self._button(btn_frame, "Clear Buffer", lambda: self.text_area.delete("1.0", "end"), primary=False).pack(side="left", padx=10)

        self.result_card = self._card(container)
        self.result_card.pack(fill="both", expand=True, pady=10)
        
        self.verdict_lbl = tk.Label(self.result_card, text="System Ready. Awaiting Input.", font=FONT_H2,
                                    bg=T["card"], fg=T["subtext"])
        self.verdict_lbl.pack(pady=(25, 10), anchor="w", padx=25)

        self.flags_lbl = tk.Label(self.result_card, text="", font=FONT_MAIN,
                                  bg=T["card"], fg=T["text"], justify="left", wraplength=850)
        self.flags_lbl.pack(fill="both", expand=True, padx=25, pady=(0, 20), anchor="nw")

    def _scan_text(self):
        text = self.text_area.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Input Required", "Buffer is empty. Please input text for analysis.")
            return

        lower_text = text.lower()
        flags = []

        if any(w in lower_text for w in ["urgent", "immediate action", "will be suspended", "account closed", "within 24 hours", "final warning"]):
            flags.append("[!] ARTIFICIAL URGENCY: Text contains patterns indicating psychological pressure to bypass standard verification.")
        
        if any(w in lower_text for w in ["password", "verify your account", "ssn", "social security", "credit card", "bank account", "login here"]):
            flags.append("[!] CREDENTIAL SOLICITATION: Unsolicited requests for sensitive data or authentication tokens detected.")
        
        if "http://" in lower_text:
            flags.append("[!] UNENCRYPTED PROTOCOL: Detected 'http://' URI. Traffic to this destination is subject to interception.")
        if any(w in lower_text for w in ["bit.ly", "tinyurl.com", "ow.ly", "t.co"]):
            flags.append("[!] OBFUSCATED ROUTING: Utilization of URL shorteners. Destination authenticity cannot be verified prior to connection.")
        
        if any(w in lower_text for w in ["lottery", "winner", "inheritance", "gift card", "claim your prize"]):
            flags.append("[!] INCENTIVE BAIT: Text relies on improbable financial incentives, a common social engineering vector.")

        if "kindly" in lower_text and any(w in lower_text for w in ["revert", "do the needful"]):
            flags.append("[-] LINGUISTIC ANOMALY: Phrasing aligns with known regional scam profiles.")

        if len(flags) == 0:
            self.verdict_lbl.config(text="[OK] No Immediate Indicators of Compromise", fg=T["accent2"])
            self.flags_lbl.config(text="Semantic analysis returned no definitive social engineering triggers.\n\nPolicy Reminder: Automated analysis is not absolute. Continue to verify sender authenticity and avoid executing unverified links.")
        elif len(flags) <= 2:
            self.verdict_lbl.config(text="[WARNING] Suspicious Patterns Detected", fg=T["accent"])
            self.flags_lbl.config(text="\n\n".join(flags))
        else:
            self.verdict_lbl.config(text="[CRITICAL] High Probability of Phishing", fg=T["warning"])
            self.flags_lbl.config(text="\n\n".join(flags))

        self.app.award_badge("phishing_expert")
        log_activity("Executed Message Threat Analysis.")



class PasswordPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        self._section_header(container, "Credential Security Analyzer").pack(fill="x", pady=(0, 5))


        checker_frame = self._card(container)
        checker_frame.pack(fill="x", pady=(10, 20))
        
        tk.Label(checker_frame, text="Entropy Evaluation", font=FONT_H2, bg=T["card"], fg=T["text"]).pack(anchor="w", padx=25, pady=(20, 10))

        entry_container = tk.Frame(checker_frame, bg=T["card"])
        entry_container.pack(fill="x", padx=25, pady=5)
        
        self.pw_var = tk.StringVar()
        self.pw_var.trace_add("write", lambda *_: self._check_strength())
        self.pw_entry = tk.Entry(entry_container, textvariable=self.pw_var, font=FONT_MONO, show="•",
                                 bg=T["input_bg"], fg=T["text"], insertbackground=T["text"],
                                 relief="flat", highlightthickness=1, highlightbackground=T["border"])
        self.pw_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.show_btn = tk.Button(entry_container, text="Reveal", font=FONT_SMALL, relief="flat",
                                  cursor="hand2", bg=T["border"], fg=T["text"], command=self._toggle_show, padx=10)
        self.show_btn.pack(side="left", padx=10)

        self.strength_lbl = tk.Label(checker_frame, text="", font=FONT_BOLD, bg=T["card"], fg=T["text"])
        self.strength_lbl.pack(anchor="w", padx=25, pady=(10, 5))
        self.bar_canvas = tk.Canvas(checker_frame, height=8, bg=T["input_bg"], highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=25)
        
        self.suggestions_lbl = tk.Label(checker_frame, text="Awaiting input for structural analysis...", font=FONT_MAIN,
                                        bg=T["card"], fg=T["subtext"], justify="left")
        self.suggestions_lbl.pack(anchor="w", padx=25, pady=(10, 20))


        gen_frame = self._card(container)
        gen_frame.pack(fill="x")

        tk.Label(gen_frame, text="Secure Credential Generation", font=FONT_H2, bg=T["card"], fg=T["text"]).pack(anchor="w", padx=25, pady=(20, 15))

        form_frame = tk.Frame(gen_frame, bg=T["card"])
        form_frame.pack(fill="x", padx=25)

        tk.Label(form_frame, text="Service/Entity Identifier:", font=FONT_MAIN, bg=T["card"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, font=FONT_MONO, bg=T["input_bg"], fg=T["text"], insertbackground=T["text"],
                                   relief="flat", highlightthickness=1, highlightbackground=T["border"], width=35)
        self.name_entry.grid(row=0, column=1, padx=15, pady=5, ipady=6)

        self._button(form_frame, "Generate & Store", self._generate_password).grid(row=0, column=2, padx=10, pady=5)

        self.gen_result_entry = tk.Entry(gen_frame, font=("Consolas", 14, "bold"), bg=T["input_bg"], fg=T["accent"], 
                                         relief="flat", state="readonly", justify="center", highlightthickness=1, highlightbackground=T["border"])
        self.gen_result_entry.pack(fill="x", padx=25, pady=(20, 5), ipady=10)

        self.gen_status = tk.Label(gen_frame, text="", font=FONT_SMALL, bg=T["card"], fg=T["subtext"])
        self.gen_status.pack(pady=(5, 20))

    def _toggle_show(self):
        current = self.pw_entry.cget("show")
        self.pw_entry.config(show="" if current == "•" else "•")
        self.show_btn.config(text="Hide" if current == "•" else "Reveal")

    def _check_strength(self):
        pw = self.pw_var.get()
        if not pw:
            self.strength_lbl.config(text="")
            self.suggestions_lbl.config(text="Awaiting input for structural analysis...")
            self.bar_canvas.delete("all")
            return

        score = 0
        tips = []
        if len(pw) >= 14: score += 2
        else: tips.append("[-] Length requirement: Enterprise standard recommends 14+ characters.")
        
        if re.search(r'[A-Z]', pw): score += 1
        else: tips.append("[-] Complexity: Missing uppercase alphabetical character.")
        
        if re.search(r'[a-z]', pw): score += 1
        
        if re.search(r'\d', pw): score += 1
        else: tips.append("[-] Complexity: Missing numeric character.")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', pw): score += 1
        else: tips.append("[-] Complexity: Missing specialized symbol.")

        level_map = {
            6: ("Status: Cryptographically Strong", T["accent2"], 1.0),
            5: ("Status: Acceptable / Standard", T["accent"], 0.8),
            4: ("Status: Sub-optimal", T["warning"], 0.6),
            3: ("Status: Weak / Vulnerable", T["warning"], 0.4),
            2: ("Status: Highly Vulnerable", T["warning"], 0.2),
            1: ("Status: Critical Risk", T["warning"], 0.1),
            0: ("Status: Critical Risk", T["warning"], 0.05)
        }
        
        level, color, ratio = level_map.get(score, ("Status: Critical Risk", T["warning"], 0.05))

        self.bar_canvas.delete("all")
        w = self.bar_canvas.winfo_width() or 800
        self.bar_canvas.create_rectangle(0, 0, w, 8, fill=T["input_bg"], outline="")
        self.bar_canvas.create_rectangle(0, 0, int(w * ratio), 8, fill=color, outline="")

        self.strength_lbl.config(text=level, fg=color)
        self.suggestions_lbl.config(text="\n".join(tips) if tips else "Analysis complete. Credential meets enterprise entropy guidelines.")

        if score >= 5:
            self.app.award_badge("strong_password")

    def _generate_password(self):
        pw_name = self.name_entry.get().strip()
        if not pw_name:
            self.gen_status.config(text="[!] Error: Identifier field cannot be empty.", fg=T["warning"])
            return

        if os.path.exists(PASSWORD_FILE):
            try:
                with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith(f"name - {pw_name} and password -"):
                            self.gen_status.config(text=f"[!] Collision Error: Entry for '{pw_name}' already exists in the database.", fg=T["warning"])
                            return
            except Exception as e:
                messagebox.showerror("I/O Error", f"Database read failure: {e}")
                return

        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
        while True:
            new_pw = ''.join(random.choice(chars) for _ in range(18))
            if (any(c.islower() for c in new_pw) and any(c.isupper() for c in new_pw)
                and any(c.isdigit() for c in new_pw) and sum(c in "!@#$%^&*()-_+=" for c in new_pw) >= 2):
                break

        try:
            with open(PASSWORD_FILE, "a", encoding="utf-8") as f:
                f.write(f"name - {pw_name} and password - {new_pw}\n")
            
            self.gen_result_entry.config(state="normal")
            self.gen_result_entry.delete(0, "end")
            self.gen_result_entry.insert(0, new_pw)
            self.gen_result_entry.config(state="readonly")

            self.gen_status.config(text=f"[OK] Credential provisioned and written to '{PASSWORD_FILE}' successfully.", fg=T["accent2"])
            self.name_entry.delete(0, "end")
            self.app.award_badge("password_creator")
            log_activity(f"Provisioned secure credential for identifier: {pw_name}")

        except Exception as e:
            messagebox.showerror("I/O Error", f"Database write failure: {e}")



class FileDetectPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        self._section_header(container, "Local File Integrity Scanner").pack(fill="x", pady=(0, 10))

        info_lbl = tk.Label(container, text="Select a local asset to analyze its extension hierarchy and structural risk.\nProcessing is performed entirely locally without network transmission.",
                            font=FONT_MAIN, bg=T["bg"], fg=T["subtext"], justify="left")
        info_lbl.pack(anchor="w", pady=(0, 25))

        browse_frame = tk.Frame(container, bg=T["bg"])
        browse_frame.pack(anchor="w", pady=10)
        self._button(browse_frame, "Select Asset for Analysis...", self._browse_file).pack()

        self.result_card = self._card(container)
        self.result_card.pack(fill="both", expand=True, pady=20)
        
        self.file_name_lbl = tk.Label(self.result_card, text="Target: None selected", font=FONT_MONO, bg=T["card"], fg=T["subtext"])
        self.file_name_lbl.pack(anchor="w", padx=25, pady=(25, 10))

        tk.Frame(self.result_card, bg=T["border"], height=1).pack(fill="x", padx=25)

        self.verdict_lbl = tk.Label(self.result_card, text="", font=FONT_H2, bg=T["card"])
        self.verdict_lbl.pack(anchor="w", padx=25, pady=(20, 5))

        self.details_lbl = tk.Label(self.result_card, text="", font=FONT_MAIN, bg=T["card"], fg=T["text"], justify="left")
        self.details_lbl.pack(padx=25, pady=10, fill="both", expand=True, anchor="nw")

    def _browse_file(self):
        filepath = filedialog.askopenfilename(title="Select Asset")
        if not filepath:
            return

        filename = os.path.basename(filepath)
        self.file_name_lbl.config(text=f"Target: {filename}")
        self._analyze_actual_file(filename)

    def _analyze_actual_file(self, fname: str):
        ext = os.path.splitext(fname)[1].lower()
        warnings = []

        if DOUBLE_EXTENSION_PATTERN.search(fname):
            warnings.append("[WARNING] Obfuscated Extension Detected: The asset utilizes a dual-extension structure commonly associated with payload delivery (e.g., '.jpg.exe').")

        if ext in SUSPICIOUS_EXTENSIONS:
            warnings.append(f"[WARNING] Executable Extension ('{ext}'): This asset contains direct execution capabilities. Verification of origin and cryptographic signature is mandatory before execution.")

        if re.search(r'\s{3,}', fname):
            warnings.append("[WARNING] Whitespace Anomaly: Excessive spacing detected in the filename, a technique often used to visually push the true extension out of view in standard OS file explorers.")

        if warnings:
            self.verdict_lbl.config(text="STATUS: Structural Anomalies Detected", fg=T["warning"])
            self.details_lbl.config(text="\n\n".join(warnings) + "\n\nPolicy Action: Do NOT execute this asset unless explicitly authorized by IT Administration.")
        else:
            self.verdict_lbl.config(text="STATUS: No Anomalies Detected", fg=T["accent2"])
            self.details_lbl.config(text=f"Extension '{ext}' adheres to standard naming conventions without obvious obfuscation.\n\nNote: This module performs structural naming analysis. Full heuristic scanning via enterprise Endpoint Detection and Response (EDR) is still required.")

        self.app.award_badge("file_detective")
        log_activity(f"Executed integrity scan on asset: {fname}")



class TipsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        self._section_header(container, "Security Protocols & Policies").pack(fill="x", pady=(0, 10))

        tf = tk.Frame(container, bg=T["card"], highlightbackground=T["border"], highlightthickness=1)
        tf.pack(fill="both", expand=True)

        self.text_area = scrolledtext.ScrolledText(tf, font=FONT_MAIN, bg=T["card"], fg=T["text"], relief="flat", bd=0, wrap="word", padx=25, pady=25)
        self.text_area.pack(fill="both", expand=True)
        self.text_area.insert("1.0", SAFETY_TIPS)
        self.text_area.config(state="disabled")

    def on_show(self):
        log_activity("Reviewed Security Protocols")
        self.app.award_badge("tips_reader")



class LogPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        header = self._section_header(container, "System Audit Logs")
        header.pack(fill="x", pady=(0, 10))
        
        btn_frame = tk.Frame(header, bg=T["bg"])
        btn_frame.pack(side="right")
        self._button(btn_frame, "Refresh Log", self._refresh).pack(side="left", padx=5)
        self._button(btn_frame, "Purge Records", self._clear_log, primary=False).pack(side="left")

        tf = tk.Frame(container, bg=T["input_bg"], highlightbackground=T["border"], highlightthickness=1)
        tf.pack(fill="both", expand=True)

        self.text_area = scrolledtext.ScrolledText(tf, font=FONT_MONO, bg=T["input_bg"], fg=T["subtext"], relief="flat", bd=0, wrap="word", padx=20, pady=20)
        self.text_area.pack(fill="both", expand=True)

    def on_show(self):
        self._refresh()

    def _refresh(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", "end")
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_area.insert("1.0", content if content else "[SYS] Log sequence is empty.")
                self.text_area.see("end")
            except IOError:
                self.text_area.insert("1.0", "[ERR] I/O error reading audit file.")
        else:
            self.text_area.insert("1.0", "[SYS] No audit records located.")
        self.text_area.config(state="disabled")

    def _clear_log(self):
        if messagebox.askyesno("Confirm Purge", "Authorize permanent deletion of local audit records?"):
            try:
                open(LOG_FILE, "w").close()
                log_activity("Audit sequence purged by user.")
                self._refresh()
            except IOError:
                messagebox.showerror("Error", "Access denied. Cannot purge records.")



class BadgesPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=T["bg"], padx=40, pady=30)
        container.pack(fill="both", expand=True)

        self._section_header(container, "Compliance Milestones").pack(fill="x", pady=(0, 10))

        self.grid_frame = tk.Frame(container, bg=T["bg"])
        self.grid_frame.pack(fill="both", expand=True, pady=10)

    def on_show(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        badges_list = list(BADGES.items())
        for i, (bid, (name, desc)) in enumerate(badges_list):
            row, col = divmod(i, 3)
            earned = bid in self.app.earned_badges
            
            card = tk.Frame(self.grid_frame, bg=T["card"] if earned else T["panel"], highlightbackground=T["accent"] if earned else T["border"], highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.grid_frame.columnconfigure(col, weight=1)
            self.grid_frame.rowconfigure(row, weight=1)

            inner = tk.Frame(card, bg=card.cget("bg"), padx=20, pady=25)
            inner.pack(fill="both", expand=True)

            icon_text = name.split(" ")[0]
            tk.Label(inner, text=icon_text if earned else "■", font=("Helvetica", 24), bg=card.cget("bg"), fg=T["accent"] if earned else T["border"]).pack(pady=(5, 10))
            tk.Label(inner, text=" ".join(name.split(" ")[1:]), font=FONT_H2, bg=card.cget("bg"), fg=T["text"] if earned else T["subtext"]).pack()
            tk.Label(inner, text=desc, font=FONT_MAIN, bg=card.cget("bg"), fg=T["subtext"], wraplength=200, justify="center").pack(pady=(10, 15))
            
            status = "VERIFIED" if earned else "PENDING"
            tk.Label(inner, text=status, font=FONT_SMALL, bg=card.cget("bg"), fg=T["accent2"] if earned else T["subtext"]).pack(pady=(0, 5))


if __name__ == "__main__":
    app = CyberShieldApp()
    app.mainloop()
