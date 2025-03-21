# Shopping Cart Database Project

## Overview
This project is a **Shopping Cart Database System** built using **PostgreSQL** for managing users, products, and transactions efficiently. The system allows users to browse products, add them to a cart, and complete the checkout process.

## Features
- **User Management**: Register and manage user accounts.
- **Product Listing**: View and manage available products.
- **Shopping Cart**: Add, remove, and update items in the cart.
- **Checkout Process**: Calculate the final price and complete the purchase.
- **Database Relationships**: Uses **joins and foreign keys** for efficient queries.

## Technologies Used
- **Database**: PostgreSQL
- **Backend**: Python
- **GUI**: Tkinter (for the user interface)

## Setup Instructions

### Prerequisites
- **Install **PostgreSQL** and ensure the database service is running.**  
- **Install **Python** (version 3.x recommended)**.
- **Clone the Repository**:
```sh
git clone https://github.com/akshit-rathore/Shopping-Cart-DB.git
cd Shopping-Cart-DB
```
- **Set Up a Virtual Environment**:
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```
- **Install required dependencies**:
```sh
pip install -r requirements.txt
```


### Database Configuration
- **Create Database:**
```sql
CREATE DATABASE shoppingcart;
```
- **Set Up Tables:**
Run `Table.sql` then `Insert.sql`


### Running the Project
- Start the application:
```sh
python login.py
```
The GUI will open, allowing users to interact with the application.

## Contribution
Feel free to contribute! Fork the repo, make changes, and submit a pull request.

## License
This project is open-source and available under the **MIT License**.

