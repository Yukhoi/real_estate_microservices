# Real Estate Microservices

This project is a microservices-based application for managing real estate properties and their associated rooms. It includes features for creating, updating, and querying properties and rooms, with user authentication and authorization handled via JWT.

## Features

- **Property Management**: Create, update, and query properties.
- **Room Management**: Manage rooms associated with properties.
- **JWT Authentication**: Secure endpoints with JSON Web Tokens.
- **Microservices Architecture**: Separate services for authentication，user and property management.

## Project Structure

- **Authentication Service**:
  - Handles user authentication and JWT generation.
  - Provides endpoints for user login and token verification.
  - Ensures secure access to other services by validating JWT tokens.

- **User Service**:
  - Manages user-related data, such as user profiles and roles.
  - Provides endpoints for creating, updating, and querying user information.
  - Integrates with the Authentication Service for secure user management.

- **Property Service**:
  - Manages real estate properties and their associated rooms.
  - Provides endpoints for creating, updating, and querying properties and rooms.
  - Includes business logic for property ownership validation and room management.
  - Uses JWT to ensure only authorized users can access or modify data.

## Database Chosen:

- **Authentication Service**: Redis
- **User Service**: PostgreSQL
- **Property Service**: PostgreSQL

## Prerequisites

- **Python 3.10+**
- **Docker** and **Docker Compose**
- **Postman** or **cURL** for testing APIs

## Setup Instructions

1. **Clone the Repository**:
 
  ```
  git clone https://github.com/Yukhoi/real_estate_microservices.git
  cd real_estate_microservices
  ```

2. **Run the services**: Use Docker Compose to build and run the services:

  `docker-compose up --build`

3. **Seed the Database**: Run the seeds.py script in another terminal to populate the database with initial data.

  ```
  docker exec -it user_service python seeds.py 
  docker exec -it property_service python seeds.py
  ```

## API Endpoints

### Authentication Service (auth_service)

1. **Login** `POST /auth/login`

``` bash
  curl -X POST "http://localhost:5002/auth/login" \  
  -H "Content-Type: application/json" \
  -d '{
      "email": "user@example.com",
      "password": "password123"
  }'
```

### User Service (user_service)

1. **Registration** `POST /user/register`

``` bash
  curl -X POST "http://localhost:5001/user/register" \
  -H "Content-Type: application/json" \
  -d '{
      "first_name": "Alice",
      "last_name": "Johnson",
      "email": "alice.johnson@example.com",
      "password": "password123"
  }'
```

2. **Update a user** `PUT /user/<int:user_id>`

``` bash
  curl -X PUT "http://localhost:5001/user/1" \
  -H "Content-Type: application/json" \
  -d '{
      "first_name": "John",
      "last_name": "Smith",
      "birth_date": "1995-01-02",
  }'
  ```

3. **Delete a user** `DELETE /user/<int:user_id>`

``` curl -X DELETE "http://localhost:5001/user/1" \ ```



### Property Service (property_service)

1. **Search by City** `GET /properties/search`

The user can search for properties in any city in the beginning, and then he can only search for properties in that one city.

``` bash
curl -X DELETE "http://localhost:5003/properties/search?city=Paris" \
-H "Authorization: Bearer <your-jwt-token>"
```

2. **Update Property** `PUT /properties/update`

``` bash
  curl -X PUT "http://localhost:5003/properties/update/1" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
      "name": "Updated Property Name",
      "description": "Updated description",
      "property_type": "Apartment",
      "city": "Paris",
      "rooms": [
          {
              "id": 1,
              "name": "Updated Living Room",
              "size": 35
          },
          {
              "name": "New Room",
              "size": 15
          }
      ]
  }'
```

3. **Create a Property** `POST properties/create`

``` bash
  curl -X PUT "http://localhost:5003/properties/update/1" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
      "name": "Updated Property Name",
      "description": "Updated description",
      "property_type": "Apartment",
      "city": "Paris",
      "rooms": [
          {
              "id": 1,
              "name": "Updated Living Room",
              "size": 35
          },
          {
              "name": "New Room",
              "size": 15
          }
      ]
  }'
```

**This project is never perfect, I'm looking forward to discuss with you during the interview!**











