import smtplib
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid, formataddr
from config.config import LOCAL_IP, get_config
from internal.models.user import BookPenalty
from internal.database.books import get_book_by_id
from .logger import logger


async def send_email_to_user(user, html_body: str, subject: str) -> bool:
    try:
        host = get_config("email_host")
        port = get_config("email_port")
        username = get_config("email_username")
        password = get_config("email_password")
        sender_name = "Library Notifications"
        sender_email = username

        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(username, password)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = formataddr((sender_name, sender_email))
            msg["To"] = user.email
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid()
            msg["Reply-To"] = sender_email

            part = MIMEText(html_body, "html", "utf-8")
            msg.attach(part)

            server.sendmail(sender_email, [user.email], msg.as_string())
            return True

    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {e}")
        return False


async def send_email_to_subscribers(user, book, subject):
    try:
        host = get_config("email_host")
        port = get_config("email_port")
        username = get_config("email_username")
        password = get_config("email_password")
        sender_name = "Library Notifications"
        sender_email = username

        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(username, password)

            user_email = user.email
            html_body = generate_html_email(book)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = formataddr((sender_name, sender_email))
            msg["To"] = user_email
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid()
            msg["Reply-To"] = sender_email

            part2 = MIMEText(html_body, "html", "utf-8")
            msg.attach(part2)

            server.sendmail(sender_email, [user_email], msg.as_string())
            return True

    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {e}")
        return False


def generate_html_email(book) -> str:
    cover_image = book.cover_image or "https://drive.google.com/uc?export=view&id=1ooKL3fZq8Py5tWi0eoruLTMsCsGl39Cj"
    authors = ", ".join(book.authors)
    description = book.description or "No description available."
    borrow_link = f"http://{LOCAL_IP}:8085/books/{book.id}"

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
          <h2 style="color: #2d6a4f;">📚 '{book.title}' is now available</h2>
          <table>
            <tr>
              <td style="padding-right: 20px;">
                <img src="{cover_image}" alt="Book Cover" style="width: 100px; height: 150px; object-fit: cover; border: 1px solid #ccc; border-radius: 4px;">
              </td>
              <td>
                <p><strong>Title:</strong> {book.title}</p>
                <p><strong>Author(s):</strong> {authors}</p>
                <p><strong>Available Copies:</strong> {book.available_copies}</p>
                <p>{description[:200]}...</p>
                <a href="{borrow_link}" style="display: inline-block; margin-top: 10px; padding: 10px 15px; background-color: #40916c; color: white; text-decoration: none; border-radius: 5px;">Borrow Now</a>
              </td>
            </tr>
          </table>
          <hr style="margin-top: 30px;">
          <p style="font-size: 12px; color: #888;">You received this email because you requested to be notified when this book becomes available.</p>
        </div>
      </body>
    </html>
    """


async def generate_penalty_email_html(user, penalties: List[BookPenalty]) -> str:
    total_fee = sum(p.amount for p in penalties)
    penalty_rows = ""

    for penalty in penalties:
        book = await get_book_by_id(penalty.book_id)
        book_title = book.title if book else "Unknown Title"
        penalty_rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{book_title}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">₺{penalty.amount:.2f}</td>
        </tr>
        """

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
          <h2 style="color: #c0392b;">Penalty Fee Reminder</h2>
          <p>Dear {user.username},</p>
          <p>You currently have penalty fees for the following book(s):</p>
          <table style="border-collapse: collapse; width: 100%; margin-top: 16px;">
            <thead>
              <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; border: 1px solid #ddd;">Book</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Fee</th>
              </tr>
            </thead>
            <tbody>
              {penalty_rows}
              <tr style="font-weight: bold;">
                <td style="padding: 8px; border: 1px solid #ddd;">Total</td>
                <td style="padding: 8px; border: 1px solid #ddd;">₺{total_fee:.2f}</td>
              </tr>
            </tbody>
          </table>
          <p style="margin-top: 20px;">Please resolve these penalties at your earliest convenience.</p>
        </div>
      </body>
    </html>
    """
