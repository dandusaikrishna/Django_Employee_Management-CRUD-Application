This project is a Django-based CRUD application that uses MySQL as the database with SQLAlchemy for managing database operations. The system provides features for managing employees and departments efficiently, integrated with Redis caching for better performance.

The application has the following key features:

Django Framework: The application uses Django to build the web interface and provide REST API functionality.
Database Management: MySQL is used for storing employee and department data, and SQLAlchemy is utilized for object-relational mapping (ORM).
Caching: To optimize data retrieval, Redis is used to cache frequently accessed data like employee and department lists.
Authentication: JWT (JSON Web Tokens) is implemented for secure login and user authentication.
Validation: Cerberus is used for input validation to ensure the integrity of department and employee data.

The system provides API endpoints for:
CRUD operations on employees and departments.
Fetching employees ordered by salary.
Efficient querying with pagination and offset.


Technologies Used:
Django for web framework
MySQL for database
SQLAlchemy for ORM
Redis for caching
JWT for authentication
Cerberus for data validation
Django REST Framework for API creation
