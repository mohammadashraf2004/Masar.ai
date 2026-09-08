"""
backend/seeds/seed_tool_fastapi.py

Adds topic content (lessons/exercises/quiz/project) to the FastAPI
tool course, which must already exist as a shell (seeded by
seeds/seed_tool_courses.py — TOOL_SLUG "fastapi"). Idempotent — safe
to re-run.

Run from backend/:
    docker compose exec api python seeds/seed_tool_fastapi.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.learning, app.models.progress    # noqa: F401
import app.models.community, app.models.wallet, app.models.auth_token  # noqa: F401
import app.models.challenge, app.models.exam                         # noqa: F401
from app.models.learning import Lesson, Exercise, Quiz, Project, DifficultyLevel
from app.models.tool_course import ToolCourse, ToolTopic

Base.metadata.create_all(bind=engine)

TOOL_SLUG = "fastapi-serving"  # must already exist — created by seed_tool_courses.py

# ---------------------------------------------------------------------------
# Topics (flat — no levels). Add one dict per topic, in the order they
# should appear.
# ---------------------------------------------------------------------------
TOPICS = [
    {
        # ToolTopic fields
        "title":            "FastAPI Basics",
        "slug":              "fastapi-basics",
        "description":       "What FastAPI is, installing it, and building your first API with automatic docs.",
        "order":             1,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.5,
        "skill_tags":        ["fastapi", "python", "api"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "FastAPI Basics",
            "content": """## 1. What is FastAPI?

FastAPI is a Python framework for building APIs.

For example, imagine your frontend asks:

> "Give me the information about course CSE251"

Your FastAPI backend receives the request:

```
Frontend → FastAPI → Python code → Response
```

and returns:

```json
{
  "course": "CSE251",
  "name": "Machine Learning",
  "credits": 3
}
```

## 2. Install FastAPI

Inside your virtual environment:

```bash
pip install fastapi uvicorn
```

Check the install:

```bash
pip show fastapi
```

## 3. Create Your First API

Create a file `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI!"}
```

That's it! You've created your first FastAPI application.

## 4. Run the API

```bash
uvicorn main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

Open `http://127.0.0.1:8000` in your browser and you'll get:

```json
{
  "message": "Hello FastAPI!"
}
```

## 5. Understanding `@app.get("/")`

This decorator means: when someone sends a GET request to `/`, run the
function below it.

```
GET /
   ↓
home()
   ↓
{"message": "Hello FastAPI!"}
```

## 6. Add Another Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI!"}

@app.get("/about")
def about():
    return {
        "name": "Mohammad",
        "field": "AI Engineering"
    }
```

Visit `http://127.0.0.1:8000/about` and you'll get:

```json
{
  "name": "Mohammad",
  "field": "AI Engineering"
}
```

## 7. Automatic Documentation

FastAPI automatically generates interactive docs from your Python code:

- `http://127.0.0.1:8000/docs` — interactive Swagger UI where you can
  click endpoints and test them directly from the browser.
- `http://127.0.0.1:8000/redoc` — alternative ReDoc-style docs.

## 🧠 The 4 Things to Remember

1. `from fastapi import FastAPI` — imports FastAPI.
2. `app = FastAPI()` — creates your application.
3. `@app.get("/")` — creates a GET endpoint.
4. `uvicorn main:app --reload` — runs your application.

## Mental Model

```
main.py
   │
   ├── FastAPI app
   │
   ├── GET /
   │
   ├── GET /about
   │
   └── ...
        ↓
     Uvicorn
        ↓
   http://localhost:8000
```

