# Teacher Trek Program

The Teacher Trek Program is a web application designed to streamline the process of teacher transfers within educational institutions. It provides a platform for teachers to submit transfer requests and manage their account information.

## Features

- **User Authentication:** Teachers can create accounts, log in, and log out. Authentication is handled securely using hashed passwords.

- **Profile Management:** Teachers can update their account information, including username, email, and profile picture.

- **Transfer Requests:** Teachers can submit transfer requests by providing details such as school, subjects, county, destination, and purpose.

- **Request Validation:** The system checks if a teacher already has an existing transfer request before allowing the submission of a new one.

- **Notifications:** Flash messages are used to provide feedback on successful actions or display warnings when necessary.

## Technologies Used

- **Flask:** A web framework for Python used to build the backend of the application.

- **SQLAlchemy:** An ORM (Object-Relational Mapping) library for Python, used for database interactions.

- **SQLite:** A lightweight and self-contained database engine used to store application data.

- **Jinja2:** A template engine for Python, integrated with Flask for dynamic HTML rendering.

- **WTForms:** A library for handling web forms in Flask applications.

- **bcrypt:** Used for password hashing to enhance security.

- **Pillow (PIL):** A library for image processing, utilized for resizing and saving profile pictures.

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
## Author
Abdulai Dawuni Abubakar
Fena Olwal Onditi

