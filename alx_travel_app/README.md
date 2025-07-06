# ALX Travel App

A Django REST API for managing property listings and bookings.

## Features

- Property listings with detailed information
- Booking system with availability checking
- User authentication and authorization
- RESTful API endpoints
- Swagger documentation
- MySQL database support
- CORS support

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mj-weshh/alx_travel_app.git
   cd alx_travel_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirement.txt
   ```

4. Create a `.env` file in the project root with your database configuration:
   ```
   MYSQL_DATABASE=alx_travel_db
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, you can access the following endpoints:

- API Documentation (Swagger UI): http://127.0.0.1:8000/swagger/
  ![Screenshot 2025-07-06 110359](https://github.com/user-attachments/assets/a8faeb99-80df-461f-8f33-629fdbbcbeeb)
- Admin Interface: http://127.0.0.1:8000/admin/
  ![Screenshot 2025-07-06 110336](https://github.com/user-attachments/assets/69a044f8-7d9f-41a9-a42d-1d0685851ead)
- API Root: http://127.0.0.1:8000/api/
  ![Screenshot 2025-07-06 110344](https://github.com/user-attachments/assets/5a159416-2208-4c6a-8f99-b26a386be1da)

## Available Endpoints

- `GET /api/listings/` - List all property listings
- `POST /api/listings/` - Create a new listing (authenticated)
- `GET /api/listings/{id}/` - Get listing details
- `GET /api/listings/{id}/available/` - Check availability for specific dates
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create a new booking
- `POST /api/bookings/{id}/cancel/` - Cancel a booking

## Project Structure

```
alx_travel_app/
├── alx_travel_app/         # Project settings
├── listings/               # Listings app
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Admin interface configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── urls.py           # App URLs
│   └── views.py          # API views
├── .env                  # Environment variables
├── manage.py            # Django management script
└── requirements.txt     # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
