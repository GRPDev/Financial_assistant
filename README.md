# Django Financial App #

This project is a Django web application that allows users to register, log in, view their transaction history, perform balance operations (deposit/withdraw), and check currency exchange rates. It uses Bootstrap for front-end elements and integrates with an external API for real-time currency exchange data.

## Features ##
**User Registration**: Users can create an account  
**User Authentication**: Users can log in and log out  
**Balance Operations**: Users can check their balance, deposit money, and withdraw money  
**Transaction History**: Users can view their transaction history  
**Currency Exchange**: Users can check currency exchange rates via a third-party API  

## Database Models

### User Model
The application uses Django's built-in `User` model from `django.contrib.auth.models`, which is linked to a database table that stores user accounts.

### History Model
The `History` model tracks transaction records (like deposits and withdrawals). Each record is associated with a user and stored in a dedicated database table.

### ORM Usage
- **Creating Users**: Users are created through the `CreateUserView`, which saves new user accounts in the database using Django's ORM.
- **Transaction Management**: The application calculates balances by querying the `History` model to sum successful deposits and withdrawals. The `getBalance(user)` function aggregates data from the database using ORM methods.
- **Transaction History**: The `ViewTransactionHistoryView` class retrieves and displays all transaction records for the logged-in user by querying the `History` model with Django's ORM.

## Endpoints

- **Register**: `/create_account/` - Allows new users to create an account.
- **Login**: `/login/` - Authenticates users.
- **Main Menu**: `/main_menu/` - Displays user options.
- **Balance Operations**: `/operations/` - Allows users to manage their balance.
- **Transaction History**: `/history/` - Displays transaction history.
- **Currency Exchange**: `/currency_exchange/` - Allows users to exchange currencies.

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/repository-name.git
  cd repository-name
  ```

2. Create a virtual environment and activate it:
  ```bash
  python -m venv env
  source env/bin/activate  # On Windows use `env\Scripts\activate`
  ```

3. Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```

4. Set up the database:
  ```bash
  python manage.py migrate
  ```

5. Create a superuser to access the admin interface:
  ```bash
  python manage.py createsuperuser
  ```
6. Run the development server:
  ```bash
  python manage.py runserver
  ```
## Usage
Access the application at http://127.0.0.1:8000/  
Register a new account or log in with an existing account.  
Use the main menu to navigate through balance operations, transaction history, and currency exchange functionalities.  
