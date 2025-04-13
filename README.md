# CRUD Project with FastAPI

## Overview
### This project involves building an interactive Dashboard to perform an API's basics operations (Create, Read, Update and Delete). The application uses Docker, which allows us to run anywhere if we have docker installed in our own machine. Steps Bellow ⬇️⬇️!

## Architecture:
![CRUD Image](assets/project_arch)

## Installing and Using Docker

```bash
docker-compose up -d --build
```

- Frontend:
Access the address http://localhost:8502

- Backend Docs with Swagger:
Access the address http://localhost:8000

- pgAdmin to directly access the Database:
Access the address http://localhost:8080
Standard credentials:

`User : admin@admin.com`

`Password : admin@123`

## Folder Structure and files:
```
├── README.md # Project Docs
├── .python-version # Local env Python version
├── backend # Backend Folder (FastAPI, SQLAlchemy, Uvicorn, Pydantic)
├── frontend # Frontend Folder (Streamlit, Requests, Pandas)
├── docker-compose.yml # Docker compose file (backend, frontend, postgres, pgAdmin)
└── requirements.txt # Requirements file containing all Dependencies to be installed
```

## Backend

The Backend is an API responsible for the communication between our Frontend and our Postgres Database. Let's detail it little bit.

## FastAPI

FastAPI is a web framework for building API's. It's based on Starlette, which is an asynchronous framework for building API's.

## Uvicorn

Uvicorn is an asynchronous web server based on ASGI, specified to assync web servers. It is the most recommended one to use with FastAPI.

## SQLAlchemy

SQLAlchemy is a library that allows us to communicate with our database. It's an ORM (Object Relational Mapper), which is an object-relational feature that allows the communication with a database using an object. It's compatible with many databases (MySQL, PostgreSQL, SQlite, Oracle, SQL Server and many more). SQLAlchemy even handles data sanitization, avoiding SQL Injection attacks.

## Pydantic
Pydantic it's a library responsible for validating the data that we're receiving from the API.

## docker-compose.yml
This file `docker-compose.yml` defines an application with 4 services: `postgres`, `backend`, `frontend`, and `pgAdmin`, and creates a network `mynetwork`. 

#### Postgres:
* `image: postgres:latest`: This service uses the latest PostgreSQL image available on Docker Hub.
* `volumes`: Maps the `/var/lib/postgresql/data` directory inside the PostgreSQL container to a volume called `postgres_data` on the host system. This ensures that the database data persists even when the container is stopped.
* `environment`: Defines environment variables to configure the PostgreSQL database, such as the database name (`POSTGRES_DB`), username (`POSTGRES_USER`), and password (`POSTGRES_PASSWORD`).
* `networks`: Specifies that this service is on the network called `mynetwork`.

#### Backend

* `build:` Specifies that Docker should build an image for this service using a Dockerfile located in the `./backend` directory.
* `volumes:` Maps the `./backend` directory (on the host system) to the `/app` directory inside the container. This allows changes in the backend source code to be reflected in the container in real time.
* `environment:` Defines the `DATABASE_URL` environment variable, which specifies the connection URL for the PostgreSQL database.
* `ports:` Maps port `8000` on the host system to port `8000` on the container, allowing the service to be accessed through port `8000`.
* `depends_on:` Indicates that this service depends on the `postgres` service, ensuring that the database is ready before the backend is started.
* `networks:` Also specifies that this service is on the mynetwork `network`.

Backend Directory Structure:
```
├── Dockerfile
├── crud.py # Contains the functions for each operation using the SLQAlchemy ORM
├── database.py # Contains the config to the SQLAlchemy
├── main.py
├── models.py # Reflects the database table model
├── schemas.py # Contains the Pydantic validator model, which is going to be input by the user. It doesn't have the ID and created_at fields
├── router.py # Contains all the routes calling the funcions from the crud.py file
└── requirements.txt # Requirements and libs for the Backend
```

