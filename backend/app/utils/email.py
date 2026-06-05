import smtplib


def send_email(subject: str, body: str, receiver_email: str = "adityakarn0001@gmail.com") -> None:
    """Send a plain-text e-mail via Gmail SMTP."""
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("liflynk@gmail.com", "xpju deju dhge hcds")

    sender_email = "liflynk@gmail.com"
    message = f"Subject: {subject}\n\n{body}"
    s.sendmail(sender_email, receiver_email, message)
    s.quit()
