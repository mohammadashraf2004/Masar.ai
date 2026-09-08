"""
backend/seeds/seed_tool_langgraph.py

Adds topic content (lessons/exercises/quiz/project) to the LangGraph
tool course, which already exists as a shell (seeded by
seeds/seed_tool_courses.py). Idempotent — safe to re-run.

Run from backend/:
    docker compose exec api python seeds/seed_tool_langgraph.py
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

TOOL_SLUG = "langgraph"  # must already exist — created by seed_tool_courses.py

# ---------------------------------------------------------------------------
# Topics (flat — no levels). Add one dict per topic, in the order they
# should appear. Course outline (20 lessons total):
#   1  What is LangGraph?
#   2  Graphs, Nodes, and Edges
#   3  State — the most important concept
#   4  Your first LangGraph
#   5  Conditional Edges
#   6  Loops
#   7  Using an LLM
#   8  Messages
#   9  Building a Chatbot
#   10 Tools
#   11 Tool Calling
#   12 Agents
#   13 Memory
#   14 Checkpoints
#   15 Human-in-the-Loop
#   16 RAG with LangGraph
#   17 LangGraph + LangChain
#   18 Building a real AI Agent
#   19 Debugging & common errors
#   20 Final Project
# ---------------------------------------------------------------------------
TOPICS = [
    {
        # ToolTopic fields
        "title":            "What is LangGraph?",
        "slug":              "what-is-langgraph",
        "description":       "The core mental model behind LangGraph: State, Nodes, Edges, and Graphs — and how LangGraph relates to LangChain.",
        "order":             1,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["langgraph", "langchain", "python", "graphs"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "What is LangGraph?",
            "content": """# 🧠 LangGraph — Lesson 1: What is LangGraph?

## LangChain vs LangGraph

Think of it like this:

- **LangChain** → helps you build AI applications using components (LLMs, prompts, tools, retrievers).
- **LangGraph** → helps you control the **flow** of those AI applications.

For example, imagine an AI system:

```
User Question
      ↓
   Analyze
      ↓
Is it a math question?
   ↙       ↘
 YES       NO
 ↓          ↓
Calculator  Search
   ↘       ↙
      ↓
   Generate Answer
      ↓
     END
```

LangGraph lets us build this kind of decision-making workflow.

## The Basic Mental Model

A graph consists mainly of three pieces:

### 1. State
Information that your application currently knows.

```python
state = {
    "question": "What is Python?",
    "answer": ""
}
```

### 2. Node
A node is a function that does something.

```python
def answer_question(state):
    state["answer"] = "Python is a programming language."
    return state
```

This function is a node.

### 3. Edge
An edge tells LangGraph: *"After this node, go to that node."*

```
START
  ↓
answer_question
  ↓
 END
```

Putting it together:

```
        STATE
          ↓
       ┌──────┐
       │ NODE │
       └──────┘
          ↓
        EDGE
          ↓
       ┌──────┐
       │ NODE │
       └──────┘
          ↓
         END
```

So:
- **State** = information
- **Node** = action
- **Edge** = direction
- **Graph** = complete workflow

That's the core idea of LangGraph.

## Tiny Example

Suppose we want an AI workflow:

```
START
  ↓
Say Hello
  ↓
Say Goodbye
  ↓
END
```

We could have two nodes:

```python
def hello(state):
    print("Hello!")
    return state

def goodbye(state):
    print("Goodbye!")
    return state
```

Then connect them:

```
START → hello → goodbye → END
```

That's a LangGraph.

## The Most Important Thing

Don't think of LangGraph as something completely different from LangChain. Think:

```
LangChain
   ↓
LLMs + Prompts + Tools + Retrievers
   +
LangGraph
   ↓
Control the workflow
```

For example, a future RAG system could become:

```
User Question
      ↓
Understand Question
      ↓
Retrieve Documents
      ↓
Check Results
   ↙       ↘
Good       Bad
 ↓          ↓
Answer    Search Again
 ↓          ↓
END      Retrieve
```

This is where LangGraph becomes extremely useful — you'll build workflows just like this later in the course.
""",
            "order": 1,
            "estimated_minutes": 25,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Define your first two nodes",
                "description": (
                    "Write two Python functions, `hello` and `goodbye`, that each take a `state` "
                    "dict, print a greeting/farewell, and return the state unchanged. Then, in a "
                    "comment, describe the order they would run in if connected as "
                    "`START → hello → goodbye → END`."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "def hello(state):\n"
                    "    # TODO: print \"Hello!\" and return state\n"
                    "    pass\n\n"
                    "def goodbye(state):\n"
                    "    # TODO: print \"Goodbye!\" and return state\n"
                    "    pass\n\n"
                    "# TODO: in a comment, describe the run order for\n"
                    "# START -> hello -> goodbye -> END\n"
                ),
                "solution_code": (
                    "def hello(state):\n"
                    "    print(\"Hello!\")\n"
                    "    return state\n\n"
                    "def goodbye(state):\n"
                    "    print(\"Goodbye!\")\n"
                    "    return state\n\n"
                    "# Run order: START triggers hello() first, which prints \"Hello!\"\n"
                    "# and returns the (unchanged) state. That state is then passed to\n"
                    "# goodbye(), which prints \"Goodbye!\" and returns the state again.\n"
                    "# Finally the graph reaches END.\n\n"
                    "state = {}\n"
                    "state = hello(state)\n"
                    "state = goodbye(state)\n"
                ),
                "skill_tested": ["langgraph", "nodes", "state"],
            },
            {
                "title": "Model a state dict",
                "description": (
                    "Given the workflow `User Question → Analyze → Generate Answer → END`, write "
                    "a Python dict representing the initial `state` before any node runs, and a "
                    "second dict representing the state after `Generate Answer` has run. Assume "
                    "the question is \"What is a graph?\" and the generated answer is "
                    "\"A graph is a structure of nodes connected by edges.\""
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "initial_state = {\n"
                    "    # TODO\n"
                    "}\n\n"
                    "final_state = {\n"
                    "    # TODO\n"
                    "}\n"
                ),
                "solution_code": (
                    "initial_state = {\n"
                    "    \"question\": \"What is a graph?\",\n"
                    "    \"answer\": \"\"\n"
                    "}\n\n"
                    "final_state = {\n"
                    "    \"question\": \"What is a graph?\",\n"
                    "    \"answer\": \"A graph is a structure of nodes connected by edges.\"\n"
                    "}\n"
                ),
                "skill_tested": ["langgraph", "state"],
            },
        ],
        "quiz": {
            "title": "What is LangGraph? — Quiz",
            "questions": [
                {
                    "question": "In LangGraph, what does 'State' represent?",
                    "options": [
                        "The information your application currently knows",
                        "A function that performs an action",
                        "A connection telling the graph what to run next",
                        "The final output of the entire graph",
                    ],
                    "correct": 0,
                    "explanation": "State is the data your application is carrying around, e.g. a dict like {\"question\": ..., \"answer\": ...}.",
                },
                {
                    "question": "What is a 'Node' in LangGraph?",
                    "options": [
                        "A piece of data",
                        "A function that does something",
                        "A direction between two steps",
                        "The entry point of the graph",
                    ],
                    "correct": 1,
                    "explanation": "A node is a function — like answer_question(state) — that takes the state, does work, and returns it.",
                },
                {
                    "question": "What is an 'Edge' in LangGraph?",
                    "options": [
                        "A function that transforms state",
                        "The data stored between steps",
                        "Something that tells LangGraph which node to go to next",
                        "The end of the program",
                    ],
                    "correct": 2,
                    "explanation": "An edge defines the direction of flow: 'after this node, go to that node.'",
                },
                {
                    "question": "How does LangGraph relate to LangChain?",
                    "options": [
                        "LangGraph replaces LangChain entirely",
                        "LangGraph controls the workflow/flow of LangChain components like LLMs, prompts, and tools",
                        "They are unrelated projects",
                        "LangChain is used only for graphs, and LangGraph only for prompts",
                    ],
                    "correct": 1,
                    "explanation": "LangChain provides the building blocks (LLMs, prompts, tools, retrievers); LangGraph controls how those blocks are wired together into a workflow.",
                },
                {
                    "question": "For the workflow START → hello → goodbye → END, which best describes a 'Graph'?",
                    "options": [
                        "Just the hello function by itself",
                        "Just the state dict",
                        "The complete workflow made up of state, nodes, and edges",
                        "Only the END marker",
                    ],
                    "correct": 2,
                    "explanation": "A graph is the full workflow: the state flowing through nodes, connected by edges, from START to END.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Trace-Through: Design a 3-Node Graph on Paper",
            "description": (
                "Without writing any LangGraph-specific code yet, design a simple 3-node workflow "
                "for a 'greeting bot': START → greet_user → ask_name → farewell → END. For each "
                "node, write the Python function signature and what it does to the state. Then "
                "write out, step by step, what the state dict looks like after each node runs, "
                "starting from an empty state."
            ),
            "difficulty": DifficultyLevel.beginner,
            "tech_stack": ["Python"],
            "objectives": [
                "Identify what belongs in State vs what belongs in a Node",
                "Write plain Python functions that represent nodes",
                "Trace how state changes step-by-step through a graph",
                "Describe the edges connecting each node in order",
            ],
            "rubric": {
                "state_design": "State dict is defined clearly and includes all needed fields (25%)",
                "node_functions": "Each node is a valid function that reads/updates state and returns it (35%)",
                "trace": "Step-by-step state trace after each node is correct (30%)",
                "clarity": "Explanation of edges/order is clear (10%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Your First LangGraph",
        "slug":              "your-first-langgraph",
        "description":       "Install LangGraph and build a real, runnable graph: StateGraph, nodes, edges, compile, and invoke.",
        "order":             2,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["langgraph", "python", "stategraph"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Your First LangGraph",
            "content": """# 🚀 Lesson 2 — Your First LangGraph

Today we're going to build a real LangGraph. Don't worry about LLMs or agents yet — first we
need to understand the basic structure.

## 1. Install LangGraph

In your virtual environment:

```bash
pip install -U langgraph
```

If you're using a Jupyter/Colab notebook:

```bash
!pip install -U langgraph
```

## 2. Our First Graph

We'll build this:

```
START
  ↓
greet
  ↓
END
```

The `greet` node will simply say `Hello Mohammad!`.

## 3. Import LangGraph

```python
from langgraph.graph import StateGraph, START, END
```

The important pieces are:

- `StateGraph` → creates our graph
- `START` → where the graph begins
- `END` → where the graph finishes

## 4. Create the State

We'll use a simple `TypedDict` as our state.

```python
from typing import TypedDict

class State(TypedDict):
    message: str
```

Our state has one field: `message`. For example:

```python
{
    "message": "Hello"
}
```

## 5. Create a Node

A node is just a Python function.

```python
def greet(state: State):
    print("Hello!")
    return state
```

Notice: `state` is given to the function, and `return state` returns the updated state.

## 6. Create the Graph

```python
graph = StateGraph(State)
```

We're telling LangGraph: "Create a graph that uses my `State`."

## 7. Add Our Node

```python
graph.add_node("greet", greet)
```

Think of this as mapping a **name** to a **function**:

```
Name        Function
 ↓             ↓
greet   →   greet()
```

## 8. Connect START to Our Node

```python
graph.add_edge(START, "greet")
```

Now: `START → greet`.

## 9. Connect Our Node to END

```python
graph.add_edge("greet", END)
```

Now we have: `START → greet → END`.

## 10. Compile the Graph

Before running it:

```python
app = graph.compile()
```

Think of `compile()` as: "Prepare this graph so I can execute it."

## 11. Run It

```python
result = app.invoke({
    "message": "Hello LangGraph"
})
```

You should see `Hello!` printed, and `result` will contain the state:

```python
{
    "message": "Hello LangGraph"
}
```

## 🧩 Complete Code

Put everything together:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State
class State(TypedDict):
    message: str

# 2. Node
def greet(state: State):
    print("Hello!")
    return state

# 3. Create graph
graph = StateGraph(State)

# 4. Add node
graph.add_node("greet", greet)

# 5. Add edges
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

# 6. Compile
app = graph.compile()

# 7. Run
result = app.invoke({"message": "Hello LangGraph"})
print(result)
```

## 🧠 Understand the Code

The general LangGraph pattern is always the same:

```
Define State
     ↓
Create Graph
     ↓
Add Nodes
     ↓
Connect Nodes
     ↓
Compile
     ↓
Invoke
```

Concretely:

```
graph = StateGraph(State)
        ↓
graph.add_node("greet", greet)
        ↓
graph.add_edge(START, "greet")
        ↓
graph.add_edge("greet", END)
        ↓
app = graph.compile()
        ↓
app.invoke(...)
```

## ⭐ One Important Concept

You might wonder: why do we need a `State`? Because later our AI system will need to carry
information between nodes. For example:

```
State
├── question
├── documents
├── answer
└── user_name
```

Then:

```
Question Node
      ↓
Retriever Node
      ↓
Validation Node
      ↓
