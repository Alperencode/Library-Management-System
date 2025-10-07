# Library Management System

A modern, API-driven Library Management System developed using FastAPI (Python), MongoDB, and Vue.js. This system allows users to manage borrowing and returning of books, request new titles for the library, and receive email notifications when requested or borrowed books become available.

## Scan Videos

<div align="center">

<p align=center> <img src="images/RFID-Scan.gif" width=650> </p>
<p align=center> <img src="images/Barcode-Scan.gif" width=650> </p>

</div>

## Related Images

<img src="images/Project-1.jpg" width="600">
<img src="images/Project-2.jpg" width="600">
<img src="images/Project-3.jpg" width="600">
<img src="images/Waiting-For-Scan-State.jpg" width="600">
<img src="images/Success-State.jpg" width="600">
<img src="images/Error-State.jpg" width="600">

## Features

- **Book Identification:** Scan book RFID or barcode to retrieve information via ISBN.
- **Book Catalog:** Users can search through the book catalog and use filters.
- **Borrow & Return:** Users can borrow and return books.
- **Book Requests:** Users can request books using google-books API not currently in the library catalog.
- **Email Notifications:** Automated notifications for book availability and updates on book requests.
- **Authentication:** Secure user login and access management using JWT.
- **Admin Panel:** Separate authentication and access control for administrators.
- **Public Browsing:** Unauthenticated users can browse available books and categories.
- **Notification Subscription:** Users can subsribe for email alerts when a specific book becomes available.

## Tech Stack

- **Backend:** FastAPI (Python), MongoDB
- **Frontend:** Vue.js
- **Authentication:** JWT (JSON Web Tokens), using secure cookie-based storage
- **Email Service:** Integrated email notifications for user alerts

## API Overview

The system is fully API-driven and organized into modular components. It supports the following functional areas:

### Authentication and Session Management
Secure endpoints for user session lifecycle using JWT:
- User registration, login, logout
- Token refresh handling for session continuity

### User Account and Transactions
Endpoints that allow users to:
- View and update profile information
- Borrow and return books
- Extend return dates
- Track borrowed, returned, and overdue books

### Book Requests and Notifications
Features that enhance user interaction with the library:
- Submit, track, and delete book requests
- Subscribe or unsubscribe to email notifications when books become available

### Book and Library Operations
Core endpoints for accessing library resources:
- Search for books by ISBN, title, author, or category
- Browse book categories and popular titles
- View book details and related recommendations

### Google Books Integration
Seamless integration for external book discovery:
- Search Google Books by query
- Add books to the system using Google Books volume ID
- Bulk import books from Google Books

### Admin Operations *(Planned)*
Administrative endpoints to manage and monitor the system:
- Approve or deny book requests
- Add, update, or delete book records
- Monitor system statistics and user activity
- View login attempts and server logs
- Manage users and oversee borrowing history


## Developer Guide

Before contributing, please review the [Developer Guide](dev-guide.md), which includes setup instructions, environment configuration, and coding standards.

## License

This project is licensed under the [MIT License](LICENSE).