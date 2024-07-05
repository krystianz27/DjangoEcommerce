# Django Ecommerce Project

## Getting Started

These instructions will help you set up and run the Django Ecommerce project on your local machine for development and testing purposes.

## Features

### User Registration and Authentication:

- Users are required to have a Gmail account for registration.
- Upon registration, a confirmation email is sent to the registered email address.

### Order Management:

- Users receive an order confirmation email upon placing an order.
- Guests and logged-in users can place orders.
- Logged-in users can view their order history and manage their account.

## Notes

- This project is built using Django version 5. Ensure compatibility with this version or later.
- For SMTP email functionality, a Gmail account is required due to the project's configuration.

### Prerequisites

Make sure you have the following installed on your local machine:

- Python (version 3.12.3 recommended)
- pip

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd django-ecommerce

   ```

2. **Create and activate a virtual environment:**

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Copy the example environment file and configure your own values:

   ```bash
   cp .env.example .env
   ```

   Open the `.env` file and set the following variables:

   ```plaintext
   SECRET_KEY=your_generated_secret_key
   ```

   The following variables are optional and only needed if you want to use S3 Bucket, PostgreSQL and SMTP:

   ```plaintext
   AWS_ACCESS_KEY_ID = your_AWS_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY = your_AWS_SECRET_ACCESS_KEY
   AWS_STORAGE_BUCKET_NAME=your_aws_storage_bucket_name

   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host

   EMAIL_HOST_USER=your_email_host_user
   EMAIL_HOST_PASSWORD=your_email_host_password
   DEFAULT_FROM_EMAIL=your_default_from_email

   ```

5. **Generate a Django `SECRET_KEY`:**

   Create a new Python file called `generate_secret_key.py` with the following content:

   ```python
   from django.core.management.utils import get_random_secret_key

   print(get_random_secret_key())
   ```

   Run the script to generate a secret key.
   Copy the generated key and paste it into your `.env` file:

   ```plaintext
   SECRET_KEY=your_generated_secret_key

   ```

6. **Run database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional, for accessing the admin site):**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   Open your browser and navigate to `http://127.0.0.1:8000/` to see the application running.