Don't worry about databases, authentication, Pydantic, or AI yet —
we'll build everything step by step over the next lessons.""",
            "order":                1,
            "estimated_minutes":    50,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Three Endpoints",
                "description":   (
                    "Create three GET endpoints in a FastAPI app: `/`, `/hello`, "
                    "and `/info`.\n\n"
                    "- `/hello` should return `{\"message\": \"Hello Mohammad\"}`\n"
                    "- `/info` should return information about an AI engineer "
                    "(e.g. name and field)\n\n"
                    "Run the app with uvicorn and verify all three routes work "
                    "in the `/docs` interactive page."
                ),
                "difficulty":    DifficultyLevel.beginner,
                "starter_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "@app.get(\"/\")\n"
                    "def home():\n"
                    "    # TODO\n"
                    "    pass\n\n"
                    "# TODO: add /hello\n\n"
                    "# TODO: add /info\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "@app.get(\"/\")\n"
                    "def home():\n"
                    "    return {\"message\": \"Hello FastAPI!\"}\n\n"
                    "@app.get(\"/hello\")\n"
                    "def hello():\n"
                    "    return {\"message\": \"Hello Mohammad\"}\n\n"
                    "@app.get(\"/info\")\n"
                    "def info():\n"
                    "    return {\"name\": \"Mohammad\", \"field\": \"AI Engineering\"}\n"
                ),
                "skill_tested":  ["fastapi", "routing"],
            },
        ],
        "quiz": {
            "title": "FastAPI Basics Quiz",
            "questions": [
                {
                    "question": "What command installs FastAPI and its ASGI server?",
                    "options": [
                        "pip install fastapi uvicorn",
                        "pip install fastapi-server",
                        "npm install fastapi",
                        "pip install django uvicorn",
                    ],
                    "correct": 0,
                    "explanation": "uvicorn is the ASGI server used to actually run a FastAPI app; both packages are installed together.",
                },
                {
                    "question": "Which line creates the FastAPI application instance?",
                    "options": [
                        "app = FastAPI()",
                        "app = fastapi.run()",
                        "app = App()",
                        "app = uvicorn.App()",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI() instantiates the application object that routes and middleware attach to.",
                },
                {
                    "question": "What does the `@app.get(\"/\")` decorator do?",
                    "options": [
                        "Registers a function to handle GET requests to the `/` path",
                        "Deletes the `/` route",
                        "Creates a database table",
                        "Starts the uvicorn server",
                    ],
                    "correct": 0,
                    "explanation": "It's a route decorator that maps GET requests on `/` to the function defined below it.",
                },
                {
                    "question": "What command runs a FastAPI app defined in main.py with auto-reload on code changes?",
                    "options": [
                        "uvicorn main:app --reload",
                        "python main.py --serve",
                        "fastapi run main.py",
                        "flask run main.py",
                    ],
                    "correct": 0,
                    "explanation": "`uvicorn main:app --reload` points uvicorn at the `app` object inside `main.py` and restarts on file changes.",
                },
                {
                    "question": "Where can you find FastAPI's automatically generated interactive API docs?",
                    "options": [
                        "/docs",
                        "/swagger.html",
                        "/api-docs",
                        "/help",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI serves interactive Swagger UI docs at `/docs` (and ReDoc at `/redoc`) with zero extra config.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Personal Info API",
            "description":      (
                "Build a small FastAPI app with at least four GET endpoints "
                "returning JSON about yourself: `/`, `/about`, `/skills`, and "
                "`/contact`. Verify every endpoint through the `/docs` UI."
            ),
            "difficulty":       DifficultyLevel.beginner,
            "tech_stack":       ["FastAPI", "Python", "Uvicorn"],
            "objectives": [
                "Set up a FastAPI project and virtual environment",
                "Define multiple GET endpoints returning JSON",
                "Run the app locally with uvicorn --reload",
                "Explore and test endpoints via /docs",
            ],
            "rubric": {
                "endpoints_work":       "All endpoints return valid JSON with 200 status",
                "code_quality":         "Clear function names, one responsibility per endpoint",
                "docs_verified":        "Screenshot or note confirming /docs was used to test routes",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Routes & HTTP Methods",
        "slug":              "fastapi-routes-http-methods",
        "description":       "GET, POST, PUT, and DELETE — the four core HTTP methods for reading, creating, updating, and deleting data.",
        "order":             2,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.5,
        "skill_tags":        ["fastapi", "python", "api", "http"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Routes & HTTP Methods",
            "content": """## The 4 Most Important HTTP Methods

- **GET** → get data
- **POST** → create data
- **PUT** → update data
- **DELETE** → delete data

We'll learn them with one simple example.

## 1. GET — Get Data

You already saw this:

```python
@app.get("/")
def home():
    return {"message": "Hello FastAPI!"}
```

When the client sends `GET /`, FastAPI runs `home()`.

Think: **GET = "Give me something"**

```python
@app.get("/users")
def get_users():
    return {
        "users": ["Ali", "Ahmed", "Mohammad"]
    }
```

Visiting `http://127.0.0.1:8000/users` returns:

```json
{
    "users": ["Ali", "Ahmed", "Mohammad"]
}
```

## 2. POST — Create Data

Now imagine we want to create a new user:

```python
@app.post("/users")
def create_user():
    return {
        "message": "User created"
    }
```

The important difference:

- `@app.get("/users")` means **"Give me users."**
- `@app.post("/users")` means **"Create a user."**

## 3. PUT — Update Data

```python
@app.put("/users")
def update_user():
    return {
        "message": "User updated"
    }
```

Think: **PUT = "Change existing data"**

## 4. DELETE — Delete Data

```python
@app.delete("/users")
def delete_user():
    return {
        "message": "User deleted"
    }
```

Think: **DELETE = "Remove data"**

## 🧠 The Easiest Way to Remember

Imagine a restaurant:

| Method | Meaning |
|---|---|
| GET | "Show me the menu" |
| POST | "Add this order" |
| PUT | "Change my order" |
| DELETE | "Cancel my order" |

Or with users:

```
GET       → Get users
POST      → Create user
PUT       → Update user
DELETE    → Delete user
```

## 5. Putting It Together

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}

@app.get("/users")
def get_users():
    return {
        "users": ["Ali", "Ahmed", "Mohammad"]
    }

@app.post("/users")
def create_user():
    return {
        "message": "User created"
    }

@app.put("/users")
def update_user():
    return {
        "message": "User updated"
    }

@app.delete("/users")
def delete_user():
    return {
        "message": "User deleted"
    }
```

Run `uvicorn main:app --reload`, then open `http://127.0.0.1:8000/docs`.
You'll see all four methods and can click **Try it out** to execute
them directly.

## ⚠️ One Important Problem

Our POST endpoint currently doesn't receive any information. How do we
tell FastAPI something like:

```json
{
    "name": "Mohammad",
    "age": 24
}
```

That's where request bodies and Pydantic come in — one of the most
important parts of FastAPI, coming in a later lesson.

## 🧠 What You've Learned

```
FastAPI
   │
   ├── GET     → read
   ├── POST    → create
   ├── PUT     → update
   └── DELETE  → delete
```""",
            "order":                2,
            "estimated_minutes":    45,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Products CRUD Routes",
                "description":   (
                    "Create four endpoints for `/products`:\n\n"
                    "- `GET /products`\n"
                    "- `POST /products`\n"
                    "- `PUT /products`\n"
                    "- `DELETE /products`\n\n"
                    "Make each one return a different message describing what "
                    "it does. Test all four in `/docs`."
                ),
                "difficulty":    DifficultyLevel.beginner,
                "starter_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: GET /products\n\n"
                    "# TODO: POST /products\n\n"
                    "# TODO: PUT /products\n\n"
                    "# TODO: DELETE /products\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "@app.get(\"/products\")\n"
                    "def get_products():\n"
                    "    return {\"message\": \"Here are the products\"}\n\n"
                    "@app.post(\"/products\")\n"
                    "def create_product():\n"
                    "    return {\"message\": \"Product created\"}\n\n"
                    "@app.put(\"/products\")\n"
                    "def update_product():\n"
                    "    return {\"message\": \"Product updated\"}\n\n"
                    "@app.delete(\"/products\")\n"
                    "def delete_product():\n"
                    "    return {\"message\": \"Product deleted\"}\n"
                ),
                "skill_tested":  ["fastapi", "http-methods", "routing"],
            },
        ],
        "quiz": {
            "title": "Routes & HTTP Methods Quiz",
            "questions": [
                {
                    "question": "Which HTTP method is used to retrieve data?",
                    "options": ["GET", "POST", "PUT", "DELETE"],
                    "correct": 0,
                    "explanation": "GET is used to read/fetch data without modifying anything on the server.",
                },
                {
                    "question": "Which method would you use to create a new user?",
                    "options": ["POST", "GET", "DELETE", "PUT"],
                    "correct": 0,
                    "explanation": "POST is used to create new resources, like adding a new user.",
                },
                {
                    "question": "What does @app.put(\"/users\") typically represent?",
                    "options": [
                        "Updating existing data",
                        "Reading data",
                        "Deleting data",
                        "Creating a new database",
                    ],
                    "correct": 0,
                    "explanation": "PUT is conventionally used to update/replace existing data.",
                },
                {
                    "question": "What's the key difference between GET /users and POST /users on the same path?",
                    "options": [
                        "GET reads data, POST creates data — same path, different action",
                        "They do exactly the same thing",
                        "POST is faster than GET",
                        "GET requires a request body but POST doesn't",
                    ],
                    "correct": 0,
                    "explanation": "The HTTP method determines the action even when the URL path is identical.",
                },
                {
                    "question": "Where can you interactively test all four HTTP methods on your running FastAPI app?",
                    "options": ["/docs", "/test", "/methods", "/api"],
                    "correct": 0,
                    "explanation": "FastAPI's auto-generated /docs page lets you 'Try it out' on every registered endpoint.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Products CRUD Skeleton",
            "description":      (
                "Build a FastAPI app with full GET/POST/PUT/DELETE routes for "
                "`/products`, each returning a distinct, clearly worded JSON "
                "message. Test every route through /docs."
            ),
            "difficulty":       DifficultyLevel.beginner,
            "tech_stack":       ["FastAPI", "Python", "Uvicorn"],
            "objectives": [
                "Define all four HTTP methods on the same route path",
                "Distinguish GET/POST/PUT/DELETE semantics in responses",
                "Test each method via the /docs interactive UI",
            ],
            "rubric": {
                "all_methods_present": "GET, POST, PUT, DELETE all implemented on /products",
                "distinct_responses":  "Each method returns a unique, descriptive message",
                "docs_tested":         "Confirms testing via /docs Try it out",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Path & Query Parameters",
        "slug":              "fastapi-path-query-parameters",
        "description":       "Identify specific resources with path parameters and filter/search with query parameters.",
        "order":             3,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   2.0,
        "skill_tags":        ["fastapi", "python", "api", "parameters"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Path & Query Parameters",
            "content": """This lesson is very important — you'll use parameters in almost
every real FastAPI project.

## 1. Path Parameters

Imagine we have users: User 1, User 2, User 3. Instead of creating
separate routes like `/users1`, `/users2`, `/users3`, we use:

```
/users/1
/users/2
/users/3
```

The `1` is a **path parameter**.

## 2. Create a Path Parameter

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }
```

Visiting `http://127.0.0.1:8000/users/5` gives:

```json
{
    "user_id": 5
}
```

## 3. Why `{user_id}`?

`{user_id}` means "there will be a value here," and
`def get_user(user_id: int):` receives that value.

```
/users/25
     ↓
user_id = 25
```

## 4. FastAPI Validates the Type

Since we wrote `user_id: int`, it must be an integer.

- `/users/25` — works
- `/users/hello` — FastAPI automatically returns a validation error

This is one of the things that makes FastAPI so convenient.

## 5. Multiple Path Parameters

```python
@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {
        "user_id": user_id,
        "order_id": order_id
    }
```

Request `/users/10/orders/50` returns:

```json
{
    "user_id": 10,
    "order_id": 50
}
```

## 6. Query Parameters

Now imagine we want to search users:

```
/users?name=Mohammad
```

Here, `name=Mohammad` is a **query parameter**.

## 7. Create a Query Parameter

```python
@app.get("/users")
def search_users(name: str):
    return {
        "search": name
    }
```

Request `/users?name=Mohammad` returns:

```json
{
    "search": "Mohammad"
}
```

## 8. Path vs Query — The Most Important Part

**Path parameter** — `/users/25` means "get user number 25":

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    ...
```

**Query parameter** — `/users?name=Mohammad` means "search users whose
name is Mohammad":

```python
@app.get("/users")
def search_users(name: str):
    ...
```

```
PATH
/users/25
      ↑
   specific resource

QUERY
/users?name=Ali
       ↑
   filter/search
```

## 9. Multiple Query Parameters

```python
@app.get("/products")
def search_products(category: str, price: int):
    return {
        "category": category,
        "price": price
    }
```

Request `/products?category=laptop&price=50000` returns:

```json
{
    "category": "laptop",
    "price": 50000
}
```

## 10. Optional Query Parameters

Give a default value to make a parameter optional:

```python
@app.get("/users")
def get_users(name: str = "all"):
    return {
        "name": name
    }
```

- `/users` → `{"name": "all"}`
- `/users?name=Ahmed` → `{"name": "Ahmed"}`

## 🧠 Simple Mental Model

```
URL
 │
 ├── /users/10
 │      ↑
 │      PATH PARAMETER
 │
 └── /users?name=Ali
          ↑
          QUERY PARAMETER
```

**Path** — use it to identify what resource you're talking about:
`/users/10`, `/products/50`, `/courses/CSE251`

**Query** — use it to filter, search, sort, or customize the request:
`/users?name=Ali`, `/products?category=laptop`, `/products?price=50000`""",
            "order":                3,
            "estimated_minutes":    60,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Course Lookup & Search",
                "description":   (
                    "Build three endpoints:\n\n"
                    "1. `GET /courses/{course_id}` — e.g. `/courses/CSE251` "
                    "returns `{\"course_id\": \"CSE251\"}`\n"
                    "2. `GET /courses?name=Machine Learning` — returns the "
                    "course name\n"
                    "3. `GET /courses?name=Machine Learning&credits=3` — "
                    "returns both the name and credits\n\n"
                    "Test all three in `/docs`."
                ),
                "difficulty":    DifficultyLevel.beginner,
                "starter_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: GET /courses/{course_id}\n\n"
                    "# TODO: GET /courses?name=...\n\n"
                    "# TODO: GET /courses?name=...&credits=...\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI\n\n"
                    "app = FastAPI()\n\n"
                    "@app.get(\"/courses/{course_id}\")\n"
                    "def get_course(course_id: str):\n"
                    "    return {\"course_id\": course_id}\n\n"
                    "@app.get(\"/courses\")\n"
                    "def search_courses(name: str, credits: int = None):\n"
                    "    if credits is not None:\n"
                    "        return {\"name\": name, \"credits\": credits}\n"
                    "    return {\"name\": name}\n"
                ),
                "skill_tested":  ["fastapi", "path-parameters", "query-parameters"],
            },
        ],
        "quiz": {
            "title": "Path & Query Parameters Quiz",
            "questions": [
                {
                    "question": "In @app.get(\"/users/{user_id}\"), what kind of parameter is user_id?",
                    "options": ["Path parameter", "Query parameter", "Header parameter", "Body parameter"],
                    "correct": 0,
                    "explanation": "Values embedded directly in the URL path, marked with curly braces, are path parameters.",
                },
                {
                    "question": "What happens if you request /users/hello when the route expects user_id: int?",
                    "options": [
                        "FastAPI automatically returns a validation error",
                        "It silently converts 'hello' to 0",
                        "The server crashes with no response",
                        "FastAPI ignores the type hint and returns the string",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI validates path parameter types automatically and returns a 422 error for mismatches.",
                },
                {
                    "question": "Which URL correctly uses a query parameter to search by name?",
                    "options": [
                        "/users?name=Mohammad",
                        "/users/name/Mohammad",
                        "/users/{name}",
                        "/users#name=Mohammad",
                    ],
                    "correct": 0,
                    "explanation": "Query parameters follow a '?' and use key=value pairs, e.g. ?name=Mohammad.",
                },
                {
                    "question": "How do you make a query parameter optional with a default value of 'all'?",
                    "options": [
                        "def get_users(name: str = \"all\"):",
                        "def get_users(name: str, optional=True):",
                        "def get_users(name: Optional):",
                        "def get_users(*, name):",
                    ],
                    "correct": 0,
                    "explanation": "Assigning a default value in the function signature makes that query parameter optional.",
                },
                {
                    "question": "Conceptually, when should you use a path parameter instead of a query parameter?",
                    "options": [
                        "When identifying one specific resource, like /products/50",
                        "When filtering or searching a collection",
                        "When sorting results",
                        "Path and query parameters are always interchangeable",
                    ],
                    "correct": 0,
                    "explanation": "Path parameters identify a specific resource; query parameters filter, search, or customize a request.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Course Catalog API",
            "description":      (
                "Build a small FastAPI app that looks up individual courses by "
                "ID via a path parameter and searches courses by name and "
                "credits via query parameters."
            ),
            "difficulty":       DifficultyLevel.beginner,
            "tech_stack":       ["FastAPI", "Python", "Uvicorn"],
            "objectives": [
                "Implement a path-parameter route for a single resource",
                "Implement a query-parameter route for search/filter",
                "Combine multiple query parameters, one optional",
            ],
            "rubric": {
                "path_param_route":  "GET /courses/{course_id} returns the correct id, type-validated as needed",
                "query_param_route": "GET /courses?name=... returns matching data",
                "optional_param":    "At least one query parameter has a working default value",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Request Body & Pydantic",
        "slug":              "fastapi-request-body-pydantic",
        "description":       "Send structured JSON in a request body and validate it automatically with Pydantic models.",
        "order":             4,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   2.0,
        "skill_tags":        ["fastapi", "python", "api", "pydantic"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Request Body & Pydantic",
            "content": """This is one of the most important FastAPI lessons.

Until now, we sent data through the URL — `/users/10` or
`/users?name=Mohammad`. But when creating or updating something, we
usually send a JSON body, for example:

```json
{
  "name": "Mohammad",
  "age": 24,
  "email": "mohammad@example.com"
}
```

FastAPI + Pydantic makes this extremely easy.

## 1. What is a Request Body?

Imagine your frontend wants to create a user. It sends `POST /users`
with:

```json
{
  "name": "Mohammad",
  "age": 24
}
```

That JSON is the request body:

```
URL
  ↓
POST /users

Body
  ↓
{
  "name": "Mohammad",
  "age": 24
}
```

## 2. Create a Pydantic Model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
```

This tells FastAPI: a `User` must have a `name` that is a string and
an `age` that is an integer.

## 3. Use the Model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user
```

## 4. Test It

Open `http://127.0.0.1:8000/docs`, find `POST /users`, click **Try it
out**, and put in the JSON box:

```json
{
  "name": "Mohammad",
  "age": 24
}
```

Click Execute — you'll get the same JSON back. 🎉 You just created an
API that receives JSON.

## 5. Why Pydantic Is Useful

Suppose someone sends:

```json
{
  "name": "Mohammad",
  "age": "hello"
}
```

But we said `age: int`. FastAPI automatically detects the problem.
Instead of your application crashing somewhere later, FastAPI returns
a validation error. That's powerful.

## 6. Add More Fields

```python
class User(BaseModel):
    name: str
    age: int
    email: str
```

Now the expected JSON includes `email` too.

## 7. Optional Fields

Give a field a default value to make it optional:

```python
class User(BaseModel):
    name: str
    age: int
    email: str = ""
```

Now this is valid without `email`, which defaults to `""`.

## 8. Default Values

```python
class User(BaseModel):
    name: str
    age: int
    active: bool = True
```

If the client sends just `name` and `age`, Pydantic fills in
`"active": true` automatically.

## 9. Pydantic = Data Rules

The easiest way to think about Pydantic:

```
Pydantic Model
      ↓
Defines the shape of your data
      ↓
FastAPI validates incoming data
```

For example:

```python
class Course(BaseModel):
    code: str
    name: str
    credits: int
```

means:

```
Course
 ├── code     → string
 ├── name     → string
 └── credits  → integer
```

The frontend must then send something like:

```json
{
  "code": "CSE251",
  "name": "Machine Learning",
  "credits": 3
}
```

## 10. This Is Extremely Useful for Your AI Projects

Imagine your RAG API. The frontend sends:

```json
{
  "question": "What are the requirements for graduation?"
}
```

You define:

```python
class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(data: Question):
    return {
        "answer": "..."
    }
```

Later, your actual system becomes:

```
Frontend
   ↓
POST /ask
   ↓
Pydantic
   ↓
FastAPI
   ↓
LangChain / LangGraph
   ↓
Qdrant
   ↓
LLM
   ↓
Answer
```

This is exactly the kind of API you'll eventually build for your RAG
system.

## 🧠 The Most Important Pattern

Memorize this:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user
```

That's the basic FastAPI pattern for receiving JSON.""",
            "order":                4,
            "estimated_minutes":    55,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Create a Course via Request Body",
                "description":   (
                    "Create a `Course` Pydantic model with `code: str`, "
                    "`name: str`, and `credits: int`. Then build "
                    "`POST /courses` that accepts a JSON body matching this "
                    "model and returns it back.\n\n"
                    "Test with:\n\n"
                    "```json\n"
                    "{\n"
                    "  \"code\": \"CSE251\",\n"
                    "  \"name\": \"Machine Learning\",\n"
                    "  \"credits\": 3\n"
                    "}\n"
                    "```"
                ),
                "difficulty":    DifficultyLevel.beginner,
                "starter_code": (
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: define Course model\n\n"
                    "# TODO: POST /courses\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "class Course(BaseModel):\n"
                    "    code: str\n"
                    "    name: str\n"
                    "    credits: int\n\n"
                    "@app.post(\"/courses\")\n"
                    "def create_course(course: Course):\n"
                    "    return course\n"
                ),
                "skill_tested":  ["fastapi", "pydantic", "request-body"],
            },
        ],
        "quiz": {
            "title": "Request Body & Pydantic Quiz",
            "questions": [
                {
                    "question": "What class do you inherit from to define a Pydantic model?",
                    "options": ["BaseModel", "PydanticModel", "Schema", "RequestBody"],
                    "correct": 0,
                    "explanation": "Pydantic models subclass BaseModel from the pydantic package.",
                },
                {
                    "question": "What happens if a client sends age: \"hello\" but the model defines age: int?",
                    "options": [
                        "FastAPI automatically returns a validation error",
                        "The server crashes with no message",
                        "Pydantic silently converts it to 0",
                        "FastAPI ignores the field entirely",
                    ],
                    "correct": 0,
                    "explanation": "Pydantic validates incoming data against the model's type hints and FastAPI surfaces mismatches as validation errors.",
                },
                {
                    "question": "How do you make a Pydantic field optional with a default of an empty string?",
                    "options": [
                        "email: str = \"\"",
                        "email: str?",
                        "email: Optional",
                        "email: str = required",
                    ],
                    "correct": 0,
                    "explanation": "Assigning a default value directly in the model definition makes that field optional.",
                },
                {
                    "question": "In a route like def create_user(user: User):, where does 'user' come from?",
                    "options": [
                        "FastAPI parses and validates the JSON request body into a User instance",
                        "It's a query parameter",
                        "It's a path parameter",
                        "It must be manually parsed with json.loads()",
                    ],
                    "correct": 0,
                    "explanation": "Declaring a Pydantic model as a parameter tells FastAPI to read and validate the JSON request body automatically.",
                },
                {
                    "question": "Why is Pydantic especially useful for an /ask endpoint in a RAG API?",
                    "options": [
                        "It validates that the incoming question field is a string before it reaches your LLM pipeline",
                        "It automatically calls the LLM for you",
                        "It replaces the need for LangChain",
                        "It stores the question directly into Qdrant",
                    ],
                    "correct": 0,
                    "explanation": "Pydantic ensures the request shape is correct before your code (and downstream LangChain/Qdrant/LLM calls) ever runs.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "User Signup Endpoint",
            "description":      (
                "Build a FastAPI app with a User Pydantic model (name, age, "
                "email with a default, active with a default) and a "
                "POST /users endpoint that accepts and returns it."
            ),
            "difficulty":       DifficultyLevel.beginner,
            "tech_stack":       ["FastAPI", "Pydantic", "Python", "Uvicorn"],
            "objectives": [
                "Define a Pydantic model with required and optional fields",
                "Accept a JSON request body via a POST route",
                "Trigger and observe a validation error on bad input",
            ],
            "rubric": {
                "model_defined":      "Pydantic model has correct required/optional fields",
                "endpoint_works":     "POST /users accepts valid JSON and returns it",
                "validation_checked": "Confirms a validation error occurs on bad input (e.g. wrong type)",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Response Models & Status Codes",
        "slug":              "fastapi-response-models-status-codes",
        "description":       "Control exactly what an API returns with response_model, and communicate outcomes with proper HTTP status codes and HTTPException.",
        "order":             5,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   2.0,
        "skill_tags":        ["fastapi", "python", "api", "pydantic", "http"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Response Models & Status Codes",
            "content": """You're doing well. Now let's learn what FastAPI should return and
what HTTP status codes mean.

## 1. What is a Response Model?

Previously we did:

```python
@app.get("/users")
def get_user():
    return {
        "name": "Mohammad",
        "age": 24
    }
```

FastAPI simply returns whatever dictionary we give it. But sometimes
we want to control the response structure — that's where
`response_model` comes in.

## 2. Create a Response Model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.get("/user", response_model=User)
def get_user():
    return {
        "name": "Mohammad",
        "age": 24
    }
```

The important part is `response_model=User`. It tells FastAPI: "the
response should follow the User model."

## 3. Why Is This Useful?

Imagine your internal data contains:

```json
{
  "name": "Mohammad",
  "age": 24,
  "password": "secret123"
}
```

But you don't want to send the password to the frontend. Create a
response model:

```python
class UserResponse(BaseModel):
    name: str
    age: int
```

```python
@app.get("/user", response_model=UserResponse)
def get_user():
    return {
        "name": "Mohammad",
        "age": 24,
        "password": "secret123"
    }
```

FastAPI returns only `name` and `age` — the password is stripped out:

```
Internal data
     ↓
FastAPI
     ↓
Response Model
     ↓
Safe response
```

## 4. Request Model vs Response Model

**Request model** — defines what the client sends:

```python
class UserCreate(BaseModel):
    name: str
    age: int
```

```python
@app.post("/users")
def create_user(user: UserCreate):
    ...
```

**Response model** — defines what the server returns:

```python
class UserResponse(BaseModel):
    id: int
    name: str
```

```python
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    ...
```

```
Frontend
   │
   │ Request
   ↓
UserCreate
   │
 FastAPI
   │
   │ Response
   ↓
UserResponse
   │
   ↓
Frontend
```

## 5. Status Codes

An API response usually includes a **status code** plus a **response
body**. For example, `200 OK` means "everything worked."

## 6. Common Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | Success, no response body |
| 400 | Bad request |
| 401 | Not authenticated |
| 403 | Forbidden |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

Don't try to memorize everything — for now remember:

```
200 → OK
201 → Created
404 → Not Found
422 → Validation Error
500 → Server Error
```

## 7. Returning 201 Created

When we create something, 201 is usually appropriate:

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message": "User created"
    }
```

Now a successful request returns `201 Created` instead of the default
200.

## 8. 404 Not Found

Suppose we search for a user that doesn't exist. We use
`HTTPException`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "id": 1,
        "name": "Mohammad"
    }
```

`/users/1` returns the user; `/users/99` returns
`{"detail": "User not found"}` with a `404 Not Found` status.

## 9. Why Raise HTTPException?

```python
raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

This tells FastAPI: "stop processing this request and return an error
response." You'll use this a lot in real APIs.

## 10. A Small Complete Example

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "age": user.age
    }

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "id": 1,
        "name": "Mohammad",
        "age": 24
    }
```

Notice the flow:

```
POST /users
     ↓
UserCreate
     ↓
FastAPI
     ↓
UserResponse
     ↓
201 Created
```

```
GET /users/99
     ↓
User doesn't exist
     ↓
HTTPException
     ↓
404 Not Found
```

## 🧠 The 3 Things to Remember

1. **response_model** — controls the response: `response_model=UserResponse`
2. **status_code** — controls the HTTP status: `status_code=201`
3. **HTTPException** — returns an error:

```python
raise HTTPException(
    status_code=404,
    detail="Not found"
)
```""",
            "order":                5,
            "estimated_minutes":    55,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Course Create & Lookup with Status Codes",
                "description":   (
                    "Using `CourseCreate` (`code: str`, `name: str`, "
                    "`credits: int`) and `CourseResponse` (`id: int, code: "
                    "str, name: str, credits: int`), build:\n\n"
                    "- `POST /courses` — accepts a `CourseCreate` body, "
                    "returns a `CourseResponse`, with status code 201\n"
                    "- `GET /courses/{course_id}` — returns the course if "
                    "`course_id == 1`, otherwise raises a 404 HTTPException"
                ),
                "difficulty":    DifficultyLevel.beginner,
                "starter_code": (
                    "from fastapi import FastAPI, HTTPException, status\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: CourseCreate model\n\n"
                    "# TODO: CourseResponse model\n\n"
                    "# TODO: POST /courses -> 201\n\n"
                    "# TODO: GET /courses/{course_id} -> 404 if not found\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI, HTTPException, status\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "class CourseCreate(BaseModel):\n"
                    "    code: str\n"
                    "    name: str\n"
                    "    credits: int\n\n"
                    "class CourseResponse(BaseModel):\n"
                    "    id: int\n"
                    "    code: str\n"
                    "    name: str\n"
                    "    credits: int\n\n"
                    "@app.post(\n"
                    "    \"/courses\",\n"
                    "    response_model=CourseResponse,\n"
                    "    status_code=status.HTTP_201_CREATED,\n"
                    ")\n"
                    "def create_course(course: CourseCreate):\n"
                    "    return {\n"
                    "        \"id\": 1,\n"
                    "        \"code\": course.code,\n"
                    "        \"name\": course.name,\n"
                    "        \"credits\": course.credits,\n"
                    "    }\n\n"
                    "@app.get(\"/courses/{course_id}\", response_model=CourseResponse)\n"
                    "def get_course(course_id: int):\n"
                    "    if course_id != 1:\n"
                    "        raise HTTPException(status_code=404, detail=\"Course not found\")\n"
                    "    return {\n"
                    "        \"id\": 1,\n"
                    "        \"code\": \"CSE251\",\n"
                    "        \"name\": \"Machine Learning\",\n"
                    "        \"credits\": 3,\n"
                    "    }\n"
                ),
                "skill_tested":  ["fastapi", "response-model", "status-codes", "httpexception"],
            },
        ],
        "quiz": {
            "title": "Response Models & Status Codes Quiz",
            "questions": [
                {
                    "question": "What does response_model=UserResponse do?",
                    "options": [
                        "Filters and shapes the returned data to match UserResponse's fields",
                        "Validates the incoming request body",
                        "Sets the HTTP status code to 200",
                        "Creates a new database table",
                    ],
                    "correct": 0,
                    "explanation": "response_model controls and filters what's sent back to the client, e.g. stripping out fields like passwords.",
                },
                {
                    "question": "Which status code typically indicates a resource was successfully created?",
                    "options": ["201", "200", "204", "404"],
                    "correct": 0,
                    "explanation": "201 Created is the conventional status code for successful POST requests that create a resource.",
                },
                {
                    "question": "What does raising HTTPException(status_code=404, detail=\"User not found\") do?",
                    "options": [
                        "Stops processing and returns a 404 response with that detail message",
                        "Logs an error but continues processing",
                        "Automatically retries the request",
                        "Creates a new user with id 404",
                    ],
                    "correct": 0,
                    "explanation": "HTTPException immediately halts the route function and sends the specified status code and detail as the response.",
                },
                {
                    "question": "What's the key difference between a request model and a response model?",
                    "options": [
                        "Request model defines what the client sends; response model defines what the server returns",
                        "They are always the exact same model",
                        "Request models are optional but response models are required",
                        "Response models validate JSON, request models don't",
                    ],
                    "correct": 0,
                    "explanation": "Request models (e.g. UserCreate) shape incoming data; response models (e.g. UserResponse) shape outgoing data.",
                },
                {
                    "question": "What status code generally means 'validation error'?",
                    "options": ["422", "400", "500", "200"],
                    "correct": 0,
                    "explanation": "422 Unprocessable Entity is FastAPI's default status code when request data fails Pydantic validation.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Course Catalog with Safe Responses",
            "description":      (
                "Extend the Course Catalog API with request/response models, "
                "correct status codes on creation, and a 404 HTTPException "
                "when a course isn't found."
            ),
            "difficulty":       DifficultyLevel.beginner,
            "tech_stack":       ["FastAPI", "Pydantic", "Python", "Uvicorn"],
            "objectives": [
                "Separate request and response Pydantic models",
                "Return 201 Created on successful POST",
                "Raise a 404 HTTPException for missing resources",
            ],
            "rubric": {
                "models_separated": "CourseCreate and CourseResponse are distinct models",
                "status_codes":     "POST returns 201, missing GET returns 404",
                "httpexception":    "HTTPException used correctly with status_code and detail",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "CRUD API",
        "slug":              "fastapi-crud-api",
        "description":       "Combine everything so far to build a full Create/Read/Update/Delete API for courses, backed by an in-memory list.",
        "order":             6,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.5,
        "skill_tags":        ["fastapi", "python", "api", "crud"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Build Your First CRUD API",
            "content": """Now we're going to put everything together and build a **Course
API**.

## CRUD

| Letter | Meaning | HTTP |
|---|---|---|
| C | Create | POST |
| R | Read | GET |
| U | Update | PUT |
| D | Delete | DELETE |

Our API will look like:

```
POST   /courses
GET    /courses
GET    /courses/{course_id}
PUT    /courses/{course_id}
DELETE /courses/{course_id}
```

## 1. The Idea

We'll temporarily store courses in a Python list:

```
courses
   │
   ├── Course 1
   ├── Course 2
   └── Course 3
```

Later we'll replace this list with a real database.

## 2. Complete Code

Create `main.py`:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class CourseCreate(BaseModel):
    code: str
    name: str
    credits: int

class CourseResponse(BaseModel):
    id: int
    code: str
    name: str
    credits: int

courses = []
next_id = 1

# -------------------------
# CREATE
# -------------------------

@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(course: CourseCreate):
    global next_id

    new_course = {
        "id": next_id,
        "code": course.code,
        "name": course.name,
        "credits": course.credits
    }
    courses.append(new_course)
    next_id += 1

    return new_course

# -------------------------
# READ (list)
# -------------------------

@app.get("/courses", response_model=list[CourseResponse])
def get_courses():
    return courses

# -------------------------
# READ (single)
# -------------------------

@app.get(
    "/courses/{course_id}",
    response_model=CourseResponse
)
def get_course(course_id: int):

    for course in courses:

        if course["id"] == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )

# -------------------------
# UPDATE
# -------------------------

@app.put(
    "/courses/{course_id}",
    response_model=CourseResponse
)
def update_course(
    course_id: int,
    updated_course: CourseCreate
):

    for course in courses:

        if course["id"] == course_id:

            course["code"] = updated_course.code
            course["name"] = updated_course.name
            course["credits"] = updated_course.credits

            return course

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )

# -------------------------
# DELETE
# -------------------------

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    for course in courses:

        if course["id"] == course_id:

            courses.remove(course)

            return {
                "message": "Course deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )
```

## 3. Run It

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` — you'll see all five endpoints.

## 4. CREATE — POST

Choose `POST /courses`, send:

```json
{
  "code": "CSE251",
  "name": "Machine Learning",
  "credits": 3
}
```

You'll get:

```json
{
  "id": 1,
  "code": "CSE251",
  "name": "Machine Learning",
  "credits": 3
}
```

Because we used `status_code=status.HTTP_201_CREATED`, the status is
`201 Created`.

## 5. Create Another Course

Send:

```json
{
  "code": "CSE252",
  "name": "Deep Learning",
  "credits": 3
}
```

Now our fake database looks like:

```python
courses = [
    {
        "id": 1,
        "code": "CSE251",
        "name": "Machine Learning",
        "credits": 3
    },
    {
        "id": 2,
        "code": "CSE252",
        "name": "Deep Learning",
        "credits": 3
    }
]
```

## 6. READ — GET

Call `GET /courses`:

```json
[
  {
    "id": 1,
    "code": "CSE251",
    "name": "Machine Learning",
    "credits": 3
  },
  {
    "id": 2,
    "code": "CSE252",
    "name": "Deep Learning",
    "credits": 3
  }
]
```

## 7. Get One Course

`GET /courses/1` returns the course. `GET /courses/999` returns:

```json
{
  "detail": "Course not found"
}
```

with `404 Not Found`.

## 8. UPDATE — PUT

Suppose we want to change Machine Learning. Call `PUT /courses/1`,
send:

```json
{
  "code": "CSE251",
  "name": "Advanced Machine Learning",
  "credits": 4
}
```

The course becomes:

```json
{
  "id": 1,
  "code": "CSE251",
  "name": "Advanced Machine Learning",
  "credits": 4
}
```

## 9. DELETE

Call `DELETE /courses/1`:

```json
{
  "message": "Course deleted"
}
```

Course 1 is removed.

## 🧠 Understand the Architecture

You don't need to memorize the entire code — understand this flow:

```
                 COURSE API

                    │
        ┌───────────┴───────────┐
        │                       │
      CREATE                   READ
       POST                   GET
        │                       │
        └───────────┬───────────┘
                    │
                  courses
                    │
        ┌───────────┴───────────┐
        │                       │
      UPDATE                  DELETE
       PUT                   DELETE
```

And each request goes through:

```
Request
   ↓
FastAPI
   ↓
Pydantic validation
   ↓
Python logic
   ↓
Response model
   ↓
JSON response
```

## ⭐ One Important Thing

Our database is currently `courses = []` — this is not a real
database. If you stop the server, everything disappears:

```
uvicorn
   ↓
STOP
   ↓
courses = []
```

That's why real applications use databases such as PostgreSQL, MySQL,
or SQLite. In the next lesson we'll learn how FastAPI connects to a
real database.""",
            "order":                6,
            "estimated_minutes":    75,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Students CRUD API",
                "description":   (
                    "Build the same CRUD pattern for students:\n\n"
                    "```\n"
                    "POST   /students\n"
                    "GET    /students\n"
                    "GET    /students/{student_id}\n"
                    "PUT    /students/{student_id}\n"
                    "DELETE /students/{student_id}\n"
                    "```\n\n"
                    "Use:\n\n"
                    "```python\n"
                    "class StudentCreate(BaseModel):\n"
                    "    name: str\n"
                    "    age: int\n"
                    "    department: str\n"
                    "```\n\n"
                    "Store students in an in-memory list, matching the "
                    "Course API pattern from the lesson."
                ),
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code": (
                    "from fastapi import FastAPI, HTTPException, status\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: StudentCreate, StudentResponse models\n\n"
                    "students = []\n"
                    "next_id = 1\n\n"
                    "# TODO: POST /students\n\n"
                    "# TODO: GET /students\n\n"
                    "# TODO: GET /students/{student_id}\n\n"
                    "# TODO: PUT /students/{student_id}\n\n"
                    "# TODO: DELETE /students/{student_id}\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI, HTTPException, status\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "class StudentCreate(BaseModel):\n"
                    "    name: str\n"
                    "    age: int\n"
                    "    department: str\n\n"
                    "class StudentResponse(BaseModel):\n"
                    "    id: int\n"
                    "    name: str\n"
                    "    age: int\n"
                    "    department: str\n\n"
                    "students = []\n"
                    "next_id = 1\n\n"
                    "@app.post(\"/students\", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)\n"
                    "def create_student(student: StudentCreate):\n"
                    "    global next_id\n"
                    "    new_student = {\"id\": next_id, **student.dict()}\n"
                    "    students.append(new_student)\n"
                    "    next_id += 1\n"
                    "    return new_student\n\n"
                    "@app.get(\"/students\", response_model=list[StudentResponse])\n"
                    "def get_students():\n"
                    "    return students\n\n"
                    "@app.get(\"/students/{student_id}\", response_model=StudentResponse)\n"
                    "def get_student(student_id: int):\n"
                    "    for student in students:\n"
                    "        if student[\"id\"] == student_id:\n"
                    "            return student\n"
                    "    raise HTTPException(status_code=404, detail=\"Student not found\")\n\n"
                    "@app.put(\"/students/{student_id}\", response_model=StudentResponse)\n"
                    "def update_student(student_id: int, updated: StudentCreate):\n"
                    "    for student in students:\n"
                    "        if student[\"id\"] == student_id:\n"
                    "            student[\"name\"] = updated.name\n"
                    "            student[\"age\"] = updated.age\n"
                    "            student[\"department\"] = updated.department\n"
                    "            return student\n"
                    "    raise HTTPException(status_code=404, detail=\"Student not found\")\n\n"
                    "@app.delete(\"/students/{student_id}\")\n"
                    "def delete_student(student_id: int):\n"
                    "    for student in students:\n"
                    "        if student[\"id\"] == student_id:\n"
                    "            students.remove(student)\n"
                    "            return {\"message\": \"Student deleted\"}\n"
                    "    raise HTTPException(status_code=404, detail=\"Student not found\")\n"
                ),
                "skill_tested":  ["fastapi", "crud", "pydantic", "httpexception"],
            },
        ],
        "quiz": {
            "title": "CRUD API Quiz",
            "questions": [
                {
                    "question": "What does the 'U' in CRUD stand for, and which HTTP method maps to it?",
                    "options": ["Update, PUT", "Upload, POST", "Undo, DELETE", "Upsert, GET"],
                    "correct": 0,
                    "explanation": "CRUD's 'U' is Update, conventionally mapped to the PUT HTTP method.",
                },
                {
                    "question": "In the lesson's Course API, why does GET /courses/999 return 404?",
                    "options": [
                        "No course in the in-memory list has id 999, so HTTPException is raised",
                        "999 is an invalid integer",
                        "FastAPI blocks IDs above 100 by default",
                        "The route only accepts POST requests",
                    ],
                    "correct": 0,
                    "explanation": "The loop searches for a matching id; if none is found, it falls through to raise a 404 HTTPException.",
                },
                {
                    "question": "Why does stopping the uvicorn server erase all created courses?",
                    "options": [
                        "The data lives in a Python list in memory, not a persistent database",
                        "FastAPI automatically clears data every hour",
                        "Pydantic models reset on shutdown",
                        "This only happens if you forget --reload",
                    ],
                    "correct": 0,
                    "explanation": "An in-memory Python list only exists while the process is running — there's no persistence layer yet.",
                },
                {
                    "question": "In the update_course endpoint, what are the two parameters and where does each come from?",
                    "options": [
                        "course_id from the URL path, updated_course from the JSON request body",
                        "Both come from query parameters",
                        "Both come from the request body",
                        "course_id from headers, updated_course from cookies",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI infers path parameters from the route pattern and request bodies from Pydantic model type hints.",
                },
                {
                    "question": "What response does DELETE /courses/1 return on success in this lesson's pattern?",
                    "options": [
                        "A JSON message confirming deletion, e.g. {\"message\": \"Course deleted\"}",
                        "The full list of remaining courses",
                        "204 No Content with an empty body only, nothing else",
                        "The deleted course's data unchanged",
                    ],
                    "correct": 0,
                    "explanation": "The lesson's delete_course function returns a simple confirmation message after removing the course from the list.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "In-Memory Book Library API",
            "description":      (
                "Build a full CRUD API for books (title, author, year) using "
                "an in-memory list, following the exact Course API pattern: "
                "POST, GET list, GET one, PUT, DELETE, with correct status "
                "codes and 404 handling."
            ),
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["FastAPI", "Pydantic", "Python", "Uvicorn"],
            "objectives": [
                "Implement all five CRUD routes for a new resource",
                "Reuse Create/Response Pydantic model separation",
                "Handle not-found cases with HTTPException",
                "Understand why in-memory storage doesn't persist",
            ],
            "rubric": {
                "all_routes_work": "POST/GET/GET-one/PUT/DELETE all function correctly",
                "models_correct":  "BookCreate and BookResponse are properly separated",
                "error_handling":  "404 raised correctly for missing books",
            },
            "starter_repo_url": None,
            "estimated_hours":  2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Dependency Injection",
        "slug":              "fastapi-dependency-injection",
        "description":       "Use Depends() to share reusable logic like authentication, pagination, and database connections across endpoints.",
        "order":             7,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["fastapi", "python", "api", "dependency-injection"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Dependency Injection with Depends()",
            "content": """This sounds complicated, but the idea is actually very simple.
We'll learn `Depends()` and why FastAPI uses it so much.

## 1. What is a Dependency?

Imagine several API endpoints need the same thing — for example, many
endpoints need to check "is the user logged in?"

Instead of writing the same code everywhere:

```python
@app.get("/courses")
def get_courses():
    # check login
    # ...
    return courses

@app.get("/students")
def get_students():
    # check login
    # ...
    return students
```

we create one function:

```python
def check_user():
    return "User is valid"
```

Then FastAPI can automatically call it for us. That's **Dependency
Injection**.

## 2. The Simplest Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_message():
    return "Hello from dependency"

@app.get("/")
def home(message=Depends(get_message)):
    return {
        "message": message
    }
```

When you call `GET /`, FastAPI does approximately this:

```
Request
   ↓
FastAPI
   ↓
get_message()
   ↓
"Hello from dependency"
   ↓
home(message)
   ↓
Response
```

You didn't manually call `get_message()` — FastAPI did it.

## 3. What Does Depends() Mean?

Look at `message=Depends(get_message)`. Read it as:

> "FastAPI, before running this endpoint, give me the result of
> get_message()."

That's basically it.

## 4. A More Realistic Example

```python
def get_current_user():
    return {
        "id": 1,
        "name": "Mohammad"
    }

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "user": user
    }
```

When `/profile` is requested:

```
/profile
   ↓
get_current_user()
   ↓
user
   ↓
profile(user)
```

Response:

```json
{
  "user": {
    "id": 1,
    "name": "Mohammad"
  }
}
```

## 5. Why Not Just Call the Function?

You could write:

```python
@app.get("/profile")
def profile():
    user = get_current_user()
    return {
        "user": user
    }
```

That works too. But `Depends()` becomes useful as your application
grows — when many endpoints share concerns like:

```
100 endpoints
     ↓
authentication
     ↓
database connection
     ↓
permissions
     ↓
configuration
```

Instead of repeating the same code everywhere, dependencies let you
reuse it.

## 6. Authentication Example

Imagine `GET /profile`, `GET /courses`, `POST /courses`, and
`DELETE /courses` all require authentication:

```python
def get_current_user():
    # later we'll check JWT
    return {
        "id": 1,
        "name": "Mohammad"
    }

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return user

@app.get("/courses")
def courses(user=Depends(get_current_user)):
    return {
        "courses": [],
        "user": user
    }
```

Both endpoints automatically use the dependency.

## 7. Dependency With Parameters

Dependencies can themselves receive things from FastAPI:

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_page(page: int = 1):
    return page

@app.get("/courses")
def get_courses(page=Depends(get_page)):
    return {
        "page": page
    }
```

Now `/courses?page=3` returns `{"page": 3}`. FastAPI sees
`page: int = 1` inside the dependency and pulls the value from the
query parameter.

## 8. Dependencies Are Great for Databases

Later, you'll see something like:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
@app.get("/courses")
def get_courses(db=Depends(get_db)):
    ...
```

The flow becomes:

```
Request
   ↓
get_db()
   ↓
Database connection
   ↓
get_courses(db)
   ↓
Query database
   ↓
Response
   ↓
Close database
```

This is one of the most common FastAPI patterns.

## 9. Dependencies Can Be Nested

This is where things become powerful:

```python
def get_db():
    ...

def get_current_user(db=Depends(get_db)):
    ...

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    ...
```

FastAPI handles the chain:

```
profile
  ↓
get_current_user
  ↓
get_db
```

You don't manually manage the entire chain.

## 🧠 The Simple Mental Model

Don't overthink "dependency injection." Think:

> A dependency is reusable code that FastAPI runs for your endpoint.

And `Depends(function)` means:

> "FastAPI, run this function and give me its result."

## ⭐ Why This Matters for Your AI Projects

You'll eventually have something like:

```
POST /ask
       ↓
Authentication dependency
       ↓
Database dependency
       ↓
RAG service
       ↓
Qdrant
       ↓
LLM
       ↓
Response
```

So `Depends()` is an important piece for building production FastAPI
AI applications.""",
            "order":                7,
            "estimated_minutes":    60,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Dashboard with a User Dependency",
                "description":   (
                    "Create a `get_user()` function returning "
                    "`{\"name\": \"Mohammad\", \"role\": \"admin\"}`. Then "
                    "build `GET /dashboard` using `Depends(get_user)` that "
                    "returns:\n\n"
                    "```json\n"
                    "{\n"
                    "  \"message\": \"Welcome\",\n"
                    "  \"user\": {\n"
                    "    \"name\": \"Mohammad\",\n"
                    "    \"role\": \"admin\"\n"
                    "  }\n"
                    "}\n"
                    "```"
                ),
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code": (
                    "from fastapi import FastAPI, Depends\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: get_user() dependency\n\n"
                    "# TODO: GET /dashboard using Depends(get_user)\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI, Depends\n\n"
                    "app = FastAPI()\n\n"
                    "def get_user():\n"
                    "    return {\"name\": \"Mohammad\", \"role\": \"admin\"}\n\n"
                    "@app.get(\"/dashboard\")\n"
                    "def dashboard(user=Depends(get_user)):\n"
                    "    return {\"message\": \"Welcome\", \"user\": user}\n"
                ),
                "skill_tested":  ["fastapi", "dependency-injection"],
            },
        ],
        "quiz": {
            "title": "Dependency Injection Quiz",
            "questions": [
                {
                    "question": "What does Depends(get_message) tell FastAPI?",
                    "options": [
                        "Run get_message() before the endpoint and pass its result in",
                        "Delete the get_message function after use",
                        "Only run get_message() if an error occurs",
                        "Cache get_message() forever across all requests",
                    ],
                    "correct": 0,
                    "explanation": "Depends() tells FastAPI to call the given function and inject its return value as the parameter's value.",
                },
                {
                    "question": "Why use Depends() instead of just calling a function directly inside the endpoint?",
                    "options": [
                        "It lets you reuse shared logic (auth, db, config) across many endpoints without repeating code",
                        "Depends() is required syntax and functions can never be called directly",
                        "It makes the endpoint run faster",
                        "It automatically writes tests for the endpoint",
                    ],
                    "correct": 0,
                    "explanation": "The main benefit of dependency injection is avoiding repeated logic across many endpoints as an app grows.",
                },
                {
                    "question": "In def get_page(page: int = 1): used as a dependency, where does 'page' come from when called?",
                    "options": [
                        "FastAPI resolves it as a query parameter, e.g. from ?page=3",
                        "It's always hardcoded to 1",
                        "It comes from the request body",
                        "It's read from an environment variable",
                    ],
                    "correct": 0,
                    "explanation": "Dependencies can declare their own parameters, which FastAPI resolves the same way as regular endpoint parameters.",
                },
                {
                    "question": "What is the purpose of yield in a dependency like get_db()?",
                    "options": [
                        "It provides the db session to the endpoint, then runs cleanup code (like closing it) afterward",
                        "It pauses the entire FastAPI server",
                        "It converts the function into an async function automatically",
                        "It has no special purpose and could be replaced with return",
                    ],
                    "correct": 0,
                    "explanation": "yield lets a dependency provide a resource, then execute cleanup code (e.g. db.close()) after the request finishes.",
                },
                {
                    "question": "In a nested dependency chain like profile → get_current_user → get_db, who manages calling get_db()?",
                    "options": [
                        "FastAPI resolves the entire dependency chain automatically",
                        "The developer must manually call get_db() inside get_current_user()",
                        "get_db() is called separately in a background thread",
                        "Nested dependencies are not supported in FastAPI",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI automatically resolves nested Depends() chains without the developer manually wiring each call.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Shared Auth & Pagination Dependencies",
            "description":      (
                "Refactor the Course CRUD API to use two dependencies: a "
                "get_current_user() dependency applied to all routes, and a "
                "get_pagination(page: int = 1, limit: int = 10) dependency "
                "applied to the list endpoint."
            ),
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["FastAPI", "Python", "Uvicorn"],
            "objectives": [
                "Create a reusable get_current_user dependency",
                "Create a pagination dependency with default values",
                "Apply dependencies via Depends() across multiple routes",
                "Verify a nested dependency chain resolves correctly",
            ],
            "rubric": {
                "auth_dependency_used": "get_current_user is injected into at least two routes",
                "pagination_works":     "GET /courses respects ?page= and ?limit= via a dependency",
                "no_duplicated_logic":  "Shared logic is not copy-pasted across route functions",
            },
            "starter_repo_url": None,
            "estimated_hours":  1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Database with FastAPI",
        "slug":              "fastapi-database-sqlalchemy",
        "description":       "Replace the in-memory list with a persistent SQLite database using SQLAlchemy models, sessions, and a get_db() dependency.",
        "order":             8,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   3.0,
        "skill_tags":        ["fastapi", "python", "api", "sqlalchemy", "sqlite"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Database + SQLAlchemy",
            "content": """Now we're going to make our FastAPI application remember data
permanently.

Until now we used `courses = []`. The problem is: stop the server and
the data disappears ❌. A database solves this:

```
FastAPI
   ↓
SQLAlchemy
   ↓
Database
   ↓
Data stays saved ✅
```

We'll use SQLite because it's the easiest database to learn with.

## 1. What is SQLAlchemy?

SQLAlchemy is a Python library that lets Python communicate with
databases. Instead of writing lots of SQL manually, you work with
Python objects:

```
Python
  ↓
SQLAlchemy
  ↓
SQLite
```

Later, the same concepts apply to PostgreSQL.

## 2. Install the Packages

```bash
pip install sqlalchemy
```

You already have FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

## 3. Create the Database

Create `database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./courses.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

Don't worry about memorizing this yet. The important part is
`DATABASE_URL = "sqlite:///./courses.db"` — this means "use a SQLite
database called courses.db."

## 4. Create the Database Model

Create `models.py`:

```python
from sqlalchemy import Column, Integer, String
from database import Base

class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    credits = Column(Integer)
```

This Python class represents a database table:

```
Course class
     ↓
courses table

id
code
name
credits
```

## 5. Create the Table

In `main.py`:

```python
from fastapi import FastAPI
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
```

Now when you run `uvicorn main:app --reload`, SQLAlchemy creates
`courses.db` and, inside it, the `courses` table.

## 6. Create a Database Dependency

Remember `Depends()` from Lesson 7? Now we'll use it for database
sessions. In `database.py`, add:

```python
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

The idea:

```
Request
   ↓
Open database
   ↓
Use database
   ↓
Finish request
   ↓
Close database
```

## 7. Pydantic Model

In `schemas.py`:

```python
from pydantic import BaseModel

class CourseCreate(BaseModel):

    code: str
    name: str
    credits: int

class CourseResponse(BaseModel):

    id: int
    code: str
    name: str
    credits: int

    class Config:
        from_attributes = True
```

The difference is important:

```
SQLAlchemy Model
       ↓
Database

Pydantic Model
       ↓
API input/output
```

## 8. Create a Course

`main.py`:

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Course
from schemas import CourseCreate, CourseResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/courses", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    new_course = Course(
        code=course.code,
        name=course.name,
        credits=course.credits
    )

    db.add(new_course)

    db.commit()

    db.refresh(new_course)

    return new_course
```

This looks like a lot — let's break it down.

## 9. The Important Part

The frontend sends:

```json
{
  "code": "CSE251",
  "name": "Machine Learning",
  "credits": 3
}
```

Pydantic receives it as `course: CourseCreate`. Then we create a
database object:

```python
new_course = Course(
    code=course.code,
    name=course.name,
    credits=course.credits
)
```

- `db.add(new_course)` — prepare this object to be inserted.
- `db.commit()` — save it permanently.
- `db.refresh(new_course)` — get the generated database values, such
  as the `id`.

## 10. Read Courses

```python
@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):

    courses = db.query(Course).all()

    return courses
```

Now `GET /courses` retrieves the courses from SQLite.

## 11. Read One Course

```python
from fastapi import HTTPException
```

```python
@app.get(
    "/courses/{course_id}",
    response_model=CourseResponse
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course
```

Now `GET /courses/1` looks for `Course.id == 1`.

## 12. The Architecture

At this point your project looks like:

```
project/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
│
└── courses.db
```

And the request flow is:

```
                Frontend
                   │
                   ↓
                FastAPI
                   │
                   ↓
              Pydantic
                   │
                   ↓
             Depends(get_db)
                   │
                   ↓
              SQLAlchemy
                   │
                   ↓
                SQLite
```

This architecture is very important.

## 🧠 SQLAlchemy vs Pydantic

This is one of the things beginners often confuse.

**Pydantic** — used for API data:

```python
class CourseCreate(BaseModel):
    code: str
    name: str
    credits: int
```

Think: *what data can the API receive?*

**SQLAlchemy** — used for database data:

```python
class Course(Base):
    id = Column(Integer)
    code = Column(String)
    name = Column(String)
```

Think: *how is the data stored?*

```
Pydantic
   ↓
API

SQLAlchemy
   ↓
Database
```""",
            "order":                8,
            "estimated_minutes":    80,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Persist Courses with SQLite",
                "description":   (
                    "Take the CRUD API from Lesson 6 and replace `courses = "
                    "[]` with SQLite + SQLAlchemy. At minimum, implement:\n\n"
                    "```\n"
                    "POST   /courses\n"
                    "GET    /courses\n"
                    "GET    /courses/{course_id}\n"
                    "```\n\n"
                    "using `database.py`, `models.py`, and `schemas.py` as "
                    "shown in the lesson. Restart the server and confirm "
                    "your courses are still there."
                ),
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code": (
                    "# database.py\n"
                    "from sqlalchemy import create_engine\n"
                    "from sqlalchemy.orm import sessionmaker, declarative_base\n\n"
                    "DATABASE_URL = \"sqlite:///./courses.db\"\n\n"
                    "# TODO: engine, SessionLocal, Base, get_db()\n"
                ),
                "solution_code": (
                    "# database.py\n"
                    "from sqlalchemy import create_engine\n"
                    "from sqlalchemy.orm import sessionmaker, declarative_base\n\n"
                    "DATABASE_URL = \"sqlite:///./courses.db\"\n\n"
                    "engine = create_engine(DATABASE_URL, connect_args={\"check_same_thread\": False})\n"
                    "SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\n"
                    "Base = declarative_base()\n\n"
                    "def get_db():\n"
                    "    db = SessionLocal()\n"
                    "    try:\n"
                    "        yield db\n"
                    "    finally:\n"
                    "        db.close()\n\n"
                    "# models.py\n"
                    "from sqlalchemy import Column, Integer, String\n"
                    "from database import Base\n\n"
                    "class Course(Base):\n"
                    "    __tablename__ = \"courses\"\n"
                    "    id = Column(Integer, primary_key=True, index=True)\n"
                    "    code = Column(String)\n"
                    "    name = Column(String)\n"
                    "    credits = Column(Integer)\n\n"
                    "# schemas.py\n"
                    "from pydantic import BaseModel\n\n"
                    "class CourseCreate(BaseModel):\n"
                    "    code: str\n"
                    "    name: str\n"
                    "    credits: int\n\n"
                    "class CourseResponse(BaseModel):\n"
                    "    id: int\n"
                    "    code: str\n"
                    "    name: str\n"
                    "    credits: int\n\n"
                    "    class Config:\n"
                    "        from_attributes = True\n\n"
                    "# main.py\n"
                    "from fastapi import FastAPI, Depends, HTTPException\n"
                    "from sqlalchemy.orm import Session\n"
                    "from database import Base, engine, get_db\n"
                    "from models import Course\n"
                    "from schemas import CourseCreate, CourseResponse\n\n"
                    "Base.metadata.create_all(bind=engine)\n"
                    "app = FastAPI()\n\n"
                    "@app.post(\"/courses\", response_model=CourseResponse)\n"
                    "def create_course(course: CourseCreate, db: Session = Depends(get_db)):\n"
                    "    new_course = Course(code=course.code, name=course.name, credits=course.credits)\n"
                    "    db.add(new_course)\n"
                    "    db.commit()\n"
                    "    db.refresh(new_course)\n"
                    "    return new_course\n\n"
                    "@app.get(\"/courses\", response_model=list[CourseResponse])\n"
                    "def get_courses(db: Session = Depends(get_db)):\n"
                    "    return db.query(Course).all()\n\n"
                    "@app.get(\"/courses/{course_id}\", response_model=CourseResponse)\n"
                    "def get_course(course_id: int, db: Session = Depends(get_db)):\n"
                    "    course = db.query(Course).filter(Course.id == course_id).first()\n"
                    "    if course is None:\n"
                    "        raise HTTPException(status_code=404, detail=\"Course not found\")\n"
                    "    return course\n"
                ),
                "skill_tested":  ["fastapi", "sqlalchemy", "sqlite", "dependency-injection"],
            },
        ],
        "quiz": {
            "title": "Database + SQLAlchemy Quiz",
            "questions": [
                {
                    "question": "What problem does a database solve compared to a Python list like courses = []?",
                    "options": [
                        "Data persists even after the server stops, instead of disappearing",
                        "Lists are slower than databases for all operations",
                        "Databases are required for FastAPI to start at all",
                        "Lists can't hold dictionaries",
                    ],
                    "correct": 0,
                    "explanation": "In-memory lists lose all data when the process stops; a database persists data to disk.",
                },
                {
                    "question": "What does DATABASE_URL = \"sqlite:///./courses.db\" specify?",
                    "options": [
                        "To use a local SQLite database file named courses.db",
                        "A PostgreSQL connection string",
                        "A remote API endpoint",
                        "An environment variable name only",
                    ],
                    "correct": 0,
                    "explanation": "This connection string tells SQLAlchemy to use a SQLite database stored in the local file courses.db.",
                },
                {
                    "question": "What is the key difference between a SQLAlchemy model and a Pydantic model in this architecture?",
                    "options": [
                        "SQLAlchemy models define database storage; Pydantic models define API input/output",
                        "They are identical and interchangeable",
                        "Pydantic models talk to the database directly",
                        "SQLAlchemy models are used only for testing",
                    ],
                    "correct": 0,
                    "explanation": "SQLAlchemy models (Base subclasses) map to database tables; Pydantic models (BaseModel subclasses) shape API requests/responses.",
                },
                {
                    "question": "In get_db(), why is yield used instead of return?",
                    "options": [
                        "It lets the dependency provide the session, then run cleanup (db.close()) after the request finishes",
                        "yield makes the function run faster",
                        "return isn't valid inside any FastAPI dependency",
                        "It has no functional difference from return here",
                    ],
                    "correct": 0,
                    "explanation": "yield pauses the function to hand off the db session, then resumes after the request to close it in the finally block.",
                },
                {
                    "question": "What does db.refresh(new_course) do after db.commit()?",
                    "options": [
                        "Reloads the object with database-generated values, like the auto-assigned id",
                        "Deletes the object from the database",
                        "Reverts the commit",
                        "Sends the object back to the frontend directly",
                    ],
                    "correct": 0,
                    "explanation": "refresh() re-fetches the object's state from the database, picking up values like the auto-generated primary key.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Persistent Book Library API",
            "description":      (
                "Convert the in-memory Book Library API from Lesson 6's "
                "project into a SQLite-backed API using SQLAlchemy models, "
                "a get_db() dependency, and separate Pydantic schemas."
            ),
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["FastAPI", "SQLAlchemy", "SQLite", "Pydantic", "Python"],
            "objectives": [
                "Define a SQLAlchemy Book model and create the table on startup",
                "Implement a get_db() dependency for session management",
                "Rewrite POST/GET/GET-one routes to use the database",
                "Confirm data survives a server restart",
            ],
            "rubric": {
                "model_defined":   "Book SQLAlchemy model matches schema fields",
                "db_persists":     "Data survives a restart of the uvicorn server",
                "schemas_correct": "BookCreate/BookResponse Pydantic models used correctly with from_attributes",
            },
            "starter_repo_url": None,
            "estimated_hours":  2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Authentication",
        "slug":              "fastapi-authentication-jwt",
        "description":       "Secure your API with password hashing, JWT tokens, a login endpoint, and a get_current_user() dependency to protect routes.",
        "order":             9,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   3.0,
        "skill_tags":        ["fastapi", "python", "api", "jwt", "authentication", "security"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Authentication + JWT",
            "content": """Now we're going to learn how to make your API secure.

Imagine your API has `GET /courses`, `POST /courses`, and
`DELETE /courses`. You don't want everyone to be able to use them.

```
User
 ↓
Login
 ↓
JWT Token
 ↓
Send token with requests
 ↓
FastAPI checks token
 ↓
Allow / Reject
```

## 1. What is Authentication?

Authentication answers: **"Who are you?"**

```
Username: Mohammad
Password: ********
```

If they're correct: ✅ Logged in.

**Authorization** is different — it answers **"What are you allowed to
do?"**:

```
Mohammad → Admin   → Can delete courses
Ahmed    → Student → Can only read courses
```

For now, we'll focus on authentication.

## 2. What is JWT?

JWT = JSON Web Token. After successful login, the server gives the
user a token, e.g. `eyJhbGciOiJIUzI1NiIs...`. The client stores it and
sends it with future requests.

```
LOGIN
  ↓
Username + Password
  ↓
FastAPI
  ↓
JWT Token
  ↓
Client
```

Then:

```
GET /courses
Authorization: Bearer <token>
```

FastAPI checks the token.

## 3. Install the Libraries

```bash
pip install python-jose passlib[bcrypt]
```

We'll use `python-jose` to create/verify JWTs and `passlib` to hash
passwords.

## 4. Never Store Plain Passwords

❌ Don't do this:

```python
users = {
    "mohammad": "123456"
}
```

If your database leaks, the password is exposed. Instead:

```
Password
   ↓
Hash
   ↓
Database
```

For example, `123456` becomes `$2b$12$....` — the database stores the
hash, not the original password.

## 5. Password Hashing

Create `security.py`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

`hash_password("123456")` produces a password hash. `verify_password("123456", hashed_password)` returns `True` if the password is correct.

## 6. Create a JWT

```python
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
```

`create_access_token({"sub": "mohammad"})` returns a JWT.

## 7. Why sub?

You'll often see `{"sub": "mohammad"}`. `sub` means *subject* — it's
commonly used to identify the user, e.g. a user ID or username.

## 8. Create Login

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str
```

```python
@app.post("/login")
def login(data: LoginRequest):

    if data.username != "mohammad":
        return {
            "error": "Invalid username"
        }

    if data.password != "123456":
        return {
            "error": "Invalid password"
        }

    token = create_access_token({
        "sub": data.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

⚠️ This is only for learning. A real application should verify a
hashed password from a database.

## 9. Login Flow

The user sends `{"username": "mohammad", "password": "123456"}` to
`POST /login`. FastAPI verifies the credentials, then returns:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## 10. How Does the Client Use the Token?

For future requests, the client sends:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

```
Authorization
     ↓
Bearer
     ↓
JWT Token
```

## 11. Protect an Endpoint

FastAPI provides:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

```python
from fastapi import Depends

@app.get("/profile")
def profile(
    token: str = Depends(oauth2_scheme)
):
    return {
        "token": token
    }
```

Now FastAPI expects an authorization token.

## 12. Verify the JWT

Receiving the token isn't enough — we need to verify it:

```python
from jose import JWTError, jwt
from fastapi import HTTPException

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
```

Now protect an endpoint:

```python
@app.get("/profile")
def profile(
    username: str = Depends(get_current_user)
):

    return {
        "username": username
    }
```

## 13. What's Happening?

When someone requests `GET /profile`, FastAPI does:

```
Request
   ↓
Authorization Header
   ↓
JWT Token
   ↓
get_current_user()
   ↓
Decode JWT
   ↓
Check signature
   ↓
Get username
   ↓
profile()
   ↓
Response
```

If the token is invalid: ❌ 401 Unauthorized.

## 🧠 The Most Important Concept

```
                 REGISTER
                    ↓
             Store password hash
                    ↓
                  LOGIN
                    ↓
          Check username/password
                    ↓
                Create JWT
                    ↓
              Client gets token
                    ↓
         ┌──────────┴──────────┐
         ↓                     ↓
     API Request            API Request
         ↓                     ↓
      JWT Token             JWT Token
         ↓                     ↓
       Verify                Verify
         ↓                     ↓
       Allow                Reject
```

## 14. Where Depends() Fits

Remember Lesson 7? We created:

```python
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    ...
```

Then:

```python
@app.get("/courses")
def courses(
    user=Depends(get_current_user)
):
    ...
```

```
GET /courses
      ↓
get_current_user()
      ↓
JWT verification
      ↓
Valid?
  ↙       ↘
YES       NO
 ↓         ↓
Courses   401
```

This is a very common FastAPI architecture.""",
            "order":                9,
            "estimated_minutes":    85,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Login + Protected Profile",
                "description":   (
                    "Create `POST /login` and `GET /profile`.\n\n"
                    "`/login` should return a JWT for a hardcoded username/"
                    "password check. `/profile` should require that JWT via "
                    "`Depends(get_current_user)` and return the username.\n\n"
                    "The flow: `/login` → JWT → send as `Authorization: "
                    "Bearer <token>` → `/profile` → user info. Test it "
                    "through `/docs`."
                ),
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code": (
                    "from fastapi import FastAPI, Depends, HTTPException\n"
                    "from fastapi.security import OAuth2PasswordBearer\n"
                    "from pydantic import BaseModel\n"
                    "from jose import jwt, JWTError\n\n"
                    "SECRET_KEY = \"your-secret-key\"\n"
                    "ALGORITHM = \"HS256\"\n\n"
                    "app = FastAPI()\n"
                    "oauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"login\")\n\n"
                    "class LoginRequest(BaseModel):\n"
                    "    username: str\n"
                    "    password: str\n\n"
                    "# TODO: create_access_token()\n\n"
                    "# TODO: POST /login\n\n"
                    "# TODO: get_current_user() dependency\n\n"
                    "# TODO: GET /profile\n"
                ),
                "solution_code": (
                    "from fastapi import FastAPI, Depends, HTTPException\n"
                    "from fastapi.security import OAuth2PasswordBearer\n"
                    "from pydantic import BaseModel\n"
                    "from jose import jwt, JWTError\n\n"
                    "SECRET_KEY = \"your-secret-key\"\n"
                    "ALGORITHM = \"HS256\"\n\n"
                    "app = FastAPI()\n"
                    "oauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"login\")\n\n"
                    "class LoginRequest(BaseModel):\n"
                    "    username: str\n"
                    "    password: str\n\n"
                    "def create_access_token(data: dict):\n"
                    "    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)\n\n"
                    "@app.post(\"/login\")\n"
                    "def login(data: LoginRequest):\n"
                    "    if data.username != \"mohammad\" or data.password != \"123456\":\n"
                    "        raise HTTPException(status_code=401, detail=\"Invalid credentials\")\n"
                    "    token = create_access_token({\"sub\": data.username})\n"
                    "    return {\"access_token\": token, \"token_type\": \"bearer\"}\n\n"
                    "def get_current_user(token: str = Depends(oauth2_scheme)):\n"
                    "    try:\n"
                    "        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])\n"
                    "        username = payload.get(\"sub\")\n"
                    "        if username is None:\n"
                    "            raise HTTPException(status_code=401, detail=\"Invalid token\")\n"
                    "        return username\n"
                    "    except JWTError:\n"
                    "        raise HTTPException(status_code=401, detail=\"Invalid token\")\n\n"
                    "@app.get(\"/profile\")\n"
                    "def profile(username: str = Depends(get_current_user)):\n"
                    "    return {\"username\": username}\n"
                ),
                "skill_tested":  ["fastapi", "jwt", "authentication", "dependency-injection"],
            },
        ],
        "quiz": {
            "title": "Authentication + JWT Quiz",
            "questions": [
                {
                    "question": "What question does authentication answer, as distinct from authorization?",
                    "options": [
                        "'Who are you?' — authorization answers 'what are you allowed to do?'",
                        "'What are you allowed to do?' — the same as authorization",
                        "'How fast is the request?'",
                        "'Which database table is being used?'",
                    ],
                    "correct": 0,
                    "explanation": "Authentication verifies identity; authorization determines permissions for an already-identified user.",
                },
                {
                    "question": "Why should passwords be hashed instead of stored as plain text?",
                    "options": [
                        "So a database leak doesn't expose the original passwords",
                        "Hashing makes login faster",
                        "FastAPI requires all strings to be hashed",
                        "Hashing is only needed for JWT tokens, not passwords",
                    ],
                    "correct": 0,
                    "explanation": "If a database is compromised, hashed passwords can't be trivially reversed to reveal the originals.",
                },
                {
                    "question": "What does the 'sub' field typically represent inside a JWT payload?",
                    "options": [
                        "The subject — usually a user ID or username identifying who the token belongs to",
                        "The subscription plan of the user",
                        "A subroutine name in the backend code",
                        "The HTTP method used to request the token",
                    ],
                    "correct": 0,
                    "explanation": "'sub' stands for subject, conventionally used to identify the token's owner.",
                },
                {
                    "question": "How does a client send its JWT on subsequent authenticated requests?",
                    "options": [
                        "In an Authorization: Bearer <token> header",
                        "As a query parameter named jwt",
                        "In the request body only",
                        "JWTs are automatically remembered by the browser with no header needed",
                    ],
                    "correct": 0,
                    "explanation": "The standard convention is sending the token in the Authorization header prefixed with 'Bearer'.",
                },
                {
                    "question": "What status code does get_current_user() raise when the JWT is invalid or missing the username claim?",
                    "options": ["401 Unauthorized", "404 Not Found", "403 Forbidden", "500 Server Error"],
                    "correct": 0,
                    "explanation": "Invalid or malformed tokens are rejected with a 401 Unauthorized HTTPException in this lesson's pattern.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "Secured Book Library API",
            "description":      (
                "Add authentication to the persistent Book Library API: a "
                "/login endpoint issuing JWTs, and protect POST/PUT/DELETE "
                "book routes with a get_current_user() dependency while "
                "keeping GET routes public."
            ),
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["FastAPI", "python-jose", "passlib", "SQLAlchemy", "Python"],
            "objectives": [
                "Hash and verify passwords with passlib",
                "Issue JWTs on successful login",
                "Protect write routes with Depends(get_current_user)",
                "Leave read routes public and confirm the split works",
            ],
            "rubric": {
                "login_works":       "POST /login returns a valid JWT for correct credentials",
                "protected_routes":  "POST/PUT/DELETE reject requests without a valid token (401)",
                "public_routes":     "GET routes remain accessible without a token",
            },
            "starter_repo_url": None,
            "estimated_hours":  2.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "AI/RAG API Project",
        "slug":              "fastapi-ai-rag-api-project",
        "description":       "Turn a RAG system into a FastAPI backend — request/response models, a pipeline function, auth protection, and the shape of a production AI backend.",
        "order":             10,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   3.0,
        "skill_tags":        ["fastapi", "python", "api", "rag", "llm", "architecture"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "Build an AI/RAG API",
            "content": """This is the lesson where everything comes together. You already
learned FastAPI, Pydantic, CRUD, Dependencies, Database, and JWT. Now
we'll use FastAPI to expose an AI/RAG system through an API.

## 1. What Are We Building?

Imagine you have a RAG system that can answer questions about
university regulations. The frontend sends:

```json
{
  "question": "What are the graduation requirements?"
}
```

to `POST /ask`. FastAPI receives it and sends it to your RAG pipeline.
The final response:

```json
{
  "question": "What are the graduation requirements?",
  "answer": "..."
}
```

## 2. The Architecture

```
                    Frontend
                       │
                       │ POST /ask
                       ↓
                 ┌───────────┐
                 │  FastAPI  │
                 └─────┬─────┘
                       │
                       ↓
                 Pydantic Model
                       │
                       ↓
                  RAG Pipeline
                       │
                ┌──────┴──────┐
                ↓             ↓
             Qdrant          LLM
                │             │
                └──────┬──────┘
                       ↓
                     Answer
                       │
                       ↓
                    FastAPI
                       │
                       ↓
                    Frontend
```

This is the basic architecture behind many AI applications.

## 3. Create the Project

```
ai_api/
│
├── main.py
├── schemas.py
├── rag.py
└── requirements.txt
```

Later, when the project becomes larger, we'll split it into more
folders.

## 4. Create the Request Model

`schemas.py`:

```python
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
```

Now FastAPI knows exactly what the client must send.

## 5. Create a Fake RAG Pipeline

`rag.py` — for now, don't connect Qdrant or an LLM. We'll simulate the
RAG system:

```python
def answer_question(question: str):

    return f"AI answer for: {question}"
```

That's enough for now. Later we'll replace this function with your
actual RAG pipeline.

## 6. Create the FastAPI Endpoint

`main.py`:

```python
from fastapi import FastAPI
from schemas import QuestionRequest, AnswerResponse
from rag import answer_question

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "AI API is running"
    }

@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask_question(request: QuestionRequest):

    answer = answer_question(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }
```

That's your first AI API.

## 7. Run It

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`, find `POST /ask`, click **Try it
out**, and send:

```json
{
  "question": "What are the graduation requirements?"
}
```

You should get:

```json
{
  "question": "What are the graduation requirements?",
  "answer": "AI answer for: What are the graduation requirements?"
}
```

🎉 You just exposed an AI-style system through FastAPI.

## 8. Now Replace the Fake RAG

Currently:

```python
def answer_question(question: str):

    return f"AI answer for: {question}"
```

In a real application, it could become:

```python
def answer_question(question: str):

    documents = retrieve_documents(question)

    answer = generate_answer(
        question,
        documents
    )

    return answer
```

```
Question
   ↓
Embedding
   ↓
Qdrant
   ↓
Relevant documents
   ↓
LLM
   ↓
Answer
```

This is where your previous Qdrant/RAG knowledge becomes useful.

## 9. Connect Qdrant Conceptually

Your real pipeline might look like:

```python
def answer_question(question: str):

    documents = qdrant_search(question)

    answer = llm_generate(
        question,
        documents
    )

    return answer
```

FastAPI doesn't really care what's happening inside — that's an
important concept. FastAPI's job is primarily:

```
Receive request
      ↓
Validate request
      ↓
Call your Python function
      ↓
Return response
```

Your RAG code handles retrieval + generation.

## 10. Add Authentication

Remember the JWT lesson? We can protect `/ask`:

```python
@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    user=Depends(get_current_user)
):
    ...
```

```
Frontend
   ↓
JWT
   ↓
POST /ask
   ↓
Authentication
   ↓
RAG
   ↓
Answer
```

Only authenticated users can use your AI assistant.

## 11. Add Conversation History

Eventually you may want:

```json
{
  "question": "What is CSE251?",
  "conversation_id": 123
}
```

Your model could become:

```python
class QuestionRequest(BaseModel):
    question: str
    conversation_id: int | None = None
```

Then your API can support conversations — question 1, question 2,
question 3 — which is useful for an AI chatbot.

## 12. Streaming AI Responses

A normal API makes the user wait for the complete answer. But AI
applications often want to stream partial text as it's generated:
`"Machine..."` → `"Machine learning..."` → `"Machine learning is..."`
→ complete.

FastAPI can stream responses, which is useful for LLM applications.
You'll encounter this when building ChatGPT-style interfaces.

## 13. A Better Project Structure

When your project gets bigger, don't put everything in `main.py`. A
real AI backend could look like:

```
ai_api/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── courses.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── course.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── rag.py
│   │   ├── llm.py
│   │   └── retrieval.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   └── core/
│       ├── security.py
│       └── config.py
│
└── requirements.txt
```

Don't try to memorize this — it's just showing how a large project can
be organized.

## 🧠 The Most Important Idea

FastAPI is not the RAG system. **FastAPI is the doorway into your RAG
system.**

```
                   FastAPI
                      │
             ┌────────┴────────┐
             ↓                 ↓
          /login             /ask
                                │
                                ↓
                              RAG
                                │
                         ┌──────┴──────┐
                         ↓             ↓
                       Qdrant         LLM
```

FastAPI handles the web/API layer. Your AI code handles the
intelligence.

## What You Can Now Understand

A production AI backend might look like:

```
                    React / Frontend
                           │
                           ↓
                    ┌────────────┐
                    │  FastAPI   │
                    └──────┬─────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Auth         Request       Database
           JWT          Pydantic      PostgreSQL
              │            │
              └──────┬─────┘
                     ↓
                 AI Service
                     │
             ┌───────┴────────┐
             ↓                ↓
           Qdrant             LLM
             │                │
             └───────┬────────┘
                     ↓
                   Answer
                     ↓
                  Frontend
```

And that is a very useful architecture for an AI Engineer.""",
            "order":                10,
            "estimated_minutes":    90,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "Wire Up a Minimal RAG API",
                "description":   (
                    "Build the `ai_api/` project from the lesson: "
                    "`schemas.py` with `QuestionRequest`/`AnswerResponse`, "
                    "`rag.py` with a fake `answer_question()`, and `main.py` "
                    "exposing `GET /` and `POST /ask`.\n\n"
                    "Then protect `/ask` with `Depends(get_current_user)` "
                    "from Lesson 9's JWT pattern, so only a logged-in user "
                    "can ask questions. Test the full flow: login → copy "
                    "token → call /ask with the Authorization header."
                ),
                "difficulty":    DifficultyLevel.intermediate,
                "starter_code": (
                    "# schemas.py\n"
                    "from pydantic import BaseModel\n\n"
                    "# TODO: QuestionRequest, AnswerResponse\n\n"
                    "# rag.py\n"
                    "# TODO: fake answer_question(question: str)\n\n"
                    "# main.py\n"
                    "from fastapi import FastAPI, Depends\n\n"
                    "app = FastAPI()\n\n"
                    "# TODO: GET /\n\n"
                    "# TODO: POST /ask protected with Depends(get_current_user)\n"
                ),
                "solution_code": (
                    "# schemas.py\n"
                    "from pydantic import BaseModel\n\n"
                    "class QuestionRequest(BaseModel):\n"
                    "    question: str\n\n"
                    "class AnswerResponse(BaseModel):\n"
                    "    question: str\n"
                    "    answer: str\n\n"
                    "# rag.py\n"
                    "def answer_question(question: str):\n"
                    "    return f\"AI answer for: {question}\"\n\n"
                    "# main.py\n"
                    "from fastapi import FastAPI, Depends\n"
                    "from schemas import QuestionRequest, AnswerResponse\n"
                    "from rag import answer_question\n"
                    "# assume get_current_user is imported from the auth lesson's module\n\n"
                    "app = FastAPI()\n\n"
                    "@app.get(\"/\")\n"
                    "def home():\n"
                    "    return {\"message\": \"AI API is running\"}\n\n"
                    "@app.post(\"/ask\", response_model=AnswerResponse)\n"
                    "def ask_question(request: QuestionRequest, user=Depends(get_current_user)):\n"
                    "    answer = answer_question(request.question)\n"
                    "    return {\"question\": request.question, \"answer\": answer}\n"
                ),
                "skill_tested":  ["fastapi", "rag", "pydantic", "authentication"],
            },
        ],
        "quiz": {
            "title": "AI/RAG API Quiz",
            "questions": [
                {
                    "question": "In the lesson's architecture, what is FastAPI's primary role relative to the RAG system?",
                    "options": [
                        "It's the doorway/web layer that receives, validates, and routes requests — not the intelligence itself",
                        "FastAPI performs the embedding and retrieval directly",
                        "FastAPI replaces the need for an LLM",
                        "FastAPI stores the vector embeddings internally",
                    ],
                    "correct": 0,
                    "explanation": "FastAPI handles receiving, validating, and responding to requests; the actual retrieval and generation logic lives in your RAG code.",
                },
                {
                    "question": "What does the fake answer_question(question: str) function let you do before connecting a real RAG pipeline?",
                    "options": [
                        "Test and build the full API flow (request → response) without needing Qdrant or an LLM yet",
                        "Permanently replace the need for a real LLM",
                        "Automatically train a new model",
                        "Store questions in a database",
                    ],
                    "correct": 0,
                    "explanation": "Stubbing the RAG function lets you validate the API contract and flow before wiring in real retrieval and generation.",
                },
                {
                    "question": "How would you protect POST /ask so only authenticated users can use it?",
                    "options": [
                        "Add user=Depends(get_current_user) as a parameter",
                        "Rename the route to /ask-secure",
                        "Move the route into schemas.py",
                        "FastAPI protects all POST routes automatically",
                    ],
                    "correct": 0,
                    "explanation": "Adding the get_current_user dependency reuses the JWT verification pattern from Lesson 9 to require a valid token.",
                },
                {
                    "question": "What does adding conversation_id: int | None = None to QuestionRequest enable?",
                    "options": [
                        "Supporting multi-turn conversations by linking questions to a specific chat thread",
                        "Automatically deleting old questions",
                        "Making the question field optional instead",
                        "Switching the response to streaming mode",
                    ],
                    "correct": 0,
                    "explanation": "An optional conversation_id lets the API associate a sequence of questions with the same ongoing conversation.",
                },
                {
                    "question": "Why might a production AI backend split code into api/, models/, schemas/, services/, and core/ folders instead of one main.py?",
                    "options": [
                        "It keeps concerns separated and organized as the project grows in size and complexity",
                        "FastAPI requires this exact folder structure to run",
                        "It makes the app run faster at request time",
                        "Splitting files disables authentication by default",
                    ],
                    "correct": 0,
                    "explanation": "The folder structure is a scalability and maintainability convention, not a technical FastAPI requirement.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title":            "RAG API Capstone",
            "description":      (
                "Combine everything from the roadmap into one capstone: a "
                "JWT-protected FastAPI backend exposing POST /ask, backed by "
                "a swappable RAG pipeline function, with conversation_id "
                "support and a SQLite-persisted conversation log."
            ),
            "difficulty":       DifficultyLevel.advanced,
            "tech_stack":       ["FastAPI", "Pydantic", "SQLAlchemy", "python-jose", "Python"],
            "objectives": [
                "Expose POST /ask with a QuestionRequest/AnswerResponse contract",
                "Protect /ask with the JWT get_current_user dependency",
                "Persist each question/answer pair to SQLite, linked by conversation_id",
                "Keep the RAG logic isolated in its own function/module so it's swappable later",
            ],
            "rubric": {
                "auth_enforced":       "Unauthenticated requests to /ask are rejected with 401",
                "conversation_support":"conversation_id correctly groups related questions",
                "persistence":          "Q&A history survives a server restart via SQLite",
                "clean_separation":     "RAG logic is isolated from routing/auth/database code",
            },
            "starter_repo_url": None,
            "estimated_hours":  4.0,
        },
    },
]

# ---------------------------------------------------------------------------
# Seed logic — do not modify below this line
# ---------------------------------------------------------------------------
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty",
                 "estimated_hours", "skill_tags", "prerequisite_ids")


def seed(db):
    course = db.query(ToolCourse).filter(ToolCourse.slug == TOOL_SLUG).first()
    if not course:
        print(f"✗ ToolCourse '{TOOL_SLUG}' not found — run seed_tool_courses.py first")
        return

    for t in TOPICS:
        topic = db.query(ToolTopic).filter(
            ToolTopic.tool_course_id == course.id,
            ToolTopic.order == t["order"],
        ).first()
        if not topic:
            topic = ToolTopic(tool_course_id=course.id, **{k: t[k] for k in TOPIC_FIELDS})
            db.add(topic)
            db.flush()
            print(f"  + ToolTopic: {topic.title}")
        else:
            print(f"  - ToolTopic exists: {topic.title}, skipping")

        if not db.query(Lesson).filter(Lesson.tool_topic_id == topic.id).first():
            db.add(Lesson(tool_topic_id=topic.id, **t["lesson"]))
            print("    + Lesson added")
        else:
            print("    - Lesson exists, skipping")

        if db.query(Exercise).filter(Exercise.tool_topic_id == topic.id).count() == 0:
            for ex in t["exercises"]:
                db.add(Exercise(tool_topic_id=topic.id, **ex))
            print(f"    + {len(t['exercises'])} exercise(s) added")
        else:
            print("    - Exercises exist, skipping")

        if not db.query(Quiz).filter(Quiz.tool_topic_id == topic.id).first():
            db.add(Quiz(tool_topic_id=topic.id, **t["quiz"]))
            print("    + Quiz added")
        else:
            print("    - Quiz exists, skipping")

        if not db.query(Project).filter(Project.tool_topic_id == topic.id).first():
            db.add(Project(tool_topic_id=topic.id, **t["project"]))
            print("    + Project added")
        else:
            print("    - Project exists, skipping")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
