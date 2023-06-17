import tkinter as tk
from tkinter import messagebox
import webbrowser
from logic.sender import Sender


class Application(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.sender = None
        self.create_login_screen()

    def create_login_screen(self):
        self.warning_label = tk.Label(
            self, text="Warning! This program is working ONLY with Yandex."
        )
        self.username_label = tk.Label(self, text="E-mail:")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password:")
        self.password_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Connect", command=self.connect)
        self.github_link = tk.Label(self, text="GitHub: DannyTheFlower", cursor="hand2", fg="blue")

        self.github_link.bind(
            "<Button-1>", lambda x: webbrowser.open_new_tab("https://github.com/DannyTheFlower")
        )

        self.warning_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        self.password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.github_link.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def create_email_screen(self):
        self.instructions_label = tk.Label(
            self,
            text="E-mails must be entered, separated by commas, without spaces.\nE.g.: "
            "example1@gmail.com,example2@hotmail.com,example3@yahoo.com",
        )
        self.to_email_label = tk.Label(self, text="E-mails:")
        self.to_email_entry = tk.Entry(self)
        self.subject_label = tk.Label(self, text="Subject:")
        self.subject_entry = tk.Entry(self)
        self.body_label = tk.Label(self, text="Body:")
        self.body_entry = tk.Text(self)
        self.notify_var = tk.IntVar()
        self.notify_checkbutton = tk.Checkbutton(
            self, text="Notify of reading", variable=self.notify_var
        )
        self.html_var = tk.IntVar()
        self.html_checkbutton = tk.Checkbutton(self, text="HTML format", variable=self.html_var)
        self.send_button = tk.Button(self, text="Send Mail", command=self.send_mail)

        self.instructions_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.to_email_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.to_email_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.subject_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.subject_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.body_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.body_entry.grid(row=3, column=1, padx=5, pady=5)
        self.notify_checkbutton.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.html_checkbutton.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.send_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def connect(self) -> None:
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.sender = Sender(username, password)

        try:
            self.sender.connect()

            self.warning_label.grid_forget()
            self.username_label.grid_forget()
            self.username_entry.grid_forget()
            self.password_label.grid_forget()
            self.password_entry.grid_forget()
            self.login_button.grid_forget()
            self.github_link.grid_forget()

            self.create_email_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_mail(self):
        to_emails = self.to_email_entry.get().split(",")
        subject = self.subject_entry.get()
        body = self.body_entry.get("1.0", "end")
        notify = bool(self.notify_var.get())
        is_html = bool(self.html_var.get())
        try:
            self.sender.send_email(to_emails, subject, body, notify=notify, is_html=is_html)
            messagebox.showinfo("Success", "The email has been sent!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
