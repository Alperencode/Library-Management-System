import bcrypt
from jose import jwt
import smtplib
from fastapi import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid, formataddr
from config.config import get_config
from internal.database.users import get_user_by_id
from internal.models.user import User
from internal.database.books import get_book_by_isbn
from internal.types.exceptions import FailResponseException
from config.config import LOCAL_IP
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
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise FailResponseException(401, "You must be logged in to continue.")

    try:
        payload = jwt.decode(
            access_token,
            get_config("secret_key"),
            algorithms=[get_config("algorithm")]
        )
        user_id = payload.get("id")
        if not user_id:
            raise FailResponseException(401, "Authentication token is invalid or corrupted.")

        user = await get_user_by_id(user_id)
        if not user:
            raise FailResponseException(404, "User account not found. Please contact support.")

        return user

    except jwt.ExpiredSignatureError:
        raise FailResponseException(401, "Your session has expired. Please log in again.")
    except jwt.JWTError:
        raise FailResponseException(401, "Authentication token could not be verified.")


async def get_scanned_book(request: Request):
    token = request.cookies.get("scanned_book")
    if not token:
        raise FailResponseException(401, "Please scan a book to proceed.")

    try:
        payload = jwt.decode(
            token,
            get_config("secret_key"),
            algorithms=[get_config("algorithm")]
        )
        isbn = payload.get("book_isbn")
        scanned = payload.get("scanned")

        if not isbn or not scanned:
            raise FailResponseException(401, "Scanned data is incomplete or invalid.")

        book = await get_book_by_isbn(isbn)
        if not book:
            raise FailResponseException(404, "Scanned book was not found in the library catalog.")

        return book

    except jwt.ExpiredSignatureError:
        raise FailResponseException(401, "Scan expired. Please scan the book again.")
    except jwt.InvalidTokenError:
        raise FailResponseException(401, "The scanned book token is invalid or has been tampered with.")


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
