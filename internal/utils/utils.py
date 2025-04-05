import bcrypt
import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid, formataddr
from config.config import get_config
from internal.models.user import User
from fastapi import HTTPException, Request
from internal.database.users import get_user_by_id
from .logger import logger


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_token_owner(request: Request, user: User, token_name: str) -> bool:
    existing_access_token = request.cookies.get(token_name)
    if existing_access_token:
        payload = jwt.decode(existing_access_token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        user_id = payload.get("id")
        return user_id == user.id
    return False


async def get_current_user(request: Request):
    # Check for access_token cookie
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        payload = jwt.decode(access_token, get_config("secret_key"), algorithms=[get_config("algorithm")])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from database
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


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
    cover_image = book.cover_image or "https://via.placeholder.com/100x150?text=No+Cover"
    authors = ", ".join(book.authors)
    description = book.description or "No description available."
    borrow_link = ""

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
