# Work genius python challenge
This is the solution of work genius challenge completed by Yamin Tashakkori.



> The challenge instructions can be found on instructions.md file.



## How to run the application:


### Method 1: Run with docker compose

This method is recommended as it is easier to setup. make sure you have docker installed on your machine (docker compose will be installed if you use recent versions of docker).
Then run the below command inside the directory:

```bash
$ docker compose up -d
```

The API will be accessible in this addres: `http://localhost:8000/` and the openAPI docs can be found on `http://localhost:8000/redoc`

### Method 2: run locally.

Make sure you have `Python` and `PostgreSQL` installed on your machine.
 
### Step 1 : Configure the database:

Edit .env file in the project and provide your database DSN. a sample DSN is already set in the .env file.

For postgreSQL it should look like this:

> DATABASE_DSN=postgresql://{DB_USER_NAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

**Note** that if `DATABASE_URL` environment variable exists, it has higher priority to .env file to load the DB.

### Step 2: run the app

Then use the below command to run it locally:
```bash
$ uvicorn main:app
```

Then the app would be accessible in this address: `http://localhost:8000/` 

### Accessing openAPI interface

OpenAPI interface and docs would be accessible using `http://localhost:8000/redoc`

## Run tests:

The app uses SqLite to test the application. as SqLite will be installed along python3, you don't need to do anything unless you have removed this package. in that case, install SqLite first. Then run the below command:

```bash
$ pytest
```

It should test all the cases automatically. 

> Right now, the tests are depended to each other as one test case might provide data for another one. so running them individually may not work the best. It would be a good improvement to provide a fixed state of database before running each test but that would take more time to setup and run and I believe it is out of scope of this challenge.

