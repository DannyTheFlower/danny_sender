import imaplib
import logging
import smtplib
import time
import typing as tp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Sender:
    def __init__(
        self,
        username: str,
        password: str,
        smtp: str = "smtp.yandex.ru",
        smtp_port: int = 465,
        imap: str = "imap.yandex.com",
        imap_port: int = 993,
    ) -> None:
        self.username = username
        self.password = password
        self.smtp_server = smtplib.SMTP_SSL(smtp, smtp_port)
        self.imap_server = imaplib.IMAP4_SSL(imap)

    def connect(self) -> None:
        try:
            self.smtp_server.login(self.username, self.password)
            self.imap_server.login(self.username, self.password)
            logging.info("Successfully connected!")
        except Exception as e:
            self.smtp_server.quit()
            self.imap_server.logout()
            raise Exception("Failed to connect to the server.") from e

    def send_email(
        self,
        to_email: tp.Union[str, tp.List[str]],
        subject: str,
        body: str,
        is_html: bool = False,
        notify: bool = False,
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["Subject"] = subject
        if is_html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))
        if isinstance(to_email, str):
            to_email = [to_email]

        for email in to_email:
            msg["To"] = email
            if notify:
                msg["Disposition-Notification-To"] = email
            text = msg.as_string()
            try:
                self.smtp_server.sendmail(self.username, email, text)
                self.save_to_sent_folder(text)
                logging.info(f"Sent to {to_email}")
            except Exception:
                logging.error(f"Failed to send message to {email}.")

    def save_to_sent_folder(self, message_as_string) -> None:
        self.imap_server.select("sent")
        self.imap_server.append(
            "Sent", "\\Seen", imaplib.Time2Internaldate(time.time()), message_as_string.encode("utf-8")
        )

    def quit(self) -> None:
        self.smtp_server.quit()
        self.imap_server.logout()