#### Frontend
* `build`: Similar to the backend, specifies that Docker should build an image for this service using a Dockerfile located in the `./frontend` directory.
* `volumes`: Maps the `./frontend` directory (on the host system) to the `/app` directory inside the container, allowing real-time changes.
* `ports`: Maps port `8502` on the host system to port 8502 on the container, allowing access to the frontend through port `8502`.
* `networks`: Specifies that this service is also on the `mynetwork` network.
  
Frontend directory Structure:
```
├── Dockerfile
├── .dockerignore
├── app.py
└── requirements.txt # Requirements and libs for the Backend
```

### Networks:
* `mynetwork`: Defines a custom network for the services to communicate with each other.

### Volumes:
* `postgres_data`: Defines a volume to store the PostgreSQL database data.

## `database.py` File

The `database.py` file is responsible for setting up the database connection using SQLAlchemy. It handles both establishing the connection with the database and creating the database session.

If you want to switch databases, you only need to change the connection URL, which is stored in the POSTGRES_URL variable. SQLAlchemy is compatible with various databases, such as MySQL, PostgreSQL, SQLite, Oracle, Microsoft SQL Server, Firebird, Sybase, and even Microsoft Access.

The main components of this file are the engine, which is the connection to the database, and SessionLocal, which is the session used to interact with the database. SessionLocal is responsible for executing queries in the database.

Remember:
1) Declare the Database URL
2) Create the engine using the `create_engine` statement
3) Create a Session for the database
4) Create the ORM Base (The model is going to inherit from it)
5) Create a Session generator to be re-used (I created a `get_db()`)

## `models.py` File:
The models.py file is responsible for defining the SQLAlchemy models, which are the classes that represent the tables in the database. These models are used to communicate with the database.
In this file, we define the table name, the fields, and their data types. We can also include automatically generated fields, such as the `id` and `created_at`. For example:
For the `id` field, by setting the field type to `Integer` and using the `primary_key=True` parameter, SQLAlchemy automatically recognizes this field as the primary key of the table.

For the `created_at` field, by setting the field type to DateTime and using the default=datetime parameter, SQLAlchemy understands that this field will store the creation date of the record.

Remember:
1) The model doesn't know which database is created, it's indifferent. It'll import the base from the database!
2) Declare your table

## `schemas.py` File:
The `schemas.py` file is responsible for defining the Pydantic schemas, which are the classes that define the data types used in the API. These schemas are used to validate the data received by the API and to define the data types that are returned by the API.

Pydantic is the main library for data validation in Python, and is used by FastAPI to perform validation on the incoming data and to define the data types returned by the API.

Additionally, Pydantic integrates very well with SQLAlchemy, the library used to communicate with the database.

`ProductBase` Schema
This is the base schema for creating products. It defines the fields and validation rules for data received by the API. It is used for both validating incoming data and defining the response types that are returned by the API.

`ProductCreate` Schema
This schema is used when creating a product. It inherits from ProductBase and adds an id field, which is used to uniquely identify the product in the database.

`ProductResponse` Schema
This schema is used for the response sent back by the API. It inherits from ProductBase and adds two extra fields: id and created_at. These fields are generated by the database.

`ProductUpdate` Schema
This schema is used for updating product data. It is similar to ProductBase but with optional fields. Not all fields need to be provided for an update, which makes it flexible for partial updates.

## `crud.py` File:
The `router.py` file is responsible for defining the API routes using FastAPI. It is where the routes are set up and where the functions that will be executed for each route are defined. Each function defined here takes a parameter called request, which is the object that contains the data of the incoming request.

The main parameters are:

* `path`: The route path, which defines the URL endpoint.

* `methods`: The HTTP methods that the route accepts.

* `response_model`: The schema that is returned by the route.

```python
@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db:Session = Depends(get_db)):
    db_product = get_product_by_id(product_id, db=db)
    if db_product is None:
        raise HTTPException(status_code=404, detail= "Product not found")
    return db_product
```

## `main.py` File:
The `main.py` file is responsible for defining the FastAPI application and also for setting up the `Uvicorn` web server. It is where you configure the web server, as well as its settings, such as the host and port.

## Streamlit
Streamlit is a library for building web applications with Python. It is widely used for creating dashboards and also for building applications that consume APIs.