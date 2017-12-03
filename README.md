# f17-authentication-siritalilomu

## RESOURCES
* users
### ATTRIBUTES
* fname VARCHAR(50)
* lname VARCHAR(50)
* email VARCHAR(50)
* password VARCHAR(50)

## RESOURCES
* todos
### ATTRIBUTES
* todo VARCHAR(255)

## RESOURCES
* session
### ATTRIBUTES
* sessionId
* sessionData
* encryption
  * use bcrypt to encrypted the password which also generate a random salt

## Database Schema for users
* CREATE TABLE users (id INTEGER PRIMARY KEY, fname VARCHAR(50), lname VARCHAR(50), email VARCHAR(50), password VARCHAR(255));
## Database Schema for todos
* CREATE TABLE todos (id INTEGER PRIMARY KEY, todo VARCHAR(255));

## API todos
Name  | Method | Path
------|--------|-----
List  |  GET  |  /todos
Retrieve  | GET  |  /todos/id
Replace  |  PUT  |  /todos/id
Create  |  POST  |  /todos
Delete  | DELETE  | /todos/id

## API users
Name  | Method | Path
------|--------|-----
Create  |  POST  |  /users

## API current user data
Name  | Method | Path
------|--------|-----
Retrieve  |  GET  |  /me

## API cookie
Name  | Method | Path
------|--------|-----
Create  |  POST  |  /session