Answer Node
```

All these nodes can read and update the same state. That's one of the most important ideas
in LangGraph.

## 🧪 Small Exercise

Change the `greet` function so that it modifies the state. Instead of just printing "Hello!",
make it produce `"Hello, Mohammad!"` by changing `state["message"]`.

Input:

```python
{"message": "Mohammad"}
```

Final state should become:

```python
{"message": "Hello, Mohammad!"}
```

Don't worry if this feels slightly confusing — the next lesson focuses entirely on State, and
once State clicks, LangGraph becomes much easier.
""",
            "order": 2,
            "estimated_minutes": 35,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Make greet() modify the state",
                "description": (
                    "Rewrite the `greet` node so that instead of just printing \"Hello!\", it "
                    "reads `state['message']` (a name, e.g. \"Mohammad\") and updates "
                    "`state['message']` to `\"Hello, <name>!\"`. Given the input "
                    "`{\"message\": \"Mohammad\"}`, running the compiled graph should produce the "
                    "final state `{\"message\": \"Hello, Mohammad!\"}`."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    message: str\n\n\n"
                    "def greet(state: State):\n"
                    "    # TODO: turn state['message'] (a name) into \"Hello, <name>!\"\n"
                    "    # and return the updated field\n"
                    "    pass\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"greet\", greet)\n"
                    "graph.add_edge(START, \"greet\")\n"
                    "graph.add_edge(\"greet\", END)\n"
                    "app = graph.compile()\n\n"
                    "result = app.invoke({\"message\": \"Mohammad\"})\n"
                    "print(result)  # expect: {'message': 'Hello, Mohammad!'}\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    message: str\n\n\n"
                    "def greet(state: State):\n"
                    "    return {\"message\": f\"Hello, {state['message']}!\"}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"greet\", greet)\n"
                    "graph.add_edge(START, \"greet\")\n"
                    "graph.add_edge(\"greet\", END)\n"
                    "app = graph.compile()\n\n"
                    "result = app.invoke({\"message\": \"Mohammad\"})\n"
                    "print(result)  # {'message': 'Hello, Mohammad!'}\n"
                ),
                "skill_tested": ["langgraph", "stategraph", "nodes"],
            },
            {
                "title": "Build the graph from scratch",
                "description": (
                    "Without looking at the lesson, write the full six-step pattern from memory: "
                    "define a `State` TypedDict with a single `message` field, define a `greet` "
                    "node that prints \"Hello!\" and returns the state unchanged, create a "
                    "`StateGraph`, add the node, wire `START -> greet -> END`, compile, and "
                    "invoke with `{\"message\": \"Hello LangGraph\"}`."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# TODO: 1. imports\n"
                    "# TODO: 2. State TypedDict\n"
                    "# TODO: 3. greet node\n"
                    "# TODO: 4. graph = StateGraph(State)\n"
                    "# TODO: 5. add_node + add_edge x2\n"
                    "# TODO: 6. compile + invoke\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    message: str\n\n\n"
                    "def greet(state: State):\n"
                    "    print(\"Hello!\")\n"
                    "    return state\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"greet\", greet)\n"
                    "graph.add_edge(START, \"greet\")\n"
                    "graph.add_edge(\"greet\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"message\": \"Hello LangGraph\"})\n"
                    "print(result)\n"
                ),
                "skill_tested": ["langgraph", "stategraph", "compile", "invoke"],
            },
        ],
        "quiz": {
            "title": "Your First LangGraph — Quiz",
            "questions": [
                {
                    "question": "Which import gives you the core building blocks to create a graph?",
                    "options": [
                        "from langgraph.graph import StateGraph, START, END",
                        "from langchain import Graph",
                        "import langgraph.core as lg",
                        "from langgraph import Node, Edge",
                    ],
                    "correct": 0,
                    "explanation": "StateGraph builds the graph, while START and END mark the entry and exit points.",
                },
                {
                    "question": "What does graph.compile() do?",
                    "options": [
                        "Deletes the graph",
                        "Prepares the graph so it can be executed with .invoke()",
                        "Adds a new node",
                        "Connects START to END automatically",
                    ],
                    "correct": 1,
                    "explanation": "compile() finalizes the graph definition into a runnable app.",
                },
                {
                    "question": "What is the correct order of steps to build and run a LangGraph?",
                    "options": [
                        "Invoke → Compile → Add Nodes → Define State",
                        "Define State → Create Graph → Add Nodes → Connect Nodes → Compile → Invoke",
                        "Create Graph → Invoke → Define State → Compile",
                        "Add Nodes → Define State → Invoke → Compile",
                    ],
                    "correct": 1,
                    "explanation": "The standard LangGraph pattern always flows: State -> Graph -> Nodes -> Edges -> Compile -> Invoke.",
                },
                {
                    "question": "In graph.add_node(\"greet\", greet), what does the string \"greet\" represent?",
                    "options": [
                        "The value returned by the node",
                        "A name/identifier used to reference this node when adding edges",
                        "The state field the node updates",
                        "A required docstring",
                    ],
                    "correct": 1,
                    "explanation": "The string is the node's name, used later in add_edge() calls like add_edge(START, \"greet\").",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Three-Node Greeting Pipeline",
            "description": (
                "Extend the lesson's graph into a 3-node pipeline: START → build_greeting → "
                "shout → END. `build_greeting` sets `message` to \"Hello, <name>!\" using a `name` "
                "field on the state. `shout` uppercases `message`. Compile and invoke the graph "
                "with `{\"name\": \"Mohammad\", \"message\": \"\"}` and confirm the final state's "
                "`message` is `\"HELLO, MOHAMMAD!\"`."
            ),
            "difficulty": DifficultyLevel.beginner,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Define a State with more than one field",
                "Chain three nodes together with add_edge",
                "Have one node build on another node's output",
                "Compile and invoke the graph, verifying the final state",
            ],
            "rubric": {
                "state_design": "State TypedDict includes both name and message (20%)",
                "nodes": "Both nodes correctly read/update state and return partial updates (40%)",
                "wiring": "START/END and edges are wired in the correct order (20%)",
                "output": "Final invoked result matches the expected uppercase greeting (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "State — The Most Important Concept",
        "slug":              "state-the-most-important-concept",
        "description":       "A deep dive into State: TypedDict, reading vs modifying state, partial updates, and why state is the backbone of LangGraph agents.",
        "order":             3,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "python", "state", "typeddict"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "State — The Most Important Concept",
            "content": """# 🧠 Lesson 3 — State: The Most Important Concept

This is one of the most important lessons in LangGraph. If you understand State, you'll
understand most of LangGraph.

## 1. What is State?

Simply: **State is the information that moves through your graph.**

Imagine your LangGraph is a pipeline:

```
START
  ↓
Node 1
  ↓
Node 2
  ↓
Node 3
  ↓
END
```

The State travels through all of these nodes:

```
        STATE
          ↓
      ┌───────┐
      │ Node1 │
      └───────┘
          ↓
        STATE
          ↓
      ┌───────┐
      │ Node2 │
      └───────┘
          ↓
        STATE
```

## 2. Creating a State

We normally define the state using `TypedDict`.

```python
from typing import TypedDict

class State(TypedDict):
    name: str
    age: int
```

Our state can now contain:

```python
{
    "name": "Mohammad",
    "age": 25
}
```

## 3. Nodes Can Read the State

```python
def greet(state: State):
    print(f"Hello {state['name']}")
    return state
```

If the state is `{"name": "Mohammad", "age": 25}`, the node can access `state["name"]` and
`state["age"]`. So the output is `Hello Mohammad`.

## 4. Nodes Can Modify the State

This is where things become interesting. Suppose we have:

```python
class State(TypedDict):
    name: str
    message: str
```

Our node:

```python
def greet(state: State):
    return {
        "message": f"Hello {state['name']}!"
    }
```

Input: `{"name": "Mohammad", "message": ""}`

The node updates `message`, so the state becomes:

```python
{
    "name": "Mohammad",
    "message": "Hello Mohammad!"
}
```

## ⭐ Important LangGraph Rule

A node usually returns only the **changes** it wants to make to the state.

```
Input State
     ↓
   Node
     ↓
State Update
```

For example:

```python
def greet(state):
    return {"message": "Hello!"}
```

It is saying: "Update `message` to `\"Hello!\"`."

## 5. Multiple Nodes Sharing State

This is where LangGraph becomes powerful. Let's create:

```
START
  ↓
greet
  ↓
introduce
  ↓
END
```

State:

```python
class State(TypedDict):
    name: str
    message: str
```

First node:

```python
def greet(state: State):
    return {
        "message": f"Hello {state['name']}!"
    }
```

Second node:

```python
def introduce(state: State):
    print(state["message"])
    return state
```

The second node receives the state produced by the first node:

```
              STATE
                ↓
             greet
                ↓
message = "Hello Mohammad!"
                ↓
          introduce
                ↓
             print
```

## 6. Complete Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    message: str


def greet(state: State):
    return {
        "message": f"Hello {state['name']}!"
    }


def introduce(state: State):
    print(state["message"])
    return state


graph = StateGraph(State)

graph.add_node("greet", greet)
graph.add_node("introduce", introduce)

graph.add_edge(START, "greet")
graph.add_edge("greet", "introduce")
graph.add_edge("introduce", END)

app = graph.compile()

result = app.invoke({
    "name": "Mohammad",
    "message": ""
})

print(result)
```

Output:

```
Hello Mohammad!

{'name': 'Mohammad', 'message': 'Hello Mohammad!'}
```

### Visualize What Happened

Initially: `{"name": "Mohammad", "message": ""}`

**Node 1: greet** — changes `{"message": "Hello Mohammad!"}`, so state becomes
`{"name": "Mohammad", "message": "Hello Mohammad!"}`.

**Node 2: introduce** — reads `state["message"]` and prints `Hello Mohammad!`.

## 🔥 Why State Is So Important for AI Agents

Later, we'll have much more information in the state, for example:

```python
class State(TypedDict):
    question: str
    documents: list
    answer: str
    tool_result: str
```

Then our agent could work like this:

```
                 STATE
                   ↓
             ┌──────────┐
             │ Question │
             └────┬─────┘
                  ↓
             ┌──────────┐
             │ Retrieve │
             └────┬─────┘
                  ↓
          documents updated
                  ↓
             ┌──────────┐
             │   LLM    │
             └────┬─────┘
                  ↓
            answer updated
                  ↓
                 END
```

The state carries everything between the nodes.

## 🎯 Remember These 3 Things

1. **State = shared information** — `class State(TypedDict): question: str; answer: str`
2. **Node = function that reads/updates State** — `def my_node(state): return {"answer": "..."}`
3. **State moves through the graph** — State → Node → Updated State → Node → Updated State

## 🧪 Mini Exercise

Create this workflow:

```
START
  ↓
add_name
  ↓
add_age
  ↓
END
```

State:

```python
class State(TypedDict):
    name: str
    age: int
```

`add_name` should set `name = "Mohammad"`. `add_age` should set `age = 25`. The final result
should look like `{"name": "Mohammad", "age": 25}`. Try it yourself first.
""",
            "order": 3,
            "estimated_minutes": 45,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "add_name → add_age pipeline",
                "description": (
                    "Build the workflow START → add_name → add_age → END using the State "
                    "`{name: str, age: int}`. `add_name` should update `name` to \"Mohammad\", "
                    "and `add_age` should update `age` to 25. Invoke the compiled graph with an "
                    "empty-ish starting state and confirm the final result is "
                    "`{\"name\": \"Mohammad\", \"age\": 25}`."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    name: str\n"
                    "    age: int\n\n\n"
                    "def add_name(state: State):\n"
                    "    # TODO: return an update setting name to \"Mohammad\"\n"
                    "    pass\n\n\n"
                    "def add_age(state: State):\n"
                    "    # TODO: return an update setting age to 25\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add nodes, add edges, compile, invoke\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    name: str\n"
                    "    age: int\n\n\n"
                    "def add_name(state: State):\n"
                    "    return {\"name\": \"Mohammad\"}\n\n\n"
                    "def add_age(state: State):\n"
                    "    return {\"age\": 25}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"add_name\", add_name)\n"
                    "graph.add_node(\"add_age\", add_age)\n\n"
                    "graph.add_edge(START, \"add_name\")\n"
                    "graph.add_edge(\"add_name\", \"add_age\")\n"
                    "graph.add_edge(\"add_age\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"name\": \"\", \"age\": 0})\n"
                    "print(result)  # {'name': 'Mohammad', 'age': 25}\n"
                ),
                "skill_tested": ["langgraph", "state", "typeddict"],
            },
            {
                "title": "Add a third node that reads everything",
                "description": (
                    "Extend the greet → introduce example with a third node, `summary`, placed "
                    "after `introduce`. It should read both `state['name']` and "
                    "`state['message']` and return an update setting a new field `summary` to "
                    "`\"<name> said: <message>\"`. Add `summary: str` to the State definition and "
                    "wire `introduce -> summary -> END`."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "class State(TypedDict):\n"
                    "    name: str\n"
                    "    message: str\n"
                    "    summary: str\n\n\n"
                    "def summary(state: State):\n"
                    "    # TODO: build \"<name> said: <message>\" and return as summary update\n"
                    "    pass\n\n"
                    "# TODO: add_node(\"summary\", summary) and rewire introduce -> summary -> END\n"
                ),
                "solution_code": (
                    "class State(TypedDict):\n"
                    "    name: str\n"
                    "    message: str\n"
                    "    summary: str\n\n\n"
                    "def summary(state: State):\n"
                    "    return {\"summary\": f\"{state['name']} said: {state['message']}\"}\n\n\n"
                    "graph.add_node(\"summary\", summary)\n"
                    "graph.add_edge(\"introduce\", \"summary\")\n"
                    "graph.add_edge(\"summary\", END)\n"
                    "# (remove/replace the old introduce -> END edge)\n"
                ),
                "skill_tested": ["langgraph", "state", "nodes"],
            },
        ],
        "quiz": {
            "title": "State — The Most Important Concept — Quiz",
            "questions": [
                {
                    "question": "What does State represent in LangGraph?",
                    "options": [
                        "A single node's private variables",
                        "The information that moves through the whole graph",
                        "A compiled version of the graph",
                        "The name of the START node",
                    ],
                    "correct": 1,
                    "explanation": "State is shared information that travels from node to node as the graph runs.",
                },
                {
                    "question": "Which is the typical way to define a State's shape in LangGraph?",
                    "options": [
                        "Using a plain Python list",
                        "Using a TypedDict",
                        "Using a global variable",
                        "It cannot be typed",
                    ],
                    "correct": 1,
                    "explanation": "TypedDict lets you declare the expected keys and types of the state dict, e.g. class State(TypedDict): name: str.",
                },
                {
                    "question": "When a node returns { \"message\": \"Hello!\" }, what does that mean?",
                    "options": [
                        "It replaces the entire state with just {\"message\": \"Hello!\"}",
                        "It's an error — nodes must return the full state",
                        "It's an update: the message field changes, and other fields are merged in by LangGraph",
                        "It deletes the message field",
                    ],
                    "correct": 2,
                    "explanation": "A node usually returns only the changes it wants to make; LangGraph merges that update into the existing state.",
                },
                {
                    "question": "In the greet -> introduce example, how does introduce know the greeting message?",
                    "options": [
                        "It re-computes the message itself",
                        "It reads state['message'], which was set by the greet node before it",
                        "It receives it as a function argument, not through state",
                        "It doesn't have access to it",
                    ],
                    "correct": 1,
                    "explanation": "Because greet updated the shared state, introduce (which runs after it) can read state['message'] directly.",
                },
                {
                    "question": "Why does State become especially important for AI agents (e.g. with question, documents, answer fields)?",
                    "options": [
                        "It lets each node work in isolation with no shared data",
                        "It lets multiple stages (retrieve, LLM, validate, etc.) share and build on the same information as the workflow progresses",
                        "It's only used for debugging, not for real logic",
                        "It replaces the need for nodes entirely",
                    ],
                    "correct": 1,
                    "explanation": "As workflows grow (retrieval, LLM calls, tool results), state is what carries all of that information between steps.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Mini Profile Builder Graph",
            "description": (
                "Build a 4-node graph: START → add_name → add_age → add_bio → END, using a State "
                "with fields name, age, and bio. add_name sets name to a value passed in the "
                "initial state, add_age sets age to a fixed number, and add_bio reads both name "
                "and age to build a sentence like \"Mohammad is 25 years old.\" stored in bio. "
                "Invoke the graph and print the final state."
            ),
            "difficulty": DifficultyLevel.beginner,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Define a State with 3+ fields using TypedDict",
                "Write nodes that return partial state updates",
                "Chain 4 nodes together in the correct order",
                "Have a later node combine data set by earlier nodes",
            ],
            "rubric": {
                "state_design": "State fields (name, age, bio) are correctly typed (20%)",
                "nodes": "Each node correctly reads/returns only the relevant partial update (40%)",
                "wiring": "Edges connect START -> add_name -> add_age -> add_bio -> END (20%)",
                "output": "Final bio string correctly combines name and age (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Nodes & Edges",
        "slug":              "nodes-and-edges",
        "description":       "A closer look at Edges: how they control flow, normal edges vs the idea of conditional edges, and a realistic multi-route example.",
        "order":             4,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   1.0,
        "skill_tags":        ["langgraph", "python", "edges", "nodes"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Nodes & Edges",
            "content": """# 🔗 Lesson 4 — Nodes & Edges

You already know:

- **State** = information
- **Node** = a function that does something
- **Edge** = tells the graph where to go next

Now let's understand Edges properly.

## 1. What Is an Edge?

Imagine this:

```
START
  ↓
node_a
  ↓
node_b
  ↓
END
```

The arrows are edges. In LangGraph:

```python
graph.add_edge("node_a", "node_b")
```

means: *after `node_a` finishes, run `node_b`.*

## 2. A Simple Example

Let's create two nodes.

```python
def first_node(state):
    print("I am the first node")
    return state

def second_node(state):
    print("I am the second node")
    return state
```

Then connect them:

```python
graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)
```

The workflow is:

```
START
  ↓
first
  ↓
second
  ↓
END
```

## 3. Why Are Edges Important?

Because they control the flow. Imagine an AI application:

```
START
  ↓
Understand Question
  ↓
Retrieve Documents
  ↓
Generate Answer
  ↓
END
```

The edges determine that order. Without edges, LangGraph doesn't know: *"What should happen
next?"*

## 4. Multiple Paths

Now things get more interesting. Suppose we have:

```
             ┌──→ Calculator
             │
START → Analyze
             │
             └──→ Search
```

The AI analyzes the question and decides: *is this a math question?* If yes → Calculator,
if no → Search. This is called a **conditional edge** — we'll study it in the next lesson.

For now, understand the difference:

**Normal edge**

```
A → B
```

means: always go from A to B.

**Conditional edge**

```
       → B
A → ?
       → C
```

means: decide where to go based on some condition.

## 5. Normal Edges in Code

Here's a complete example:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def first(state: State):
    print("First node")
    return state


def second(state: State):
    print("Second node")
    return state


graph = StateGraph(State)

graph.add_node("first", first)
graph.add_node("second", second)

graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)

app = graph.compile()

app.invoke({"message": "Hello"})
```

Output:

```
First node
Second node
```

## 6. Think of Edges Like Road Signs 🚗

This is a useful mental model. Imagine your graph is a road system:

```
START
  │
  ▼
Node A
  │
  ▼
Node B
  │
  ▼
END
```

The edge is basically saying: *"After Node A, drive to Node B."*

A conditional edge is like a road sign:

```
              ┌── Calculator
              │
Analyze ──────┤
              │
              └── Search
```

The sign decides which road to take.

## 7. A More Realistic Example

Imagine we're building a customer-support AI:

```
START
  ↓
Classify Question
  ↓
Answer Question
  ↓
END
```

There could be three types: Billing, Technical, General. Eventually we could build:

```
                  ┌── Billing
                  │
Classify ─────────┼── Technical
                  │
                  └── General
```

Each route could have different nodes:

```
                 ┌── Billing → Billing Agent
                 │
Classify ────────┼── Technical → Technical Agent
                 │
                 └── General → General Agent
```

This is the kind of workflow LangGraph is designed for.

## 8. The Big Difference: LangChain vs LangGraph

This is worth remembering.

**LangChain** — you might build a straight line:

```
Question → Retriever → LLM → Answer
```

**LangGraph** — you can build branching, looping workflows:

```
Question
   ↓
Analyze
   ↓
 ┌───────────────┐
 │               │
 ↓               ↓
RAG             Tool
 │               │
 └───────┬───────┘
         ↓
       Check
         ↓
      Good?
      ↙   ↘
    Yes     No
     ↓       ↓
   Answer   Retry
```

LangGraph gives you control over the workflow.

## 🧠 Important Vocabulary

| Term | Meaning |
|---|---|
| State | Data shared between nodes |
| Node | Function that performs an action |
| Edge | Connection between nodes |
| START | Beginning of graph |
| END | End of graph |
| Normal Edge | Always follows the same path |
| Conditional Edge | Chooses a path based on logic |

## 🧪 Mini Exercise

Build this:

```
START
  ↓
node_a
  ↓
node_b
  ↓
node_c
  ↓
END
```

Where `node_a` prints "A", `node_b` prints "B", `node_c` prints "C". Expected output:

```
A
B
C
```

Try to build it without looking at the complete example above.
""",
            "order": 4,
            "estimated_minutes": 30,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Three-node A/B/C chain",
                "description": (
                    "Build the graph START → node_a → node_b → node_c → END. `node_a` prints "
                    "\"A\", `node_b` prints \"B\", `node_c` prints \"C\", each returning the state "
                    "unchanged. Compile and invoke it with any simple state and confirm the "
                    "printed output is A, B, C in order."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    message: str\n\n\n"
                    "def node_a(state: State):\n"
                    "    # TODO: print \"A\" and return state\n"
                    "    pass\n\n\n"
                    "def node_b(state: State):\n"
                    "    # TODO: print \"B\" and return state\n"
                    "    pass\n\n\n"
                    "def node_c(state: State):\n"
                    "    # TODO: print \"C\" and return state\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add 3 nodes, chain edges START->a->b->c->END, compile, invoke\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    message: str\n\n\n"
                    "def node_a(state: State):\n"
                    "    print(\"A\")\n"
                    "    return state\n\n\n"
                    "def node_b(state: State):\n"
                    "    print(\"B\")\n"
                    "    return state\n\n\n"
                    "def node_c(state: State):\n"
                    "    print(\"C\")\n"
                    "    return state\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"node_a\", node_a)\n"
                    "graph.add_node(\"node_b\", node_b)\n"
                    "graph.add_node(\"node_c\", node_c)\n\n"
                    "graph.add_edge(START, \"node_a\")\n"
                    "graph.add_edge(\"node_a\", \"node_b\")\n"
                    "graph.add_edge(\"node_b\", \"node_c\")\n"
                    "graph.add_edge(\"node_c\", END)\n\n"
                    "app = graph.compile()\n"
                    "app.invoke({\"message\": \"go\"})\n"
                    "# Output: A\\nB\\nC\n"
                ),
                "skill_tested": ["langgraph", "edges", "nodes"],
            },
            {
                "title": "Sketch a support-ticket router",
                "description": (
                    "Without writing full LangGraph code, sketch (as a diagram in comments) a "
                    "graph for a support ticket system: START → classify → one of "
                    "billing_agent / technical_agent / general_agent → END. List the node names "
                    "you'd create and the edges you'd need to add (which ones are normal edges, "
                    "and which single point needs a conditional edge)."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# TODO: list node names\n"
                    "# TODO: list add_edge(...) calls that are normal edges\n"
                    "# TODO: identify which node needs add_conditional_edges instead, and why\n"
                ),
                "solution_code": (
                    "# Nodes: classify, billing_agent, technical_agent, general_agent\n"
                    "#\n"
                    "# Normal edges:\n"
                    "#   add_edge(START, \"classify\")\n"
                    "#   add_edge(\"billing_agent\", END)\n"
                    "#   add_edge(\"technical_agent\", END)\n"
                    "#   add_edge(\"general_agent\", END)\n"
                    "#\n"
                    "# classify needs a CONDITIONAL edge, because after classifying the\n"
                    "# ticket type, the graph must choose one of three different next nodes\n"
                    "# based on the result -- a normal edge can only ever go to one fixed node.\n"
                ),
                "skill_tested": ["langgraph", "edges", "design"],
            },
        ],
        "quiz": {
            "title": "Nodes & Edges — Quiz",
            "questions": [
                {
                    "question": "What does graph.add_edge(\"node_a\", \"node_b\") mean?",
                    "options": [
                        "node_b always runs before node_a",
                        "After node_a finishes, always run node_b",
                        "node_a and node_b run at the same time",
                        "node_a is deleted and replaced by node_b",
                    ],
                    "correct": 1,
                    "explanation": "A normal edge always routes from the first node to the second, unconditionally.",
                },
                {
                    "question": "What is the key difference between a normal edge and a conditional edge?",
                    "options": [
                        "Normal edges are faster to execute",
                        "A normal edge always goes to the same next node; a conditional edge picks the next node based on logic",
                        "Conditional edges can only be used with START",
                        "There is no difference",
                    ],
                    "correct": 1,
                    "explanation": "Normal edges are fixed (A -> B); conditional edges decide between multiple possible next nodes.",
                },
                {
                    "question": "In the customer-support example, why might 'classify' route to different agent nodes?",
                    "options": [
                        "Because every node must connect to every other node",
                        "Because the ticket type (billing/technical/general) determines which specialized node should handle it next",
                        "Because LangGraph requires at least 3 nodes",
                        "Because normal edges cannot connect to END",
                    ],
                    "correct": 1,
                    "explanation": "Different ticket categories need different downstream handling, which is exactly the branching behavior conditional routing supports.",
                },
                {
                    "question": "Without any edges at all, what happens to a LangGraph graph?",
                    "options": [
                        "It still runs nodes in the order they were added",
                        "LangGraph doesn't know what should happen next, so the flow is undefined",
                        "It automatically connects START directly to END",
                        "It throws a compile-time syntax error only if there are 2+ nodes",
                    ],
                    "correct": 1,
                    "explanation": "Edges are what define the flow; without them, LangGraph has no instructions for what runs after what.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Three-Stage Pipeline with Printed Trace",
            "description": (
                "Build a graph modeling 'Understand Question → Retrieve Documents → Generate "
                "Answer → END'. Each node should print its own name when it runs and append its "
                "name to a `trace` list field on the state (e.g. state['trace'] = "
                "[..., 'retrieve']). After invoking, print the final `trace` list to confirm the "
                "nodes ran in the correct order."
            ),
            "difficulty": DifficultyLevel.beginner,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Model a realistic 3-stage AI pipeline using only normal edges",
                "Have each node append to a shared list in state",
                "Verify execution order via the final state",
            ],
            "rubric": {
                "state_design": "State includes a trace list field alongside the pipeline's other fields (20%)",
                "nodes": "Each of the 3 nodes prints its name and appends correctly to trace (40%)",
                "wiring": "Edges connect START -> understand -> retrieve -> generate -> END (25%)",
                "verification": "Final trace list is printed and matches the expected order (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Conditional Edges",
        "slug":              "conditional-edges",
        "description":       "Build real branching logic with add_conditional_edges: routing functions, a math-vs-search router, and why this powers AI agent decision-making.",
        "order":             5,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "python", "conditional-edges", "routing"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Conditional Edges",
            "content": """# 🔀 Lesson 5 — Conditional Edges

This is where LangGraph starts becoming really interesting.

So far, our graphs were always: `A → B → C → END`. But real AI applications need to make
decisions, for example:

```
Question
    ↓
  Analyze
    ↓
Is it math?
  ↙     ↘
YES     NO
 ↓       ↓
Calc   Search
```

This is a conditional edge.

## 1. Normal Edge vs Conditional Edge

**Normal edge**

```python
graph.add_edge("a", "b")
```

Means `A → B` — it always goes to B.

**Conditional edge** — a conditional edge asks *"Where should I go next?"*

```
       ┌──→ calculator
       │
analyze
       │
       └──→ search
```

The answer depends on the state.

## 2. Let's Build One

Our goal:

```
START
  ↓
check_question
  ↓
 ┌─────────────┐
 │             │
math         other
 ↓             ↓
calculator    search
 ↓             ↓
 └──────┬──────┘
        ↓
       END
```

## 3. Create the State

```python
from typing import TypedDict

class State(TypedDict):
    question: str
    category: str
```

Example: `{"question": "What is 5 + 5?", "category": ""}`

## 4. Create the First Node

This node decides the category.

```python
def check_question(state: State):
    question = state["question"].lower()

    if any(word in question for word in ["+", "-", "*", "/", "calculate"]):
        return {"category": "math"}

    return {"category": "other"}
```

So `"What is 5 + 5?"` → category → `"math"`.

## 5. Create the Two Nodes

```python
def calculator(state: State):
    print("Using calculator...")
    return state

def search(state: State):
    print("Using search...")
    return state
```

## 6. Create the Routing Function

This is the important part.

```python
def route_question(state: State):
    if state["category"] == "math":
        return "calculator"

    return "search"
```

This function tells LangGraph: *"Which node should I go to?"*

## 7. Create the Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("check_question", check_question)
graph.add_node("calculator", calculator)
graph.add_node("search", search)
```

## 8. Add the Normal Edge

```python
graph.add_edge(START, "check_question")
```

## 9. Add the Conditional Edge

Here's the important line:

```python
graph.add_conditional_edges(
    "check_question",
    route_question
)
```

This means: *after `check_question`, call `route_question` to decide what happens next.* Our
routing function returns either `"calculator"` or `"search"`, and LangGraph follows the
appropriate path.

## 10. Connect Both Nodes to END

```python
graph.add_edge("calculator", END)
graph.add_edge("search", END)
```

Now our graph is:

```
                    ┌── calculator ──→ END
                    │
START → check_question
                    │
                    └── search ──────→ END
```

## 11–12. Compile & Test It

```python
app = graph.compile()
```

**Math question:**

```python
result = app.invoke({"question": "What is 5 + 5?", "category": ""})
```

Workflow: `START → check_question → math → calculator → END`. Output: `Using calculator...`

**Non-math question:**

```python
result = app.invoke({"question": "What is LangGraph?", "category": ""})
```

Workflow: `START → check_question → other → search → END`. Output: `Using search...`

## 🧩 Complete Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    category: str


def check_question(state: State):
    question = state["question"].lower()

    if any(word in question for word in ["+", "-", "*", "/", "calculate"]):
        return {"category": "math"}

    return {"category": "other"}


def calculator(state: State):
    print("Using calculator...")
    return state


def search(state: State):
    print("Using search...")
    return state


def route_question(state: State):
    if state["category"] == "math":
        return "calculator"

    return "search"


graph = StateGraph(State)

graph.add_node("check_question", check_question)
graph.add_node("calculator", calculator)
graph.add_node("search", search)

graph.add_edge(START, "check_question")

graph.add_conditional_edges(
    "check_question",
    route_question
)

graph.add_edge("calculator", END)
graph.add_edge("search", END)

app = graph.compile()

result = app.invoke({"question": "What is 5 + 5?", "category": ""})

print(result)
```

## 🧠 The Most Important Line

Remember this:

```python
graph.add_conditional_edges(
    "check_question",
    route_question
)
```

Think of it as:

```
             route_question()
                    ↓
             "Where should I go?"
                    ↓
              ┌─────┴─────┐
              ↓           ↓
        calculator      search
```

## 🔥 Why This Matters for AI Agents

Imagine an AI assistant. If the user says *"What is 15 × 20?"*:

```
User → LLM analyzes question → Is a tool needed? → YES → Calculator Tool → LLM → Answer
```

If they ask *"Explain LangGraph."*:

```
User → LLM analyzes question → Is a tool needed? → NO → LLM → Answer
```

And if they ask *"Find information about LangGraph."*:

```
User → Analyze → Search needed? → YES → Search Tool → Analyze Results → Answer
```

Conditional edges are what let us create these decision-making workflows.

## 🧪 Your Exercise

Modify the example so there are three routes:

```
                ┌── math
                │
Question ───────┼── programming
                │
                └── general
```

Create `math_node()`, `programming_node()`, and `general_node()`, and route based on
keywords. For example: `"2 + 5"` → math, `"How do I use Python?"` → programming, `"What is
LangGraph?"` → general.

Don't worry if you can't do it yet — the next lesson will make the routing concept even
easier.
""",
            "order": 5,
            "estimated_minutes": 55,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Three-way router: math / programming / general",
                "description": (
                    "Extend the check_question example into a three-route graph. Write "
                    "`classify(state)` that sets `category` to \"math\" (if the question contains "
                    "digits or math symbols like + - * /), \"programming\" (if it mentions words "
                    "like 'python', 'code', 'function', 'bug'), or \"general\" otherwise. Write "
                    "`math_node`, `programming_node`, and `general_node`, each printing which "
                    "route was taken. Write `route_question` returning the right node name, and "
                    "wire it up with `add_conditional_edges`."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    category: str\n\n\n"
                    "def classify(state: State):\n"
                    "    # TODO: set category to 'math', 'programming', or 'general'\n"
                    "    pass\n\n\n"
                    "def math_node(state: State):\n"
                    "    print(\"Routed to: math\")\n"
                    "    return state\n\n\n"
                    "def programming_node(state: State):\n"
                    "    print(\"Routed to: programming\")\n"
                    "    return state\n\n\n"
                    "def general_node(state: State):\n"
                    "    print(\"Routed to: general\")\n"
                    "    return state\n\n\n"
                    "def route_question(state: State):\n"
                    "    # TODO: return 'math_node', 'programming_node', or 'general_node'\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add nodes, add_edge(START, 'classify'),\n"
                    "# add_conditional_edges('classify', route_question),\n"
                    "# connect all three route nodes to END, compile, invoke\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    category: str\n\n\n"
                    "def classify(state: State):\n"
                    "    q = state[\"question\"].lower()\n"
                    "    if any(ch in q for ch in [\"+\", \"-\", \"*\", \"/\"]) or any(c.isdigit() for c in q):\n"
                    "        return {\"category\": \"math\"}\n"
                    "    if any(word in q for word in [\"python\", \"code\", \"function\", \"bug\"]):\n"
                    "        return {\"category\": \"programming\"}\n"
                    "    return {\"category\": \"general\"}\n\n\n"
                    "def math_node(state: State):\n"
                    "    print(\"Routed to: math\")\n"
                    "    return state\n\n\n"
                    "def programming_node(state: State):\n"
                    "    print(\"Routed to: programming\")\n"
                    "    return state\n\n\n"
                    "def general_node(state: State):\n"
                    "    print(\"Routed to: general\")\n"
                    "    return state\n\n\n"
                    "def route_question(state: State):\n"
                    "    if state[\"category\"] == \"math\":\n"
                    "        return \"math_node\"\n"
                    "    if state[\"category\"] == \"programming\":\n"
                    "        return \"programming_node\"\n"
                    "    return \"general_node\"\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"classify\", classify)\n"
                    "graph.add_node(\"math_node\", math_node)\n"
                    "graph.add_node(\"programming_node\", programming_node)\n"
                    "graph.add_node(\"general_node\", general_node)\n\n"
                    "graph.add_edge(START, \"classify\")\n"
                    "graph.add_conditional_edges(\"classify\", route_question)\n"
                    "graph.add_edge(\"math_node\", END)\n"
                    "graph.add_edge(\"programming_node\", END)\n"
                    "graph.add_edge(\"general_node\", END)\n\n"
                    "app = graph.compile()\n"
                    "app.invoke({\"question\": \"2 + 5\", \"category\": \"\"})          # math\n"
                    "app.invoke({\"question\": \"How do I use Python?\", \"category\": \"\"})  # programming\n"
                    "app.invoke({\"question\": \"What is LangGraph?\", \"category\": \"\"})    # general\n"
                ),
                "skill_tested": ["langgraph", "conditional-edges", "routing"],
            },
            {
                "title": "Trace which branch ran",
                "description": (
                    "Using the original calculator/search graph from the lesson, add a "
                    "`route_taken` field to State. Update `calculator` and `search` so each sets "
                    "`route_taken` to its own name. Invoke the graph with both a math and a "
                    "non-math question and print `result['route_taken']` for each to prove the "
                    "conditional edge picked the correct path."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    category: str\n"
                    "    route_taken: str\n\n\n"
                    "def calculator(state: State):\n"
                    "    # TODO: print + return update setting route_taken = 'calculator'\n"
                    "    pass\n\n\n"
                    "def search(state: State):\n"
                    "    # TODO: print + return update setting route_taken = 'search'\n"
                    "    pass\n"
                ),
                "solution_code": (
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    category: str\n"
                    "    route_taken: str\n\n\n"
                    "def calculator(state: State):\n"
                    "    print(\"Using calculator...\")\n"
                    "    return {\"route_taken\": \"calculator\"}\n\n\n"
                    "def search(state: State):\n"
                    "    print(\"Using search...\")\n"
                    "    return {\"route_taken\": \"search\"}\n\n\n"
                    "# result1 = app.invoke({\"question\": \"5 + 5\", \"category\": \"\", \"route_taken\": \"\"})\n"
                    "# print(result1[\"route_taken\"])  # 'calculator'\n"
                    "# result2 = app.invoke({\"question\": \"hi\", \"category\": \"\", \"route_taken\": \"\"})\n"
                    "# print(result2[\"route_taken\"])  # 'search'\n"
                ),
                "skill_tested": ["langgraph", "conditional-edges", "state"],
            },
        ],
        "quiz": {
            "title": "Conditional Edges — Quiz",
            "questions": [
                {
                    "question": "What does a routing function passed to add_conditional_edges return?",
                    "options": [
                        "A boolean only",
                        "The full updated state",
                        "The name of the next node to run",
                        "Nothing — it's void",
                    ],
                    "correct": 2,
                    "explanation": "The routing function inspects the state and returns a string naming which node LangGraph should go to next.",
                },
                {
                    "question": "graph.add_conditional_edges(\"check_question\", route_question) — what does the first argument mean?",
                    "options": [
                        "The node the conditional routing applies AFTER",
                        "The name of the destination node",
                        "The name of the State class",
                        "It's ignored by LangGraph",
                    ],
                    "correct": 0,
                    "explanation": "It's the source node — after check_question finishes, route_question decides where to go next.",
                },
                {
                    "question": "In the math-vs-search example, what determines whether the graph goes to calculator or search?",
                    "options": [
                        "A random choice",
                        "The order nodes were added",
                        "The value of state['category'], set earlier by check_question",
                        "Whether END was reached first",
                    ],
                    "correct": 2,
                    "explanation": "check_question sets category based on the question text, and route_question reads that category to decide the path.",
                },
                {
                    "question": "Why are conditional edges essential for AI agents that decide whether to use a tool?",
                    "options": [
                        "They aren't needed — normal edges are enough",
                        "They let the graph branch to different next steps (e.g. tool vs. no tool) based on the LLM's decision stored in state",
                        "They only work with the calculator tool",
                        "They remove the need for a routing function",
                    ],
                    "correct": 1,
                    "explanation": "Agent decisions ('is a tool needed?') are exactly the kind of branching logic conditional edges are built for.",
                },
                {
                    "question": "How many different next-node destinations can a single add_conditional_edges call support?",
                    "options": [
                        "Exactly one",
                        "Exactly two",
                        "As many as the routing function's return values map to",
                        "Zero — it just ends the graph",
                    ],
                    "correct": 2,
                    "explanation": "As shown in the exercise, a routing function can return any number of different node names (math_node, programming_node, general_node, etc.).",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Three-Route Question Classifier",
            "description": (
                "Build a full LangGraph program with a `classify` node and a conditional edge "
                "routing to `math_node`, `programming_node`, or `general_node`, based on keyword "
                "rules you design. Test it against at least 6 sample questions (2 per category) "
                "and print a table of question -> category -> node output."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Design a classification node with clear keyword-based rules",
                "Write a routing function used with add_conditional_edges",
                "Wire three destination nodes back to END",
                "Validate behavior against multiple test questions",
            ],
            "rubric": {
                "classification_logic": "classify() correctly separates math/programming/general using reasonable rules (30%)",
                "conditional_wiring": "add_conditional_edges is used correctly with a working routing function (35%)",
                "nodes": "All three destination nodes are implemented and connected to END (20%)",
                "testing": "At least 6 test cases are run and their outputs are shown (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Loops in LangGraph",
        "slug":              "loops-in-langgraph",
        "description":       "How to make a graph repeat a step using conditional edges that route back to an earlier node, with stopping conditions to avoid infinite loops.",
        "order":             6,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "python", "loops", "conditional-edges"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Loops in LangGraph",
            "content": """# 🔁 Lesson 6 — Loops in LangGraph

You've learned how to make LangGraph move from one node to another, and make decisions
using conditional edges. Now we'll learn something very important: **how to make a graph
repeat a step.** This is called a loop.

## 1. Why Do We Need Loops?

Imagine an AI generating an answer:

```
Question
   ↓
Generate Answer
   ↓
Check Answer
   ↓
Is it good?
  ↙     ↘
 YES     NO
 ↓        ↓
 END   Generate Again
```

Notice what happens when the answer isn't good:

```
Check Answer
     ↓
Generate Answer
```

We're going backward to an earlier node. That's a loop.

## 2. Simple Loop

Imagine:

```
START
  ↓
A
  ↓
B
  ↓
A
  ↓
B
  ↓
...
```

The graph keeps repeating. We need a condition to eventually stop it, for example:

```
START
  ↓
A
  ↓
Check
 ↙    ↘
YES    NO
 ↓      ↓
END     A
```

## 3. Our Example

Let's build a simple counter. The goal:

```
Count = 0
   ↓
increment
   ↓
Is count >= 3?
  ↙      ↘
 YES      NO
  ↓        ↓
 END    increment
```

So the graph will produce: `0 → 1 → 2 → 3 → END`.

## 4. Create the State

```python
from typing import TypedDict

class State(TypedDict):
    count: int
```

Our state: `{"count": 0}`.

## 5. Create the Node

Our node increases the count.

```python
def increment(state: State):
    return {
        "count": state["count"] + 1
    }
```

If `count = 0` it becomes `count = 1`, then `1 → 2`, then `2 → 3`.

## 6. Create the Routing Function

Now we need to decide: should we stop or continue?

```python
def should_continue(state: State):
    if state["count"] >= 3:
        return "end"

    return "continue"
```

So `count = 3` → `"end"`, but `count < 3` → `"continue"`.

## 7. Build the Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("increment", increment)
```

Connect START:

```python
graph.add_edge(START, "increment")
```

Then add the conditional edge:

```python
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue": "increment",
        "end": END
    }
)
```

This part is extremely important. We're telling LangGraph: `"continue" → increment`,
`"end" → END`.

```
             ┌──────────────┐
             │              │
             ↓              │
START → increment → continue
             │
             │ end
             ↓
            END
```

## 8–9. Compile & Run It

```python
app = graph.compile()

result = app.invoke({"count": 0})

print(result)
```

The graph executes: `count = 0 → increment → count = 1 → increment → count = 2 → increment →
count = 3 → END`. Final result: `{"count": 3}`.

## 🧩 Complete Code

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    count: int


def increment(state: State):
    print("Count:", state["count"])

    return {
        "count": state["count"] + 1
    }


def should_continue(state: State):

    if state["count"] >= 3:
        return "end"

    return "continue"


graph = StateGraph(State)

graph.add_node("increment", increment)

graph.add_edge(START, "increment")

graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue": "increment",
        "end": END
    }
)

app = graph.compile()

result = app.invoke({"count": 0})

print("Final:", result)
```

You should see something similar to:

```
Count: 0
Count: 1
Count: 2
Final: {'count': 3}
```

## 🧠 Understand the Loop

This is the key: `"continue": "increment"` means *go back to the increment node*. That's
the loop. While a normal edge looks like `A → B`, a loop looks like:

```
A → B
↑   ↓
└───┘
```

## 🔥 Real AI Example

Now imagine a RAG system:

```
             ┌─────────────────────┐
             │                     │
             ↓                     │
Question → Retrieve → Check Results
                         │
                    ┌────┴────┐
                    ↓         ↓
                  Good       Bad
                    ↓         │
                  Answer      │
                    ↓         │
                   END        │
                              │
                              ↓
                           Retrieve
```

If retrieval isn't good enough: `Retrieve → Check → Bad → Retrieve again`. This is extremely
useful for RAG agents.

## 🤖 Another AI Agent Example

An agent might work like:

```
User Question
     ↓
Think
     ↓
Use Tool
     ↓
Look at Result
     ↓
Need another tool?
   ↙        ↘
 YES        NO
 ↓           ↓
Think       Answer
 ↓           ↓
Tool        END
```

The agent can repeatedly `Think → Tool → Think → Tool → Think → Answer`. That's a loop.

## ⚠️ Important: Avoid Infinite Loops

This is dangerous:

```
A → B → A → B → A → ...
```

If there is no stopping condition, your graph may run indefinitely. Always have something
like `if count >= 3: return "end"`, or for an AI agent, a `maximum_iterations = 10` guard.

## 🎯 What You Should Remember

There are now three important types of flow you've learned:

1. **Sequential** — `A → B → C`
2. **Conditional** — branches to B or C based on logic
3. **Loop** — `A → B`, then back up to A again

These three concepts are enough to build surprisingly powerful workflows.
""",
            "order": 6,
            "estimated_minutes": 45,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Countdown loop",
                "description": (
                    "Build a graph with a `count` field starting at 5 that counts DOWN to 0. "
                    "Write a `decrement` node that subtracts 1 and prints the current count, "
                    "and a `should_continue` routing function that returns \"continue\" while "
                    "count > 0 and \"end\" once count reaches 0. Wire it with "
                    "add_conditional_edges so decrement loops back to itself."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    count: int\n\n\n"
                    "def decrement(state: State):\n"
                    "    # TODO: print count, then return update subtracting 1\n"
                    "    pass\n\n\n"
                    "def should_continue(state: State):\n"
                    "    # TODO: return 'continue' while count > 0, else 'end'\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add_node('decrement', decrement),\n"
                    "# add_edge(START, 'decrement'), add_conditional_edges(...),\n"
                    "# compile, invoke with {'count': 5}\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "class State(TypedDict):\n"
                    "    count: int\n\n\n"
                    "def decrement(state: State):\n"
                    "    print(\"Count:\", state[\"count\"])\n"
                    "    return {\"count\": state[\"count\"] - 1}\n\n\n"
                    "def should_continue(state: State):\n"
                    "    if state[\"count\"] > 0:\n"
                    "        return \"continue\"\n"
                    "    return \"end\"\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"decrement\", decrement)\n"
                    "graph.add_edge(START, \"decrement\")\n"
                    "graph.add_conditional_edges(\n"
                    "    \"decrement\",\n"
                    "    should_continue,\n"
                    "    {\"continue\": \"decrement\", \"end\": END}\n"
                    ")\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"count\": 5})\n"
                    "print(\"Final:\", result)  # {'count': 0}\n"
                ),
                "skill_tested": ["langgraph", "loops", "conditional-edges"],
            },
            {
                "title": "Retry-until-good loop",
                "description": (
                    "Model a simplified 'generate answer, check quality, retry if bad' loop. "
                    "State has `attempts: int` and `good: bool`. A `generate` node increments "
                    "`attempts` and sets `good = True` once `attempts >= 3` (simulating that the "
                    "3rd try succeeds), otherwise `good = False`. Write a routing function that "
                    "loops back to `generate` while `good` is False, and goes to END once `good` "
                    "is True. Cap it with a max of 5 attempts as a safety net even if `good` "
                    "never becomes True."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "class State(TypedDict):\n"
                    "    attempts: int\n"
                    "    good: bool\n\n\n"
                    "def generate(state: State):\n"
                    "    # TODO: increment attempts, set good=True once attempts >= 3\n"
                    "    pass\n\n\n"
                    "def should_continue(state: State):\n"
                    "    # TODO: 'end' if good is True OR attempts >= 5 (safety net), else 'continue'\n"
                    "    pass\n"
                ),
                "solution_code": (
                    "class State(TypedDict):\n"
                    "    attempts: int\n"
                    "    good: bool\n\n\n"
                    "def generate(state: State):\n"
                    "    attempts = state[\"attempts\"] + 1\n"
                    "    good = attempts >= 3\n"
                    "    print(f\"Attempt {attempts}, good={good}\")\n"
                    "    return {\"attempts\": attempts, \"good\": good}\n\n\n"
                    "def should_continue(state: State):\n"
                    "    if state[\"good\"] or state[\"attempts\"] >= 5:\n"
                    "        return \"end\"\n"
                    "    return \"continue\"\n\n\n"
                    "# graph.add_conditional_edges(\"generate\", should_continue,\n"
                    "#     {\"continue\": \"generate\", \"end\": END})\n"
                ),
                "skill_tested": ["langgraph", "loops", "safety-limits"],
            },
        ],
        "quiz": {
            "title": "Loops in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What makes a LangGraph flow a 'loop'?",
                    "options": [
                        "Having more than 2 nodes",
                        "A conditional edge that routes back to an earlier node instead of moving forward",
                        "Using a TypedDict for State",
                        "Calling app.invoke() more than once",
                    ],
                    "correct": 1,
                    "explanation": "A loop happens when the routing logic sends execution back to a node that already ran, like 'continue': 'increment'.",
                },
                {
                    "question": "In the counter example, what does the mapping {\"continue\": \"increment\", \"end\": END} do?",
                    "options": [
                        "It defines two separate graphs",
                        "It maps the routing function's return values to actual destination nodes",
                        "It sets the initial state",
                        "It limits the graph to 2 nodes",
                    ],
                    "correct": 1,
                    "explanation": "add_conditional_edges' third argument maps each possible string the routing function can return to a real node (or END).",
                },
                {
                    "question": "Why is a stopping condition essential in a loop?",
                    "options": [
                        "It isn't essential, loops always stop automatically",
                        "Without one, the graph could run indefinitely (an infinite loop)",
                        "It's only needed for RAG systems",
                        "It only affects performance, not correctness",
                    ],
                    "correct": 1,
                    "explanation": "Without a condition like count >= 3 or a max-iterations cap, a loop has no way to know when to stop.",
                },
                {
                    "question": "In a RAG agent, when would a loop back to 'Retrieve' make sense?",
                    "options": [
                        "Every single time, regardless of quality",
                        "When the check step determines the retrieved results weren't good enough",
                        "Only when the user asks twice",
                        "Loops are never useful in RAG systems",
                    ],
                    "correct": 1,
                    "explanation": "If Check Results finds the retrieval insufficient, looping back to Retrieve lets the system try again before answering.",
                },
                {
                    "question": "What's a good safety practice when building agent loops that might not naturally terminate?",
                    "options": [
                        "Never use conditional edges",
                        "Add a maximum iteration cap (e.g. stop after 10 tries) in addition to the main stopping condition",
                        "Avoid using State entirely",
                        "Only loop a fixed number of times with no condition at all",
                    ],
                    "correct": 1,
                    "explanation": "A max-iterations guard protects against cases where the primary condition never becomes true, preventing true infinite loops.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Guess-the-Number Loop",
            "description": (
                "Build a graph simulating a simple guessing game. State has `target: int`, "
                "`guess: int`, and `attempts: int`. A `guess_node` increases `guess` by a fixed "
                "step each time it runs (simulating getting closer) and increments `attempts`. "
                "A routing function loops back to `guess_node` while `guess != target` and "
                "`attempts < 10`, otherwise goes to END. Print each attempt's guess and the "
                "final result, including whether it succeeded or hit the attempt cap."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Model a loop with more than one stopping condition (success OR max attempts)",
                "Use add_conditional_edges with a continue/end mapping",
                "Print a step-by-step trace of the loop's progress",
                "Demonstrate the graph terminates correctly in both success and cap-reached cases",
            ],
            "rubric": {
                "state_design": "State tracks target, guess, and attempts correctly (20%)",
                "loop_logic": "guess_node and routing function correctly implement the loop and both stop conditions (45%)",
                "safety": "Max-attempts cap reliably prevents infinite looping (20%)",
                "output": "Clear printed trace of each attempt and the final outcome (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Using an LLM with LangGraph",
        "slug":              "using-an-llm-with-langgraph",
        "description":       "Turn an LLM call into a LangGraph node: setting up ChatOpenAI, building an ask_llm node, and understanding when LangGraph adds value over calling an LLM directly.",
        "order":             7,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "langchain", "llm", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Using an LLM with LangGraph",
            "content": """# 🤖 Lesson 7 — Using an LLM with LangGraph

Now we're going to connect the two things you've been learning: **LangGraph + LLM**. Our
goal is very simple:

```
User Question
      ↓
   LangGraph
      ↓
     LLM
      ↓
   Answer
```

We'll not build an agent yet. First, let's understand how an LLM becomes a LangGraph node.

## 1. The Big Idea

You already know that a LangGraph node is just a function:

```python
def my_node(state):
    ...
```

An LLM can be called inside that function:

```python
def ask_llm(state):
    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }
```

That's the key idea: `State → LLM Node → Updated State`.

## 2. Install the OpenAI Integration

If you want to use OpenAI:

```bash
pip install -U langchain-openai
```

You'll also need an API key. For example, in your terminal:

```bash
export OPENAI_API_KEY="your_api_key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

Don't put your API key directly into your Python code or GitHub repository.

## 3. Create the LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)
```

Now `llm` represents our language model.

## 4. Create the State

We'll need two pieces of information:

```python
from typing import TypedDict

class State(TypedDict):
    question: str
    answer: str
```

So our state looks like: `{"question": "What is LangGraph?", "answer": ""}`.

## 5. Create an LLM Node

Now comes the important part:

```python
def ask_llm(state: State):

    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }
```

Let's understand it: `state["question"]` gets the question text, `llm.invoke(...)` sends it
to the LLM, and `response.content` gets the actual text response, which we put into
`"answer"`.

## 6–7. Build the Graph & Compile

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("ask_llm", ask_llm)

graph.add_edge(START, "ask_llm")
graph.add_edge("ask_llm", END)

app = graph.compile()
```

Our graph is: `START → ask_llm → END`.

## 8. Run It

```python
result = app.invoke({
    "question": "Explain LangGraph in one simple sentence.",
    "answer": ""
})

print(result["answer"])
```

The LLM might return something like: *"LangGraph is a framework for building AI workflows
with connected steps and decisions."*

## 🧩 Complete Example

```python
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# State
class State(TypedDict):
    question: str
    answer: str


# Node
def ask_llm(state: State):

    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }


# Graph
graph = StateGraph(State)

graph.add_node("ask_llm", ask_llm)

graph.add_edge(START, "ask_llm")
graph.add_edge("ask_llm", END)


# Compile
app = graph.compile()


# Run
result = app.invoke({
    "question": "What is LangGraph?",
    "answer": ""
})


print(result["answer"])
```

## 🧠 What's Actually Happening?

```
app.invoke({"question": "What is LangGraph?", "answer": ""})
```

starts the graph. Then:

```
                 State
                   ↓
       question = "What is LangGraph?"
                   ↓
              ask_llm
                   ↓
             llm.invoke()
                   ↓
              LLM response
                   ↓
             answer = "..."
                   ↓
                  END
```

## ⭐ Very Important Concept

You might be thinking: *"Why not just call the LLM directly?"* You absolutely can — for a
simple application, `response = llm.invoke("What is LangGraph?")` is enough. But LangGraph
becomes useful when you have multiple steps, for example:

```
Question
   ↓
Analyze
   ↓
Retrieve
   ↓
LLM
   ↓
Check Answer
   ↓
Good?
 ↙     ↘
YES     NO
 ↓       ↓
END    Retrieve Again
```

That's where LangGraph starts providing real value.

## 9. Multiple LLM Nodes

We can also have more than one LLM node. For example:

```
START
  ↓
generate_question
  ↓
generate_answer
  ↓
END
```

Or:

```
START
  ↓
Analyze
  ↓
Draft Answer
  ↓
Review Answer
  ↓
Final Answer
  ↓
END
```

Each node could use the same LLM.

## 🔥 A Simple AI Workflow

Let's imagine we're building an AI tutor:

```
             User Question
                   ↓
              Understand
                   ↓
             Generate Answer
                   ↓
                Review
                   ↓
             Good Answer?
              ↙       ↘
            YES        NO
             ↓          ↓
            END      Generate Again
```

You now have all the fundamental LangGraph concepts needed to understand this: State,
Nodes, Edges, Conditional edges, Loops, and LLM nodes. That's a big milestone.

## ⚠️ One Important Change: Messages

When working with chat models, we usually don't want to treat everything as a plain string
forever. Instead, we'll start using `HumanMessage`, `AIMessage`, and `SystemMessage`:

```python
from langchain_core.messages import HumanMessage

messages = [
    HumanMessage(content="What is LangGraph?")
]
```

This becomes especially important when we build chatbots and agents — that's our next
topic.

## 🧪 Exercise

Modify the example so the LLM receives a prompt like:

```
You are a helpful AI teacher.

Explain the following topic in very simple language:

{question}
```

Hint:

```python
prompt = f\"\"\"
You are a helpful AI teacher.

Explain the following topic in very simple language:

{state["question"]}
\"\"\"

response = llm.invoke(prompt)
```
""",
            "order": 7,
            "estimated_minutes": 50,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Wrap the question in a teacher prompt",
                "description": (
                    "Modify `ask_llm` so that instead of sending `state['question']` directly to "
                    "the LLM, it wraps it in a prompt: \"You are a helpful AI teacher. Explain "
                    "the following topic in very simple language: {question}\". Use an f-string "
                    "to build the prompt, then call `llm.invoke(prompt)` and store "
                    "`response.content` in `answer` as before."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    answer: str\n\n\n"
                    "def ask_llm(state: State):\n"
                    "    # TODO: build the teacher prompt with state['question'] inserted,\n"
                    "    # call llm.invoke(prompt), and return the answer update\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add_node/add_edge x2, compile, invoke\n"
                ),
                "solution_code": (
                    "from typing import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    answer: str\n\n\n"
                    "def ask_llm(state: State):\n"
                    "    prompt = f\"\"\"\n"
                    "You are a helpful AI teacher.\n\n"
                    "Explain the following topic in very simple language:\n\n"
                    "{state['question']}\n"
                    "\"\"\"\n"
                    "    response = llm.invoke(prompt)\n"
                    "    return {\"answer\": response.content}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"ask_llm\", ask_llm)\n"
                    "graph.add_edge(START, \"ask_llm\")\n"
                    "graph.add_edge(\"ask_llm\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"question\": \"What is LangGraph?\", \"answer\": \"\"})\n"
                    "print(result[\"answer\"])\n"
                ),
                "skill_tested": ["langgraph", "llm", "prompts"],
            },
            {
                "title": "Two-step: draft then review",
                "description": (
                    "Build a graph with two LLM nodes: `draft_answer` (asks the LLM to answer "
                    "`state['question']` and stores it in `draft`), and `review_answer` (asks the "
                    "LLM to shorten/improve `state['draft']` into a friendlier version, storing "
                    "the result in `answer`). Wire START → draft_answer → review_answer → END, "
                    "and update the State TypedDict to include `question`, `draft`, and "
                    "`answer`."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    draft: str\n"
                    "    answer: str\n\n\n"
                    "def draft_answer(state: State):\n"
                    "    # TODO: llm.invoke(state['question']) -> store in 'draft'\n"
                    "    pass\n\n\n"
                    "def review_answer(state: State):\n"
                    "    # TODO: ask llm to friendlier-ify state['draft'] -> store in 'answer'\n"
                    "    pass\n"
                ),
                "solution_code": (
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    draft: str\n"
                    "    answer: str\n\n\n"
                    "def draft_answer(state: State):\n"
                    "    response = llm.invoke(state[\"question\"])\n"
                    "    return {\"draft\": response.content}\n\n\n"
                    "def review_answer(state: State):\n"
                    "    prompt = f\"Rewrite this answer in a friendlier, simpler tone:\\n\\n{state['draft']}\"\n"
                    "    response = llm.invoke(prompt)\n"
                    "    return {\"answer\": response.content}\n\n\n"
                    "# graph.add_node('draft_answer', draft_answer)\n"
                    "# graph.add_node('review_answer', review_answer)\n"
                    "# graph.add_edge(START, 'draft_answer')\n"
                    "# graph.add_edge('draft_answer', 'review_answer')\n"
                    "# graph.add_edge('review_answer', END)\n"
                ),
                "skill_tested": ["langgraph", "llm", "multi-step"],
            },
        ],
        "quiz": {
            "title": "Using an LLM with LangGraph — Quiz",
            "questions": [
                {
                    "question": "How does an LLM get used inside a LangGraph node?",
                    "options": [
                        "LangGraph has a special LLMNode class that's different from a normal node",
                        "It's just called inside a regular node function, e.g. llm.invoke(...) inside def ask_llm(state)",
                        "LLMs cannot be used inside LangGraph nodes",
                        "The LLM must be passed as an edge, not a node",
                    ],
                    "correct": 1,
                    "explanation": "An LLM node is just a normal Python function that happens to call llm.invoke() and return an update to state.",
                },
                {
                    "question": "What does response.content give you after llm.invoke(...)?",
                    "options": [
                        "The raw HTTP status code",
                        "The actual text response from the LLM",
                        "The original prompt sent to the LLM",
                        "A list of all previous messages",
                    ],
                    "correct": 1,
                    "explanation": "response.content holds the text the model generated in reply to the prompt.",
                },
                {
                    "question": "If you only need one single LLM call with no branching or multiple steps, is LangGraph required?",
                    "options": [
                        "Yes, LangGraph is required for any LLM call",
                        "No — calling llm.invoke(...) directly is enough; LangGraph adds value once you have multiple steps, branches, or loops",
                        "No, and LangGraph cannot be used for single calls at all",
                        "Yes, because LLMs can only run inside a graph",
                    ],
                    "correct": 1,
                    "explanation": "The lesson makes clear that for simple, single-call use cases, calling the LLM directly is sufficient — LangGraph shines with multi-step workflows.",
                },
                {
                    "question": "Why does the lesson recommend NOT hardcoding your API key into your Python code?",
                    "options": [
                        "It slows down the LLM",
                        "Hardcoded keys can be accidentally committed to a repo and exposed/leaked",
                        "LangGraph doesn't support environment variables",
                        "It only matters for local development",
                    ],
                    "correct": 1,
                    "explanation": "Using an environment variable (e.g. OPENAI_API_KEY) keeps the secret out of source code, reducing the risk of it leaking, e.g. via GitHub.",
                },
                {
                    "question": "Why does the lesson introduce HumanMessage/AIMessage/SystemMessage as an upcoming change?",
                    "options": [
                        "Because plain strings are always better",
                        "Because chat-based workflows (chatbots, agents) typically need structured message roles, not just raw strings",
                        "Because LangGraph cannot accept strings anymore",
                        "Because these are unrelated to LangGraph",
                    ],
                    "correct": 1,
                    "explanation": "As you move toward chatbots and agents, distinguishing who said what (user, assistant, system) becomes important — hence structured message types.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "AI Tutor: Draft → Review Pipeline",
            "description": (
                "Build the 'AI tutor' workflow sketched in the lesson: Understand → Generate "
                "Answer → Review → END (skip the loop-back for now; that's next lesson's topic). "
                "`understand` can simply pass the question through, `generate_answer` calls the "
                "LLM with a teacher-style prompt, and `review` asks the LLM to check clarity and "
                "produce a final polished `answer`. Test it with at least 3 different questions."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Chain 3 nodes together where 2 of them call an LLM",
                "Use a custom system-style prompt for the teaching persona",
                "Pass information between LLM calls via state",
                "Test the full pipeline against multiple questions",
            ],
            "rubric": {
                "state_design": "State includes question, draft/intermediate fields, and final answer (15%)",
                "llm_nodes": "Both LLM-calling nodes correctly build prompts and store results (45%)",
                "wiring": "Nodes are correctly chained START -> understand -> generate_answer -> review -> END (20%)",
                "testing": "At least 3 different questions are tested with results shown (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Messages in LangGraph",
        "slug":              "messages-in-langgraph",
        "description":       "SystemMessage, HumanMessage, and AIMessage; representing conversations as a messages list; and the add_messages reducer for accumulating chat history in State.",
        "order":             8,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "langchain", "messages", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Messages in LangGraph",
            "content": """# 💬 Lesson 8 — Messages in LangGraph

Now we're going to learn an important concept for building chatbots and agents: **Messages**.

You've already seen this: `llm.invoke("What is LangGraph?")`. That's fine for a single
question. But a chatbot needs conversations:

```
User: What is LangGraph?
AI: LangGraph is...

User: Why do I need it?
AI: You can use it...

User: Give me an example.
AI: Sure...
```

We need a way to keep track of these messages. That's what we're learning today.

## 1. What Is a Message?

A message is simply a piece of conversation. There are three important types:
`SystemMessage`, `HumanMessage`, `AIMessage`. Think of them as: System → instructions,
Human → user, AI → assistant.

## 2. HumanMessage

A message from the user:

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content="What is LangGraph?"
)
```

## 3. AIMessage

A message from the AI:

```python
from langchain_core.messages import AIMessage

message = AIMessage(
    content="LangGraph is a framework for building AI workflows."
)
```

## 4. SystemMessage

A system message gives instructions to the AI:

```python
from langchain_core.messages import SystemMessage

message = SystemMessage(
    content="You are a helpful AI teacher."
)
```

## 5. A Conversation

We can put messages together:

```python
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

messages = [
    SystemMessage(content="You are a helpful AI teacher."),
    HumanMessage(content="What is LangGraph?"),
    AIMessage(content="LangGraph helps you build AI workflows."),
    HumanMessage(content="Why is State important?")
]
```

Then we can send the conversation to the LLM.

## 6. Calling the LLM

```python
response = llm.invoke(messages)

print(response.content)
```

The model can use the previous messages to understand the conversation.

## 7. Why Messages Matter in LangGraph

Previously our State looked like:

```python
class State(TypedDict):
    question: str
    answer: str
```

For a chatbot, we can have:

```python
class State(TypedDict):
    messages: list
```

This lets the graph carry the conversation:
`messages → [HumanMessage, AIMessage, HumanMessage, AIMessage]`.

## 8. Our First Chatbot Graph

We'll build `START → chatbot → END`. The chatbot node will: read the messages, send them to
the LLM, generate an AI message, and add that message to the state.

## 9. State

```python
from typing import TypedDict

class State(TypedDict):
    messages: list
```

## 10. Create the Chatbot Node

```python
def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }
```

`state["messages"]` contains the conversation, `llm.invoke(...)` sends it to the LLM, and it
returns an `AIMessage`.

## 11–12. Build the Graph & Run It

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()
```

Run it:

```python
from langchain_core.messages import HumanMessage

result = app.invoke({
    "messages": [
        HumanMessage(content="What is LangGraph?")
    ]
})

print(result["messages"][-1].content)
```

The final message should be the AI's response.

## 🧩 Complete Example

```python
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END


# LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


# State
class State(TypedDict):
    messages: list


# Chatbot node
def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {"messages": [response]}


# Graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# Compile
app = graph.compile()

# Run
result = app.invoke({
    "messages": [HumanMessage(content="Explain LangGraph simply.")]
})

print(result["messages"][-1].content)
```

## ⚠️ One Problem

Suppose we run `app.invoke({"messages": [HumanMessage(content="Hello")]})` and get
`AI: Hello! How can I help?`. If we then invoke it again with
`HumanMessage(content="What did I just ask?")`, the graph doesn't automatically know about
the previous invocation. Why? Because **each invocation starts with a new state.** We'll
learn how to solve this later with memory and checkpoints.

## 🧠 Another Important Concept: add_messages

LangGraph provides a useful way to manage message history. Instead of simply replacing
`"messages": [response]`, we can use a **message reducer**:

```python
from typing import Annotated

from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Now LangGraph knows: *"When a node returns new messages, add them to the existing message
list."* This is extremely useful.

## 13. Why add_messages?

Imagine our state initially contains `H: What is LangGraph?`. The chatbot returns
`AI: LangGraph is...`. We want the combined history — `H: What is LangGraph?` followed by
`AI: LangGraph is...` — not just the AI message on its own, overwriting the human message.
The `add_messages` reducer helps maintain that history.

## ⭐ The Pattern You'll See Often

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Don't worry if this looks complicated. For now remember: `messages` grows as
`HumanMessage → AIMessage → HumanMessage → AIMessage → ...`, and `add_messages` helps
LangGraph manage this list.

## 🧠 The Three Message Types

| Message | Purpose |
|---|---|
| SystemMessage | Instructions |
| HumanMessage | User input |
| AIMessage | AI response |

Example: `SystemMessage("You are a Python teacher.")` → `HumanMessage("Explain
decorators.")` → `AIMessage("A decorator is...")`.

## 🎯 Mini Exercise

Create a chatbot state:

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Then create a node that sends the messages to the LLM. The workflow should be
`START → chatbot → END`. Try asking "Explain Python dictionaries." Then print
`result["messages"]` and inspect the messages — you should see a `HumanMessage` and an
`AIMessage`.
""",
            "order": 8,
            "estimated_minutes": 50,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Build a 3-message conversation",
                "description": (
                    "Without calling the LLM, manually construct a `messages` list representing "
                    "this conversation: a SystemMessage telling the AI it's a helpful math "
                    "tutor, a HumanMessage asking \"What is 12 * 8?\", and an AIMessage "
                    "answering \"96\". Then print each message's type (class name) and content "
                    "in order."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from langchain_core.messages import SystemMessage, HumanMessage, AIMessage\n\n"
                    "# TODO: build the messages list\n"
                    "messages = []\n\n"
                    "# TODO: loop over messages and print type(m).__name__ and m.content\n"
                ),
                "solution_code": (
                    "from langchain_core.messages import SystemMessage, HumanMessage, AIMessage\n\n"
                    "messages = [\n"
                    "    SystemMessage(content=\"You are a helpful math tutor.\"),\n"
                    "    HumanMessage(content=\"What is 12 * 8?\"),\n"
                    "    AIMessage(content=\"96\"),\n"
                    "]\n\n"
                    "for m in messages:\n"
                    "    print(type(m).__name__, \"->\", m.content)\n"
                ),
                "skill_tested": ["langgraph", "messages"],
            },
            {
                "title": "Chatbot node with add_messages",
                "description": (
                    "Build the full chatbot graph from the lesson: State using "
                    "`Annotated[list, add_messages]`, a `chatbot` node calling the LLM, wired "
                    "START → chatbot → END. Invoke it with a HumanMessage asking \"Explain "
                    "Python dictionaries.\" and print `result['messages']` to inspect the full "
                    "message list, confirming it contains both the HumanMessage and the "
                    "resulting AIMessage."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing import Annotated\n"
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.graph.message import add_messages\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n\n"
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n\n\n"
                    "def chatbot(state: State):\n"
                    "    # TODO: call llm.invoke(state['messages']) and return the update\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add_node/add_edge x2, compile, invoke, print messages\n"
                ),
                "solution_code": (
                    "from typing import Annotated\n"
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.graph.message import add_messages\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n\n"
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n\n\n"
                    "def chatbot(state: State):\n"
                    "    response = llm.invoke(state[\"messages\"])\n"
                    "    return {\"messages\": [response]}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"chatbot\", chatbot)\n"
                    "graph.add_edge(START, \"chatbot\")\n"
                    "graph.add_edge(\"chatbot\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\n"
                    "    \"messages\": [HumanMessage(content=\"Explain Python dictionaries.\")]\n"
                    "})\n"
                    "print(result[\"messages\"])\n"
                ),
                "skill_tested": ["langgraph", "messages", "add_messages"],
            },
        ],
        "quiz": {
            "title": "Messages in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What is the purpose of a SystemMessage?",
                    "options": [
                        "It represents the user's question",
                        "It represents the AI's response",
                        "It gives instructions/context to the AI",
                        "It logs errors from the graph",
                    ],
                    "correct": 2,
                    "explanation": "SystemMessage sets up instructions or persona for the AI, e.g. 'You are a helpful AI teacher.'",
                },
                {
                    "question": "Without using add_messages, what happens if a chatbot node returns {\"messages\": [response]} and the State field is just `messages: list`?",
                    "options": [
                        "The new message is automatically appended to the old list",
                        "The messages list gets replaced entirely by the new value returned, losing prior history",
                        "It raises a runtime error",
                        "Nothing changes in state",
                    ],
                    "correct": 1,
                    "explanation": "Without a reducer, LangGraph's default behavior is to overwrite the field with whatever the node returns, dropping earlier messages.",
                },
                {
                    "question": "What does Annotated[list, add_messages] tell LangGraph to do?",
                    "options": [
                        "Sort the messages alphabetically",
                        "Delete duplicate messages",
                        "Append new messages to the existing messages list instead of overwriting it",
                        "Convert messages into plain strings",
                    ],
                    "correct": 2,
                    "explanation": "add_messages is a reducer function that merges new messages into the existing list rather than replacing it.",
                },
                {
                    "question": "Why doesn't a second, separate app.invoke() call automatically know about a prior conversation?",
                    "options": [
                        "Because LangGraph forgets messages after 5 minutes",
                        "Because each invocation starts with a fresh state unless persistence/memory is added",
                        "Because add_messages disables memory",
                        "Because HumanMessage objects expire",
                    ],
                    "correct": 1,
                    "explanation": "Each call to invoke() begins with whatever initial state you pass in; without persistence, there's no link between separate invocations.",
                },
                {
                    "question": "Which message type represents the AI's own reply in a conversation?",
                    "options": [
                        "SystemMessage",
                        "HumanMessage",
                        "AIMessage",
                        "ToolMessage",
                    ],
                    "correct": 2,
                    "explanation": "AIMessage represents content generated by the assistant, as opposed to the user's HumanMessage or the SystemMessage's instructions.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Persona-Driven Q&A Logger",
            "description": (
                "Build a graph using `Annotated[list, add_messages]` state. Start every "
                "conversation with a SystemMessage giving the AI a specific persona of your "
                "choice (e.g. 'sarcastic pirate', 'strict grammar teacher'). Invoke the graph "
                "with 3 different HumanMessage questions (across 3 separate invocations, each "
                "starting fresh with the same SystemMessage + new question), and print the full "
                "resulting messages list each time, labeling each message with its type."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Use SystemMessage to establish a consistent AI persona",
                "Use add_messages correctly in the State definition",
                "Run the graph against 3 different questions",
                "Clearly print/label each message's role and content",
            ],
            "rubric": {
                "state_design": "State correctly uses Annotated[list, add_messages] (20%)",
                "persona": "SystemMessage clearly establishes a distinct, consistent persona (25%)",
                "chatbot_node": "chatbot node correctly calls the LLM and returns a message update (35%)",
                "output": "All 3 runs are shown with clearly labeled message types (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Building a Chatbot",
        "slug":              "building-a-chatbot",
        "description":       "Combine State, Nodes, Edges, Messages, and the LLM into a working chatbot graph — and understand the distinction between conversation history and persistent memory.",
        "order":             9,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "langchain", "chatbot", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Building a Chatbot",
            "content": """# 🤖 Lesson 9 — Build Your First LangGraph Chatbot

Now we're going to combine what you've learned: State, Nodes, Edges, Messages, LLM. Our
goal is a simple chatbot:

```
User
 ↓
HumanMessage
 ↓
Chatbot Node
 ↓
LLM
 ↓
AIMessage
 ↓
User
 ↓
...
```

## 1. What Makes This a Chatbot?

A normal LLM call, `llm.invoke("What is Python?")`, answers one question. A chatbot needs
conversation history:

```
User: What is Python?
AI: Python is a programming language.

User: What is it used for?
AI: It is used for web development, AI, automation...
```

The second question depends on the first answer. So we need:
`messages → [HumanMessage, AIMessage, HumanMessage, AIMessage, ...]`.

## 2. Our State

We'll use `add_messages`.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

The important part, `Annotated[list, add_messages]`, tells LangGraph: *"when new messages
arrive, add them to the existing messages."*

## 3. Create the LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
```

## 4. Create the Chatbot Node

```python
def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }
```

That's our entire AI node. The flow is: State → messages → LLM → AIMessage → State.

## 5–6. Build the Graph & Compile

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()
```

So: `START → chatbot → END`. Now our graph is ready.

## 7. Send a Message

```python
from langchain_core.messages import HumanMessage

result = app.invoke({
    "messages": [
        HumanMessage(content="What is LangGraph?")
    ]
})

print(result["messages"][-1].content)
```

The last message should be the AI's answer.

## 8. Complete Code

```python
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


# State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Chatbot Node
def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {"messages": [response]}


# Graph
graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


# Compile
app = graph.compile()


# Run
result = app.invoke({
    "messages": [HumanMessage(content="Explain LangGraph in simple words.")]
})

print(result["messages"][-1].content)
```

## 9. Let's Understand the Flow

Suppose the user asks "What is LangGraph?". The initial state has a single HumanMessage.
The chatbot node calls the LLM and produces an AIMessage. The final state's `messages`
contains both: `[HumanMessage, AIMessage]`.

## 10. But Is This Really a Chatbot?

Not quite yet — there's a problem. If we call `app.invoke(...)` and then invoke it again
separately, the graph doesn't automatically remember the first conversation. For example:

**First invocation:** User: "My name is Mohammad." → AI: "Nice to meet you!"

**Second invocation:** User: "What's my name?" → AI: "I don't know."

Why? Because each `invoke()` starts with a new state unless we add persistence. This brings
us to a very important LangGraph feature: **💾 Memory**.

## 11. Before Memory — Let's Make a Loop

A real chatbot conceptually does this:

```
          ┌──────────────┐
          │     User     │
          └──────┬───────┘
                 ↓
           HumanMessage
                 ↓
             Chatbot
                 ↓
             AIMessage
                 ↓
          ┌──────┴───────┐
          │              │
          ↓              │
       User again ───────┘
```

The graph needs to keep running. However, we don't want to create an infinite loop inside a
single `invoke()` call. Instead, the application can process one user message per
invocation, while persistent memory keeps the conversation history. That's what we'll learn
next.

## 🧠 Important Distinction

There are two different ideas:

**Conversation history** — `Human → AI → Human → AI`, i.e. the `messages` list.

**Persistent memory** — `Conversation 1 → Conversation 2 → Conversation 3`, i.e. this allows
the application to remember information across separate graph invocations.

So: **Messages = conversation data. Memory = persistence of that data.**

## 🧪 Exercise

Modify the chatbot's system instructions. Make it behave like a Python teacher — the AI
should explain concepts simply, give small examples, and avoid unnecessary complexity. You
can add a SystemMessage:

```python
from langchain_core.messages import SystemMessage
```

```python
SystemMessage(
    content="You are a friendly Python teacher. Explain concepts simply."
)
```

Your message history should look like: `SystemMessage → HumanMessage → AIMessage`.
""",
            "order": 9,
            "estimated_minutes": 50,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Add a Python-teacher persona",
                "description": (
                    "Modify the chatbot graph so every invocation starts with a SystemMessage: "
                    "\"You are a friendly Python teacher. Explain concepts simply.\" Invoke it "
                    "with a HumanMessage asking \"What is a list comprehension?\" and print the "
                    "AI's reply. Confirm the final messages list is "
                    "[SystemMessage, HumanMessage, AIMessage]."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from langchain_core.messages import SystemMessage, HumanMessage\n\n"
                    "# TODO: build the initial messages list with a SystemMessage persona\n"
                    "# followed by a HumanMessage question, then invoke the compiled chatbot\n"
                    "# app and print result['messages']\n"
                ),
                "solution_code": (
                    "from langchain_core.messages import SystemMessage, HumanMessage\n\n"
                    "result = app.invoke({\n"
                    "    \"messages\": [\n"
                    "        SystemMessage(content=\"You are a friendly Python teacher. Explain concepts simply.\"),\n"
                    "        HumanMessage(content=\"What is a list comprehension?\"),\n"
                    "    ]\n"
                    "})\n\n"
                    "print(result[\"messages\"][-1].content)\n"
                    "print(result[\"messages\"])  # [SystemMessage, HumanMessage, AIMessage]\n"
                ),
                "skill_tested": ["langgraph", "chatbot", "messages"],
            },
            {
                "title": "Demonstrate the 'no memory' problem",
                "description": (
                    "Using the chatbot graph from the lesson, run two SEPARATE invocations: "
                    "first with HumanMessage(\"My name is Mohammad.\"), then with "
                    "HumanMessage(\"What's my name?\"). Print both AI responses, and in a "
                    "comment explain why the second response can't correctly answer the "
                    "question given how the graph is currently built."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# TODO: first invocation with 'My name is Mohammad.'\n"
                    "# TODO: second, SEPARATE invocation with \"What's my name?\"\n"
                    "# TODO: print both AI responses\n"
                    "# TODO: comment explaining why the second call doesn't know the name\n"
                ),
                "solution_code": (
                    "result1 = app.invoke({\"messages\": [HumanMessage(content=\"My name is Mohammad.\")]})\n"
                    "print(result1[\"messages\"][-1].content)\n\n"
                    "result2 = app.invoke({\"messages\": [HumanMessage(content=\"What's my name?\")]})\n"
                    "print(result2[\"messages\"][-1].content)\n\n"
                    "# The second call can't know the name because each app.invoke() call\n"
                    "# starts from the initial state passed to it -- result2's starting\n"
                    "# messages list only contains the new HumanMessage, with no reference\n"
                    "# to result1's conversation. Without persistence/memory (a later lesson),\n"
                    "# the two invocations are completely independent.\n"
                ),
                "skill_tested": ["langgraph", "chatbot", "state"],
            },
        ],
        "quiz": {
            "title": "Building a Chatbot — Quiz",
            "questions": [
                {
                    "question": "What makes a chatbot different from a single llm.invoke() call?",
                    "options": [
                        "Chatbots use a different programming language",
                        "A chatbot needs to track conversation history so later questions can depend on earlier answers",
                        "Chatbots never use LangGraph",
                        "There is no real difference",
                    ],
                    "correct": 1,
                    "explanation": "A chatbot's later replies often depend on earlier context, which requires tracking the growing messages list.",
                },
                {
                    "question": "In the chatbot node, what does llm.invoke(state['messages']) receive?",
                    "options": [
                        "A single string",
                        "The full list of prior messages (system/human/AI) so far",
                        "Just the most recent AIMessage",
                        "An empty list",
                    ],
                    "correct": 1,
                    "explanation": "Passing the whole messages list lets the LLM see the full conversation context, not just the latest message.",
                },
                {
                    "question": "Why doesn't the chatbot remember a user's name across two separate app.invoke() calls?",
                    "options": [
                        "Because add_messages disables memory",
                        "Because each invoke() call starts fresh with whatever initial state is passed to it, with no built-in persistence between calls",
                        "Because names aren't supported message content",
                        "Because the LLM has no memory feature",
                    ],
                    "correct": 1,
                    "explanation": "Without adding checkpoints/persistence, each invocation is independent, so information from a prior call isn't automatically available.",
                },
                {
                    "question": "What's the key difference between 'conversation history' and 'persistent memory' as described in the lesson?",
                    "options": [
                        "They are exactly the same thing",
                        "Conversation history is the messages list within one invocation; persistent memory lets information carry across separate invocations",
                        "Conversation history only applies to SystemMessage",
                        "Persistent memory replaces the need for messages entirely",
                    ],
                    "correct": 1,
                    "explanation": "Messages track the back-and-forth within a run, while memory is what would let the app recall things across multiple separate runs.",
                },
                {
                    "question": "Why does the lesson avoid building a real infinite conversation loop inside a single invoke() call?",
                    "options": [
                        "Because LangGraph doesn't support loops",
                        "Because we don't want the graph to run forever inside one invocation; instead, the app processes one message per invocation while memory (a later topic) handles continuity",
                        "Because loops are only used for counters",
                        "Because chatbots don't need loops at all",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly notes we don't want an infinite loop inside a single invoke() call, and points to persistent memory as the right solution, covered next.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Multi-Turn Chat Simulator (No Memory Yet)",
            "description": (
                "Build the full chatbot graph with a SystemMessage persona of your choice. "
                "Simulate a 3-turn conversation by manually carrying the growing messages list "
                "yourself between invocations (i.e. take the previous result's messages list "
                "and pass it back in as the starting point for the next invoke() call, adding "
                "one new HumanMessage each time). Print the full message history after each "
                "turn to show the conversation building up correctly, even without built-in "
                "persistence."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Build a working chatbot graph with add_messages",
                "Establish a persona via SystemMessage",
                "Manually chain 3 turns of conversation by reusing prior state",
                "Demonstrate why this manual approach is clunky, motivating the next lesson on memory",
            ],
            "rubric": {
                "chatbot_graph": "Chatbot graph is built correctly with add_messages (25%)",
                "persona": "SystemMessage establishes and maintains a consistent persona (15%)",
                "manual_chaining": "Each new invocation correctly reuses the previous result's messages plus one new HumanMessage (40%)",
                "output": "All 3 turns are printed clearly, showing history growing correctly (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Tools in LangGraph",
        "slug":              "tools-in-langgraph",
        "description":       "What a tool is, the @tool decorator, binding tools to an LLM with bind_tools, and how tool calls (request vs execution) set up the agent loop.",
        "order":             10,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "langchain", "tools", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Tools in LangGraph",
            "content": """# 🔧 Lesson 10 — Tools in LangGraph

Now we reach one of the most important concepts for AI agents: **Tools**. Until now, our LLM
could only generate text. With tools, it can do things.

## 1. What Is a Tool?

A tool is simply a function that an AI can use.

```python
def add(a, b):
    return a + b
```

This function is a tool. The AI could decide: *"I need to calculate 25 × 4."* → Use
calculator → `100`.

## 2. LLM vs Tool

An LLM is good at: explaining, reasoning, writing, summarizing, understanding language. But
tools are good at actually performing specific operations: Calculator → exact arithmetic,
Search → retrieve information, Database → get records, API → communicate with another
service, Python → execute calculations/code.

So: **LLM = Brain 🧠, Tool = Ability 🔧**

## 3. Simple Python Tool

Let's start without LangGraph.

```python
def add(a: int, b: int) -> int:
    return a + b

result = add(10, 20)
print(result)  # 30
```

That's a tool in its simplest form.

## 4. Turn It Into a LangChain Tool

LangChain provides a `@tool` decorator.

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers together.\"\"\"
    return a + b
```

Now `add` is a proper LangChain tool.

## 5. Why the Description Matters

Notice the docstring `\"\"\"Add two numbers together.\"\"\"` — this is important. The LLM
uses the tool's name, description, and arguments to understand when it should use the tool.
So when the user asks *"What is 20 + 30?"*, the model may decide: use `add`, `a=20`,
`b=30`.

## 6. Another Tool

```python
@tool
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers together.\"\"\"
    return a * b
```

Now we have `add` and `multiply`.

## 7. Our AI System

Eventually, we want:

```
                 User
                   ↓
                  LLM
                   ↓
             Need a tool?
              ↙       ↘
            YES        NO
             ↓          ↓
           Tool       Answer
             ↓
            Result
             ↓
            LLM
             ↓
          Answer
```

This is the basic architecture of a tool-using agent.

## 8. Binding Tools to the LLM

Now comes an important LangChain concept — we can give the tools to the LLM:

```python
tools = [add, multiply]

llm_with_tools = llm.bind_tools(tools)
```

This tells the model: *"These tools are available to you."* But there's an important
distinction: **binding a tool does NOT execute the tool.** It only makes the LLM aware that
the tool exists and allows it to request the tool.

## 9. What Happens When the User Asks a Math Question?

Suppose the user asks *"What is 10 × 20?"*. The LLM might produce a message containing a
tool call:

```
AIMessage
tool_calls:
    name = multiply
    args = {"a": 10, "b": 20}
```

The LLM hasn't calculated it itself. It has said: *"Please execute the multiply tool with
these arguments."*

## 10. Tool Execution

Our application then executes `multiply(10, 20)` → `200`. Then the result is sent back to
the LLM:

```
User → LLM → Tool Call → multiply(10, 20) → 200 → LLM → "The answer is 200."
```

This is the basic tool-calling loop.

## 11. Why LangGraph Is Perfect for This

Look at the workflow:

```
START
  ↓
LLM
  ↓
Tool needed?
 ↙       ↘
NO       YES
 ↓        ↓
END      Tool
          ↓
          LLM
          ↓
       Tool needed?
        ↙       ↘
      NO        YES
       ↓         ↓
      END       Tool
```

Notice something? It's a loop. You already learned loops in Lesson 6. So the concepts are
coming together:

```
State + Messages + LLM + Tools + Conditional Edges + Loops = AI Agent
```

🔥 This is the core idea.

## 12. LangGraph Has a ToolNode

Instead of manually executing every tool, LangGraph provides:

```python
from langgraph.prebuilt import ToolNode
```

`ToolNode` can execute tool calls produced by the LLM. This makes agent construction much
easier. Conceptually: `LLM Node → ToolNode → LLM Node`.

## 13. The Architecture

A simple tool-using graph looks like:

```
                 START
                   ↓
              ┌─────────┐
              │   LLM   │
              └────┬────┘
                   ↓
             Need a tool?
               ↙     ↘
             NO       YES
              ↓         ↓
             END     ToolNode
                        ↓
                       LLM
                        ↓
                  Need another tool?
                    ↙        ↘
                  NO          YES
                   ↓            ↓
                  END        ToolNode
```

This is basically the architecture we'll use to build an agent.

## 14. Important New Concept: Tool Calls

You'll frequently see `message.tool_calls`, for example `if message.tool_calls: ...`. This
checks whether the AI requested a tool. A tool call contains: tool name, arguments, tool
call ID. Conceptually: `{"name": "multiply", "args": {"a": 10, "b": 20}}`.

## 15. Why Tool Calling Is Powerful

Imagine an academic advisor RAG project. Your AI could have tools like `search_courses()`,
`search_regulations()`, `calculate_gpa()`, `calculate_tuition()`. Then:

```
Student: What is my GPA if I get A in these courses?
       ↓
      LLM
       ↓
Needs GPA calculation
       ↓
  calculate_gpa()
       ↓
    Result
       ↓
      LLM
       ↓
 Final answer
```

Or: *"How many credits is CSE 251?"* → LLM → `search_courses()` → Course information → LLM
→ Answer. This is exactly the direction you'll eventually use for sophisticated AI systems.

## 🧠 Don't Memorize the Code Yet

At this stage, focus on the concept: **Tool = function the AI can use**, and:

```
LLM → requests tool → Tool executes → result → LLM
```

That's the important part.

## 🧪 Mini Exercise

Create these two tools:

```python
@tool
def subtract(a: int, b: int) -> int:
    \"\"\"Subtract b from a.\"\"\"
    return a - b
```

```python
@tool
def divide(a: float, b: float) -> float:
    \"\"\"Divide a by b.\"\"\"
    return a / b
```

Then:

```python
tools = [add, multiply, subtract, divide]
```

Try to understand what information the LLM would need to decide which tool to use.

## ⚠️ One Important Thing

Don't confuse `llm.invoke(...)` with `llm.bind_tools(...)`.

- **invoke** actually sends the messages to the model: `response = llm.invoke(messages)`
- **bind_tools** makes tools available to the model: `llm_with_tools = llm.bind_tools(tools)`

Usually you'll use both: `bind_tools` → LLM knows about tools → `invoke` → LLM may request
a tool.
""",
            "order": 10,
            "estimated_minutes": 55,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Write subtract and divide tools",
                "description": (
                    "Using the @tool decorator, write `subtract(a, b)` (returns a - b) and "
                    "`divide(a, b)` (returns a / b, both floats), each with a clear one-line "
                    "docstring the LLM could use to decide when to call them. Combine them with "
                    "add and multiply into a single `tools` list, and print each tool's `.name` "
                    "and `.description` attribute to confirm they're registered correctly."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "from langchain_core.tools import tool\n\n\n"
                    "@tool\n"
                    "def subtract(a: int, b: int) -> int:\n"
                    "    # TODO: docstring + return a - b\n"
                    "    pass\n\n\n"
                    "@tool\n"
                    "def divide(a: float, b: float) -> float:\n"
                    "    # TODO: docstring + return a / b\n"
                    "    pass\n\n\n"
                    "# TODO: build tools list and print each tool's name + description\n"
                ),
                "solution_code": (
                    "from langchain_core.tools import tool\n\n\n"
                    "@tool\n"
                    "def subtract(a: int, b: int) -> int:\n"
                    "    \"\"\"Subtract b from a.\"\"\"\n"
                    "    return a - b\n\n\n"
                    "@tool\n"
                    "def divide(a: float, b: float) -> float:\n"
                    "    \"\"\"Divide a by b.\"\"\"\n"
                    "    return a / b\n\n\n"
                    "tools = [subtract, divide]\n"
                    "for t in tools:\n"
                    "    print(t.name, \"->\", t.description)\n"
                ),
                "skill_tested": ["langgraph", "tools", "langchain"],
            },
            {
                "title": "Bind tools and inspect a request",
                "description": (
                    "Bind a list of tools (add, multiply, subtract, divide) to an LLM using "
                    "`bind_tools`. Send a HumanMessage asking \"What is 45 divided by 9?\" and "
                    "print `response.tool_calls`. In a comment, explain why `response.content` "
                    "might be empty even though the model 'answered' the question."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.messages import HumanMessage\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n"
                    "# TODO: llm_with_tools = llm.bind_tools([...])\n"
                    "# TODO: invoke with HumanMessage('What is 45 divided by 9?')\n"
                    "# TODO: print response.tool_calls\n"
                    "# TODO: comment explaining why response.content may be empty\n"
                ),
                "solution_code": (
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.messages import HumanMessage\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n"
                    "llm_with_tools = llm.bind_tools([add, multiply, subtract, divide])\n\n"
                    "response = llm_with_tools.invoke([\n"
                    "    HumanMessage(content=\"What is 45 divided by 9?\")\n"
                    "])\n\n"
                    "print(response.tool_calls)\n"
                    "# response.content is often empty because the model chose to REQUEST a\n"
                    "# tool call (divide, a=45, b=9) instead of writing a text answer itself.\n"
                    "# It hasn't computed anything yet -- it's asking the application to run\n"
                    "# the divide() function and give it the result before it produces a\n"
                    "# final natural-language answer.\n"
                ),
                "skill_tested": ["langgraph", "tools", "bind_tools"],
            },
        ],
        "quiz": {
            "title": "Tools in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What is a 'tool' in the LangChain/LangGraph sense?",
                    "options": [
                        "A separate LLM model",
                        "A function the AI can request to be executed, decorated with @tool",
                        "A type of conditional edge",
                        "A special kind of State field",
                    ],
                    "correct": 1,
                    "explanation": "A tool is simply a Python function, wrapped with @tool, that the LLM can decide to call.",
                },
                {
                    "question": "Why does the tool's docstring matter?",
                    "options": [
                        "It has no effect on behavior, it's just documentation",
                        "The LLM uses the tool's name, description, and arguments to decide when and how to use it",
                        "It determines the tool's execution speed",
                        "It's required only for Python's own documentation tools",
                    ],
                    "correct": 1,
                    "explanation": "The description tells the model what the tool does, which is essential for the model to choose the right tool for a given request.",
                },
                {
                    "question": "What does llm.bind_tools(tools) actually do?",
                    "options": [
                        "It immediately executes all the tools",
                        "It makes the LLM aware that these tools exist and can be requested, without executing anything",
                        "It replaces llm.invoke() entirely",
                        "It converts tools into messages",
                    ],
                    "correct": 1,
                    "explanation": "Binding only informs the model of available tools; it does not run them. Execution is a separate step the application performs.",
                },
                {
                    "question": "When the LLM 'calls' a tool, who actually runs the underlying Python function?",
                    "options": [
                        "The LLM itself, internally",
                        "The tool runs automatically the moment bind_tools is called",
                        "The application/LangGraph executes the function based on the LLM's tool_calls request",
                        "The user must manually type the function call",
                    ],
                    "correct": 2,
                    "explanation": "The LLM only produces a tool_calls request (name + args); LangGraph's ToolNode or your own code actually executes the Python function.",
                },
                {
                    "question": "Why is this tool-use pattern naturally a loop, as described in the lesson?",
                    "options": [
                        "Because Python functions are always loops",
                        "Because after a tool executes, the result goes back to the LLM, which may decide it needs yet another tool before finally answering",
                        "Because bind_tools requires exactly 2 calls",
                        "It isn't a loop, it always executes exactly one tool",
                    ],
                    "correct": 1,
                    "explanation": "LLM -> tool? -> execute -> LLM -> tool? -> ... continues until the LLM decides no more tools are needed, which is the loop pattern from Lesson 6.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Four-Function Calculator Toolkit",
            "description": (
                "Build a set of four tools (add, subtract, multiply, divide) using @tool, each "
                "with a clear docstring. Bind all four to an LLM with bind_tools. Send at least "
                "4 different math questions (one per operation) as separate llm_with_tools "
                "invocations, and for each, print the resulting response.tool_calls to confirm "
                "the model picked the correct tool and arguments every time."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangChain", "OpenAI"],
            "objectives": [
                "Define 4 well-documented tools using the @tool decorator",
                "Bind all tools to an LLM with bind_tools",
                "Send multiple test questions covering each operation",
                "Verify tool_calls output matches the expected tool/arguments for each question",
            ],
            "rubric": {
                "tool_definitions": "All 4 tools are correctly defined with clear docstrings (35%)",
                "binding": "Tools are correctly bound to the LLM via bind_tools (15%)",
                "testing": "At least 4 distinct test questions are run, one per operation (30%)",
                "verification": "tool_calls output is printed and correctly matches expectations for each test (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Tool Calling",
        "slug":              "tool-calling",
        "description":       "Wire up a complete tool-calling loop with ToolNode and a should_continue routing function — the core architecture behind LangGraph agents.",
        "order":             11,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["langgraph", "langchain", "tool-calling", "agents", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Tool Calling",
            "content": """# 🔁 Lesson 11 — Tool Calling

Now we're going to connect everything we've learned. The goal is to build this:

```
User
 ↓
LLM
 ↓
Does it need a tool?
 ↓ YES
Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

This is the basic pattern behind many AI agents.

## 1. Tool vs Tool Calling

First, an important distinction.

**Tool** — a function:

```python
@tool
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b
```

**Tool calling** — the LLM decides to use that tool.

```
User: What is 25 + 17?
       ↓
LLM: I should use the add tool.
       ↓
Tool: add(25, 17)
       ↓
      42
       ↓
LLM: The answer is 42.
```

## 2. Create Our Tool

Let's start with a calculator.

```python
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers together.\"\"\"
    return a * b
```

Test it:

```python
print(multiply.invoke({"a": 5, "b": 10}))  # 50
```

## 3. Give the Tool to the LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

llm_with_tools = llm.bind_tools([multiply])
```

Now the LLM knows that `multiply` is available.

## 4. Send a Question

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(content="What is 12 multiplied by 8?")

response = llm_with_tools.invoke([message])
```

Now inspect `print(response)`. You may see an AIMessage containing a tool call.
Conceptually: `AIMessage content: "" tool_calls: multiply a=12 b=8`. The important part is
`response.tool_calls`.

## 5. Inspect the Tool Call

```python
print(response.tool_calls)
```

Conceptually you'll get something similar to:

```python
[{"name": "multiply", "args": {"a": 12, "b": 8}, "id": "..."}]
```

Don't worry about the exact ID. The important information is `name → multiply`,
`args → a=12, b=8`.

## 🧠 Important Concept

The LLM doesn't execute the Python function itself. It says: *"I want to call multiply with
these arguments."* Then your application executes the tool. This distinction is extremely
important.

## 6. ToolNode

LangGraph gives us a convenient component:

```python
from langgraph.prebuilt import ToolNode

tools = [multiply]

tool_node = ToolNode(tools)
```

Now LangGraph knows how to execute the tool calls.

## 7. Our Graph

We want:

```
START
  ↓
  LLM
  ↓
Tool requested?
 ↙       ↘
NO       YES
 ↓         ↓
END      Tool
          ↓
         LLM
```

This requires a conditional edge — you've already learned conditional edges!

## 8. Create the State

We'll use messages:

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

## 9. Create the LLM Node

```python
def chatbot(state: State):

    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}
```

Notice we're using `llm_with_tools` instead of `llm`, because we want the model to be able
to request tools.

## 10. Create the Tool Node

```python
tool_node = ToolNode([multiply])
```

This node executes tool calls.

## 11. Create the Routing Function

We need to ask: *does the LLM want to use a tool?*

```python
def should_continue(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

This is very important. The last message is the AI response. If it contains
`last_message.tool_calls`, then the AI requested a tool.

## 12. Build the Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chatbot")

graph.add_conditional_edges(
    "chatbot",
    should_continue,
    {"tools": "tools", "end": END}
)

graph.add_edge("tools", "chatbot")
```

That last edge creates our loop.

## 13. Visualize the Graph

Our graph is:

```
                  ┌──────────┐
                  │  Tools   │
                  └────┬─────┘
                       │
                       ↓
START → Chatbot → Tool? → Chatbot
            │
            ↓
           END
```

## 14. Complete Code

```python
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# -------------------------
# Tool
# -------------------------
@tool
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers together.\"\"\"
    return a * b


tools = [multiply]
tool_node = ToolNode(tools)


# -------------------------
# LLM
# -------------------------
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# -------------------------
# State
# -------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]


# -------------------------
# Chatbot Node
# -------------------------
def chatbot(state: State):

    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


# -------------------------
# Routing Function
# -------------------------
def should_continue(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


# -------------------------
# Graph
# -------------------------
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chatbot")

graph.add_conditional_edges(
    "chatbot",
    should_continue,
    {"tools": "tools", "end": END}
)

graph.add_edge("tools", "chatbot")


# -------------------------
# Compile
# -------------------------
app = graph.compile()


# -------------------------
# Run
# -------------------------
result = app.invoke({
    "messages": [HumanMessage(content="What is 12 multiplied by 8?")]
})

print(result["messages"][-1].content)
```

The final answer should be something like: *"12 multiplied by 8 is 96."*

## 🧠 Let's Follow the Execution

This is the most important part of today's lesson.

User asks *"What is 12 × 8?"*

1. Graph starts: `START → Chatbot`
2. LLM sees the available tool `multiply(a, b)` and decides: *"I need multiply."*
3. The LLM produces a tool call: `multiply a=12 b=8`
4. Our routing function sees `last_message.tool_calls`, so it returns `"tools"`
5. LangGraph goes to `ToolNode`. The tool executes `multiply(12, 8)` → `96`
6. The result goes back to the chatbot: `Tools → Chatbot`
7. The LLM now sees the tool result and generates: *"12 × 8 = 96."*
8. There are no more tool calls, so `Chatbot → END`

## 🔥 You Just Built the Core of an AI Agent

Look at what you've created:

```
                ┌──────────────┐
                │     LLM      │
                └──────┬───────┘
                       ↓
                 Need a tool?
                  ↙        ↘
                NO          YES
                ↓             ↓
               END         ToolNode
                              ↓
                             LLM
                              ↓
                       Need another tool?
                         ↙          ↘
                       NO            YES
                        ↓              ↓
                       END         ToolNode
```

This is essentially an agent loop.

## 🧠 One Very Important Pattern

Memorize this pattern:

```python
def should_continue(state):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

This pattern appears in many LangGraph agent implementations. The idea is: AI wants tool? →
YES → Tool, NO → END.

## 🧪 Exercise

Add another tool:

```python
@tool
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers together.\"\"\"
    return a + b
```

Then `tools = [add, multiply]`. Now test *"What is 20 + 30?"* and *"What is 7 multiplied by
9?"* — the LLM should choose the appropriate tool.

## 🎯 The Architecture You Should Remember

```
State → Messages → LLM → Tool Call → ToolNode → Tool Result → LLM → Final Answer
```

And the LangGraph pieces are:

| Concept | LangGraph |
|---|---|
| Shared data | State |
| AI | LLM node |
| Tool execution | ToolNode |
| Decision | Conditional edge |
| Repeating | Loop |
| Conversation | Messages |
""",
            "order": 11,
            "estimated_minutes": 65,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Add a second tool and re-run should_continue",
                "description": (
                    "Extend the complete example with an `add` tool alongside `multiply`, bound "
                    "together via `llm.bind_tools([add, multiply])` and passed to `ToolNode`. "
                    "Invoke the compiled graph with two separate questions -- \"What is 20 + "
                    "30?\" and \"What is 7 multiplied by 9?\" -- and print the final answer for "
                    "each, confirming the model picked the right tool both times."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "@tool\n"
                    "def add(a: int, b: int) -> int:\n"
                    "    # TODO: docstring + return a + b\n"
                    "    pass\n\n\n"
                    "# TODO: tools = [add, multiply]; rebuild tool_node and llm_with_tools\n"
                    "# TODO: reuse the graph from the lesson (chatbot/tools/should_continue)\n"
                    "# TODO: invoke with 'What is 20 + 30?' and print final answer\n"
                    "# TODO: invoke with 'What is 7 multiplied by 9?' and print final answer\n"
                ),
                "solution_code": (
                    "@tool\n"
                    "def add(a: int, b: int) -> int:\n"
                    "    \"\"\"Add two numbers together.\"\"\"\n"
                    "    return a + b\n\n\n"
                    "tools = [add, multiply]\n"
                    "tool_node = ToolNode(tools)\n"
                    "llm_with_tools = llm.bind_tools(tools)\n\n"
                    "# (chatbot, should_continue, and graph wiring stay the same as the lesson,\n"
                    "#  just referencing the updated tools/llm_with_tools/tool_node)\n\n"
                    "app = graph.compile()\n\n"
                    "r1 = app.invoke({\"messages\": [HumanMessage(content=\"What is 20 + 30?\")]})\n"
                    "print(r1[\"messages\"][-1].content)  # ...50...\n\n"
                    "r2 = app.invoke({\"messages\": [HumanMessage(content=\"What is 7 multiplied by 9?\")]})\n"
                    "print(r2[\"messages\"][-1].content)  # ...63...\n"
                ),
                "skill_tested": ["langgraph", "tool-calling", "toolnode"],
            },
            {
                "title": "Trace tool calls across the loop",
                "description": (
                    "Add a print statement inside `should_continue` that logs whether it's "
                    "routing to \"tools\" or \"end\" each time it's called. Invoke the graph with "
                    "a question that requires a tool (e.g. \"What is 15 * 6?\") and observe how "
                    "many times should_continue runs before the loop ends. In a comment, explain "
                    "why should_continue runs more than once for a single user question."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "def should_continue(state: State):\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    # TODO: print whether routing to 'tools' or 'end'\n"
                    "    if last_message.tool_calls:\n"
                    "        return \"tools\"\n"
                    "    return \"end\"\n\n"
                    "# TODO: invoke with a math question and observe the printed trace\n"
                    "# TODO: comment explaining why should_continue runs more than once\n"
                ),
                "solution_code": (
                    "def should_continue(state: State):\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    if last_message.tool_calls:\n"
                    "        print(\"should_continue -> tools\")\n"
                    "        return \"tools\"\n"
                    "    print(\"should_continue -> end\")\n"
                    "    return \"end\"\n\n"
                    "app.invoke({\"messages\": [HumanMessage(content=\"What is 15 * 6?\")]})\n\n"
                    "# should_continue runs once right after the FIRST chatbot call (routes to\n"
                    "# 'tools' because the LLM requested multiply), and again after the SECOND\n"
                    "# chatbot call once the tool result has been folded back in -- this time it\n"
                    "# routes to 'end' because the LLM has no more tool calls to make. That's\n"
                    "# the tools -> chatbot loop edge in action.\n"
                ),
                "skill_tested": ["langgraph", "tool-calling", "loops"],
            },
        ],
        "quiz": {
            "title": "Tool Calling — Quiz",
            "questions": [
                {
                    "question": "What does last_message.tool_calls being non-empty indicate?",
                    "options": [
                        "The tool has already been executed",
                        "The AI message includes a request to call one or more tools",
                        "The graph has reached END",
                        "There was an error in the LLM call",
                    ],
                    "correct": 1,
                    "explanation": "tool_calls holds the tool name(s) and arguments the LLM wants to invoke, checked by should_continue to decide routing.",
                },
                {
                    "question": "What does ToolNode do?",
                    "options": [
                        "It calls the LLM",
                        "It executes the tool call(s) requested by the LLM and returns the result(s) as messages",
                        "It defines the State schema",
                        "It compiles the graph",
                    ],
                    "correct": 1,
                    "explanation": "ToolNode is a prebuilt LangGraph node that runs whichever tools the LLM's tool_calls asked for.",
                },
                {
                    "question": "Why does graph.add_edge(\"tools\", \"chatbot\") matter?",
                    "options": [
                        "It ends the graph immediately after a tool runs",
                        "It sends the tool's result back to the LLM so it can produce a final (or next) response — this is what creates the loop",
                        "It's optional and has no real effect",
                        "It skips the chatbot node entirely",
                    ],
                    "correct": 1,
                    "explanation": "Without this edge, the tool's result would never reach the LLM again, and the LLM couldn't use it to finish answering.",
                },
                {
                    "question": "In the should_continue pattern, what happens once the LLM's response has no tool_calls?",
                    "options": [
                        "The graph errors out",
                        "It routes to 'end', ending the graph because no more tools are needed",
                        "It automatically calls another tool anyway",
                        "It restarts from START",
                    ],
                    "correct": 1,
                    "explanation": "An empty tool_calls means the LLM is ready to give its final answer, so should_continue returns 'end' and the graph finishes.",
                },
                {
                    "question": "Why is llm_with_tools used inside the chatbot node instead of the plain llm?",
                    "options": [
                        "llm_with_tools is faster",
                        "Only llm_with_tools is aware of the available tools and can produce tool_calls; the plain llm cannot request tools",
                        "There's no difference between them",
                        "llm_with_tools skips the need for a State",
                    ],
                    "correct": 1,
                    "explanation": "bind_tools() is what equips the model with knowledge of the tools, enabling it to emit tool_calls when appropriate.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Multi-Step Tool-Calling Agent",
            "description": (
                "Build the complete chatbot + ToolNode + should_continue graph with 4 tools "
                "(add, subtract, multiply, divide). Test it with a question that requires only "
                "one tool call (\"What is 8 * 7?\"), and with a two-part question that might "
                "trigger the loop twice (\"What is 5 + 3, and then multiply that result by "
                "2?\"). Print the full messages list for the second case to show the sequence of "
                "AIMessage tool requests and ToolMessage results leading to the final answer."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Assemble the full tool-calling graph (chatbot, tools, conditional routing, loop-back edge)",
                "Register 4 tools and bind them to the LLM",
                "Test both single-tool-call and potentially multi-tool-call scenarios",
                "Inspect and explain the full messages list produced by a multi-step run",
            ],
            "rubric": {
                "graph_wiring": "chatbot/tools nodes and edges (including the loop-back edge) are correctly wired (35%)",
                "tools": "All 4 tools are correctly defined and bound (20%)",
                "single_call_test": "Single-tool question is tested and produces a correct answer (20%)",
                "multi_call_test": "Multi-step question is tested, with the full message trace printed and explained (25%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Agents in LangGraph",
        "slug":              "agents-in-langgraph",
        "description":       "What an AI agent actually is (LLM + Tools + State + Decisions + Loop), the agent loop, ReAct, and when to use an agent vs. a fixed workflow.",
        "order":             12,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "agents", "react", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Agents in LangGraph",
            "content": """# 🤖 Lesson 12 — Agents in LangGraph

You've now learned almost all the pieces needed to understand an AI Agent. Let's put them
together.

## 1. What Is an AI Agent?

The simplest definition: **an AI agent is an LLM that can decide what action to take, use
tools, observe the results, and continue until it can answer the user.**

```
User
 ↓
LLM
 ↓
"Do I need a tool?"
 ↓
YES
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
"Do I need another tool?"
 ↓
YES
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

The important word is **decide** — the LLM decides what to do next.

## 2. Normal LLM vs Agent

**Normal LLM:** `Question → LLM → Answer`. The LLM simply responds.

**Agent:**

```
Question
   ↓
LLM
   ↓
Think about what to do
   ↓
Choose tool
   ↓
Tool
   ↓
Observe result
   ↓
Think again
   ↓
Choose another action
   ↓
...
   ↓
Final Answer
```

The agent has a loop.

## 3. You Already Built an Agent!

Remember Lesson 11? You created:

```
                 ┌──────────┐
                 │   LLM    │
                 └────┬─────┘
                      ↓
                Tool needed?
                 ↙       ↘
               NO         YES
               ↓            ↓
              END        ToolNode
                            ↓
                            ↓
                           LLM
                            ↓
                          ...
```

That's the fundamental structure of a tool-using agent. So don't think an agent is
something magical. It's basically: **LLM + Tools + Decision + Loop + State**.

## 4. The Agent Loop

This is the most important diagram of today's lesson:

```
             ┌─────────────┐
             │     User    │
             └──────┬──────┘
                    ↓
             ┌─────────────┐
             │     LLM     │
             └──────┬──────┘
                    ↓
              What should I do?
                 ↙       ↘
              Answer     Tool
                ↓          ↓
               END      Tool Result
                            ↓
                           LLM
                            ↓
                       What next?
```

The agent repeatedly cycles through **Think → Act → Observe → Think → Act → Observe.** This
is often called the agent loop.

## 5. Example: Calculator Agent

Suppose the user asks *"What is 20 × 5 + 10?"*. The agent might do:

```
User → LLM → Use multiply → multiply(20, 5) → 100
   → LLM → Use add → add(100, 10) → 110
   → LLM → Final answer: 110
```

Notice that the agent used two tools. That's something a simple one-step LLM call doesn't
automatically do.

## 6. The Agent Needs State

At minimum, the agent needs `messages`:

```
H: What is 20 × 5 + 10?
AI: I'll calculate 20 × 5.
Tool: 100
AI: Now I'll add 10.
Tool: 110
AI: The answer is 110.
```

All of these messages are part of the agent's state.

## 7. The Agent Needs Tools

```python
@tool
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers.\"\"\"
    return a * b
```

The agent can choose between them.

## 8. The Agent Needs a Decision

```python
if last_message.tool_calls:
    return "tools"

return "end"
```

This is the decision mechanism: tool call? YES → Tool, NO → END.

## 9. The Agent Needs a Loop

After the tool runs:

```python
graph.add_edge("tools", "chatbot")
```

This sends the result back to the LLM. So: `LLM → Tool → LLM → Tool → LLM → END`. That's the
agent loop.

## 10. Modern LangGraph Agent Creation

LangGraph provides higher-level APIs that can build much of this agent structure for you.
Depending on the LangGraph version you're using, you'll encounter APIs such as
`create_react_agent` or newer agent-building patterns. The important thing is not to
memorize the helper function — you should understand what happens underneath:

```
Agent
 ├── State
 ├── Messages
 ├── LLM
 ├── Tools
 ├── Tool execution
 ├── Conditional routing
 └── Loop
```

If you understand those pieces, you can understand the higher-level APIs.

## 11. ReAct

You may hear the word **ReAct** — it stands for **Reasoning + Acting**. The basic idea is:

```
Reason → Act → Observe → Reason → Act → Observe
```

For example: *"What is the population of Egypt?"* → Agent: *"I need current information."*
→ Search Tool → Search Result → Agent: *"Now I can answer."* → Final Answer.

## 12. Don't Confuse Agent With LLM

This is very important. An LLM by itself: `LLM → Text`. An agent:

```
LLM → Decision → Tool → Observation → LLM → Decision → ...
```

So: **the LLM is the brain inside the agent, not the entire agent.**

## 13. Your First Conceptual Agent

Imagine our academic advisor AI. The user asks *"How many credits do I need to graduate?"*.
The agent might do: `User → LLM → Need university regulations? → YES →
search_regulations() → Retrieved information → LLM → Answer`.

Another question, *"Calculate my GPA,"* could do: `User → LLM → Need GPA calculator? → YES
→ calculate_gpa() → Result → LLM → Answer`.

Another, *"Hello,"* the agent may simply do: `User → LLM → No tool needed → Answer`. That's
the power of agents.

## 14. Agent vs Workflow

This distinction is extremely important.

**Workflow** — you decide the path: `Question → Retrieve → Generate → Answer`. The
programmer controls the flow.

**Agent** — the LLM helps decide:

```
Question
 ↓
LLM
 ↓
What should I do?
 ↙      ↓       ↘
Search  Calc   Answer
```

The model has more control over the path.

## ⭐ When Should You Use Which?

Use a **workflow** when you know exactly what should happen, e.g.
`Question → Retrieve → Rerank → Generate`. Use an **agent** when the system needs to decide
dynamically, e.g. *should I search? should I calculate? should I call an API? should I ask
the user?*

## 15. The Big Picture

```
                 LangGraph
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     State         Nodes        Edges
       │            │            │
       └────────────┼────────────┘
                    ↓
                   LLM
                    ↓
                  Tools
                    ↓
             Conditional Logic
                    ↓
                  Loops
                    ↓
                  Agent
```

This is the foundation.

## 🧪 Mini Exercise

Imagine you're building a shopping assistant. Available tools: `search_products()`,
`calculate_total()`, `check_stock()`. The user asks *"Is the laptop in stock and how much
would two cost?"*. What should the agent do? Think through:
`User → LLM → Tool 1? → Tool 2? → LLM → Answer`. The key is that the agent may need multiple
tools.

## 🎯 The Most Important Formula

Memorize this:

```
Agent = LLM + Tools + State + Decisions + Loop
```

If you understand this formula, you understand the basic architecture of an AI agent.
""",
            "order": 12,
            "estimated_minutes": 55,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Trace the shopping assistant agent",
                "description": (
                    "For the shopping assistant example (search_products, calculate_total, "
                    "check_stock), write out — as a numbered list of steps, no code needed — "
                    "exactly what the agent loop would do for the question \"Is the laptop in "
                    "stock and how much would two cost?\" Include which tool is called at each "
                    "step, what result it produces, and when the LLM finally answers."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# TODO: write the step-by-step trace as numbered comments, e.g.\n"
                    "# 1. User asks the question\n"
                    "# 2. LLM decides it needs check_stock() first...\n"
                ),
                "solution_code": (
                    "# 1. User asks: \"Is the laptop in stock and how much would two cost?\"\n"
                    "# 2. LLM reasons it needs two pieces of info: stock status and price.\n"
                    "#    It first requests check_stock(product=\"laptop\").\n"
                    "# 3. ToolNode executes check_stock(\"laptop\") -> {\"in_stock\": True}\n"
                    "# 4. Result goes back to the LLM. It now decides it needs the total price,\n"
                    "#    so it requests calculate_total(product=\"laptop\", quantity=2).\n"
                    "# 5. ToolNode executes calculate_total(...) -> {\"total\": 2400}\n"
                    "# 6. Result goes back to the LLM. No more tool_calls are needed.\n"
                    "# 7. LLM produces the final answer: \"Yes, the laptop is in stock, and\n"
                    "#    two would cost $2400.\"\n"
                    "# 8. should_continue sees no tool_calls -> routes to END.\n"
                ),
                "skill_tested": ["langgraph", "agents", "reasoning"],
            },
            {
                "title": "Workflow vs Agent classification",
                "description": (
                    "For each of these 4 scenarios, decide whether a fixed WORKFLOW or a "
                    "dynamic AGENT is the better fit, and write one sentence justifying each: "
                    "(1) A pipeline that always retrieves documents, reranks them, then "
                    "generates an answer. (2) A customer-support bot that might need to check "
                    "billing, search docs, or escalate to a human, depending on the question. "
                    "(3) A fixed nightly ETL job that extracts, transforms, and loads data in "
                    "the same order every time. (4) A general-purpose assistant that might need "
                    "to search the web, do math, or just chat, depending on what's asked."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# 1. Retrieve -> Rerank -> Generate pipeline: WORKFLOW or AGENT? Why?\n"
                    "# 2. Support bot with billing/docs/escalate options: WORKFLOW or AGENT? Why?\n"
                    "# 3. Fixed nightly ETL job: WORKFLOW or AGENT? Why?\n"
                    "# 4. General-purpose assistant (search/math/chat): WORKFLOW or AGENT? Why?\n"
                ),
                "solution_code": (
                    "# 1. WORKFLOW - the exact sequence of steps never changes, so a fixed\n"
                    "#    path (no decisions needed) is simpler and more predictable.\n"
                    "# 2. AGENT - the right next action genuinely depends on the question, so\n"
                    "#    the LLM needs to dynamically choose between tools/paths.\n"
                    "# 3. WORKFLOW - ETL order is fixed and deterministic; there's no decision\n"
                    "#    to make, so a programmer-controlled flow is appropriate.\n"
                    "# 4. AGENT - the assistant must decide per-message whether a tool is\n"
                    "#    needed at all, and if so, which one -- classic agent territory.\n"
                ),
                "skill_tested": ["langgraph", "agents", "design"],
            },
        ],
        "quiz": {
            "title": "Agents in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What is the key word that distinguishes an agent from a plain LLM call?",
                    "options": [
                        "Speed",
                        "Decide — the agent decides what action to take next",
                        "Cost",
                        "Length of the answer",
                    ],
                    "correct": 1,
                    "explanation": "An agent's defining feature is that the LLM decides what to do next (use a tool, use another tool, or answer), rather than just producing one fixed response.",
                },
                {
                    "question": "What five ingredients make up the 'Agent = ...' formula from the lesson?",
                    "options": [
                        "LLM + Tools + State + Decisions + Loop",
                        "LLM + Prompts + Retrievers + Chains + Memory",
                        "State + Nodes + Edges + START + END",
                        "Messages + ToolNode + Checkpointer + Thread + Graph",
                    ],
                    "correct": 0,
                    "explanation": "The lesson's key formula is Agent = LLM + Tools + State + Decisions + Loop.",
                },
                {
                    "question": "What does ReAct stand for?",
                    "options": [
                        "Reactive Actions",
                        "Reasoning + Acting",
                        "Recursive Activation",
                        "Read + Act",
                    ],
                    "correct": 1,
                    "explanation": "ReAct combines Reasoning (thinking about what to do) and Acting (using a tool), repeated in a loop.",
                },
                {
                    "question": "According to the lesson, when should you prefer a fixed workflow over an agent?",
                    "options": [
                        "Never — agents are always better",
                        "When you already know exactly what steps should happen, e.g. Retrieve -> Rerank -> Generate",
                        "Only when there are no tools available",
                        "Only for chatbots, never for pipelines",
                    ],
                    "correct": 1,
                    "explanation": "A workflow is the right choice when the sequence of steps is known ahead of time and doesn't need to vary based on the input.",
                },
                {
                    "question": "Is the LLM the entire agent, or part of it?",
                    "options": [
                        "The LLM IS the entire agent — nothing else is needed",
                        "The LLM is the 'brain' inside the agent, working alongside tools, state, decisions, and a loop",
                        "The LLM is unrelated to agents",
                        "Agents don't use LLMs at all",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly warns not to confuse the agent with just the LLM — the agent is the LLM plus the surrounding tool/decision/loop machinery.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Design (and Optionally Build) a Study-Helper Agent",
            "description": (
                "Design an agent for a 'study helper' assistant with three tools: "
                "search_notes(topic), calculate_grade(scores), and define_term(word). First, on "
                "paper/in comments, trace through the agent loop for 3 different sample "
                "questions, one that needs zero tools, one that needs exactly one tool, and one "
                "that needs two tools in sequence. Then (optional stretch goal) implement the "
                "three tools as stub functions and wire up the full LangGraph agent loop from "
                "Lesson 11 to actually run your traces."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Design 3 tools with clear names/docstrings appropriate for the domain",
                "Correctly trace the agent loop for zero-tool, one-tool, and two-tool scenarios",
                "(Stretch) Implement and run the actual LangGraph agent loop",
            ],
            "rubric": {
                "tool_design": "Tools are well-named with clear, LLM-friendly docstrings (25%)",
                "trace_zero_tool": "Zero-tool trace correctly shows the LLM answering directly (20%)",
                "trace_multi_tool": "One-tool and two-tool traces correctly show the decision/loop pattern (35%)",
                "implementation": "Optional working implementation runs correctly end-to-end (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Memory in LangGraph",
        "slug":              "memory-in-langgraph",
        "description":       "Persist conversation state across separate invocations using a checkpointer and thread_id, and understand short-term vs long-term memory.",
        "order":             13,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "memory", "checkpointer", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Memory in LangGraph",
            "content": """# 💾 Lesson 13 — Memory in LangGraph

Now we solve a very important problem: **how can our LangGraph application remember
previous conversations?** You've already seen that `messages` stores conversation history
inside a graph execution. But if the application starts a new execution, we need
**persistent state**.

## 1. The Problem

Imagine our chatbot:

```
User: My name is Mohammad.
AI: Nice to meet you, Mohammad!
```

Later:

```
User: What's my name?
```

Without memory, the AI may say *"I don't know your name."* Why? Because the new invocation
doesn't automatically contain the previous conversation.

## 2. What We Want

```
Conversation → State → Save it → Later → Load it → Continue conversation
```

For example: `Message 1 → Message 2 → Message 3 → SAVE → Message 4 → LOAD previous state →
Continue`.

## 3. The Key Concept: Checkpointer

In LangGraph, a **checkpointer** saves graph state so it can be restored later. Think of it
like a 💾 Save Game:

```
Game → Reach Level 5 → SAVE → Close game → Open game → LOAD → Continue Level 5
```

A LangGraph checkpointer does something similar with graph state.

## 4. In-Memory Checkpointer

For learning, we'll use:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

This stores the state in memory.

⚠️ **Important:** `InMemorySaver` is mainly useful for learning/testing. If the Python
process stops, the stored data is lost.

## 5. Add It to the Graph

Previously: `app = graph.compile()`. Now:

```python
app = graph.compile(checkpointer=checkpointer)
```

That's the key change.

## 6. But We Need One More Thing

Suppose we have User A and User B — their conversations must be separate. We need something
that identifies the conversation. LangGraph uses configuration such as `thread_id`. Think of
it as `thread_id = conversation ID`, for example `thread-1 → Mohammad's conversation`,
`thread-2 → Another user's conversation`.

## 7. Create a Thread

When invoking the graph:

```python
config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}
```

Then:

```python
result = app.invoke(
    {"messages": [HumanMessage(content="My name is Mohammad.")]},
    config=config
)
```

The important part is `"thread_id": "conversation-1"`. LangGraph now knows: *"Save this
state under conversation-1."*

## 8. Send Another Message

Now we invoke the same graph again:

```python
result = app.invoke(
    {"messages": [HumanMessage(content="What is my name?")]},
    config=config
)
```

Notice something important: we didn't manually provide *"My name is Mohammad"* again,
because the checkpointer can restore the previous state for `conversation-1`.

## 🧩 The Complete Example

```python
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver


# LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


# State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Chatbot Node
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# Graph
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


# Checkpointer
checkpointer = InMemorySaver()


# Compile
app = graph.compile(checkpointer=checkpointer)


# Conversation ID
config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}


# Message 1
result = app.invoke(
    {"messages": [HumanMessage(content="My name is Mohammad.")]},
    config=config
)
print(result["messages"][-1].content)


# Message 2
result = app.invoke(
    {"messages": [HumanMessage(content="What is my name?")]},
    config=config
)
print(result["messages"][-1].content)
```

The second response should know the previous conversation.

## 10. What Is Actually Happening?

**First request** (`thread_id = conversation-1`): User says *"My name is Mohammad."* → Graph
→ AI response → Checkpointer SAVE. The state is associated with `conversation-1`.

**Second request** (`thread_id = conversation-1`): User asks *"What is my name?"* →
Checkpointer LOADs previous state → Messages become `H: My name is Mohammad. / AI: Nice to
meet you! / Human: What's my name?` → LLM → *"Mohammad."* That's memory.

## 11. Different Thread = Different Memory

This is very important. Suppose:

```python
config1 = {"configurable": {"thread_id": "conversation-1"}}
config2 = {"configurable": {"thread_id": "conversation-2"}}
```

They are separate conversations. `conversation-1` has its own Human/AI/Human/AI history, and
`conversation-2` has its own, separate history. The two conversations don't share their
state.

## 12. Why Thread IDs Are Important

Imagine you're building a chatbot for 1,000 users. You don't want User A's messages ending
up in User B's chatbot — that would be terrible. Instead: `User A → thread-A`,
`User B → thread-B`, `User C → thread-C`. Each conversation has its own state.

## 13. Memory ≠ Long-Term Knowledge

This distinction is extremely important.

**Conversation memory** — `User: My name is Mohammad. / AI: Nice to meet you. / User: What's
my name?` — this is conversation state.

**Knowledge** — suppose your AI knows university regulations, course descriptions, tuition
rules. That isn't usually stored in conversation memory. For that, you might use
`Documents → Embeddings → Vector Database → Retriever → RAG`. We'll learn RAG later.

## 14. Short-Term vs Long-Term Memory

For now, think about two categories.

**Short-term memory** — the current conversation (`Human, AI, Human, AI, ...`). LangGraph
checkpointers are useful for maintaining state across runs/threads.

**Long-term memory** — information you intentionally want to persist beyond one
conversation or across conversations, for example a user preference like *"Prefers
explanations in Arabic."* This is a different problem and can involve a separate storage
mechanism. Don't worry about long-term memory yet.

## 15. Inspecting the Saved State

One useful thing you can do is inspect the graph state:

```python
state = app.get_state(config)

print(state.values)
```

You can see the state associated with that thread — `State → messages → [HumanMessage,
AIMessage, HumanMessage, AIMessage]`. This is very useful when debugging.

## 🧠 The Big Picture

```
             LangGraph
                 │
                 ↓
              State
                 │
                 ↓
             Messages
                 │
                 ↓
            Checkpointer
                 │
                 ↓
            thread_id
                 │
                 ↓
         Persistent state
```

The relationship is: `State → Checkpointer → thread_id → Conversation memory`.

## 16. The Most Important Code

If you remember only three things from this lesson, remember these:

1. **Checkpointer** — `checkpointer = InMemorySaver()`
2. **Compile with it** — `app = graph.compile(checkpointer=checkpointer)`
3. **Use a thread ID** — `config = {"configurable": {"thread_id": "conversation-1"}}`

That's the foundation of LangGraph conversation memory.

## 🧪 Exercise

Modify your chatbot so that: first message is *"My favorite programming language is
Python."*, second message is *"What is my favorite programming language?"* — use the same
`thread_id` for both calls. Then try changing `"thread_id": "conversation-1"` to
`"thread_id": "conversation-2"` and ask the same question again. You'll see the difference
between the two conversations.

## ⚠️ Important Note

`InMemorySaver` is not a production database. It is excellent for learning, testing,
prototypes, and experiments. For production applications, you can use persistent
checkpointer backends such as database-backed storage. We'll get to production architecture
later.
""",
            "order": 13,
            "estimated_minutes": 55,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Same thread vs different thread",
                "description": (
                    "Build the checkpointed chatbot graph from the lesson. Using "
                    "thread_id=\"conversation-1\", send \"My favorite programming language is "
                    "Python.\" then \"What is my favorite programming language?\" and print both "
                    "answers. Then repeat the SECOND question only, this time with "
                    "thread_id=\"conversation-2\", and print that answer too. In a comment, "
                    "explain why the two answers differ."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from langgraph.checkpoint.memory import InMemorySaver\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n\n"
                    "config1 = {\"configurable\": {\"thread_id\": \"conversation-1\"}}\n"
                    "config2 = {\"configurable\": {\"thread_id\": \"conversation-2\"}}\n\n"
                    "# TODO: send both messages under config1, print each answer\n"
                    "# TODO: send only the second question under config2, print that answer\n"
                    "# TODO: comment explaining why the two answers to \"What is my favorite...\" differ\n"
                ),
                "solution_code": (
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n\n"
                    "config1 = {\"configurable\": {\"thread_id\": \"conversation-1\"}}\n"
                    "config2 = {\"configurable\": {\"thread_id\": \"conversation-2\"}}\n\n"
                    "r1 = app.invoke({\"messages\": [HumanMessage(content=\"My favorite programming language is Python.\")]}, config=config1)\n"
                    "print(r1[\"messages\"][-1].content)\n\n"
                    "r2 = app.invoke({\"messages\": [HumanMessage(content=\"What is my favorite programming language?\")]}, config=config1)\n"
                    "print(r2[\"messages\"][-1].content)  # knows it's Python\n\n"
                    "r3 = app.invoke({\"messages\": [HumanMessage(content=\"What is my favorite programming language?\")]}, config=config2)\n"
                    "print(r3[\"messages\"][-1].content)  # doesn't know, different thread\n\n"
                    "# conversation-2 has never received the earlier message about Python,\n"
                    "# because each thread_id maintains its own independent saved state --\n"
                    "# the checkpointer only loads history that was saved under the SAME\n"
                    "# thread_id, so conversation-2 starts with no relevant context.\n"
                ),
                "skill_tested": ["langgraph", "memory", "checkpointer", "thread_id"],
            },
            {
                "title": "Inspect saved state",
                "description": (
                    "After running at least 2 messages under the same thread_id, call "
                    "`app.get_state(config)` and print `state.values['messages']`, showing the "
                    "type and content of each stored message. Confirm the count matches what "
                    "you'd expect (2 HumanMessages + 2 AIMessages, for example)."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# TODO: after invoking the graph twice under the same config,\n"
                    "# call app.get_state(config) and print each message's type + content\n"
                ),
                "solution_code": (
                    "state = app.get_state(config1)\n"
                    "for m in state.values[\"messages\"]:\n"
                    "    print(type(m).__name__, \"->\", m.content)\n\n"
                    "print(\"Total messages:\", len(state.values[\"messages\"]))\n"
                ),
                "skill_tested": ["langgraph", "memory", "debugging"],
            },
        ],
        "quiz": {
            "title": "Memory in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What does a checkpointer do?",
                    "options": [
                        "It validates the State's TypedDict schema",
                        "It saves graph state so it can be restored in a later invocation",
                        "It speeds up LLM calls",
                        "It automatically writes unit tests",
                    ],
                    "correct": 1,
                    "explanation": "A checkpointer is LangGraph's mechanism for persisting state between separate invoke() calls, like a save-game system.",
                },
                {
                    "question": "What does thread_id identify?",
                    "options": [
                        "A specific Python thread/process",
                        "A specific conversation, so its state can be saved and loaded separately from other conversations",
                        "The LLM model version being used",
                        "The tool being called",
                    ],
                    "correct": 1,
                    "explanation": "thread_id acts as a conversation ID, letting the checkpointer keep different users'/conversations' state separate.",
                },
                {
                    "question": "Without passing the same thread_id on a second invoke() call, what happens?",
                    "options": [
                        "The graph automatically merges it with the most recent thread",
                        "It's treated as a new/different conversation with no access to prior history",
                        "It throws an error",
                        "It deletes all previous checkpoints",
                    ],
                    "correct": 1,
                    "explanation": "The checkpointer only restores state for a matching thread_id; a new or missing thread_id means no prior context is loaded.",
                },
                {
                    "question": "Why is InMemorySaver described as unsuitable for production?",
                    "options": [
                        "It's too slow for any use case",
                        "It only stores state in memory, so data is lost if the Python process stops",
                        "It can only store one conversation at a time",
                        "It requires a paid API key",
                    ],
                    "correct": 1,
                    "explanation": "InMemorySaver keeps state in the running process's memory; restarting the process loses everything, which is fine for learning but risky for production.",
                },
                {
                    "question": "What's the difference between 'short-term memory' (conversation history) and 'long-term memory' as described in the lesson?",
                    "options": [
                        "There is no difference, they're the same thing",
                        "Short-term memory is the current conversation's messages; long-term memory is information intentionally persisted across conversations, like user preferences",
                        "Short-term memory only works with InMemorySaver, long-term never uses a checkpointer",
                        "Long-term memory replaces the need for a thread_id",
                    ],
                    "correct": 1,
                    "explanation": "Short-term memory (via checkpointers/thread_id) covers the ongoing conversation; long-term memory is a separate, broader concern about persisting facts across many conversations.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Multi-User Chat Simulator with Memory",
            "description": (
                "Build the checkpointed chatbot graph. Simulate 2 separate users, each with "
                "their own thread_id, having a 3-turn conversation (e.g. user shares a fact "
                "about themselves, asks a follow-up that depends on it, and asks something "
                "unrelated). Interleave the two users' turns (User A, User B, User A, User B, "
                "...) to prove their conversations stay independent. Print each user's full "
                "message history at the end using app.get_state()."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Set up InMemorySaver and compile the graph with a checkpointer",
                "Manage 2 distinct thread_ids representing 2 different users",
                "Interleave turns between users and confirm no cross-contamination of context",
                "Use get_state() to display each user's final message history",
            ],
            "rubric": {
                "checkpointer_setup": "Checkpointer is correctly created and passed to compile() (20%)",
                "thread_management": "Two distinct thread_ids are used consistently per user (25%)",
                "conversation_correctness": "Each user's follow-up correctly relies only on their own prior messages (35%)",
                "state_inspection": "Final message history for both threads is printed via get_state() (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Checkpoints in LangGraph",
        "slug":              "checkpoints-in-langgraph",
        "description":       "What a checkpoint actually is: saved snapshots of graph state tied to a thread, state history inspection, and how checkpoints enable persistence, recovery, and debugging.",
        "order":             14,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "checkpoints", "memory", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Checkpoints in LangGraph",
            "content": """# 💾 Lesson 14 — Checkpoints in LangGraph

You just learned memory. Now we're going one level deeper: **what exactly is a
checkpoint?** Don't worry — this is easier than it sounds.

## 1. What Is a Checkpoint?

A checkpoint is basically a saved snapshot of your graph's state. Think about a video game:

```
Game → Level 1 → Level 2 → 💾 SAVE → Level 3
```

If something goes wrong: `LOAD SAVE → Continue from Level 2`. LangGraph can do something
similar:

```
Graph → Node 1 → Node 2 → 💾 Checkpoint → Node 3 → Node 4
```

The checkpoint contains the state at a particular point.

## 2. Checkpoint vs Memory

These two terms can be confusing.

**Checkpoint** — a saved snapshot of graph state: `State at time T → Checkpoint`.

**Memory** — the broader idea of remembering state between executions:
`Memory → Checkpoints → Saved states`.

So a simple way to remember: **Checkpoint = saved state.**

## 3. Why Do We Need Checkpoints?

They provide several useful capabilities.

**1. Persistence** — remember previous conversation: `User → Graph → Save → Later →
Continue`.

**2. Recovery** — if something fails (`Node 1 → Node 2 → 💾 → Node 3 ❌`), you can
potentially resume from the saved state.

**3. Debugging** — you can inspect what the graph looked like at a particular point.

**4. Human approval** — you can pause the graph: `AI → Need approval → ⏸️ PAUSE → Human →
Resume`. We'll use this in the next lesson.

## 4. The Checkpoint Is Connected to a Thread

Remember this from the previous lesson:

```python
config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}
```

The `thread_id` identifies the execution thread/conversation. Think:
`thread_id → Conversation → Checkpoints → Saved states`. For example, `conversation-1` might
have `Checkpoint 1 → Checkpoint 2 → Checkpoint 3 → Checkpoint 4`.

## 5. Checkpoints Are Created During Graph Execution

Imagine our graph: `START → Node A → Node B → Node C → END`. With a checkpointer, the graph
can save state as it executes:

```
START
 ↓
Node A
 ↓
💾 Checkpoint
 ↓
Node B
 ↓
💾 Checkpoint
 ↓
Node C
 ↓
💾 Checkpoint
 ↓
END
```

This gives LangGraph a history of state changes.

## 6. Simple Example

Let's use the same chatbot.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

Then:

```python
app = graph.compile(checkpointer=checkpointer)
```

And:

```python
config = {
    "configurable": {
        "thread_id": "chat-1"
    }
}
```

Run:

```python
result = app.invoke(
    {"messages": [HumanMessage(content="My name is Mohammad.")]},
    config=config
)
```

A checkpoint is created for that thread.

## 7. Inspect the Current State

You can ask the graph for its current state:

```python
state = app.get_state(config)

print(state.values)
```

You'll see something conceptually like:

```python
{
    "messages": [
        HumanMessage(...),
        AIMessage(...)
    ]
}
```

So: `app.get_state()` → Current saved state.

## 8. State History

You can also inspect the history of states:

```python
for state in app.get_state_history(config):
    print(state.values)
```

This lets you see previous checkpoints. Imagine:

```
Checkpoint 1 -> messages = [Human: Hello]
Checkpoint 2 -> messages = [Human: Hello, AI: Hi!]
Checkpoint 3 -> messages = [Human: Hello, AI: Hi!, Human: What is LangGraph?]
Checkpoint 4 -> ...
```

This is extremely useful for debugging.

## 9. Why This Is Powerful

Suppose your agent performs `Search → Calculate → Call API → Generate answer`, and the API
call fails: `Search → Calculate → Call API ❌`. Without saved state, you may need to restart
everything. With checkpoints, you can potentially recover from a previous state:
`💾 Search completed → 💾 Calculation completed → API failed → Resume`.

## 10. Checkpoints + Agents

Now combine what we've learned. Our agent:

```
        START
          ↓
         LLM
          ↓
      Tool needed?
       ↙       ↘
     NO         YES
     ↓            ↓
    END         Tool
                  ↓
                 LLM
                  ↓
                ...
```

With checkpoints:

```
        START
          ↓
         LLM
          ↓
       💾 Save
          ↓
      Tool needed?
       ↙       ↘
     NO         YES
     ↓            ↓
    END         Tool
                  ↓
                💾 Save
                  ↓
                 LLM
                  ↓
                💾 Save
```

Now the agent has a recoverable execution history.

## 11. Threads vs Checkpoints

This distinction is worth remembering.

**Thread** — identifies an execution/conversation: `thread_id = "chat-1"`.

**Checkpoint** — a saved state inside that thread:
`chat-1 ├── checkpoint 1 ├── checkpoint 2 └── checkpoint 3`.

So: `Thread → Checkpoints → State`.

## 12. Multiple Users

Imagine your AI application has three users: `User A → thread-A`, `User B → thread-B`,
`User C → thread-C`. Each thread can have its own checkpoint history — `thread-A` might have
CP1-CP3, `thread-B` might have CP1-CP2, `thread-C` might have CP1-CP4. This is one reason
`thread_id` is so important.

## 13. Checkpointing Is Not RAG

Another important distinction.

**Checkpoint** — stores application state: messages, current workflow state, execution
progress.

**RAG** — retrieves external knowledge: `PDF → Chunks → Embeddings → Vector DB → Retriever →
Context`.

So: **Checkpoint → "What was happening in my conversation?" / RAG → "What does my knowledge
base say?"** These are completely different concepts.

## 14. Checkpoints + Human Approval

Imagine an AI agent wants to send an email. You don't want it to automatically send it. You
can create:

```
LLM → Decides: send email → 💾 Checkpoint → ⏸️ PAUSE → Human approval → Resume → Send email
```

This is called Human-in-the-Loop — and that's our next lesson.

## 🧠 Simple Mental Model

Remember this diagram:

```
             THREAD
                │
        ┌───────┼───────┐
        ↓       ↓       ↓
       CP1     CP2     CP3
        ↓       ↓       ↓
      State   State   State
```

Where: **Thread = conversation/execution, Checkpoint = saved snapshot, State = data at that
snapshot.**

## 🧪 Exercise

Using your chatbot from Lesson 13:

1. Create a checkpointer — `checkpointer = InMemorySaver()`
2. Compile with it — `app = graph.compile(checkpointer=checkpointer)`
3. Create a thread — `config = {"configurable": {"thread_id": "test-1"}}`
4. Send two messages.

Then inspect `state = app.get_state(config)` and `print(state.values)`. And try
`for state in app.get_state_history(config): print(state.values)`.

Your goal isn't to memorize the API. Your goal is to understand:
`invoke() → state changes → checkpoint → state can be inspected`.

## 🎯 One-Sentence Summary

A LangGraph checkpoint is a saved snapshot of graph state associated with a thread, allowing
the application to persist, inspect, and resume execution.
""",
            "order": 14,
            "estimated_minutes": 50,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Walk the checkpoint history",
                "description": (
                    "Using the chatbot + checkpointer setup, send 3 messages under the same "
                    "thread_id (e.g. share a fact, ask a follow-up, ask something unrelated). "
                    "Then loop over `app.get_state_history(config)` and print, for each "
                    "checkpoint, the number of messages present at that point. Confirm the "
                    "count grows over the sequence of checkpoints."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "# TODO: set up checkpointer, compile, thread config\n"
                    "# TODO: invoke 3 times with the same thread_id\n"
                    "# TODO: loop over app.get_state_history(config) and print\n"
                    "# len(state.values['messages']) for each checkpoint\n"
                ),
                "solution_code": (
                    "from langgraph.checkpoint.memory import InMemorySaver\n"
                    "from langchain_core.messages import HumanMessage\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n"
                    "config = {\"configurable\": {\"thread_id\": \"history-test\"}}\n\n"
                    "app.invoke({\"messages\": [HumanMessage(content=\"My name is Mohammad.\")]}, config=config)\n"
                    "app.invoke({\"messages\": [HumanMessage(content=\"What's my name?\")]}, config=config)\n"
                    "app.invoke({\"messages\": [HumanMessage(content=\"What's the weather like?\")]}, config=config)\n\n"
                    "for state in app.get_state_history(config):\n"
                    "    print(\"Checkpoint message count:\", len(state.values[\"messages\"]))\n"
                    "# Counts should increase as you walk back through the history\n"
                ),
                "skill_tested": ["langgraph", "checkpoints", "get_state_history"],
            },
            {
                "title": "Classify: checkpoint or RAG?",
                "description": (
                    "For each scenario below, decide whether it's solved by a CHECKPOINT or by "
                    "RAG, and write one sentence why: (1) 'What did the user say 3 messages "
                    "ago?' (2) 'What does our refund policy document say about late returns?' "
                    "(3) 'Resume the agent from where it left off after a crash.' (4) 'Find "
                    "relevant passages from last year's product manual.'"
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# 1. \"What did the user say 3 messages ago?\" -> CHECKPOINT or RAG? Why?\n"
                    "# 2. \"What does our refund policy document say...?\" -> CHECKPOINT or RAG? Why?\n"
                    "# 3. \"Resume the agent from where it left off after a crash.\" -> CHECKPOINT or RAG? Why?\n"
                    "# 4. \"Find relevant passages from last year's product manual.\" -> CHECKPOINT or RAG? Why?\n"
                ),
                "solution_code": (
                    "# 1. CHECKPOINT - this is about the conversation's own history/state,\n"
                    "#    which is exactly what checkpoints track.\n"
                    "# 2. RAG - this needs external knowledge (a policy document) retrieved\n"
                    "#    from a knowledge base, not conversation state.\n"
                    "# 3. CHECKPOINT - recovering execution progress after a failure is a\n"
                    "#    core checkpoint use case.\n"
                    "# 4. RAG - retrieving relevant passages from a document store is\n"
                    "#    exactly what RAG (retrieval-augmented generation) is for.\n"
                ),
                "skill_tested": ["langgraph", "checkpoints", "rag", "design"],
            },
        ],
        "quiz": {
            "title": "Checkpoints in LangGraph — Quiz",
            "questions": [
                {
                    "question": "What is a checkpoint, most simply?",
                    "options": [
                        "A saved snapshot of the graph's state at a particular point",
                        "A type of LLM model",
                        "A conditional edge",
                        "An external vector database",
                    ],
                    "correct": 0,
                    "explanation": "A checkpoint captures the graph's state at a given moment, similar to a video game save.",
                },
                {
                    "question": "What is the relationship between threads and checkpoints?",
                    "options": [
                        "They are the same thing",
                        "A thread can contain multiple checkpoints, each a saved snapshot within that conversation/execution",
                        "A checkpoint can contain multiple threads",
                        "Threads and checkpoints are unrelated",
                    ],
                    "correct": 1,
                    "explanation": "Thread -> Checkpoints -> State: one thread_id can have many checkpoints saved over its execution history.",
                },
                {
                    "question": "What does app.get_state_history(config) let you do?",
                    "options": [
                        "Delete old checkpoints",
                        "Inspect the sequence of previous saved states for a thread, useful for debugging",
                        "Change the LLM model being used",
                        "Merge two threads together",
                    ],
                    "correct": 1,
                    "explanation": "get_state_history() walks through previously saved checkpoints, letting you see how state evolved over the execution.",
                },
                {
                    "question": "How does checkpointing differ from RAG?",
                    "options": [
                        "They are the same mechanism",
                        "Checkpointing saves application/execution state; RAG retrieves external knowledge from documents/vector stores",
                        "RAG is used only for saving conversation history",
                        "Checkpointing requires embeddings, RAG does not",
                    ],
                    "correct": 1,
                    "explanation": "Checkpoint answers 'what was happening in my conversation?' while RAG answers 'what does my knowledge base say?' — different problems entirely.",
                },
                {
                    "question": "Why are checkpoints useful if a multi-step agent's API call fails partway through?",
                    "options": [
                        "They aren't useful in that scenario",
                        "They let you potentially resume from the last successfully saved state instead of restarting everything",
                        "They automatically fix the failing API",
                        "They prevent all future failures",
                    ],
                    "correct": 1,
                    "explanation": "Since earlier steps were checkpointed, a failure partway through doesn't necessarily require redoing completed work.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Debuggable Multi-Step Agent Trace",
            "description": (
                "Build a small multi-node graph (e.g. understand -> retrieve -> answer, reusing "
                "ideas from earlier lessons) compiled with a checkpointer. Run it once under a "
                "thread_id, then write a small utility function that prints a clean, "
                "human-readable timeline of all checkpoints for that thread (checkpoint index, "
                "which fields changed, and their new values). Explain in a short comment how "
                "this timeline would help you debug a failure in a longer agent pipeline."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph"],
            "objectives": [
                "Compile a multi-node graph with a checkpointer",
                "Run the graph and generate a checkpoint history",
                "Build a utility to present the checkpoint history in a readable way",
                "Explain the debugging value of checkpoint history in your own words",
            ],
            "rubric": {
                "graph_setup": "Multi-node graph with checkpointer is correctly built and compiled (25%)",
                "history_walk": "get_state_history is correctly used to enumerate checkpoints (35%)",
                "presentation": "Checkpoint timeline is clearly formatted and readable (25%)",
                "explanation": "Debugging value is clearly explained (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 1.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "Human-in-the-Loop",
        "slug":              "human-in-the-loop",
        "description":       "Pause a graph for human approval using interrupt() and Command(resume=...), and design which actions in an agent should require human sign-off.",
        "order":             15,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["langgraph", "human-in-the-loop", "interrupt", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Human-in-the-Loop",
            "content": """# 👤 Lesson 15 — Human-in-the-Loop

This is one of the most useful ideas in LangGraph. Sometimes we don't want the AI to make an
important decision by itself. For example, AI wants to: send an email, delete a file, make a
purchase, submit an application, modify a database. Instead, we can make the AI pause and
ask a human.

## 1. The Basic Idea

**Without human approval:** `User → AI → Tool → Done`.

**With human approval:**

```
User
 ↓
AI
 ↓
Tool needed
 ↓
⏸️ PAUSE
 ↓
👤 Human
 ↓
Approve?
 ↙       ↘
YES       NO
 ↓         ↓
Tool     Stop
 ↓
Answer
```

This is called **Human-in-the-Loop (HITL)**.

## 2. Why Do We Need It?

Imagine an AI assistant with this tool:

```python
@tool
def send_email(to, message):
    ...
```

You probably don't want the AI to think *"I think I should send this email"* and then
automatically call `send_email()`. Instead: AI says *"I want to send this email"* → ⏸️ PAUSE
→ Human says *"Yes, send it."* → Tool executes. This gives humans control over important
actions.

## 3. The Important LangGraph Concept: Interrupt

LangGraph provides an `interrupt()` mechanism.

```python
from langgraph.types import interrupt
```

Then inside a node:

```python
value = interrupt("Do you approve?")
```

The graph pauses at that point: `Node → interrupt() → ⏸️ PAUSED`.

## 4. Simple Example

Let's create a node that asks for approval.

```python
from langgraph.types import interrupt


def approval_node(state):

    answer = interrupt("Do you approve this action?")

    return {"approved": answer}
```

When the graph reaches `interrupt(...)`, execution pauses.

## 5. Why Do We Need a Checkpointer?

This is very important. If we pause the graph, we need to remember where we stopped. So
Human-in-the-Loop normally uses: **interrupt + checkpointer + thread_id**. Remember the
previous lesson?

```python
checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "approval-1"
    }
}
```

Now LangGraph can pause and later resume the same execution.

## 6. The Command Object

After an interrupt, we need a way to resume the graph.

```python
from langgraph.types import Command
```

Conceptually:

```python
Command(resume="yes")
```

means: *"Resume the paused graph and provide yes as the response."*

## 7. Simple Approval Workflow

Our graph: `START → approval → END`. The approval node:

```python
from langgraph.types import interrupt


def approval_node(state):

    answer = interrupt("Do you approve?")

    return {"answer": answer}
```

## 8. State

```python
from typing_extensions import TypedDict


class State(TypedDict):
    answer: str
```

## 9. Build the Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("approval", approval_node)

graph.add_edge(START, "approval")
graph.add_edge("approval", END)
```

## 10. Add the Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)
```

## 11. Create a Thread

```python
config = {
    "configurable": {
        "thread_id": "approval-1"
    }
}
```

Remember: `thread_id → identifies this execution`.

## 12. Start the Graph

```python
result = app.invoke({}, config=config)
```

When the graph reaches `interrupt(...)`, it pauses. The application can inspect the
result/state to see that it is interrupted:

```
START
 ↓
approval_node
 ↓
interrupt()
 ↓
⏸️ PAUSED
```

## 13. Resume the Graph

Now the human decides **YES**. We resume:

```python
from langgraph.types import Command

result = app.invoke(Command(resume="yes"), config=config)
```

The graph continues:

```
⏸️ PAUSED
   ↓
Human: yes
   ↓
Resume
   ↓
approval_node
   ↓
END
```

## 14. Complete Example

```python
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# -------------------------
# State
# -------------------------
class State(TypedDict):
    answer: str


# -------------------------
# Node
# -------------------------
def approval_node(state):

    answer = interrupt("Do you approve?")

    return {"answer": answer}


# -------------------------
# Graph
# -------------------------
graph = StateGraph(State)

graph.add_node("approval", approval_node)

graph.add_edge(START, "approval")
graph.add_edge("approval", END)


# -------------------------
# Checkpointer
# -------------------------
checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)


# -------------------------
# Thread
# -------------------------
config = {
    "configurable": {
        "thread_id": "approval-1"
    }
}


# -------------------------
# Start
# -------------------------
result = app.invoke({}, config=config)


# -------------------------
# Resume
# -------------------------
result = app.invoke(Command(resume="yes"), config=config)

print(result)
```

The exact representation of the interrupted state can vary by LangGraph version, but the
core mechanism is: `interrupt() → pause → Command(resume=...) → continue`.

## 15. Approval With a Tool

Now let's make it more realistic. Suppose we have:

```python
@tool
def delete_file(filename: str):
    \"\"\"Delete a file.\"\"\"
    return f"{filename} deleted"
```

We don't want the AI to automatically execute it. Instead:

```
User
 ↓
AI
 ↓
AI requests delete_file()
 ↓
⏸️ Human approval
 ↓
YES?
 ↙     ↘
YES     NO
 ↓       ↓
Tool    Stop
 ↓
Done
```

This is where Human-in-the-Loop becomes really useful.

## 16. HITL + Agent

Remember our agent architecture:

```
                 ┌───────┐
                 │  LLM  │
                 └───┬───┘
                     ↓
                 Tool call
                     ↓
              ┌─────────────┐
              │   Approval  │
              └──────┬──────┘
                     ↓
                  Human
                 ↙      ↘
               YES       NO
                ↓         ↓
              Tool       END
                ↓
               LLM
```

Now we have an agent that isn't completely autonomous — it has human supervision.

## 17. Why This Is Important in Production

Imagine an AI assistant connected to 💳 Payment system, 📧 Email, 🗄️ Database, 📁 Files,
🌐 APIs. You don't want the AI to have unlimited authority. You can define:

**Low-risk actions** — Search, Calculate, Summarize → AI can perform automatically.

**High-risk actions** — Delete, Purchase, Send, Publish, Modify → require approval.

So: **Low risk → Automatic. High risk → Human approval.** This is a very common production
pattern.

## 18. HITL Isn't Only "Yes/No"

The human can provide additional information. For example: AI: *"I want to send an email to
Ahmed."* → H: *"Change the recipient to Mohamed and send it."* Or: AI: *"I found three
possible documents."* → H: *"Use the second one."* So the human can approve, reject, modify,
choose, or provide information.

## 🧠 The Mental Model

Remember:

```
interrupt()
    ↓
⏸️ PAUSE
    ↓
Human decision
    ↓
Command(resume=...)
    ↓
Continue
```

And remember why checkpoints are involved: `interrupt + checkpointer + thread_id = pause +
resume`.

## 🧪 Exercise

Imagine you're building a LangGraph agent that can `search_web()`, `send_email()`,
`calculate()`. Which tools should require human approval?

| Tool | Approval? |
|---|---|
| search_web() | ❌ Probably not |
| calculate() | ❌ Probably not |
| send_email() | ✅ Probably yes |

This is exactly the kind of decision you should make when designing an agent.

## 🎯 One-Sentence Summary

Human-in-the-Loop lets a LangGraph workflow pause at important points, wait for human input,
and then resume from the saved state.
""",
            "order": 15,
            "estimated_minutes": 60,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Build the approval workflow end-to-end",
                "description": (
                    "Implement the full approval_node example from the lesson: State with an "
                    "`answer` field, a node that calls `interrupt(\"Do you approve?\")`, wired "
                    "START -> approval -> END, compiled with a checkpointer under "
                    "thread_id=\"approval-1\". First call `app.invoke({}, config=config)` and "
                    "print the result to observe the paused state. Then resume with "
                    "`Command(resume=\"yes\")` and print the final result."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing_extensions import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n"
                    "from langgraph.types import interrupt, Command\n\n\n"
                    "class State(TypedDict):\n"
                    "    answer: str\n\n\n"
                    "def approval_node(state):\n"
                    "    # TODO: call interrupt(...) and return the update\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add_node/add_edge x2, compile with checkpointer\n"
                    "# TODO: create config with thread_id, invoke({}, config), print result\n"
                    "# TODO: resume with Command(resume='yes'), print final result\n"
                ),
                "solution_code": (
                    "from typing_extensions import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n"
                    "from langgraph.types import interrupt, Command\n\n\n"
                    "class State(TypedDict):\n"
                    "    answer: str\n\n\n"
                    "def approval_node(state):\n"
                    "    answer = interrupt(\"Do you approve?\")\n"
                    "    return {\"answer\": answer}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"approval\", approval_node)\n"
                    "graph.add_edge(START, \"approval\")\n"
                    "graph.add_edge(\"approval\", END)\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n\n"
                    "config = {\"configurable\": {\"thread_id\": \"approval-1\"}}\n\n"
                    "result = app.invoke({}, config=config)\n"
                    "print(\"After start:\", result)  # shows the graph is interrupted\n\n"
                    "result = app.invoke(Command(resume=\"yes\"), config=config)\n"
                    "print(\"After resume:\", result)  # {'answer': 'yes'}\n"
                ),
                "skill_tested": ["langgraph", "human-in-the-loop", "interrupt"],
            },
            {
                "title": "Classify tools by approval risk",
                "description": (
                    "For a hypothetical customer-support agent with tools search_faq(), "
                    "issue_refund(amount), update_shipping_address(order_id, new_address), and "
                    "summarize_ticket(ticket_id), classify each as LOW risk (safe to run "
                    "automatically) or HIGH risk (should require human approval via interrupt), "
                    "with one sentence of justification each."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# search_faq() -> LOW or HIGH risk? Why?\n"
                    "# issue_refund(amount) -> LOW or HIGH risk? Why?\n"
                    "# update_shipping_address(order_id, new_address) -> LOW or HIGH risk? Why?\n"
                    "# summarize_ticket(ticket_id) -> LOW or HIGH risk? Why?\n"
                ),
                "solution_code": (
                    "# search_faq() -> LOW risk: read-only, no side effects, safe to automate.\n"
                    "# issue_refund(amount) -> HIGH risk: moves real money, mistakes are costly\n"
                    "#   and hard to reverse, so it should require human approval.\n"
                    "# update_shipping_address(order_id, new_address) -> HIGH risk: modifies\n"
                    "#   order data that affects real-world delivery; an error could send a\n"
                    "#   package to the wrong place, so approval is warranted.\n"
                    "# summarize_ticket(ticket_id) -> LOW risk: read-only summarization with\n"
                    "#   no external side effects, safe to run automatically.\n"
                ),
                "skill_tested": ["langgraph", "human-in-the-loop", "design"],
            },
        ],
        "quiz": {
            "title": "Human-in-the-Loop — Quiz",
            "questions": [
                {
                    "question": "What does interrupt() do inside a node?",
                    "options": [
                        "It permanently stops the graph with no way to continue",
                        "It pauses the graph's execution at that point, waiting for external input",
                        "It deletes the current state",
                        "It automatically approves the pending action",
                    ],
                    "correct": 1,
                    "explanation": "interrupt() pauses execution, letting a human (or other external process) provide input before the graph continues.",
                },
                {
                    "question": "Why is a checkpointer required for Human-in-the-Loop to work?",
                    "options": [
                        "It isn't required at all",
                        "The graph needs to remember exactly where it paused so it can be resumed later, which requires saved state",
                        "Checkpointers speed up interrupt() calls",
                        "Checkpointers replace the need for a thread_id",
                    ],
                    "correct": 1,
                    "explanation": "Without a checkpointer, there's no saved state to resume from once the graph pauses.",
                },
                {
                    "question": "What does Command(resume=\"yes\") do?",
                    "options": [
                        "Starts a completely new graph execution",
                        "Resumes the paused graph, supplying 'yes' as the value returned by interrupt()",
                        "Deletes the checkpoint for that thread",
                        "Cancels the interrupted node",
                    ],
                    "correct": 1,
                    "explanation": "Command(resume=...) continues execution from where interrupt() paused, and the resume value becomes interrupt()'s return value.",
                },
                {
                    "question": "According to the lesson, which kinds of actions are good candidates for requiring human approval?",
                    "options": [
                        "Only read-only actions like search or summarize",
                        "High-risk actions like delete, purchase, send, publish, or modify",
                        "All actions, without exception",
                        "No actions ever need approval if an LLM is involved",
                    ],
                    "correct": 1,
                    "explanation": "The lesson's low-risk/high-risk framing suggests automating safe, reversible actions and gating risky, hard-to-reverse ones behind human approval.",
                },
                {
                    "question": "Is HITL limited to simple yes/no approval?",
                    "options": [
                        "Yes, only yes/no is supported",
                        "No — a human can also modify, choose between options, or provide additional information, not just approve or reject",
                        "HITL only works with delete_file()",
                        "HITL cannot be combined with tool calling",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly shows examples where the human changes a recipient or picks among options, not just approving/rejecting.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Approval-Gated Agent",
            "description": (
                "Build a small tool-calling agent (reusing the Lesson 11 architecture) with two "
                "tools: `search_info(query)` (low risk, runs automatically) and "
                "`delete_record(record_id)` (high risk). Add an approval step before "
                "delete_record actually executes: when the LLM requests delete_record, use "
                "interrupt() to pause and ask for human confirmation before the ToolNode is "
                "allowed to run it. Test both a query that only needs search_info (no pause) "
                "and one that requests deletion (pauses, then resumes after approval)."
            ),
            "difficulty": DifficultyLevel.advanced,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Distinguish low-risk vs high-risk tools in the graph design",
                "Use interrupt() to pause before a high-risk action executes",
                "Use a checkpointer + thread_id so the pause/resume works correctly",
                "Test both the automatic (no approval needed) and gated (approval needed) paths",
            ],
            "rubric": {
                "tool_design": "search_info and delete_record are correctly defined and distinguished by risk (20%)",
                "interrupt_logic": "interrupt() correctly gates delete_record before execution (40%)",
                "checkpointing": "Checkpointer + thread_id correctly support pause/resume (20%)",
                "testing": "Both the automatic and approval-gated paths are tested and shown working (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "RAG with LangGraph",
        "slug":              "rag-with-langgraph",
        "description":       "Build a retrieve-then-generate RAG graph, then extend it with conditional relevance checks and query rewriting into an agentic RAG pattern.",
        "order":             16,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   2.0,
        "skill_tags":        ["langgraph", "rag", "retrieval", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "RAG with LangGraph",
            "content": """# 📚 Lesson 16 — RAG with LangGraph

Now we're entering one of the most important parts of LangGraph. You already know RAG from
your previous work, so we'll keep this lesson simple and connect the concepts together.

## 1. What Is RAG?

**RAG = Retrieval-Augmented Generation.** Instead of asking the LLM to answer only from what
it knows (`Question → LLM → Answer`), we give it relevant information from our own
documents:

```
Question
   ↓
Retrieve relevant information
   ↓
Context
   ↓
LLM
   ↓
Answer
```

## 2. Simple Example

Imagine we have a university document (e.g. the unified bachelor's program regulations) and
the user asks how many hours are required for graduation. The LLM might not know your
university's specific rule, so we do:
`User Question → Retriever → University Document → Relevant Paragraph → LLM → Answer`.

## 3. Normal RAG Pipeline

```
             ┌──────────────┐
             │ User Question│
             └──────┬───────┘
                    ↓
              ┌───────────┐
              │ Retriever │
              └─────┬─────┘
                    ↓
               Documents
                    ↓
              ┌───────────┐
              │    LLM    │
              └─────┬─────┘
                    ↓
                 Answer
```

## 4. Where Does LangGraph Come In?

LangGraph allows us to represent each step as a node. For example: `START → Retrieve →
Generate → END`. Very simple. But we can make it smarter:

```
START
  ↓
Retrieve
  ↓
Are documents relevant?
  ↓
 ┌──────────────┐
 NO             YES
 ↓               ↓
Rewrite         Generate
Question          ↓
 ↓              Answer
Retrieve
```

Now LangGraph becomes very useful.

## 5. RAG as a Graph

Let's create `START → retrieve → generate → END`. Our graph has two nodes: `retrieve()` and
`generate()`.

## 6. State

Our state needs to store `question`, `documents`, `answer`.

```python
from typing_extensions import TypedDict


class State(TypedDict):
    question: str
    documents: list
    answer: str
```

## 7. Retrieval Node

Let's create a very simple retriever. For learning, we'll use a fake document collection:

```python
documents = [
    "Python is a programming language.",
    "LangGraph is a framework for building stateful AI workflows.",
    "RAG retrieves relevant documents before generating an answer."
]
```

Our retrieval node:

```python
def retrieve(state: State):

    question = state["question"]

    relevant_docs = []

    for doc in documents:
        if "LangGraph" in question and "LangGraph" in doc:
            relevant_docs.append(doc)

        elif "Python" in question and "Python" in doc:
            relevant_docs.append(doc)

        elif "RAG" in question and "RAG" in doc:
            relevant_docs.append(doc)

    return {"documents": relevant_docs}
```

This is intentionally simple. In a real system you'd use **Embeddings + Vector DB +
Retriever**.

## 8. Generation Node

Now our LLM uses the retrieved documents.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
```

Then:

```python
def generate(state: State):

    question = state["question"]
    documents = state["documents"]

    context = "\\n\\n".join(documents)

    prompt = f\"\"\"
Answer the question using only the context.

Context:
{context}

Question:
{question}
\"\"\"

    response = llm.invoke(prompt)

    return {"answer": response.content}
```

## 9–10. Build, Compile, and Run the Graph

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()
```

Ask:

```python
result = app.invoke({"question": "What is LangGraph?"})

print(result["answer"])
```

The flow is: `Question → retrieve() → documents → generate() → answer`.

## 11. This Is RAG + LangGraph

You've just created:

```
             LangGraph
                 │
                 ↓
            User Question
                 │
                 ↓
             Retriever
                 │
                 ↓
              Context
                 │
                 ↓
                LLM
                 │
                 ↓
               Answer
```

## 12–13. But Real RAG Is More Complicated

A production RAG system might look like:

```
User
 ↓
Question Analysis
 ↓
Query Rewrite
 ↓
Hybrid Retrieval
 ├── Dense Search
 └── BM25
 ↓
RRF
 ↓
Reranker
 ↓
Top Documents
 ↓
LLM
 ↓
Answer
```

And this is exactly where LangGraph becomes powerful — you can turn each operation into a
node. LangGraph can orchestrate this entire process.

## 14. Why LangGraph Is Useful for RAG

A simple LangChain RAG chain might just be `Retrieve → Generate`. But what if retrieval
fails? LangGraph lets you do:

```
Retrieve
 ↓
Relevant?
 ↙       ↘
NO       YES
 ↓         ↓
Rewrite   Generate
Query
 ↓
Retrieve
```

This is much more powerful.

## 15. Conditional RAG

Let's add a decision.

```python
def check_documents(state: State):

    if not state["documents"]:
        return "rewrite"

    return "generate"
```

Then:

```python
graph.add_conditional_edges(
    "retrieve",
    check_documents,
    {"rewrite": "rewrite", "generate": "generate"}
)
```

Now our graph can make a decision.

## 16. Query Rewriting

Add a node:

```python
def rewrite(state: State):

    question = state["question"]

    prompt = f\"\"\"
Rewrite this question so that it is
better for document retrieval.

Question:
{question}
\"\"\"

    response = llm.invoke(prompt)

    return {"question": response.content}
```

Then connect: `Retrieve → Relevant? → NO → Rewrite → Retrieve`. Notice the loop!

## 17. Now We Have an Agentic RAG Pattern

Our graph becomes:

```
                  START
                    ↓
                Retrieve
                    ↓
               Relevant?
                ↙     ↘
              NO       YES
              ↓          ↓
           Rewrite    Generate
              ↓          ↓
           Retrieve     END
```

This is sometimes called an **agentic RAG pattern** because the system can dynamically
decide what to do based on the retrieval result.

## 18. Why This Is Better

Suppose the user asks *"What is the graduation requirement?"* and the retriever returns
poor results. A basic RAG system might simply generate an answer from bad context — that's
dangerous. Our LangGraph system can do: `Poor retrieval → Rewrite query → Retrieve again →
Better documents → Generate`. Much safer.

## 19. RAG + Human-in-the-Loop

We can even combine today's and previous lessons. Imagine the system is uncertain:

```
Retrieve
 ↓
Confidence low
 ↓
⏸️ Human review
 ↓
Approved?
 ↙      ↘
YES      NO
 ↓        ↓
Generate  Rewrite
```

Now we have: **RAG + LangGraph + Human-in-the-Loop.** This is becoming a real production
architecture.

## 20. RAG + Tools + Memory

Eventually, your agent could look like:

```
                       User
                        ↓
                       LLM
                        ↓
               ┌────────┼────────┐
               ↓        ↓        ↓
             RAG      Search   Calculator
               ↓        ↓        ↓
               └────────┼────────┘
                        ↓
                       LLM
                        ↓
                      Answer
                        ↓
                   Checkpoint
```

This is the kind of architecture you can build with LangGraph.

## 🧠 Most Important Concept Today

Don't think of LangGraph as a replacement for RAG. Instead: **LangGraph is the orchestration
layer that controls how the RAG system runs.** For example: Retriever → retrieval
component, Vector DB → storage/retrieval component, LLM → generation component, LangGraph →
controls the workflow.

## 21. LangChain vs LangGraph

**LangChain** provides components such as LLMs, Embeddings, Retrievers, Vector stores,
Tools, Prompts, Document loaders.

**LangGraph** controls complex workflows: State, Nodes, Edges, Loops, Branches, Memory,
Checkpoints, Human approval, Agents.

Together: `LangChain + LangGraph → Powerful AI application`.

## 🧪 Exercise

Design this graph on paper: a user asks a question about a university regulation. Your
system should retrieve documents, check whether documents are relevant, if not relevant →
rewrite the query and retrieve again, if relevant → generate an answer. Draw:
`START → ? → ? → (branches) → ?`. Try to fill in the nodes yourself.

## 🎯 One-Sentence Summary

LangGraph lets you turn a simple RAG pipeline into a stateful, conditional, looping RAG
workflow.
""",
            "order": 16,
            "estimated_minutes": 60,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Build the basic retrieve -> generate RAG graph",
                "description": (
                    "Using the fake `documents` list from the lesson, implement `retrieve` and "
                    "`generate` nodes exactly as described, wire START -> retrieve -> generate -> "
                    "END, compile, and invoke with the question \"What is LangGraph?\". Print "
                    "both the retrieved `documents` and the final `answer`."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "documents = [\n"
                    "    \"Python is a programming language.\",\n"
                    "    \"LangGraph is a framework for building stateful AI workflows.\",\n"
                    "    \"RAG retrieves relevant documents before generating an answer.\",\n"
                    "]\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    documents: list\n"
                    "    answer: str\n\n\n"
                    "def retrieve(state: State):\n"
                    "    # TODO: filter documents based on keyword overlap with the question\n"
                    "    pass\n\n\n"
                    "def generate(state: State):\n"
                    "    # TODO: build context from documents, prompt the LLM, return answer\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add nodes, wire edges, compile, invoke, print\n"
                ),
                "solution_code": (
                    "def retrieve(state: State):\n"
                    "    question = state[\"question\"]\n"
                    "    relevant_docs = []\n"
                    "    for doc in documents:\n"
                    "        if \"LangGraph\" in question and \"LangGraph\" in doc:\n"
                    "            relevant_docs.append(doc)\n"
                    "        elif \"Python\" in question and \"Python\" in doc:\n"
                    "            relevant_docs.append(doc)\n"
                    "        elif \"RAG\" in question and \"RAG\" in doc:\n"
                    "            relevant_docs.append(doc)\n"
                    "    return {\"documents\": relevant_docs}\n\n\n"
                    "def generate(state: State):\n"
                    "    context = \"\\n\\n\".join(state[\"documents\"])\n"
                    "    prompt = f\"Answer using only the context.\\n\\nContext:\\n{context}\\n\\nQuestion:\\n{state['question']}\"\n"
                    "    response = llm.invoke(prompt)\n"
                    "    return {\"answer\": response.content}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"retrieve\", retrieve)\n"
                    "graph.add_node(\"generate\", generate)\n"
                    "graph.add_edge(START, \"retrieve\")\n"
                    "graph.add_edge(\"retrieve\", \"generate\")\n"
                    "graph.add_edge(\"generate\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"question\": \"What is LangGraph?\", \"documents\": [], \"answer\": \"\"})\n"
                    "print(result[\"documents\"])\n"
                    "print(result[\"answer\"])\n"
                ),
                "skill_tested": ["langgraph", "rag", "retrieval"],
            },
            {
                "title": "Add the conditional rewrite loop",
                "description": (
                    "Extend the RAG graph with `check_documents` (returns \"rewrite\" if "
                    "documents is empty, else \"generate\") and a `rewrite` node that asks the "
                    "LLM to rephrase the question for better retrieval, updating "
                    "`state['question']`. Wire `retrieve` through `add_conditional_edges` to "
                    "either `rewrite` (which loops back to `retrieve`) or `generate` (which goes "
                    "to END). Test it with a question that won't match any fake document on the "
                    "first try, e.g. \"Tell me about frameworks for workflows.\", and confirm it "
                    "eventually reaches generate."
                ),
                "difficulty": DifficultyLevel.advanced,
                "starter_code": (
                    "def check_documents(state: State):\n"
                    "    # TODO: return 'rewrite' if no documents found, else 'generate'\n"
                    "    pass\n\n\n"
                    "def rewrite(state: State):\n"
                    "    # TODO: ask the LLM to rewrite state['question'] for better retrieval\n"
                    "    pass\n\n\n"
                    "# TODO: graph.add_node('rewrite', rewrite)\n"
                    "# TODO: graph.add_conditional_edges('retrieve', check_documents,\n"
                    "#     {'rewrite': 'rewrite', 'generate': 'generate'})\n"
                    "# TODO: graph.add_edge('rewrite', 'retrieve')\n"
                    "# TODO: graph.add_edge('generate', END)  (remove the old retrieve->generate edge)\n"
                ),
                "solution_code": (
                    "def check_documents(state: State):\n"
                    "    if not state[\"documents\"]:\n"
                    "        return \"rewrite\"\n"
                    "    return \"generate\"\n\n\n"
                    "def rewrite(state: State):\n"
                    "    prompt = f\"Rewrite this question so it's better for document retrieval:\\n\\n{state['question']}\"\n"
                    "    response = llm.invoke(prompt)\n"
                    "    return {\"question\": response.content}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"retrieve\", retrieve)\n"
                    "graph.add_node(\"rewrite\", rewrite)\n"
                    "graph.add_node(\"generate\", generate)\n\n"
                    "graph.add_edge(START, \"retrieve\")\n"
                    "graph.add_conditional_edges(\n"
                    "    \"retrieve\", check_documents,\n"
                    "    {\"rewrite\": \"rewrite\", \"generate\": \"generate\"}\n"
                    ")\n"
                    "graph.add_edge(\"rewrite\", \"retrieve\")\n"
                    "graph.add_edge(\"generate\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\n"
                    "    \"question\": \"Tell me about frameworks for workflows.\",\n"
                    "    \"documents\": [], \"answer\": \"\"\n"
                    "})\n"
                    "print(result[\"answer\"])\n"
                    "# NOTE: add a max-rewrite safety limit in a real system to avoid infinite loops!\n"
                ),
                "skill_tested": ["langgraph", "rag", "conditional-edges", "loops"],
            },
        ],
        "quiz": {
            "title": "RAG with LangGraph — Quiz",
            "questions": [
                {
                    "question": "What does RAG stand for and what problem does it solve?",
                    "options": [
                        "Rapid AI Generation — makes LLMs respond faster",
                        "Retrieval-Augmented Generation — gives the LLM relevant external context before it answers",
                        "Random Access Generation — picks a random document to answer from",
                        "Reasoning And Grounding — a synonym for chain-of-thought prompting",
                    ],
                    "correct": 1,
                    "explanation": "RAG retrieves relevant information and feeds it to the LLM as context, so it can answer using facts it may not otherwise know.",
                },
                {
                    "question": "In the basic RAG graph (retrieve -> generate -> END), what does the retrieve node return?",
                    "options": [
                        "The final answer",
                        "A list of documents relevant to the question, stored in state",
                        "A rewritten question",
                        "Nothing, it only prints to the console",
                    ],
                    "correct": 1,
                    "explanation": "retrieve() searches the document collection and returns matching documents into the documents field of state.",
                },
                {
                    "question": "Why does the lesson add a check_documents conditional edge after retrieve?",
                    "options": [
                        "To slow down the graph intentionally",
                        "To decide whether the retrieved documents are good enough to generate from, or whether the query should be rewritten and retried",
                        "To automatically end the graph regardless of results",
                        "To bypass the generate node entirely",
                    ],
                    "correct": 1,
                    "explanation": "check_documents routes to 'rewrite' when no documents were found, and to 'generate' otherwise, avoiding answers built on empty/poor context.",
                },
                {
                    "question": "What makes the rewrite -> retrieve pattern a 'loop' rather than just a branch?",
                    "options": [
                        "It always runs exactly once",
                        "The rewrite node's edge sends execution back to an earlier node (retrieve), which may run check_documents again",
                        "It only exists in diagrams, not in real code",
                        "Loops and branches are the same thing in LangGraph",
                    ],
                    "correct": 1,
                    "explanation": "Just like the counter example from Lesson 6, this is a loop because execution can return to retrieve multiple times before finally reaching generate.",
                },
                {
                    "question": "What is the correct mental model for LangGraph's relationship to RAG, per the lesson?",
                    "options": [
                        "LangGraph replaces the need for retrieval entirely",
                        "LangGraph is the orchestration layer that controls how the RAG system's steps run, not a replacement for retrieval/generation components",
                        "RAG cannot be implemented with LangGraph",
                        "LangGraph and RAG are unrelated technologies",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly frames LangGraph as controlling the workflow around retrieval and generation, not replacing those components.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Agentic RAG with Rewrite Loop and Safety Cap",
            "description": (
                "Build the full agentic RAG graph: retrieve -> check_documents -> "
                "(rewrite -> retrieve) or (generate -> END). Add a `rewrite_count` field to "
                "State and cap it at 3 rewrites — if check_documents would otherwise route to "
                "'rewrite' but rewrite_count >= 3, route to 'generate' anyway (even with poor "
                "context) rather than looping forever. Test with a question that matches "
                "immediately, and one crafted to force at least one rewrite before matching."
            ),
            "difficulty": DifficultyLevel.advanced,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Implement the full retrieve/check/rewrite/generate agentic RAG loop",
                "Add a safety cap on the number of rewrite attempts",
                "Verify a question that matches immediately skips the rewrite loop entirely",
                "Verify a question that initially fails eventually succeeds (or hits the cap gracefully)",
            ],
            "rubric": {
                "graph_structure": "retrieve/check_documents/rewrite/generate are correctly wired with the loop-back edge (35%)",
                "safety_cap": "rewrite_count is tracked and correctly caps the number of retries (30%)",
                "testing_immediate": "Immediate-match question is tested and skips rewriting (15%)",
                "testing_loop": "Rewrite-triggering question is tested and eventually reaches generate (20%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.5,
        },
    },
    {
        # ToolTopic fields
        "title":            "LangGraph + LangChain",
        "slug":              "langgraph-plus-langchain",
        "description":       "Clarify the relationship between LangChain (components) and LangGraph (orchestration): using LCEL chains, retrievers, and tools as LangGraph nodes.",
        "order":             17,
        "difficulty":        DifficultyLevel.intermediate,
        "estimated_hours":   1.5,
        "skill_tags":        ["langgraph", "langchain", "lcel", "architecture"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "LangGraph + LangChain",
            "content": """# 🔗 Lesson 17 — LangGraph + LangChain

Now we're going to connect the two things you've been learning. The easiest way to remember
them is: **LangChain gives you the building blocks. LangGraph controls how those blocks work
together.**

## 1. LangChain vs LangGraph

Think about building a car.

**LangChain = the parts** — 🧠 LLM, 🔧 Tools, 📄 Documents, 🔍 Retrievers, 📝 Prompts, 🗄️
Vector Stores.

**LangGraph = the engine/controller** — it decides: what happens first? what happens next?
should we loop? should we call a tool? should we ask a human? should we stop?

So: `LangChain → Components`, `LangGraph → Workflow`.

## 2. A Simple Example

Suppose we want `User Question → Retriever → LLM → Answer`. The LangChain components might
be `ChatOpenAI`, `Retriever`, `Prompt`. LangGraph controls
`START → retrieve → generate → END`.

## 3. The Architecture

```
                 LANGGRAPH
        ┌────────────────────────┐
        │                        │
        │       State            │
        │         ↓              │
        │      Retriever         │
        │         ↓              │
        │        LLM             │
        │         ↓              │
        │       Answer           │
        │                        │
        └────────────────────────┘
             ↑          ↑
             │          │
         LangChain   LangChain
         components  components
```

## 4. LangChain LLM

First, we can create an LLM using LangChain:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
```

This is a LangChain component. LangGraph doesn't replace it — it uses it.

## 5. LangChain Prompt

We can also create a prompt:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "{question}")
])
```

Now we have `Prompt + LLM`.

## 6. LangChain Runnable Chain

LangChain allows us to connect components:

```python
chain = prompt | llm
```

This means `Question → Prompt → LLM → Response`. We can invoke it:

```python
response = chain.invoke({"question": "What is LangGraph?"})
```

## 7. Put That Inside LangGraph

This is where things get interesting. We can create a LangGraph node:

```python
def chatbot(state):

    response = chain.invoke({"question": state["question"]})

    return {"answer": response.content}
```

Notice: `LangChain → chain → LangGraph → node`.

## 8–10. State, Graph, and Run

```python
from typing_extensions import TypedDict


class State(TypedDict):
    question: str
    answer: str
```

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()
```

```python
result = app.invoke({"question": "What is LangGraph?"})

print(result["answer"])
```

The architecture is: `User → LangGraph → chatbot node → LangChain chain → Prompt → LLM →
Answer`.

## 11. This Is the Key Relationship

Remember:

```
             LangGraph
                 ↓
              Node
                 ↓
             LangChain
                 ↓
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Prompt      LLM      Tool
```

LangGraph can call LangChain components from its nodes.

## 12. Add a Retriever

Now let's make it more realistic. Suppose we have `retriever = ...`, a LangChain retriever.
Our graph could have `START → retrieve → generate → END`.

## 13. Retrieval Node

```python
def retrieve(state):

    docs = retriever.invoke(state["question"])

    return {"documents": docs}
```

This node is using a LangChain retriever.

## 14. Generation Node

```python
def generate(state):

    context = "\\n\\n".join(
        doc.page_content for doc in state["documents"]
    )

    response = chain.invoke({
        "question": state["question"],
        "context": context
    })

    return {"answer": response.content}
```

Again: `LangGraph node → LangChain chain`.

## 15. The Full RAG Architecture

```
                  LangGraph
                      │
                      ↓
                    START
                      │
                      ↓
                  Retrieve
                      │
                      ↓
                  LangChain
                  Retriever
                      │
                      ↓
                   Documents
                      │
                      ↓
                  Generate
                      │
                      ↓
                  LangChain
                  Prompt + LLM
                      │
                      ↓
                    Answer
                      │
                      ↓
                     END
```

This is a very common architecture.

## 16. Add Tools

We can also use LangChain tools.

```python
from langchain_core.tools import tool


@tool
def calculate(a: int, b: int):
    \"\"\"Add two numbers.\"\"\"
    return a + b
```

Then LangGraph can use `ToolNode([calculate])`. So: `LangChain → Tool → LangGraph →
ToolNode`.

## 17. One Application Can Use Both

Imagine your academic advisor AI. You could have:

**LangChain** — Document Loader, Embedding Model, Vector Store, Retriever, Reranker, LLM,
Prompt, Tools.

**LangGraph** — Query Analysis → Retrieve → Check Relevance → Rewrite Query? → Rerank →
Generate → Human Review? → Answer.

Together:

```
       LANGGRAPH
           │
           ↓
    ┌───────────────┐
    │ Query Analysis│
    └───────┬───────┘
            ↓
      LangChain
       Retriever
            ↓
        Documents
            ↓
      LangChain
       Reranker
            ↓
      LangChain LLM
            ↓
        Answer
```

## 18. Why Not Just Use LangChain?

You might ask: *"If LangChain already has chains, why do I need LangGraph?"* For simple
workflows (`Prompt → LLM → Answer`), LangChain is often enough. But imagine:

```
Question
 ↓
Retrieve
 ↓
Relevant?
 ↙       ↘
NO       YES
 ↓         ↓
Rewrite   Rerank
 ↓         ↓
Retrieve  Generate
 ↓         ↓
 ...
```

Now you need branches, loops, state, persistence, human approval, complex agents. That's
where LangGraph shines.

## 19. LangChain Expression Language

You've probably seen this: `chain = prompt | llm`. This is called **LCEL — LangChain
Expression Language.** It lets you compose LangChain components, for example
`chain = prompt | llm | parser`. Then LangGraph can put that entire chain inside one node:
`LangGraph Node → Prompt → LLM → Parser`.

## 20. Very Important Mental Model

Don't think: LangChain OR LangGraph. Think: **LangChain + LangGraph.**

**LangChain** — what can my AI application do? Call LLM, retrieve documents, call tools,
parse output, load documents.

**LangGraph** — how should those operations happen? First retrieve → Check result → Maybe
rewrite → Call tool → Ask human → Generate answer.

## 21. Real Example

Let's design your academic advisor. User asks *"What courses do I need to graduate?"*.

**LangGraph:**

```
START
 ↓
Analyze Question
 ↓
Retrieve Documents
 ↓
Check Relevance
 ↓
Relevant?
 ↙       ↘
NO       YES
 ↓         ↓
Rewrite   Rerank
 ↓         ↓
Retrieve  Generate
 ↓         ↓
 └─────────┘
      ↓
    Answer
```

**LangChain provides:** Analyze Question → LLM, Retrieve → Retriever, Rerank →
CrossEncoder, Generate → LLM.

So: **LangChain provides the components; LangGraph orchestrates them.**

## 🧠 The Most Important Thing From This Lesson

If someone asks *"What's the difference between LangChain and LangGraph?"*, your simple
answer should be: **LangChain provides components for building LLM applications, while
LangGraph provides stateful graphs and workflows for controlling complex AI applications and
agents.** That's enough for now.

## 🧪 Exercise

Create this architecture on paper: `User → LangGraph → Retrieve → Check Documents →
Relevant? → (NO: Rewrite → Retrieve) / (YES: LLM → Answer)`. Label which parts are
LangChain and which are LangGraph. A good answer would be:

**LangGraph:** State, Nodes, Conditional edge, Loop.

**LangChain:** LLM, Retriever, Prompt.
""",
            "order": 17,
            "estimated_minutes": 50,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Wrap an LCEL chain in a LangGraph node",
                "description": (
                    "Build a `ChatPromptTemplate` with a system message ('You are a helpful AI "
                    "assistant.') and a human message template ('{question}'). Compose it with "
                    "an LLM using LCEL (`chain = prompt | llm`). Write a `chatbot` node that "
                    "calls `chain.invoke({'question': state['question']})` and returns the "
                    "answer. Wire it into a minimal graph and invoke with a test question."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.prompts import ChatPromptTemplate\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n"
                    "# TODO: build the ChatPromptTemplate\n"
                    "# TODO: chain = prompt | llm\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    answer: str\n\n\n"
                    "def chatbot(state: State):\n"
                    "    # TODO: call chain.invoke(...) and return the answer update\n"
                    "    pass\n\n\n"
                    "# TODO: build graph, add_node/add_edge x2, compile, invoke, print\n"
                ),
                "solution_code": (
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.prompts import ChatPromptTemplate\n"
                    "from langgraph.graph import StateGraph, START, END\n\n\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n\n"
                    "prompt = ChatPromptTemplate.from_messages([\n"
                    "    (\"system\", \"You are a helpful AI assistant.\"),\n"
                    "    (\"human\", \"{question}\"),\n"
                    "])\n"
                    "chain = prompt | llm\n\n\n"
                    "class State(TypedDict):\n"
                    "    question: str\n"
                    "    answer: str\n\n\n"
                    "def chatbot(state: State):\n"
                    "    response = chain.invoke({\"question\": state[\"question\"]})\n"
                    "    return {\"answer\": response.content}\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"chatbot\", chatbot)\n"
                    "graph.add_edge(START, \"chatbot\")\n"
                    "graph.add_edge(\"chatbot\", END)\n\n"
                    "app = graph.compile()\n"
                    "result = app.invoke({\"question\": \"What is LangGraph?\", \"answer\": \"\"})\n"
                    "print(result[\"answer\"])\n"
                ),
                "skill_tested": ["langgraph", "langchain", "lcel"],
            },
            {
                "title": "Label the academic-advisor architecture",
                "description": (
                    "Given the architecture 'START -> Analyze Question -> Retrieve Documents -> "
                    "Check Relevance -> Relevant? -> (NO: Rewrite -> Retrieve) / (YES: Rerank -> "
                    "Generate) -> Answer', write out each component and label it as LangGraph "
                    "(orchestration: state/nodes/edges/loop/branch) or LangChain (component: "
                    "LLM/retriever/reranker/prompt)."
                ),
                "difficulty": DifficultyLevel.beginner,
                "starter_code": (
                    "# START -> LangGraph or LangChain?\n"
                    "# Analyze Question -> LangGraph or LangChain? (which underlying piece does the work?)\n"
                    "# Retrieve Documents -> LangGraph or LangChain?\n"
                    "# Check Relevance -> LangGraph or LangChain?\n"
                    "# Relevant? branch -> LangGraph or LangChain?\n"
                    "# Rewrite -> LangGraph or LangChain?\n"
                    "# Rerank -> LangGraph or LangChain?\n"
                    "# Generate -> LangGraph or LangChain?\n"
                ),
                "solution_code": (
                    "# START -> LangGraph (entry point of the graph)\n"
                    "# Analyze Question -> LangGraph node, but internally calls an LLM (LangChain component)\n"
                    "# Retrieve Documents -> LangGraph node, internally uses a LangChain Retriever\n"
                    "# Check Relevance -> LangGraph node/logic (plain routing function)\n"
                    "# Relevant? branch -> LangGraph (conditional edge)\n"
                    "# Rewrite -> LangGraph node, internally uses an LLM (LangChain component) + loop-back edge\n"
                    "# Rerank -> LangGraph node, internally uses a LangChain CrossEncoder/reranker\n"
                    "# Generate -> LangGraph node, internally uses an LLM (LangChain component)\n"
                    "#\n"
                    "# Summary: LangGraph owns the CONTROL FLOW (nodes/edges/branches/loops);\n"
                    "# LangChain provides the actual WORKING PARTS each node calls into.\n"
                ),
                "skill_tested": ["langgraph", "langchain", "architecture"],
            },
        ],
        "quiz": {
            "title": "LangGraph + LangChain — Quiz",
            "questions": [
                {
                    "question": "What's the simplest correct summary of the LangChain vs LangGraph relationship?",
                    "options": [
                        "LangChain replaces LangGraph in newer projects",
                        "LangChain provides components (LLMs, retrievers, tools, prompts); LangGraph orchestrates how they're used in a workflow",
                        "LangGraph replaces the need for any LangChain components",
                        "They are competing, incompatible frameworks",
                    ],
                    "correct": 1,
                    "explanation": "The lesson's key mental model is components (LangChain) + orchestration (LangGraph), used together rather than as alternatives.",
                },
                {
                    "question": "What is LCEL (chain = prompt | llm)?",
                    "options": [
                        "A LangGraph-only feature for building loops",
                        "LangChain Expression Language — a way to compose LangChain components together into a runnable chain",
                        "A special type of State field",
                        "A tool decorator",
                    ],
                    "correct": 1,
                    "explanation": "LCEL lets you pipe components together (e.g. prompt | llm | parser) to form a single runnable chain.",
                },
                {
                    "question": "How does an LCEL chain typically get used inside LangGraph?",
                    "options": [
                        "It can't be used inside LangGraph at all",
                        "It's called inside a node function (e.g. chain.invoke(...)), and the node returns the result as a state update",
                        "It replaces the need for a State definition",
                        "It automatically becomes a new LangGraph node type",
                    ],
                    "correct": 1,
                    "explanation": "A LangGraph node is just a function; it can call chain.invoke(...) internally and return the output as part of the state update.",
                },
                {
                    "question": "According to the lesson, when is plain LangChain (without LangGraph) often enough?",
                    "options": [
                        "Never — LangGraph is always required",
                        "For simple, linear workflows like Prompt -> LLM -> Answer with no branching, looping, or persistence needed",
                        "Only when using tools",
                        "Only for RAG applications",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly says LangChain is often enough for simple chains, and LangGraph 'shines' once you need branches, loops, state, persistence, or human approval.",
                },
                {
                    "question": "In the academic advisor example, which parts are explicitly LangGraph vs LangChain?",
                    "options": [
                        "LangGraph: LLM, Retriever, Prompt. LangChain: State, Nodes, Conditional edge, Loop.",
                        "LangGraph: State, Nodes, Conditional edge, Loop. LangChain: LLM, Retriever, Prompt.",
                        "Both terms refer to the exact same set of things",
                        "Neither term applies to this example",
                    ],
                    "correct": 1,
                    "explanation": "The lesson's answer key explicitly assigns State/Nodes/Conditional edge/Loop to LangGraph, and LLM/Retriever/Prompt to LangChain.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Component-Labeled RAG Architecture Diagram",
            "description": (
                "Design (in comments/documentation, plus optionally working code) an academic-"
                "advisor-style RAG agent with the flow: START -> Analyze Question -> Retrieve -> "
                "Check Relevance -> (Rewrite -> Retrieve) or (Rerank -> Generate) -> Human "
                "Review (for low-confidence answers) -> END. For every node, explicitly note "
                "which LangChain component it wraps (LLM, Retriever, Reranker, or none) and "
                "which LangGraph mechanism connects it to the rest of the graph (normal edge, "
                "conditional edge, or loop-back edge)."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": ["Python", "LangGraph", "LangChain"],
            "objectives": [
                "Design a realistic multi-node RAG+approval architecture",
                "Correctly attribute each node to its underlying LangChain component (or none)",
                "Correctly attribute each connection to its LangGraph edge type",
                "(Optional) Implement a simplified working version with stub retriever/reranker functions",
            ],
            "rubric": {
                "architecture_design": "Flow correctly reflects retrieve/check/rewrite/rerank/generate/review stages (30%)",
                "langchain_labeling": "Each node's underlying LangChain component (or lack thereof) is correctly identified (30%)",
                "langgraph_labeling": "Each edge is correctly labeled as normal/conditional/loop-back (25%)",
                "implementation": "Optional stub implementation runs end-to-end without errors (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Building a Real AI Agent",
        "slug":              "building-a-real-ai-agent",
        "description":       "Assemble everything so far into a full research-assistant agent: multiple tools, tool calling, conditional routing, loops, and memory in one architecture.",
        "order":             18,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   2.5,
        "skill_tags":        ["langgraph", "agents", "tools", "memory", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Building a Real AI Agent",
            "content": """# 🤖 Lesson 18 — Build a Real AI Agent

Now we stop learning separate pieces and put them together. By the end of this lesson,
you'll understand the architecture of a real LangGraph agent.

## 1. What Are We Building?

We'll build a simple **Research Assistant Agent**. It can: 💬 talk to the user, 🧮
calculate numbers, 🔍 search for information using a tool, 🔄 decide which tool to use, 🧠
remember the conversation, 💾 save its state.

The architecture:

```
                    USER
                      ↓
                 ┌─────────┐
                 │   LLM   │
                 └────┬────┘
                      ↓
                 Need a tool?
                  ↙       ↘
                NO         YES
                ↓            ↓
               END        ToolNode
                             ↓
                           Result
                             ↓
                            LLM
                             ↓
                         Need tool?
                         ↙       ↘
                       NO         YES
                       ↓            ↓
                      END        ToolNode
```

## 2. Our Tools

We'll create two tools.

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers.\"\"\"
    return a * b
```

Now the agent has `Tools → add, multiply`.

## 3. Create the LLM

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
```

Then connect the tools:

```python
tools = [add, multiply]

llm_with_tools = llm.bind_tools(tools)
```

Now the LLM knows: *"I can use add() and multiply()."*

## 4. Create the State

Our agent needs conversation history.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Remember: `State → messages → conversation history`.

## 5. Create the Agent Node

The agent node calls the LLM.

```python
def agent(state: State):

    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}
```

This is the brain of our agent.

## 6. Create the Tool Node

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

This handles `AI tool call → Execute Python function → Return result`.

## 7. Create the Decision

We need to determine whether the agent wants a tool.

```python
def should_continue(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

Remember this pattern: tool requested? YES → tools, NO → END.

## 8–9. Build & Connect the Graph

```python
from langgraph.graph import StateGraph, START, END


graph = StateGraph(State)

graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)

graph.add_edge("tools", "agent")
```

Our graph:

```
                 ┌───────────┐
                 │   Tools   │
                 └─────┬─────┘
                       │
                       ↓
START → Agent → Tool? → Agent
           │
           ↓
          END
```

## 10. Add Memory

Now let's add the checkpointer.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)
```

Now the agent can maintain state between calls.

## 11. Create a Conversation

```python
config = {
    "configurable": {
        "thread_id": "research-1"
    }
}
```

This identifies the conversation.

## 12–13. Run the Agent & Print the Answer

```python
from langchain_core.messages import HumanMessage


result = app.invoke(
    {"messages": [HumanMessage(content="What is 20 multiplied by 5?")]},
    config=config
)

print(result["messages"][-1].content)
```

The agent might do `User → Agent → multiply(20, 5) → 100 → Agent → Answer`. You should get
something similar to *"20 multiplied by 5 is 100."*

## 14. Let's Follow Every Step

This is the part you should really understand. User asks *"What is 20 × 5?"*:

1. `START → Agent`
2. LLM thinks: *"I need multiplication."*
3. LLM generates `multiply(a=20, b=5)`
4. Conditional edge sees `last_message.tool_calls`, so `Agent → Tools`
5. ToolNode executes `multiply(20, 5)` → `100`
6. Tool result goes back: `Tools → Agent`
7. LLM produces *"20 × 5 = 100."*
8. No more tool calls: `Agent → END`

## 15. Now Multiple Tools

Ask *"What is 10 + 20?"* — the agent can choose `add(10, 20)`. Ask *"What is 10 × 20?"* —
it can choose `multiply(10, 20)`. The LLM decides which tool is appropriate.

## 16. Multiple Tool Calls

Here's where agents become more interesting. Suppose you ask *"Calculate (10 × 5) + 20."*
The agent could do: `Agent → multiply(10, 5) → 50 → Agent → add(50, 20) → 70 → Agent →
Final Answer`. The graph loops: `Agent → Tool → Agent → Tool → Agent → END`. This is a real
agent loop.

## 17. Add a Simple Search Tool

For learning, we can create a fake search tool:

```python
@tool
def search_information(query: str) -> str:
    \"\"\"Search for information.\"\"\"

    knowledge = {
        "langgraph": "LangGraph is a framework for building stateful AI workflows.",
        "langchain": "LangChain provides components for building LLM applications."
    }

    return knowledge.get(query.lower(), "No information found.")
```

Add it:

```python
tools = [add, multiply, search_information]

llm_with_tools = llm.bind_tools(tools)
```

Now the agent has `Tools → add, multiply, search_information`.

## 18. The Agent Can Choose Different Paths

*"What is 20 × 5?"* → `Agent → multiply → Agent → Answer`. *"What is LangGraph?"* →
`Agent → search_information → Agent → Answer`. *"Hello!"* → `Agent → Answer`. The workflow
changes dynamically — that's why it's an agent.

## 19. Add Memory

Suppose the user says *"My name is Mohammad."* then later *"What is my name?"*. Because
we're using `checkpointer = InMemorySaver()` and `thread_id = "research-1"`, the
conversation state can be maintained: `Message 1 → Checkpoint → Message 2 → Checkpoint`.

## 20. Our Complete Architecture

```
                         USER
                           ↓
                    ┌────────────┐
                    │    State   │
                    └─────┬──────┘
                          ↓
                     ┌─────────┐
                     │   LLM   │
                     └────┬────┘
                          ↓
                     Tool needed?
                     ↙          ↘
                   NO            YES
                   ↓               ↓
                  END          ToolNode
                                  ↓
                         ┌────────┼────────┐
                         ↓        ↓        ↓
                        Add    Multiply   Search
                         │        │        │
                         └────────┼────────┘
                                  ↓
                                 LLM
                                  ↓
                             Tool needed?
                              ↙       ↘
                            NO         YES
                            ↓           ↓
                           END        Tool
```

And around the whole thing: `Checkpointer → Thread Memory`.

## 21. This Is a Real Agent Architecture

You've now combined: State, LLM, Messages, Tools, Tool Calling, Conditional Routing, Loops,
Memory, Checkpoints. That's a major milestone.

## 22. What About RAG?

We can add RAG as another tool:

```python
@tool
def search_university_rules(query: str) -> str:
    \"\"\"Search university regulations.\"\"\"
    ...
```

Now your agent can decide: `Question → LLM → Need university information? → YES → RAG Tool
→ Retrieved context → LLM → Answer`. Your academic advisor can therefore become an agentic
RAG system.

## 23. Your Academic Advisor Architecture

A more realistic version of your project could look like:

```
                         USER
                           ↓
                      ┌────────┐
                      │ Agent  │
                      └───┬────┘
                          ↓
                    What do I need?
                    ↙      ↓       ↘
                  RAG    Calculator  General
                   ↓        ↓         ↓
              Retrieval   Result     LLM
                   ↓        │         │
                   └────────┼─────────┘
                            ↓
                           LLM
                            ↓
                         Answer
```

And: `Checkpointer → Conversation`. This is a very strong architecture for an academic
assistant.

## 24. One Important Warning

Don't build every application as an agent. For example, if your application always does
`Question → Retrieve → Generate`, you don't necessarily need an agent — a simple graph
(`START → Retrieve → Generate → END`) is enough. Use an agent when the system genuinely
needs dynamic decision-making.

## 🧠 The Big Lesson

The most important thing today is not the code. It's this:

```
                AGENT
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
      LLM        Tools      State
       │          │          │
       └──────────┼──────────┘
                  ↓
             Decision
                  ↓
                Loop
                  ↓
              Final Answer
```

If you understand that architecture, you understand the core of LangGraph agents.

## 🧪 Challenge

Try to design an agent for your academic advisor. Give it these tools:
`search_regulations()`, `calculate_gpa()`, `search_courses()`. Then ask *"What courses do I
need, and what would my GPA be if I get A in all of them?"* The agent might need to: 1)
search courses, 2) search regulations, 3) calculate GPA, 4) generate answer. Think about how
the graph would loop through these tools.
""",
            "order": 18,
            "estimated_minutes": 75,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Build the full research assistant agent",
                "description": (
                    "Implement the complete agent from the lesson: add, multiply, and "
                    "search_information tools, an agent node using llm_with_tools, a ToolNode, "
                    "should_continue routing, the loop-back edge, and a checkpointer with "
                    "thread_id='research-1'. Test all three paths: a math question, a "
                    "search_information question, and a plain greeting with no tool needed. "
                    "Print the final answer for each."
                ),
                "difficulty": DifficultyLevel.advanced,
                "starter_code": (
                    "from typing import Annotated\n"
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.tools import tool\n"
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.graph.message import add_messages\n"
                    "from langgraph.prebuilt import ToolNode\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n\n\n"
                    "# TODO: define add, multiply, search_information tools\n"
                    "# TODO: llm, llm_with_tools, State, agent node, tool_node, should_continue\n"
                    "# TODO: build graph, checkpointer, compile, config with thread_id\n"
                    "# TODO: test with a math question, a search question, and a greeting\n"
                ),
                "solution_code": (
                    "from typing import Annotated\n"
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.tools import tool\n"
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.graph.message import add_messages\n"
                    "from langgraph.prebuilt import ToolNode\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n\n\n"
                    "@tool\n"
                    "def add(a: int, b: int) -> int:\n"
                    "    \"\"\"Add two numbers.\"\"\"\n"
                    "    return a + b\n\n\n"
                    "@tool\n"
                    "def multiply(a: int, b: int) -> int:\n"
                    "    \"\"\"Multiply two numbers.\"\"\"\n"
                    "    return a * b\n\n\n"
                    "@tool\n"
                    "def search_information(query: str) -> str:\n"
                    "    \"\"\"Search for information.\"\"\"\n"
                    "    knowledge = {\n"
                    "        \"langgraph\": \"LangGraph is a framework for building stateful AI workflows.\",\n"
                    "        \"langchain\": \"LangChain provides components for building LLM applications.\",\n"
                    "    }\n"
                    "    return knowledge.get(query.lower(), \"No information found.\")\n\n\n"
                    "tools = [add, multiply, search_information]\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n"
                    "llm_with_tools = llm.bind_tools(tools)\n\n\n"
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n\n\n"
                    "def agent(state: State):\n"
                    "    response = llm_with_tools.invoke(state[\"messages\"])\n"
                    "    return {\"messages\": [response]}\n\n\n"
                    "tool_node = ToolNode(tools)\n\n\n"
                    "def should_continue(state: State):\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    if last_message.tool_calls:\n"
                    "        return \"tools\"\n"
                    "    return \"end\"\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"agent\", agent)\n"
                    "graph.add_node(\"tools\", tool_node)\n"
                    "graph.add_edge(START, \"agent\")\n"
                    "graph.add_conditional_edges(\"agent\", should_continue, {\"tools\": \"tools\", \"end\": END})\n"
                    "graph.add_edge(\"tools\", \"agent\")\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n"
                    "config = {\"configurable\": {\"thread_id\": \"research-1\"}}\n\n"
                    "for q in [\"What is 20 multiplied by 5?\", \"What is LangGraph?\", \"Hello!\"]:\n"
                    "    r = app.invoke({\"messages\": [HumanMessage(content=q)]}, config=config)\n"
                    "    print(q, \"->\", r[\"messages\"][-1].content)\n"
                ),
                "skill_tested": ["langgraph", "agents", "tools", "memory"],
            },
            {
                "title": "Multi-tool-call question",
                "description": (
                    "Using the full agent from the lesson, ask \"Calculate (10 times 5) plus "
                    "20.\" and print the full messages list (not just the final answer) to show "
                    "the sequence of tool calls (multiply, then add) that led to the answer. "
                    "Count how many times the 'tools' node ran by counting ToolMessage entries "
                    "in the result."
                ),
                "difficulty": DifficultyLevel.advanced,
                "starter_code": (
                    "# TODO: invoke the agent with \"Calculate (10 times 5) plus 20.\"\n"
                    "# TODO: print the full messages list\n"
                    "# TODO: count ToolMessage instances in the result\n"
                ),
                "solution_code": (
                    "from langchain_core.messages import ToolMessage, HumanMessage\n\n"
                    "result = app.invoke(\n"
                    "    {\"messages\": [HumanMessage(content=\"Calculate (10 times 5) plus 20.\")]},\n"
                    "    config=config\n"
                    ")\n\n"
                    "for m in result[\"messages\"]:\n"
                    "    print(type(m).__name__, \"->\", getattr(m, \"content\", None), getattr(m, \"tool_calls\", None))\n\n"
                    "tool_message_count = sum(1 for m in result[\"messages\"] if isinstance(m, ToolMessage))\n"
                    "print(\"Number of tool executions:\", tool_message_count)  # expect 2 (multiply, then add)\n"
                ),
                "skill_tested": ["langgraph", "agents", "multi-step", "debugging"],
            },
        ],
        "quiz": {
            "title": "Building a Real AI Agent — Quiz",
            "questions": [
                {
                    "question": "In the research assistant agent, what does the 'agent' node do?",
                    "options": [
                        "It only executes tools",
                        "It calls llm_with_tools with the current messages and returns the LLM's response as a state update",
                        "It defines the State schema",
                        "It only handles memory/checkpointing",
                    ],
                    "correct": 1,
                    "explanation": "The agent node is the 'brain' — it invokes the tool-aware LLM and adds its response to messages.",
                },
                {
                    "question": "Why does the agent need llm_with_tools instead of the plain llm?",
                    "options": [
                        "There's no real difference",
                        "Only llm_with_tools knows which tools exist and can produce tool_calls when appropriate",
                        "llm_with_tools is required for memory to work",
                        "llm_with_tools disables looping",
                    ],
                    "correct": 1,
                    "explanation": "bind_tools() is what equips the model to request tool use; without it, the LLM could never trigger the tools path.",
                },
                {
                    "question": "When the user asks a math question followed later by a search question in the SAME thread, why can the agent choose the right tool each time?",
                    "options": [
                        "Because there's a hardcoded if/else for each question type",
                        "Because the LLM inspects the available tools' names/descriptions and the current question, deciding dynamically which (if any) tool fits",
                        "Because tools are chosen randomly",
                        "Because only one tool can ever be bound at a time",
                    ],
                    "correct": 1,
                    "explanation": "The LLM dynamically decides per-question which tool (if any) is appropriate, based on tool descriptions — that's the core of agent behavior.",
                },
                {
                    "question": "What combination of pieces is required for the agent to remember earlier messages in the SAME thread across separate invoke() calls?",
                    "options": [
                        "Nothing extra is needed, LangGraph remembers automatically",
                        "A checkpointer (e.g. InMemorySaver) compiled into the graph, plus using the same thread_id on each call",
                        "Only bind_tools is needed",
                        "Only the ToolNode is needed",
                    ],
                    "correct": 1,
                    "explanation": "As covered in Lessons 13-14, persistence across invocations requires a checkpointer plus a consistent thread_id.",
                },
                {
                    "question": "According to the lesson's warning, when should you NOT build something as an agent?",
                    "options": [
                        "Never — everything should be an agent",
                        "When the application always follows the same fixed sequence of steps with no real decision-making needed (e.g. always Retrieve -> Generate)",
                        "Only when there are no tools available",
                        "Only when using OpenAI models",
                    ],
                    "correct": 1,
                    "explanation": "The lesson explicitly says a simple fixed graph is enough when the flow never actually needs to vary — agents are for genuine dynamic decision-making.",
                },
            ],
            "passing_score": 75,
        },
        "project": {
            "title": "Academic Advisor Agent (Challenge Project)",
            "description": (
                "Implement the lesson's challenge: build an agent with three tools — "
                "search_regulations(query), calculate_gpa(grades), and search_courses(query) — "
                "each returning realistic stub data. Wire the full agent graph (agent, "
                "ToolNode, should_continue, loop-back edge, checkpointer). Test it with the "
                "question \"What courses do I need, and what would my GPA be if I get A in all "
                "of them?\" and print the full sequence of tool calls the agent makes to answer "
                "it. Reflect in a short comment on how many tools the agent actually chose to "
                "use and whether the order matched your expectations."
            ),
            "difficulty": DifficultyLevel.advanced,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Implement 3 domain-specific stub tools with clear docstrings",
                "Assemble the complete agent graph (agent/tools/routing/loop/checkpointer)",
                "Test a question that plausibly requires multiple tools in sequence",
                "Inspect and reflect on the actual tool-call sequence chosen by the LLM",
            ],
            "rubric": {
                "tool_implementation": "All 3 tools are implemented with clear docstrings and reasonable stub logic (25%)",
                "graph_assembly": "Full agent graph correctly wires agent/tools/routing/loop/memory (40%)",
                "testing": "The multi-part question is tested and the full message trace is printed (20%)",
                "reflection": "Thoughtful reflection on the observed tool-call sequence (15%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 3.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Debugging & Common Errors",
        "slug":              "debugging-and-common-errors",
        "description":       "A systematic method for debugging LangGraph apps (state -> node -> output -> routing), common bugs and their fixes, and production basics like checkpoints, logging, and guardrails.",
        "order":             19,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   2.0,
        "skill_tags":        ["langgraph", "debugging", "production", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Debugging & Common Errors",
            "content": """# 🐞 Lesson 19 — Debugging LangGraph & Production Basics

You're almost done! 🎉 Today we'll learn a very important skill: **how to find and fix
problems in a LangGraph application.** Knowing how to build a graph is good. Knowing how to
debug one is much more important.

## 1. First Rule: Don't Debug Everything at Once

Suppose your agent looks like `User → Agent → Retriever → Reranker → Tool → LLM → Answer`,
and the answer is wrong. Don't immediately change everything. Instead, inspect each step:
question correct? → retriever → documents correct? → reranker → ranking correct? → tool →
tool result correct? → LLM → prompt correct? **Debug one component at a time.**

## 2. Debug the State First

The state is the heart of LangGraph. If the state is wrong, everything after it can be
wrong. You can inspect the result:

```python
result = app.invoke(input_data, config=config)

print(result)
```

For example: `{"messages": [...], "documents": [...], "answer": "..."}`. Ask: *did my node
actually update the state?*

## 3. Add print() Inside Nodes

This is one of the easiest debugging techniques.

```python
def retrieve(state):

    print("QUESTION:")
    print(state["question"])

    docs = retriever.invoke(state["question"])

    print("DOCUMENTS:")
    print(docs)

    return {"documents": docs}
```

If documents are empty while the question looks correct, you know the problem is probably
retrieval, not the LLM.

## 4. Debug the Graph One Node at a Time

Imagine `START → retrieve → rerank → generate → END`. If the final answer is bad, test:
invoke the graph, inspect `result["documents"]` — if they're correct, retrieval works, so
inspect the prompt/LLM next. This prevents wasting time changing your vector database when
the actual problem is your prompt.

## 5. Common Problem #1 — Wrong State Key

You define `question: str`, `documents: list`, but your node does `state["query"]`. State
has `question`, node expects `query`. You'll get `KeyError: 'query'`. **Fix:** use the same
key, `state["question"]`.

## 6. Common Problem #2 — Node Doesn't Return State

**Wrong:**

```python
def retrieve(state):
    docs = retriever.invoke(state["question"])
```

The function doesn't return anything. **Correct:**

```python
def retrieve(state):

    docs = retriever.invoke(state["question"])

    return {"documents": docs}
```

Remember: a node should return the state updates it wants to make.

## 7. Common Problem #3 — Wrong Node Name

```python
graph.add_node("retrieve", retrieve)
```

But later:

```python
graph.add_edge(START, "retriever")
```

Notice `retrieve` vs `retriever` — these are different names. Use
`graph.add_edge(START, "retrieve")`.

## 8. Common Problem #4 — Wrong Conditional Routing

```python
def route(state):

    if state["documents"]:
        return "generate"

    return "rewrite"
```

But your graph says:

```python
graph.add_conditional_edges(
    "retrieve", route,
    {"yes": "generate", "no": "rewrite"}
)
```

The function returns `generate`/`rewrite`, but the mapping expects `yes`/`no` — they must
match. **Correct:**

```python
graph.add_conditional_edges(
    "retrieve", route,
    {"generate": "generate", "rewrite": "rewrite"}
)
```

## 9. Common Problem #5 — Agent Loops Forever

This is a very common problem: `Agent → Tool → Agent → Tool → Agent → Tool → ...` — your
agent never reaches END. Why? Because your routing condition always says `"tools"` instead
of eventually returning `"end"`.

## 10. How to Debug an Infinite Loop

Look at:

```python
def should_continue(state):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

Ask: *does `last_message.tool_calls` ever become empty?* If not, your agent may continue
forever.

## 11. Add a Maximum Number of Steps

For production agents, it's a good idea to have a safety limit: `Agent → Tool → Agent →
Tool → Agent → MAX STEPS → STOP`. This protects you from runaway workflows.

## 12. Common Problem #6 — Tool Isn't Called

You ask *"Calculate 10 × 20"* but the LLM just answers `200` without using the calculator.
Possible reasons: **tool wasn't bound** (you forgot `llm.bind_tools(tools)`), **tool
description is unclear** (the docstring helps the model understand when to use the tool), or
**wrong model/tool support** (not every model behaves identically with tool calling).

## 13. Common Problem #7 — Tool Returns Wrong Data

Suppose `calculate_gpa(...)` returns `None`. The LLM can't magically fix that. Debug the
tool independently:

```python
result = calculate_gpa.invoke({"grades": [...]})

print(result)
```

Make sure the tool works before putting it inside the graph.

## 14. Common Problem #8 — Memory Doesn't Work

You expect the agent to remember *"My name is Mohammad"* later, but it says *"I don't
know."* Check: did you use a checkpointer (`checkpointer = InMemorySaver()`)? Did you
compile with it (`app = graph.compile(checkpointer=checkpointer)`)? Did you use the SAME
`thread_id`? First call `thread_id = "chat-1"`, second call must also be `"chat-1"`, not
`"chat-2"`, because those represent different conversations.

## 15. Common Problem #9 — RAG Gives Bad Answers

This is especially important for your type of project. Suppose `Question → Retriever →
Wrong documents → LLM → Wrong answer`. The first thing you should inspect is
`print(documents)`. Don't immediately blame the LLM — ask *did the retriever return the
right information?* If not, investigate chunking, embedding, query, vector DB, top-k,
reranker.

## 16. RAG Debugging Checklist

When RAG produces a bad answer, check in this order: 1) is the question correct? 2) are the
retrieved documents relevant? 3) is the reranker ranking correctly? 4) is the context
actually passed to the LLM? 5) is the prompt correct? 6) is the LLM following the prompt?
This order is important.

## 17. Debugging With Graph Visualization

LangGraph graphs can also be visualized:

```python
print(app.get_graph().draw_ascii())
```

You may see something like:

```
       __start__
           |
         agent
        /     \\
     tools    __end__
       |
     agent
```

This is extremely useful for finding routing mistakes.

## 18. Debugging the Graph Architecture

Suppose you intended `START → Agent → Tools → Agent → END`, but your graph actually looks
like two disconnected pieces: `START → Agent → END` and a separate, unreachable
`Tools → Agent`. A visualization makes this much easier to spot.

## 19. Production Concept #1 — Don't Use InMemorySaver

`InMemorySaver()` is excellent for learning, but it stores data in memory — if your
application restarts, that memory is gone. For production, you generally want a persistent
checkpointer backed by a database/storage system supported by your LangGraph setup. Think:
**Development: InMemorySaver. Production: Persistent checkpointer.**

## 20. Production Concept #2 — Environment Variables

Don't write API keys directly in your code.

❌ Bad: `api_key = "sk-xxxxxxxx"`

Use environment variables:

```bash
OPENAI_API_KEY=...
```

```python
import os

api_key = os.environ["OPENAI_API_KEY"]
```

Even better, use your framework/provider's standard environment configuration.

## 21. Production Concept #3 — Logging

Instead of only `print("hello")`, real applications should have structured logging, for
example:

```
INFO  Starting graph
INFO  Retrieving documents
INFO  Retrieved 8 documents
INFO  Calling reranker
INFO  Generating answer
INFO  Graph completed
```

This helps you understand what happened when something fails.

## 22. Production Concept #4 — Timeouts

Imagine a tool calls an external API and it never responds — your graph could remain stuck.
Use appropriate timeouts, retries, and error handling for external services.

## 23. Production Concept #5 — Handle Tool Errors

Suppose `calculate_gpa()` receives invalid input. Instead of crashing the entire
application: tool error → agent sees error → agent asks for clarification, e.g. *"I need
your completed credit hours to calculate the GPA."* That's much better than a raw
`500 Internal Server Error`.

## 24. Production Concept #6 — Validate Important Outputs

Don't blindly trust LLM output. If your application expects
`{"course_code": "CSE251", "credits": 3}`, validate it: `LLM → Structured output →
Validation → Application`, not `LLM → Trust everything`.

## 25. Production Concept #7 — Don't Give Agents Too Much Power

This is extremely important. If your agent has `delete_database()`, `send_money()`,
`send_email()`, don't automatically let it execute everything — use human approval,
permissions, validation, restricted tools. Remember our Human-in-the-Loop lesson:
`Agent → Dangerous action → ⏸️ Human approval → Execute`.

## 26. Production Architecture

A more realistic production LangGraph system might look like:

```
                         USER
                           ↓
                     API / Backend
                           ↓
                       LangGraph
                           ↓
                    ┌─────────────┐
                    │    State    │
                    └──────┬──────┘
                           ↓
                         Agent
                      ↙    ↓    ↘
                   RAG    Tools  Search
                    ↓       ↓      ↓
                    └───────┼──────┘
                            ↓
                           LLM
                            ↓
                     Validation
                            ↓
                     Human Approval?
                       ↙          ↘
                     YES           NO
                      ↓             ↓
                   Execute        Stop
                      ↓
                    Answer
```

And alongside it: `Persistent Checkpointer → Threads → History`.

## 27. The Golden Debugging Method

Whenever something breaks: 1) check the input — *what did I send?* 2) check the state —
*what is inside state?* 3) check the node — *did the node execute?* 4) check the output —
*what did the node return?* 5) check routing — *where did the graph go next?* 6) check
external components — retriever? tool? API? LLM? 7) check the final answer. This gives you:
`Input → State → Node → Output → Routing → External component → Final result`. Don't
randomly change code.

## 🧠 The Most Important Lesson

When debugging LangGraph, think in terms of: **STATE → NODE → OUTPUT → ROUTING.** For every
node, ask: what came in? what did the node do? what came out? where did the graph go next?
If you can answer those four questions, most LangGraph bugs become much easier to find.

## 🧪 Mini Challenge

Imagine your graph is `START → Agent → Tool? → (YES: Tool → Agent) / (NO: END)`, but your
application keeps running forever. What should you check first?

**Answer:** Check the routing function `should_continue`, specifically whether
`last_message.tool_calls` ever becomes empty. You want the graph to eventually reach END.
""",
            "order": 19,
            "estimated_minutes": 65,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Find and fix 4 bugs",
                "description": (
                    "Below are 4 broken code snippets, each containing exactly one of the bugs "
                    "described in the lesson (wrong state key, node not returning state, "
                    "mismatched node name, or mismatched conditional-edge mapping). For each, "
                    "identify the bug and write the corrected version."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "# Bug 1\n"
                    "class State(TypedDict):\n"
                    "    question: str\n\n"
                    "def node1(state: State):\n"
                    "    return {\"query\": \"something\"}  # <- what's wrong here?\n\n\n"
                    "# Bug 2\n"
                    "def node2(state):\n"
                    "    result = do_something(state[\"question\"])\n"
                    "    # <- what's missing here?\n\n\n"
                    "# Bug 3\n"
                    "graph.add_node(\"fetch_data\", fetch_data)\n"
                    "graph.add_edge(START, \"fetch_dat\")  # <- what's wrong here?\n\n\n"
                    "# Bug 4\n"
                    "def route(state):\n"
                    "    return \"good\" if state[\"ok\"] else \"bad\"\n\n"
                    "graph.add_conditional_edges(\"check\", route, {\"yes\": \"a\", \"no\": \"b\"})  # <- what's wrong here?\n"
                ),
                "solution_code": (
                    "# Bug 1 FIX: the node returns 'query' but State only defines 'question'.\n"
                    "# This silently adds an unused key (or errors depending on strictness) --\n"
                    "# it should match the declared field name:\n"
                    "def node1(state: State):\n"
                    "    return {\"question\": \"something\"}\n\n\n"
                    "# Bug 2 FIX: node2 never returns anything, so no state update happens.\n"
                    "def node2(state):\n"
                    "    result = do_something(state[\"question\"])\n"
                    "    return {\"result\": result}\n\n\n"
                    "# Bug 3 FIX: 'fetch_dat' is a typo of 'fetch_data' -- node names must match exactly.\n"
                    "graph.add_edge(START, \"fetch_data\")\n\n\n"
                    "# Bug 4 FIX: route() returns 'good'/'bad', but the mapping expects\n"
                    "# 'yes'/'no' -- the mapping keys must match route()'s actual return values.\n"
                    "graph.add_conditional_edges(\"check\", route, {\"good\": \"a\", \"bad\": \"b\"})\n"
                ),
                "skill_tested": ["langgraph", "debugging"],
            },
            {
                "title": "Add a max-steps safety net to an agent loop",
                "description": (
                    "Take the should_continue pattern and harden it against infinite loops: add "
                    "a `step_count` field to State, increment it inside the agent node, and "
                    "modify should_continue so it forces \"end\" once step_count reaches 6, even "
                    "if tool_calls is non-empty. Explain in a comment why this matters for "
                    "production."
                ),
                "difficulty": DifficultyLevel.intermediate,
                "starter_code": (
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n"
                    "    step_count: int\n\n\n"
                    "def agent(state: State):\n"
                    "    # TODO: call llm_with_tools, increment step_count, return both updates\n"
                    "    pass\n\n\n"
                    "def should_continue(state: State):\n"
                    "    # TODO: force 'end' if step_count >= 6, else use tool_calls as normal\n"
                    "    pass\n"
                ),
                "solution_code": (
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n"
                    "    step_count: int\n\n\n"
                    "def agent(state: State):\n"
                    "    response = llm_with_tools.invoke(state[\"messages\"])\n"
                    "    return {\n"
                    "        \"messages\": [response],\n"
                    "        \"step_count\": state.get(\"step_count\", 0) + 1,\n"
                    "    }\n\n\n"
                    "def should_continue(state: State):\n"
                    "    if state.get(\"step_count\", 0) >= 6:\n"
                    "        return \"end\"  # safety net: stop even if the LLM keeps requesting tools\n\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    if last_message.tool_calls:\n"
                    "        return \"tools\"\n"
                    "    return \"end\"\n\n\n"
                    "# This matters because a buggy prompt, a confused model, or an\n"
                    "# unexpected tool result could otherwise cause the agent to loop\n"
                    "# indefinitely, burning API calls and never returning a response --\n"
                    "# a hard step cap guarantees termination regardless of model behavior.\n"
                ),
                "skill_tested": ["langgraph", "debugging", "production", "loops"],
            },
        ],
        "quiz": {
            "title": "Debugging & Common Errors — Quiz",
            "questions": [
                {
                    "question": "What is the recommended first step when a LangGraph app produces a wrong answer?",
                    "options": [
                        "Immediately rewrite the entire graph",
                        "Debug the state first, and inspect it one node/component at a time rather than changing everything at once",
                        "Switch to a different LLM provider",
                        "Delete the checkpointer",
                    ],
                    "correct": 1,
                    "explanation": "The lesson stresses debugging state and individual components incrementally, rather than making sweeping changes blindly.",
                },
                {
                    "question": "What bug does this cause: State defines 'documents', but a node writes state['docs'] instead?",
                    "options": [
                        "No bug, LangGraph automatically renames fields",
                        "A key mismatch bug — later nodes expecting 'documents' won't see the update, since it was written under 'docs'",
                        "The graph refuses to compile",
                        "It silently deletes the State class",
                    ],
    "correct": 1,
                    "explanation": "This is the 'wrong state key' bug from the lesson — mismatched keys mean the intended field is never actually updated.",
                },
                {
                    "question": "Why would an agent loop forever according to the lesson?",
                    "options": [
                        "Because add_conditional_edges is deprecated",
                        "Because the routing function keeps returning 'tools' and never returns 'end', e.g. tool_calls never becomes empty",
                        "Because the checkpointer is missing",
                        "Because too many tools were bound",
                    ],
                    "correct": 1,
                    "explanation": "An infinite loop happens when the stopping condition in should_continue is never satisfied.",
                },
                {
                    "question": "Why is InMemorySaver discouraged for production use?",
                    "options": [
                        "It's slower than other checkpointers",
                        "It only stores state in memory, so a restart of the application loses all saved state",
                        "It cannot be used with thread_id",
                        "It doesn't support tool calling",
                    ],
                    "correct": 1,
                    "explanation": "In-memory storage doesn't survive process restarts, which is unacceptable for most production systems.",
                },
                {
                    "question": "What does the 'golden debugging method' (STATE -> NODE -> OUTPUT -> ROUTING) encourage you to do?",
                    "options": [
                        "Randomly try different fixes until something works",
                        "Systematically trace what came in, what the node did, what came out, and where the graph routed next, for each node in question",
                        "Only ever check the final LLM output",
                        "Avoid using print statements",
                    ],
                    "correct": 1,
                    "explanation": "This four-question framework gives a structured way to isolate exactly where a bug is introduced in the pipeline.",
                },
            ],
            "passing_score": 70,
        },
        "project": {
            "title": "Debug-Ready Agent Wrapper",
            "description": (
                "Take any tool-calling agent graph you've built in this course (e.g. from "
                "Lesson 18) and add production-minded hardening: (1) a step_count safety cap in "
                "should_continue, (2) print()-based tracing inside the agent and tools nodes "
                "showing input/output, (3) a try/except around tool execution that returns a "
                "friendly clarification message instead of crashing on bad input, and (4) a "
                "short README-style comment block explaining, step by step, how you would "
                "debug this agent if a user reported 'it never answers my question.'"
            ),
            "difficulty": DifficultyLevel.advanced,
            "tech_stack": ["Python", "LangGraph", "OpenAI"],
            "objectives": [
                "Add a hard step-count safety cap to prevent infinite loops",
                "Add clear tracing output at each node for debuggability",
                "Handle tool errors gracefully instead of crashing",
                "Document a concrete debugging procedure for this specific agent",
            ],
            "rubric": {
                "safety_cap": "step_count cap correctly forces termination (25%)",
                "tracing": "Clear, useful print-based tracing is added to key nodes (25%)",
                "error_handling": "Tool errors are caught and produce a graceful fallback message (25%)",
                "debugging_writeup": "Debugging procedure is clear, specific, and follows the lesson's method (25%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 2.0,
        },
    },
    {
        # ToolTopic fields
        "title":            "Final Project: AI Academic Assistant",
        "slug":              "final-project-ai-academic-assistant",
        "description":       "Capstone project combining everything: an agentic academic advisor with RAG, a GPA tool, a course-lookup tool, memory, and human approval for sensitive actions.",
        "order":             20,
        "difficulty":        DifficultyLevel.advanced,
        "estimated_hours":   4.0,
        "skill_tags":        ["langgraph", "langchain", "rag", "agents", "capstone", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title": "Final Project: AI Academic Assistant",
            "content": """# 🎓 Lesson 20 — Final Project: AI Academic Assistant with LangGraph

Congratulations! 🎉 You've completed the 20-lesson LangGraph roadmap. Now we're going to
build one project that combines everything you've learned. We'll keep it simple first, then
show how it can grow into a production system.

## 🎯 What Are We Building?

An **AI Academic Assistant** that can answer questions about university regulations. For
example: *"What are the requirements for graduation?"*, *"What is the credit-hour
requirement?"*, *"Calculate my GPA."*, *"Which courses are required?"*

The assistant will use: 🧠 LLM, 📚 RAG, 🔧 Tools, 🔄 LangGraph, 💾 Memory, 👤 Human
approval.

## 1. The Final Architecture

Here's the complete system:

```
                         👤 USER
                            │
                            ↓
                     ┌─────────────┐
                     │  LangGraph  │
                     └──────┬──────┘
                            │
                            ↓
                     🧠 Agent / LLM
                            │
                ┌───────────┼───────────┐
                ↓           ↓           ↓
              📚 RAG     🧮 GPA Tool   🔍 Search
                │           │           │
                └───────────┼───────────┘
                            ↓
                         🧠 LLM
                            │
                            ↓
                       Final Answer
                            │
                            ↓
                       💾 Checkpoint
```

This is the high-level system.

## 2. First: Define Our State

Everything starts with state.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):

    messages: Annotated[list, add_messages]

    documents: list

    answer: str
```

Think: `State ├── messages ├── documents └── answer`.

## 3. Why State Is Important

Every node can read and update the state. For example: `User → messages → Retriever →
documents → LLM → answer`. The state is like a shared notebook that all nodes can access.

## 4. Create the LLM

Using LangChain:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
```

Remember: LangChain provides the LLM component. LangGraph will control when we use it.

## 5. Create Our Tools

Let's create a simple GPA calculator.

```python
from langchain_core.tools import tool


@tool
def calculate_gpa(total_points: float, total_credits: float) -> float:
    \"\"\"Calculate GPA from total grade points and total credits.\"\"\"

    if total_credits == 0:
        return 0.0

    return total_points / total_credits
```

For example, `total_points = 15.4`, `credits = 4` → the tool returns `3.85`.

## 6. Add a Course Search Tool

For now, we'll use a tiny example database.

```python
COURSES = {
    "CSE251": {"name": "Machine Learning", "credits": 3},
    "CSE252": {"name": "Deep Learning", "credits": 3}
}
```

Tool:

```python
@tool
def search_course(course_code: str) -> str:
    \"\"\"Search for information about a course.\"\"\"

    course = COURSES.get(course_code.upper())

    if not course:
        return "Course not found."

    return (
        f"Course: {course_code}\\n"
        f"Name: {course['name']}\\n"
        f"Credits: {course['credits']}"
    )
```

Now we have `Tools ├── calculate_gpa └── search_course`.

## 7. Bind the Tools to the LLM

```python
tools = [calculate_gpa, search_course]

llm_with_tools = llm.bind_tools(tools)
```

Now the model knows about our tools.

## 8. Create the Agent Node

```python
def agent(state: State):

    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}
```

This is our AI brain.

## 9. Create the Tool Node

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

This node executes tools requested by the LLM.

## 10. Create the Router

We need to decide: does the LLM want a tool?

```python
def should_continue(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
```

So: `LLM → Tool call? → (YES → Tools) / (NO → END)`.

## 11–12. Build the Graph & Add the Edges

```python
from langgraph.graph import StateGraph, START, END


graph = StateGraph(State)

graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)

graph.add_edge("tools", "agent")
```

The graph is now:

```
               ┌──────────┐
               │   Agent  │
               └────┬─────┘
                    │
               Tool call?
                ↙       ↘
              YES         NO
               ↓           ↓
            Tools         END
               │
               ↓
             Agent
```

## 13. Add Memory

Now we use everything from the checkpoint lesson.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)
```

## 14. Create a Conversation

```python
config = {
    "configurable": {
        "thread_id": "student-1"
    }
}
```

Now the graph knows: `student-1 → conversation → checkpoints → messages`.

## 15–16. Run the Agent

```python
from langchain_core.messages import HumanMessage


result = app.invoke(
    {"messages": [HumanMessage(content="What is CSE251?")]},
    config=config
)
```

The agent may decide: `User → Agent → search_course("CSE251") → Tool → Agent → Answer`.

Now:

```python
result = app.invoke(
    {"messages": [HumanMessage(content="Calculate my GPA if I have 15.4 points over 4 credits.")]},
    config=config
)
```

The agent can call `calculate_gpa(15.4, 4)` → `3.85` → `Tool → Agent → Final Answer`.

## 17. Now Add RAG

This is where the project becomes much more useful. Instead of storing regulations inside
the Python code (`documents = [...]`), we use:

```
📄 University documents
        ↓
Document Loader
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Database
        ↓
Retriever
```

That's your RAG system.

## 18. RAG as a Tool

One simple architecture is to expose retrieval as a tool:

```python
@tool
def search_regulations(query: str) -> str:
    \"\"\"Search university regulations and return relevant information.\"\"\"

    # Call your retriever here
    docs = retriever.invoke(query)

    return "\\n\\n".join(doc.page_content for doc in docs)
```

Then:

```python
tools = [calculate_gpa, search_course, search_regulations]

llm_with_tools = llm.bind_tools(tools)
```

Now your agent can decide: `Question → LLM → What do I need? ├── GPA → calculate_gpa ├──
Course → search_course └── Regulation → search_regulations`.

## 19. This Is Agentic RAG

Now your architecture becomes:

```
                       USER
                         ↓
                       LLM
                         ↓
                  What do I need?
                ↙       ↓       ↘
              RAG      GPA     Course
               ↓        ↓        ↓
               └────────┼────────┘
                        ↓
                       LLM
                        ↓
                      Answer
```

This is a very useful pattern.

## 20. Add Human Approval

Suppose the agent gets a dangerous tool, `send_email()`. Don't automatically execute it.
Instead:

```
Agent
 ↓
send_email requested
 ↓
⏸️ interrupt()
 ↓
Human
 ↓
Approve?
 ↙       ↘
YES       NO
 ↓         ↓
Send     Stop
```

Now you've combined **Agent + Tools + Human-in-the-Loop.**

## 21. Add Checkpoints

The whole system can now maintain state:

```
Student
 ↓
Question 1
 ↓
💾 Checkpoint
 ↓
Question 2
 ↓
💾 Checkpoint
 ↓
Question 3
 ↓
💾 Checkpoint
```

The conversation can continue within the same thread.

## 22. Final Architecture

Now let's put everything together.

```
                         👤 USER
                            │
                            ↓
                    ┌──────────────┐
                    │   LangGraph  │
                    └──────┬───────┘
                           │
                           ↓
                     ┌───────────┐
                     │    LLM    │
                     └─────┬─────┘
                           │
                    What do I need?
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          📚 RAG       🧮 GPA Tool   📖 Course Tool
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                          LLM
                           │
                           ↓
                  Human Approval?
                    ↙          ↘
                  YES           NO
                   ↓             ↓
                Execute        Answer
                   │
                   ↓
                 Answer


                    💾
               Checkpointer
                    │
                    ↓
                 Memory
```

That's a real AI application architecture.

## 23. What You've Learned

Let's step back. You started with *"What is LangGraph?"* And now you understand:

**Core** — State, Nodes, Edges, Conditional Edges, Loops.

**LLM applications** — Messages, Prompts, LLMs, Tools, Tool Calling, Agents.

**Advanced** — Memory, Checkpoints, Human-in-the-Loop, RAG, LangChain integration.

**Production** — Debugging, Error handling, Validation, Persistence, Safety.

That's a strong foundation.

## 24. The Most Important Mental Model

Don't memorize 100 APIs. Remember this:

```
                    STATE
                      │
                      ↓
                    NODE
                      │
                      ↓
                   DECISION
                  ↙        ↘
                NODE       NODE
                  ↘        ↙
                    LOOP
                      │
                      ↓
                    STATE
```

LangGraph is fundamentally about controlling stateful workflows.

## 25. Your Learning Path From Here

You have finished the beginner roadmap. A good next roadmap (Level 2 — Advanced LangGraph)
covers: Advanced State Management, Message Reducers, Command, Interrupts Deep Dive,
Subgraphs, Parallel Execution, Streaming, Persistence, LangGraph Server, LangSmith, Advanced
Agent Patterns, Multi-Agent Systems, Agentic RAG, Production Deployment, and an Advanced
Final Project.

## 🏆 Your Final Project Challenge

Don't just copy the code from these lessons. Build this yourself: an **Academic AI Agent**
that supports:

1. Ask about regulations → RAG
2. Ask about courses → Course database
3. Calculate GPA → GPA tool
4. Remember conversation → Checkpointer
5. Dangerous action → Human approval

Architecture:

```
                         USER
                           ↓
                         AGENT
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
             RAG        GPA TOOL    COURSE TOOL
              ↓            ↓            ↓
              └────────────┼────────────┘
                           ↓
                          LLM
                           ↓
                    Need approval?
                      ↙       ↘
                    YES        NO
                     ↓          ↓
                   Human      Answer
                     ↓
                   Action
```
""",
            "order": 20,
            "estimated_minutes": 90,
            "has_code_examples": True,
        },
        "exercises": [
            {
                "title": "Build the base academic assistant",
                "description": (
                    "Implement calculate_gpa and search_course exactly as in the lesson. Bind "
                    "them to an LLM, build the agent/tools/should_continue graph with a "
                    "checkpointer under thread_id='student-1'. Test with two questions in the "
                    "same thread: \"What is CSE251?\" and \"Calculate my GPA if I have 15.4 "
                    "points over 4 credits.\" Print both final answers."
                ),
                "difficulty": DifficultyLevel.advanced,
                "starter_code": (
                    "from typing import Annotated\n"
                    "from typing_extensions import TypedDict\n"
                    "from langchain_openai import ChatOpenAI\n"
                    "from langchain_core.tools import tool\n"
                    "from langchain_core.messages import HumanMessage\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "from langgraph.graph.message import add_messages\n"
                    "from langgraph.prebuilt import ToolNode\n"
                    "from langgraph.checkpoint.memory import InMemorySaver\n\n\n"
                    "COURSES = {\n"
                    "    \"CSE251\": {\"name\": \"Machine Learning\", \"credits\": 3},\n"
                    "    \"CSE252\": {\"name\": \"Deep Learning\", \"credits\": 3},\n"
                    "}\n\n"
                    "# TODO: implement calculate_gpa and search_course as @tool functions\n"
                    "# TODO: bind tools, build State/agent/tool_node/should_continue\n"
                    "# TODO: build graph with checkpointer, thread_id='student-1'\n"
                    "# TODO: run both test questions and print answers\n"
                ),
                "solution_code": (
                    "@tool\n"
                    "def calculate_gpa(total_points: float, total_credits: float) -> float:\n"
                    "    \"\"\"Calculate GPA from total grade points and total credits.\"\"\"\n"
                    "    if total_credits == 0:\n"
                    "        return 0.0\n"
                    "    return total_points / total_credits\n\n\n"
                    "@tool\n"
                    "def search_course(course_code: str) -> str:\n"
                    "    \"\"\"Search for information about a course.\"\"\"\n"
                    "    course = COURSES.get(course_code.upper())\n"
                    "    if not course:\n"
                    "        return \"Course not found.\"\n"
                    "    return f\"Course: {course_code}\\nName: {course['name']}\\nCredits: {course['credits']}\"\n\n\n"
                    "tools = [calculate_gpa, search_course]\n"
                    "llm = ChatOpenAI(model=\"gpt-4.1-mini\", temperature=0)\n"
                    "llm_with_tools = llm.bind_tools(tools)\n\n\n"
                    "class State(TypedDict):\n"
                    "    messages: Annotated[list, add_messages]\n\n\n"
                    "def agent(state: State):\n"
                    "    response = llm_with_tools.invoke(state[\"messages\"])\n"
                    "    return {\"messages\": [response]}\n\n\n"
                    "tool_node = ToolNode(tools)\n\n\n"
                    "def should_continue(state: State):\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    if last_message.tool_calls:\n"
                    "        return \"tools\"\n"
                    "    return \"end\"\n\n\n"
                    "graph = StateGraph(State)\n"
                    "graph.add_node(\"agent\", agent)\n"
                    "graph.add_node(\"tools\", tool_node)\n"
                    "graph.add_edge(START, \"agent\")\n"
                    "graph.add_conditional_edges(\"agent\", should_continue, {\"tools\": \"tools\", \"end\": END})\n"
                    "graph.add_edge(\"tools\", \"agent\")\n\n"
                    "checkpointer = InMemorySaver()\n"
                    "app = graph.compile(checkpointer=checkpointer)\n"
                    "config = {\"configurable\": {\"thread_id\": \"student-1\"}}\n\n"
                    "r1 = app.invoke({\"messages\": [HumanMessage(content=\"What is CSE251?\")]}, config=config)\n"
                    "print(r1[\"messages\"][-1].content)\n\n"
                    "r2 = app.invoke(\n"
                    "    {\"messages\": [HumanMessage(content=\"Calculate my GPA if I have 15.4 points over 4 credits.\")]},\n"
                    "    config=config\n"
                    ")\n"
                    "print(r2[\"messages\"][-1].content)\n"
                ),
                "skill_tested": ["langgraph", "capstone", "agents", "tools", "memory"],
            },
            {
                "title": "Add search_regulations and gate it behind approval",
                "description": (
                    "Extend the base assistant with a `search_regulations(query)` tool using a "
                    "fake in-memory document list (reuse the pattern from Lesson 16). Then add a "
                    "simple approval gate: before executing search_regulations specifically (not "
                    "the other tools), use interrupt() to ask for human confirmation. Test with "
                    "\"What are the graduation requirements?\" and show both the pause and the "
                    "resumed final answer."
                ),
                "difficulty": DifficultyLevel.advanced,
                "starter_code": (
                    "REGULATION_DOCS = [\n"
                    "    \"Students must complete 132 credit hours to graduate.\",\n"
                    "    \"A minimum cumulative GPA of 2.0 is required for graduation.\",\n"
                    "]\n\n"
                    "@tool\n"
                    "def search_regulations(query: str) -> str:\n"
                    "    # TODO: docstring + simple keyword search over REGULATION_DOCS\n"
                    "    pass\n\n\n"
                    "# TODO: add search_regulations to tools, rebind llm_with_tools\n"
                    "# TODO: add an approval step (interrupt) specifically before this tool runs\n"
                    "# TODO: test with a regulations question, showing pause + resume\n"
                ),
                "solution_code": (
                    "from langgraph.types import interrupt, Command\n\n\n"
                    "REGULATION_DOCS = [\n"
                    "    \"Students must complete 132 credit hours to graduate.\",\n"
                    "    \"A minimum cumulative GPA of 2.0 is required for graduation.\",\n"
                    "]\n\n"
                    "@tool\n"
                    "def search_regulations(query: str) -> str:\n"
                    "    \"\"\"Search university regulations and return relevant information.\"\"\"\n"
                    "    matches = [d for d in REGULATION_DOCS if any(w.lower() in d.lower() for w in query.split())]\n"
                    "    return \"\\n\\n\".join(matches) if matches else \"No relevant regulation found.\"\n\n\n"
                    "# Simplified approach: add an 'approval' node BEFORE tools that only pauses\n"
                    "# when the pending tool call is search_regulations (a stand-in for a\n"
                    "# 'sensitive' tool), then routes into the normal ToolNode after approval.\n"
                    "def approval_gate(state):\n"
                    "    last_message = state[\"messages\"][-1]\n"
                    "    wants_regulations = any(tc[\"name\"] == \"search_regulations\" for tc in last_message.tool_calls)\n"
                    "    if wants_regulations:\n"
                    "        decision = interrupt(\"Approve searching regulations?\")\n"
                    "        if decision != \"yes\":\n"
                    "            return {\"messages\": [HumanMessage(content=\"Regulation search was not approved.\")]}\n"
                    "    return {}\n\n\n"
                    "# graph.add_node('approval_gate', approval_gate)\n"
                    "# graph.add_conditional_edges('agent', should_continue, {'tools': 'approval_gate', 'end': END})\n"
                    "# graph.add_edge('approval_gate', 'tools')\n"
                    "# graph.add_edge('tools', 'agent')\n"
                    "# (compile with a checkpointer; then invoke, observe the pause, and\n"
                    "#  resume with Command(resume='yes'))\n"
                ),
                "skill_tested": ["langgraph", "capstone", "human-in-the-loop", "rag"],
            },
        ],
        "quiz": {
            "title": "Final Project: AI Academic Assistant — Quiz",
            "questions": [
                {
                    "question": "In the final architecture, what role does the 'Agent / LLM' node play relative to RAG, the GPA tool, and the course tool?",
                    "options": [
                        "It always calls all three regardless of the question",
                        "It decides which of RAG, GPA tool, or course tool (if any) is relevant to the current question, based on tool descriptions and the question itself",
                        "It ignores tools entirely and answers from memory",
                        "It only ever calls the GPA tool",
                    ],
                    "correct": 1,
                    "explanation": "This is the agent pattern from Lesson 12 applied concretely: the LLM dynamically picks the right tool(s) per question.",
                },
                {
                    "question": "Why is search_regulations implemented as a tool rather than a fixed retrieve node in this architecture?",
                    "options": [
                        "Tools cannot be used for retrieval",
                        "Exposing retrieval as a tool lets the agent decide WHETHER retrieval is even needed for a given question, alongside other tools like GPA/course lookup",
                        "It's required by LangGraph syntax",
                        "It removes the need for a State definition",
                    ],
                    "correct": 1,
                    "explanation": "Framing RAG as a tool turns the whole thing into agentic RAG: the LLM chooses whether/when to retrieve, versus always retrieving unconditionally.",
                },
                {
                    "question": "What ties together a student's multiple questions (course lookup, then GPA calculation) into one ongoing conversation?",
                    "options": [
                        "Nothing, each question is always independent",
                        "Using the same thread_id with a checkpointer across both invoke() calls",
                        "Binding more tools to the LLM",
                        "Increasing the LLM's temperature",
                    ],
                    "correct": 1,
                    "explanation": "As covered in Lessons 13-14, consistent thread_id + checkpointer is what lets separate invoke() calls share conversation state.",
                },
                {
                    "question": "Where does Human-in-the-Loop fit into this final architecture, and why?",
                    "options": [
                        "It isn't used in this project at all",
                        "It gates potentially sensitive/high-impact actions (like sending something on the student's behalf) behind explicit human approval before execution",
                        "It replaces the need for a checkpointer",
                        "It automatically blocks all tool calls",
                    ],
                    "correct": 1,
                    "explanation": "Following Lesson 15's low-risk/high-risk framing, dangerous actions get an approval gate rather than running automatically.",
                },
                {
                    "question": "According to the lesson's mental model, what is LangGraph 'fundamentally about'?",
                    "options": [
                        "Fine-tuning LLMs",
                        "Controlling stateful workflows: state moving through nodes, decisions, and loops",
                        "Managing vector database indexing exclusively",
                        "Replacing the need for Python entirely",
                    ],
                    "correct": 1,
                    "explanation": "The lesson's closing mental model (STATE -> NODE -> DECISION -> LOOP -> STATE) is presented as the single most important idea to retain from the whole course.",
                },
            ],
            "passing_score": 75,
        },
        "project": {
            "title": "Capstone: Full Academic AI Agent",
            "description": (
                "Build the complete Academic AI Agent described in the Final Project Challenge: "
                "an agent with (1) search_regulations as a RAG-style tool over a small fake "
                "document set, (2) calculate_gpa, (3) search_course, (4) a checkpointer so the "
                "conversation persists across multiple invoke() calls under one thread_id, and "
                "(5) a human-approval gate before any 'write-style' action (simulate one, e.g. "
                "a 'submit_appeal(reason)' tool that should always require approval). Write a "
                "test script that simulates a realistic multi-turn student session touching all "
                "five capabilities, and print a clean transcript of the whole conversation."
            ),
            "difficulty": DifficultyLevel.advanced,
            "tech_stack": ["Python", "LangGraph", "LangChain", "OpenAI"],
            "objectives": [
                "Integrate RAG, GPA calculation, and course lookup as tools on one agent",
                "Persist conversation state correctly across a multi-turn session",
                "Add a human-approval gate for at least one sensitive/write-style action",
                "Demonstrate the full system end-to-end with a realistic test transcript",
            ],
            "rubric": {
                "tool_integration": "All required tools (regulations, GPA, course, submit_appeal) are implemented and correctly bound (30%)",
                "agent_architecture": "Full agent graph (agent/tools/routing/loop) is correctly assembled (25%)",
                "memory": "Checkpointer + thread_id correctly preserve context across turns (20%)",
                "human_approval": "Sensitive action correctly pauses for and resumes from approval (15%)",
                "demo_quality": "Test transcript clearly demonstrates all 5 capabilities working together (10%)",
            },
            "starter_repo_url": None,
            "estimated_hours": 5.0,
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
