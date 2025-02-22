Project Description
Welcome to the Django CRUD Application! 🚀

This project is a Django-based CRUD application that utilizes MySQL for database management and SQLAlchemy for ORM functionality. The system is designed to manage employees and departments efficiently, with performance optimized through Redis caching.

Key Features ✨
Django Framework: Built using the powerful Django web framework to handle both the front-end and back-end.
MySQL Database: The application uses MySQL as the database to store all employee and department data.
SQLAlchemy ORM: Manage your data with ease using SQLAlchemy for seamless integration with the database.
Redis Caching: Redis is used to cache data and improve application performance, particularly for frequently accessed employee and department lists.
JWT Authentication: Secure your application with JWT (JSON Web Tokens) for user login and authentication.
Data Validation: Input data is validated using Cerberus to ensure integrity when creating or updating departments and employees.
REST API: The application provides multiple API endpoints for:
Creating, updating, deleting, and reading employee and department records.
Ordering employees by salary.
Paginated and offset-based querying for better performance.
Technologies Used 💻
Django for the web framework
MySQL for the database
SQLAlchemy for ORM (Object-Relational Mapping)
Redis for caching
JWT for secure authentication
Cerberus for data validation
Django REST Framework (DRF) for building APIs
How to Set Up 🛠
Install Dependencies: Make sure MySQL, Redis, and Django are installed and configured.
Run Migrations: Set up the MySQL database and apply migrations with Django's migration commands.
Start the Application: Run the server using Django's development server to launch the application locally.
