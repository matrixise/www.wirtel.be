---
title: "dsmtpd – A Lightweight SMTP Server for Python Developers"
date: "2025-05-21T10:00:00+02:00"
image: dsmtpd-logo.png
project_url: "https://github.com/matrixise/dsmtpd"
tags: ["python", "smtp", "aiosmtpd", "developer-tools", "maildir"]
slug: "dsmtpd-python-smtp"
---

## 📨 dsmtpd — A Lightweight SMTP Server for Modern Developers

As developers, we often need to test email delivery locally—without setting up a full-blown mail server. That’s exactly where **dsmtpd** comes in: a tiny, practical SMTP daemon written in Python, designed to receive emails and store them directly in a local **Maildir** folder.

---

### 🚀 What is dsmtpd?

**dsmtpd** (Developer SMTP Daemon) is an asynchronous mini SMTP server based on [`aiosmtpd`](https://aiosmtpd.readthedocs.io/). It listens on a network interface (by default `127.0.0.1:1025`) and saves all incoming emails into a Maildir-compatible directory.

It’s perfect for:

- Developers testing email features locally
- Debugging and inspection of email content
- Integration tests or CI pipelines needing a fake SMTP backend

---

### ⚙️ Key Features

- 📬 Async SMTP server using `asyncio` and `aiosmtpd`
- 🗂️ Saves emails into Maildir format
- 🔐 Proper locking/unlocking of the mailbox
- 📄 Intelligent logging of received emails (sender, recipients, subject)
- 🧰 CLI arguments for port/interface/maildir configuration and size limit

---

### 📦 Quick Example

```bash
$ python -m dsmtpd -i 127.0.0.1 -p 1025 -d ./maildir
```

In your Python application
```python
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("Hello from dsmtpd")
msg["Subject"] = "Test"
msg["From"] = "me@example.com"
msg["To"] = "you@example.com"

with smtplib.SMTP("localhost", 1025) as s:
    s.send_message(msg)
```

🎉 The message will be saved to ./maildir — you can explore it with any Maildir-compatible reader or script.

### 👨‍💻 Why I Built It

I originally created dsmtpd because I needed a simple way to test outgoing emails without sending anything to the real world. By combining the power of aiosmtpd with a local Maildir backend, I ended up with a reliable little SMTP daemon that still helps me today in my daily development and testing tasks.

### 📚 Useful Links
•   🔗 GitHub Repository : https://github.com/matrixise/dsmtpd
•   📄 License: BSD
