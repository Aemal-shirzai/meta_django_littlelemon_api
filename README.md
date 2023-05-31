# Meta Django REST Framework Little Lemon API 
The purpose of this project is to complete the final assessment for the Meta Django REST Framework Course by creating a littlelemon website.

It is a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders.

## Table of Contents

- [Groups](#user-groups)
- [API endpoints](#api-endpoints)
- [Clone and Run](#clone-and-run)

# User groups
1. Manager
2. Delivery Crew
3. Customer -> Neither Manager or Delivery Crew
**Note:** Make sure to create the above groups if you are using new database.


# API endpoints
Here are all the required API routes for this project grouped into several categories.

**1. User registration and token generation endpoints:**
| Endpoint                 | Role                         | Method | Purpose                                        |
|--------------------------|------------------------------|--------|------------------------------------------------|
| **/api/users**           | No role required             | **POST**   | Creates a new user with name, email, and password |
| **/api/users/users/me/** | Anyone with a valid user token | **GET**    | Displays only the current user                  |
| **/token/login/**        | Anyone with a valid username and password | **POST** | Generates access tokens for other API calls     |

**2. Menu-items endpoints:**
| Endpoint                    | Role                               | Method     | Purpose                                         |
|-----------------------------|------------------------------------|------------|-------------------------------------------------|
| **/api/menu-items**         | Customer, delivery crew            | **GET**    | Lists all menu items. Return a 200 – Ok status code |
| **/api/menu-items**         | Customer, delivery crew            |            | **POST, PUT, PATCH, DELETE**   | Denies access and returns 403 – Unauthorized status code |
| **/api/menu-items/{menuItem}** | Customer, delivery crew            | **GET**    | Lists single menu item                          |
| **/api/menu-items/{menuItem}** | Customer, delivery crew            |            | **POST, PUT, PATCH, DELETE**   | Returns 403 – Unauthorized status code |
| **/api/menu-items**         | Manager                            | **GET**    | Lists all menu items                             |
| **/api/menu-items**         | Manager                            | **POST**   | Creates a new menu item and returns 201 - Created |
| **/api/menu-items/{menuItem}** | Manager                            | **GET**    | Lists single menu item                          |
| **/api/menu-items/{menuItem}** | Manager                            | **PUT, PATCH** | Updates single menu item                    |
| **/api/menu-items/{menuItem}** | Manager                            | **DELETE** | Deletes menu item                             |

**3. User group management endpoints:**
| Endpoint                           | Role     | Method | Purpose                                                       |
|------------------------------------|----------|--------|---------------------------------------------------------------|
| **/api/groups/manager/users**      | Manager  | **GET**    | Returns all managers                                          |
| **/api/groups/manager/users**      | Manager  | **POST**   | Assigns the user in the payload to the manager group and returns 201 - Created |
| **/api/groups/manager/users/{userId}** | Manager  | **DELETE** | Removes this particular user from the manager group and returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found |
| **/api/groups/delivery-crew/users**   | Manager  | **GET**    | Returns all delivery crew                                     |
| **/api/groups/delivery-crew/users**   | Manager  | **POST**   | Assigns the user in the payload to the delivery crew group and returns 201 - Created |
| **/api/groups/delivery-crew/users/{userId}** | Manager  | **DELETE** | Removes this user from the manager group and returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found |

**4. Cart management endpoints:**
| Endpoint                         | Role     | Method | Purpose                                                                                           |
|----------------------------------|----------|--------|---------------------------------------------------------------------------------------------------|
| **/api/cart/menu-items**         | Customer | **GET**    | Returns current items in the cart for the current user token                                      |
| **/api/cart/menu-items**         | Customer | **POST**   | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items   |
| **/api/cart/menu-items**         | Customer | **DELETE** | Deletes all menu items created by the current user token                                          |

**5. Order management endpoints**
| Endpoint                     | Role           | Method     | Purpose                                                                                                                                 |
|------------------------------|----------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **/api/orders**              | Customer       | **GET**    | Returns all orders with order items created by this user                                                                                |
| **/api/orders**              | Customer       | **POST**   | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. |
| **/api/orders/{orderId}**    | Customer       | **GET**    | Returns all items for this order ID. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code. |
| **/api/orders**              | Manager        | **GET**    | Returns all orders with order items by all users                                                                                        |
| **/api/orders/{orderId}**    | Customer       | **PUT, PATCH** | Updates the order. A manager can use this endpoint to set a delivery crew to this order and update the order status.                                                                                  |
| **/api/orders/{orderId}**    | Manager        | **DELETE** | Deletes this order                                                                                                                       |
| **/api/orders**              | Delivery crew  | **GET**    | Returns all orders with order items assigned to the delivery crew                                                                        |
| **/api/orders/{orderId}**    | Delivery crew  | **PATCH**  | Updates the order status to 0 or 1. The delivery crew can use this endpoint to update the order status.                                 |

**6. Categories:**
| Endpoint                  | Role        | Method | Purpose                                        |
|---------------------------|-------------|--------|------------------------------------------------|
| **/api/categories**       | All Users   | GET    | Returns all categories                          |
| **/api/categories/{id}**  | All Users   | GET    | Returns a specific category by ID               |
| **/api/categories**       | Manager     | POST   | Creates a new category                          |
| **/api/categories/{id}**  | Manager     | PUT    | Updates a specific category by ID               |
| **/api/categories/{id}**  | Manager     | PATCH  | Updates a specific category by ID               |
| **/api/categories/{id}**  | Manager     | DELETE | Deletes a specific category by ID               |

# How to run
1. This project is based on pipenv so make sure to install pipenv
2. Clone/Download Project and navigate to to project.
3. Activate your pipenv and install all pipenv dependencies.
    ```
    pipenv shell
    pipenv sync
    ```
4. Run project 
    ```
    python3 manage.py runserver
    ```
**Note:** Please find the default usernames and passwords in the notes.txt file. But you can start from completly new database.

## Clone and Run

To clone and run this Django REST API project locally, follow these steps:

### Prerequisites

Make sure you have the following tools installed on your system:

- Python
- Pipenv

### Clone the Repository

1. Open a terminal or command prompt.

2. Clone this repository using the following command:

   ```bash
   git clone <repository-url>
   ```
3. Navigate to the project's directory:
    ```
    cd <project-directory>
    ```

### Install Dependencies
1. Install Pipenv using pip (if not already installed):
    ```
    pip3 install pipenv
    ```
2. Install the project dependencies using Pipenv:
    ```
    pipenv install
    ```
    This command will create a virtual environment and install all the required dependencies specified in the Pipfile and Pipfile.lock files.

    **Note:** If you encounter any issues during the installation, make sure that you have the correct version of Python installed and that Pipenv is properly configured.

### efault Database and User Credentials
By default, this project is configured with a pre-populated .sqlite database that contains default categories and users. The user credentials can be found in the notes.txt file located in the project's root directory.

Note: If you wish to use the default database, you do not need to run migrations. The database is already set up with default data. However, if you want to start with a fresh database, you can follow the steps below.

### Run Database Migrations (Optional)
If you want to start with a new database instead of the default one, follow these steps:

1. Remove the existing database data by running the following command:
    ```
    python3 manage.py flush
    ```
2. Apply the database migrations to set up the initial database schema:
    ```
    python3 manage.py migrate
    ```

### Start the Development Server
```
python3 manage.py runserver
```



