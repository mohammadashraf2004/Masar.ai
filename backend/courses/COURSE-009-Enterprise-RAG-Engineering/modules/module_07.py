"""M01.L07 — From RAG to AI Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 7, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L07"
MODULE_ORDER = 1
MODULE_TITLE = "RAG Foundations"
MODULE_DESCRIPTION = (
    "Build, evaluate, operate, and extend RAG systems into agentic workflows with tools, "
    "memory, orchestration, multi-agent collaboration, governance, and observability."
)
SOURCE_CHAPTER = 7
SOURCE_PAGES = "Not provided in supplied source"

TOPIC = {'title': 'From RAG to AI Agents',
 'slug': 'rag-foundations-m01-l07',
 'description': 'A study-ready guide to AI agents, agentic RAG, tool calling, MCP/A2A, '
                'orchestration frameworks, memory, multi-agent design, and production '
                'observability.',
 'order': 7,
 'difficulty': DifficultyLevel.intermediate,
 'estimated_hours': 12.0,
 'skill_tags': ['rag',
                'agentic-rag',
                'ai-agents',
                'tool-calling',
                'react',
                'mcp',
                'a2a',
                'multi-agent',
                'langchain',
                'llamaindex',
                'crewai',
                'agent-memory',
                'observability',
                'opentelemetry',
                'human-in-the-loop',
                'module-01'],
 'prerequisite_ids': ['M01.L01', 'M01.L02', 'M01.L03', 'M01.L04', 'M01.L05', 'M01.L06'],
 'lesson': {'title': 'From RAG to AI Agents',
            'content': '# From RAG to AI Agents\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L07  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 7. Page numbers were not '
                       'provided. This lesson is an instructor-authored study adaptation rather '
                       'than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain how modern LLM agents evolved from earlier software-agent '
                       'ideas.\n'
                       '- Distinguish classic RAG from agentic RAG.\n'
                       '- Describe the reasoning LLM, orchestration, and tool layers of the '
                       'agentic stack.\n'
                       '- Choose between single-agent and multi-agent architectures deliberately.\n'
                       '- Explain supervisor, collaborative, and orchestrator-worker patterns.\n'
                       '- Trace the observation -> reasoning/planning -> action agentic loop.\n'
                       '- Decide between retrieval-as-a-tool and RAG-as-a-tool.\n'
                       '- Explain tool calling, ReAct, tool schemas, and production controls.\n'
                       '- Explain MCP tools, resources, prompts, host/client/server architecture, '
                       'transports, and security.\n'
                       '- Explain how A2A complements MCP for agent-to-agent collaboration.\n'
                       '- Understand the LangChain, LlamaIndex, Vectara, and CrewAI examples from '
                       'the source.\n'
                       '- Design short-term and long-term memory with privacy, poisoning, and '
                       'decay controls.\n'
                       '- Diagnose agent-specific failure modes and make them observable with '
                       'traces and metrics.\n'
                       '- Explain why human approval remains important for high-impact actions.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 1. From Software Agents to LLM Agents\n'
                       '\n'
                       'The idea of an **agent** predates generative AI. Early distributed-AI '
                       'research explored autonomous software components that could operate '
                       'independently and communicate with other components. The Actor Model is an '
                       'important historical precursor because it emphasized self-contained '
                       'actors, asynchronous message passing, and concurrent behavior.\n'
                       '\n'
                       'By the 1980s and 1990s, researchers described agents as autonomous, '
                       'reactive, proactive, and socially capable software entities. The '
                       'limitation was that most of their intelligence came from hand-written '
                       'rules and symbolic logic. They could work well inside carefully structured '
                       'environments, but they were brittle outside those assumptions.\n'
                       '\n'
                       'Modern LLMs did not invent the goal of autonomous software. They supplied '
                       'a flexible natural-language reasoning engine that made old agentic ideas '
                       'far easier to apply to open-ended tasks.\n'
                       '\n'
                       '[[IMAGE_NEEDED: AI agent evolution timeline | A timeline from Actor Model '
                       'and BDI agents through voice assistants, ReAct, tool calling, and modern '
                       'LLM agents. | Autonomy predates LLMs; LLMs mainly change flexibility, '
                       'language understanding, and planning.]]\n'
                       '\n'
                       '## 2. BDI: Beliefs, Desires, and Intentions\n'
                       '\n'
                       'The **Belief-Desire-Intention (BDI)** model organized an agent around '
                       'three concepts. Beliefs describe what the agent currently understands '
                       'about the world. Desires represent goals it would like to achieve. '
                       'Intentions are the plans it has committed to pursuing.\n'
                       '\n'
                       'This separation is still a useful mental model. It distinguishes state, '
                       'goal, and planned action. But classical BDI systems were typically '
                       'programmed rather than learned, so they depended heavily on designers '
                       'anticipating possible situations.\n'
                       '\n'
                       '## 3. From Reactive Assistants to Goal-Driven LLM Agents\n'
                       '\n'
                       'The growth of the internet and APIs gave software more systems to interact '
                       'with, while assistants such as Siri and Alexa made natural language the '
                       'interface. Yet these assistants were usually reactive: a request mapped to '
                       'a relatively fixed function such as checking the weather or setting an '
                       'alarm.\n'
                       '\n'
                       'LLMs changed the pattern because they can interpret a high-level goal, '
                       'identify missing information, choose a tool, inspect its result, and '
                       'continue. Frameworks such as ReAct made this iterative '
                       'reasoning-and-action pattern practical.\n'
                       '\n'
                       '## 4. What Is an AI Agent?\n'
                       '\n'
                       'An AI agent is an **autonomous or semi-autonomous software system whose '
                       'central reasoning engine is an LLM**. The important change from a normal '
                       'chatbot is that the model can decide what to do next rather than only '
                       'generate a final piece of text.\n'
                       '\n'
                       'A useful model is:\n'
                       '\n'
                       '> **LLM + orchestration + tools + iterative state = agentic system.**\n'
                       '\n'
                       'The model interprets goals and chooses actions. Orchestration executes '
                       'those actions and manages state. Tools connect the agent to information '
                       'and external systems. The loop continues until the task is complete.\n'
                       '\n'
                       '{{exercise:M01.L07.EX01}}\n'
                       '\n'
                       '## 5. Classic RAG vs Agentic RAG\n'
                       '\n'
                       'Classic RAG usually follows a relatively fixed path: retrieve evidence and '
                       'generate an answer. Agentic RAG makes retrieval one decision inside a '
                       'broader, dynamic loop.\n'
                       '\n'
                       'An agent may decide that one retrieval is insufficient, rewrite the '
                       'question, search another source, call a calculator, ask a database, '
                       'retrieve again, then synthesize the result. RAG therefore becomes a '
                       'capability the agent can invoke rather than the entire workflow.\n'
                       '\n'
                       '**Classic RAG:** query -> retrieve -> generate.  \n'
                       '**Agentic RAG:** goal -> reason -> choose tool -> observe -> reason again '
                       '-> possibly call more tools -> synthesize.\n'
                       '\n'
                       'The flexibility is powerful, but it also introduces new failure points: '
                       'tool choice, tool arguments, action order, stopping, and interpretation.\n'
                       '\n'
                       '## 6. The Agentic Stack\n'
                       '\n'
                       'The chapter organizes modern agent systems into three layers:\n'
                       '\n'
                       '1. **Reasoning LLM** — understands intent, decomposes goals, chooses '
                       'actions, and synthesizes results.\n'
                       '2. **Agent orchestration** — manages state, tool calls, retries, control '
                       'flow, and the loop itself.\n'
                       '3. **Tools** — expose external information or actions.\n'
                       '\n'
                       'This separation is architectural. You can replace a model without '
                       'rewriting every tool, or change an orchestration framework while '
                       'preserving the business systems beneath it.\n'
                       '\n'
                       '## 7. The Reasoning LLM\n'
                       '\n'
                       "The reasoning model is the agent's cognitive core. It can interpret user "
                       'intent, split a broad objective into subtasks, decide which tool can fill '
                       'a knowledge gap, generate tool arguments, interpret observations, and '
                       'produce the final response.\n'
                       '\n'
                       'A strong model improves planning, but model capability is only one factor. '
                       'A capable model can still use a poor tool, misread a tool output, or '
                       'misunderstand the goal. Agent quality is therefore an end-to-end system '
                       'property.\n'
                       '\n'
                       '## 8. Agent Orchestration\n'
                       '\n'
                       "The orchestration layer turns the LLM's requested actions into real "
                       'execution. It registers tools, sends schemas to the model, validates '
                       'requests, runs functions, captures outputs, and returns observations for '
                       'the next reasoning cycle.\n'
                       '\n'
                       'Production orchestration also handles timeouts, retries, state, loop '
                       'limits, streaming, concurrency, tracing, error handling, and approval '
                       'checkpoints. This is why an agent is more than a prompt around an LLM.\n'
                       '\n'
                       "## 9. Tools: The Agent's Interface to the World\n"
                       '\n'
                       'Tools determine what an agent can actually know and do. Typical tools '
                       'include search, RAG, retrieval, Text2SQL, calculators, messaging systems, '
                       'calendars, CRM APIs, and internal services.\n'
                       '\n'
                       "A tool's **name, description, schema, permissions, and output format** all "
                       'affect reliability. If several tools overlap heavily, the model can become '
                       'confused. If a tool can perform a dangerous write operation, a model '
                       'mistake has a larger blast radius.\n'
                       '\n'
                       'Treat tool design like API design for a caller that is intelligent but '
                       'probabilistic.\n'
                       '\n'
                       '## 10. The Agent Ecosystem\n'
                       '\n'
                       'The three layers map to an ecosystem of providers. Model providers supply '
                       'the reasoning LLM. Orchestration frameworks such as LangChain, LlamaIndex, '
                       'AutoGen, smolagents, CrewAI, and Pydantic AI implement the agent loop. '
                       'Commercial platforms can manage even more of the runtime. Any system with '
                       'an API can become a tool provider.\n'
                       '\n'
                       'A good architecture keeps these roles loosely coupled so that each layer '
                       'can evolve independently.\n'
                       '\n'
                       '## 11. Single-Agent Systems\n'
                       '\n'
                       'A single-agent system uses one agent to solve a focused problem. It '
                       'normally has lower latency, lower token usage, fewer state transitions, '
                       'and simpler debugging than a multi-agent design.\n'
                       '\n'
                       'Single-agent architectures are a strong default when the task is '
                       'well-defined, the tool surface is manageable, one security domain is '
                       'enough, and one team owns the workflow. Complexity should be added only '
                       'when it solves a concrete limitation.\n'
                       '\n'
                       '## 12. Multi-Agent Systems\n'
                       '\n'
                       'A multi-agent system distributes work among specialized agents. One agent '
                       'might research, another analyze numbers, and another write the final '
                       'report.\n'
                       '\n'
                       'Specialization can improve focus because each agent sees a narrower goal, '
                       'smaller context, and smaller tool set. Independent subtasks can also run '
                       'in parallel. But every additional agent introduces more model calls, '
                       'communication, state, and possible failure points.\n'
                       '\n'
                       '## 13. Supervisor and Collaborative Topologies\n'
                       '\n'
                       'In a **supervisor architecture**, one leader decomposes the global task, '
                       'delegates subtasks, collects results, and coordinates completion. Control '
                       'remains centralized.\n'
                       '\n'
                       'In a **collaborative architecture**, agents can communicate peer-to-peer '
                       'and choose which other agent to contact. This enables flexible, emergent '
                       'behavior but makes execution less predictable.\n'
                       '\n'
                       'Supervisor designs are typically easier to govern and debug. Peer-to-peer '
                       'designs can be useful for open-ended collaboration but require stronger '
                       'tracing and stopping rules.\n'
                       '\n'
                       '## 14. The Multi-Agent Complexity Tax\n'
                       '\n'
                       'Multi-agent systems pay for specialization with additional latency, token '
                       'cost, concurrency issues, recursive delegation risk, and harder '
                       'observability.\n'
                       '\n'
                       'A final answer can be wrong even when most workers behaved correctly. '
                       'Without detailed traces, finding the first failing agent or message can be '
                       'difficult. Multi-agent design is therefore a trade-off, not an automatic '
                       'improvement.\n'
                       '\n'
                       '## 15. When Multiple Agents Are Justified\n'
                       '\n'
                       'The chapter gives three especially strong reasons to move beyond one '
                       'agent:\n'
                       '\n'
                       '- **Distinct security domains:** separate workers need different '
                       'permissions or sensitive datasets.\n'
                       '- **Vast tool surfaces:** one agent has so many tools that tool selection '
                       'becomes unreliable.\n'
                       '- **Organizational boundaries:** different engineering teams need '
                       'independent ownership and versioning.\n'
                       '\n'
                       'Multi-agent design may also improve focus by shrinking context per worker, '
                       'and it can reduce cost by routing simple subtasks to cheaper models. '
                       'Still, the first question should be whether a carefully designed single '
                       'agent can solve the problem.\n'
                       '\n'
                       '{{exercise:M01.L07.EX02}}\n'
                       '\n'
                       '## 16. The Orchestrator-Worker Pattern\n'
                       '\n'
                       'The orchestrator-worker pattern is a practical middle ground. A central '
                       'orchestrator understands the global goal, decomposes it, sends narrow '
                       'tasks to specialist workers, collects results, and synthesizes the final '
                       'answer.\n'
                       '\n'
                       'Workers do not directly communicate with one another. This preserves '
                       'specialization without introducing fully emergent peer-to-peer behavior. '
                       'It also creates a clear place to enforce permissions, timeouts, and '
                       'auditability.\n'
                       '\n'
                       '## 17. Use Case: Customer Service\n'
                       '\n'
                       'Traditional support bots often depend on large decision trees. LLM agents '
                       'can instead combine natural-language reasoning with retrieval and business '
                       'tools, allowing them to answer a broader range of questions and adapt to '
                       'context.\n'
                       '\n'
                       'A support agent might retrieve policy, inspect an order, verify account '
                       'state, and then prepare a personalized response. Because the output is '
                       'customer-facing, hallucination mitigation, permission boundaries, and '
                       'human escalation are critical.\n'
                       '\n'
                       '## 18. Use Case: Financial Services\n'
                       '\n'
                       'Financial workflows such as investment research, due diligence, regulatory '
                       'analysis, and customer support often involve gathering evidence from many '
                       'sources and producing a structured result. Agents are well-suited to this '
                       'pattern.\n'
                       '\n'
                       'The more consequential the action, however, the more constrained autonomy '
                       'should be. Drafting an investment memo is very different from autonomously '
                       'moving money. High-impact actions need explicit authorization, '
                       'auditability, and often human approval.\n'
                       '\n'
                       '## 19. Use Case: Healthcare\n'
                       '\n'
                       'Healthcare applications include clinical documentation, administrative '
                       'automation, clinical-trial matching, personalized treatment support, and '
                       'virtual assistants.\n'
                       '\n'
                       'A recurring design pattern is augmentation rather than unsupervised '
                       'autonomy. An agent can draft notes, summarize evidence, or prepare a plan, '
                       'while a clinician remains responsible for review and approval in '
                       'high-stakes workflows.\n'
                       '\n'
                       '## 20. Use Case: Coding Agents\n'
                       '\n'
                       'Coding agents can inspect repositories, generate and modify files, run '
                       'tests, execute shell commands, and iterate on failures. They move far '
                       'beyond autocomplete.\n'
                       '\n'
                       'The software engineer increasingly acts as a director and reviewer: '
                       'specify the goal, inspect the patch, verify tests, review security, and '
                       'decide whether changes should be accepted.\n'
                       '\n'
                       'A useful mental model is a fast junior contributor: highly productive, but '
                       'still requiring review.\n'
                       '\n'
                       '{{exercise:M01.L07.EX03}}\n'
                       '\n'
                       '## 21. Human-in-the-Loop for High-Impact Actions\n'
                       '\n'
                       'Long-horizon tasks are risky because small reasoning or tool errors can '
                       'compound over many steps. In regulated or irreversible workflows, fully '
                       'autonomous execution may be inappropriate.\n'
                       '\n'
                       'A human-in-the-loop design lets the agent perform research, preparation, '
                       'and drafting, but pauses before actions such as sending a sensitive '
                       'message, changing production data, approving a transaction, or making a '
                       'consequential decision.\n'
                       '\n'
                       'This preserves automation while limiting the blast radius of agent '
                       'mistakes.\n'
                       '\n'
                       '## 22. The Agentic Loop\n'
                       '\n'
                       'At the center of an agent is a repeated cycle:\n'
                       '\n'
                       '1. **Observation** — receive the user request or the result of a previous '
                       'action.\n'
                       '2. **Reasoning and planning** — assess progress and choose the next step.\n'
                       '3. **Action** — execute the selected tool or operation.\n'
                       '\n'
                       'The result becomes the next observation. The loop continues until the '
                       'agent determines that the goal is satisfied or a stopping condition is '
                       'reached.\n'
                       '\n'
                       '[[IMAGE_NEEDED: The agentic loop | A cycle of Observation -> Reasoning & '
                       'Planning -> Action -> new Observation, with a termination path to Final '
                       'Answer. | Each action changes the state that the next decision sees.]]\n'
                       '\n'
                       '## 23. Observation: Building the Current State\n'
                       '\n'
                       'An observation can be user input, retrieved text, a database result, a '
                       'calculator output, an API response, or an error message.\n'
                       '\n'
                       'The next decision can only be as reliable as the observation. If a tool '
                       'returns stale or incorrect information, the model may reason coherently '
                       'over bad evidence and still fail. Tool output should therefore be '
                       'validated where practical rather than treated as unquestioned truth.\n'
                       '\n'
                       '## 24. Reasoning and Planning\n'
                       '\n'
                       'At each cycle, the agent considers the goal, previous steps, working '
                       'memory, and the newest observation. It decides whether the task is '
                       'complete, what is still unknown, which tool can reduce the uncertainty, '
                       'and what arguments should be sent.\n'
                       '\n'
                       'Planning is therefore not necessarily a one-time plan created at the '
                       'beginning. A robust agent can replan after each observation.\n'
                       '\n'
                       '## 25. Action: Executing the Plan\n'
                       '\n'
                       'The orchestration layer turns a requested action into a real operation. A '
                       'robust action layer validates tool identity and arguments, checks '
                       'authorization, enforces timeouts, captures errors, and records the '
                       'result.\n'
                       '\n'
                       'The action result then becomes the next observation, which means a faulty '
                       'action can cascade into later reasoning. Execution controls are therefore '
                       'part of reasoning reliability.\n'
                       '\n'
                       '## 26. Unstructured Data: Retrieval Tool or RAG Tool?\n'
                       '\n'
                       'An agent can access documents through **retrieval-as-a-tool** or '
                       '**RAG-as-a-tool**.\n'
                       '\n'
                       'A retrieval tool returns raw chunks and leaves interpretation and '
                       'synthesis to the agent. This gives the agent greater transparency and '
                       'flexibility.\n'
                       '\n'
                       'A RAG tool performs retrieval plus grounded generation and returns a ready '
                       'answer, often with citations. This centralizes grounding logic and can '
                       'make behavior more consistent.\n'
                       '\n'
                       'Neither option is inherently more agentic. The question is where you want '
                       'reasoning responsibility to live.\n'
                       '\n'
                       '{{exercise:M01.L07.EX04}}\n'
                       '\n'
                       '## 27. Debugging the Iterative Loop\n'
                       '\n'
                       'Agent errors cascade. A bad tool call creates a bad observation, which '
                       'then influences the next reasoning step. The final answer may hide the '
                       'original cause.\n'
                       '\n'
                       'Useful debugging data includes which tool was selected, the arguments '
                       'sent, the result returned, the duration, retries, and state transitions. '
                       'The goal is to identify the **first incorrect transition**, not merely '
                       'inspect the last response.\n'
                       '\n'
                       '## 28. Tool Calling\n'
                       '\n'
                       'Tool calling, also called function calling, lets a model request execution '
                       'of a developer-defined function using structured arguments.\n'
                       '\n'
                       'The application exposes a tool name, description, and input schema. The '
                       'model decides whether to use it and produces structured arguments. '
                       'Ordinary software then validates and executes the call.\n'
                       '\n'
                       'This separation is important: the model chooses, but application code '
                       'remains responsible for actual execution and security.\n'
                       '\n'
                       '## 29. ReAct: Reason, Act, Observe\n'
                       '\n'
                       'ReAct interleaves decision making and tool use. A simplified execution '
                       'path is:\n'
                       '\n'
                       '```text\n'
                       'Goal: answer a two-part question\n'
                       'Decision: gather evidence for part A\n'
                       'Action: call RAG tool\n'
                       'Observation: evidence A\n'
                       'Decision: gather evidence for part B\n'
                       'Action: call RAG tool\n'
                       'Observation: evidence B\n'
                       'Final: synthesize both results\n'
                       '```\n'
                       '\n'
                       'The important artifact for debugging is the externally visible sequence of '
                       'decisions, tool calls, observations, and outcomes—not hidden internal '
                       'reasoning.\n'
                       '\n'
                       '## 30. Tool Schemas and Descriptions\n'
                       '\n'
                       'A model normally sees a structured definition for every available tool. '
                       'Tool interface quality therefore directly affects agent behavior.\n'
                       '\n'
                       'Good tool definitions use a specific name, narrow responsibility, typed '
                       'arguments, clear descriptions, and predictable outputs. Overlapping '
                       'descriptions can create tool confusion, while broad write-enabled tools '
                       'increase the damage possible from one bad decision.\n'
                       '\n'
                       'Design tools as carefully as public APIs.\n'
                       '\n'
                       '{{exercise:M01.L07.EX05}}\n'
                       '\n'
                       '## 31. Production Controls for Tool Use\n'
                       '\n'
                       'Tool calls should be treated as probabilistic inputs rather than '
                       'guaranteed-correct requests. Production controls include schema '
                       'validation, permission checks outside the LLM, timeouts, safe retries, '
                       'idempotency where possible, loop detection, read/write separation, and '
                       'detailed logging.\n'
                       '\n'
                       'A stronger tool-calling model can help, but reliable tool use is '
                       'ultimately a property of the whole system.\n'
                       '\n'
                       '## 32. Model Context Protocol (MCP)\n'
                       '\n'
                       'As agent ecosystems grew, direct one-off integrations became fragmented. '
                       'The **Model Context Protocol (MCP)** standardizes how AI applications '
                       'discover capabilities and access tools or data without being tightly '
                       'coupled to implementation details.\n'
                       '\n'
                       'The main architectural benefit is decoupling. An agent can communicate '
                       'with a standardized MCP server while that server translates the request '
                       'into the vendor-specific database, file system, API, or internal service.\n'
                       '\n'
                       'MCP becomes especially valuable when many agents need access to a shared '
                       'library of enterprise capabilities.\n'
                       '\n'
                       '[[IMAGE_NEEDED: MCP overview | An AI application connects through MCP '
                       'clients to standardized servers that expose tools and data. | MCP '
                       'decouples agents from implementation-specific APIs.]]\n'
                       '\n'
                       '## 33. MCP Primitives: Tools, Resources, and Prompts\n'
                       '\n'
                       'MCP exposes three important capability types.\n'
                       '\n'
                       '**Tools** are executable functions. They can perform actions or '
                       'dynamically retrieve information.\n'
                       '\n'
                       '**Resources** represent contextual data or state, commonly addressed '
                       'through URIs. They are useful when information is too large or persistent '
                       'to fit naturally inside one tool response.\n'
                       '\n'
                       '**Prompts** are reusable instruction templates that encode intent, '
                       'constraints, and recommended interaction patterns. They guide the agent '
                       'but do not themselves perform an action.\n'
                       '\n'
                       'The distinction is useful: tools **do**, resources **provide context**, '
                       'and prompts **guide interaction**.\n'
                       '\n'
                       '## 34. MCP Host, Client, and Server\n'
                       '\n'
                       'MCP follows a client-server architecture.\n'
                       '\n'
                       '- **Host:** the application or environment in which the agent operates.\n'
                       '- **Client:** a component inside the host that speaks MCP and sends '
                       'structured requests.\n'
                       '- **Server:** an adapter that exposes tools, resources, or prompts and '
                       'translates MCP requests into operations on an underlying system.\n'
                       '\n'
                       'A server might wrap an internal database, a file system, or a Text2SQL '
                       'service. The agent therefore uses a stable protocol even if the underlying '
                       'system is proprietary.\n'
                       '\n'
                       '[[IMAGE_NEEDED: MCP host-client-server architecture | Show an agent host '
                       'containing MCP clients connected to several MCP servers, each wrapping a '
                       'tool or data source. | The client speaks MCP; each server adapts MCP '
                       'requests to an underlying capability.]]\n'
                       '\n'
                       '## 35. MCP Transports and Security\n'
                       '\n'
                       'The source describes local standard-input/output transport and remote '
                       'HTTP-style transport. The important production lesson is that the protocol '
                       'does not eliminate normal security responsibilities.\n'
                       '\n'
                       'Remote MCP services still need transport security, authentication, '
                       'authorization, secret management, access logging, and rate limits. Local '
                       'integrations still need operating-system permissions and process '
                       'isolation.\n'
                       '\n'
                       'Credentials should not be embedded casually in protocol messages. A '
                       'standardized integration layer is only safe when the surrounding '
                       'deployment is governed correctly.\n'
                       '\n'
                       '## 36. Enterprise Value of MCP\n'
                       '\n'
                       'MCP can provide a governed trust boundary between an agent and sensitive '
                       'enterprise systems. It can centralize reusable integrations, make legacy '
                       'systems accessible through standard adapters, and let tools scale '
                       'independently from agents.\n'
                       '\n'
                       'The chapter also stresses a trade-off: for a small local application with '
                       'a narrow, stable tool set, direct integration may be simpler. MCP becomes '
                       'increasingly valuable as an organization moves from isolated experiments '
                       'toward a shared agent ecosystem.\n'
                       '\n'
                       '{{exercise:M01.L07.EX06}}\n'
                       '\n'
                       '## 37. Agent-to-Agent (A2A) Communication\n'
                       '\n'
                       'MCP primarily standardizes the vertical connection from an agent to tools '
                       'and data. **Agent-to-Agent (A2A)** communication addresses the horizontal '
                       'problem of one agent collaborating with another agent.\n'
                       '\n'
                       'A2A allows agents to advertise capabilities, discover one another, '
                       'delegate work, exchange information, and track progress. The source '
                       "describes an **Agent Card** as a profile of an agent's skills and "
                       'supported tasks.\n'
                       '\n'
                       'The mental model is simple:\n'
                       '\n'
                       '- MCP: agent <-> tools and data.\n'
                       '- A2A: agent <-> agent.\n'
                       '\n'
                       'Together, these standards make large agent ecosystems more modular and '
                       'interoperable.\n'
                       '\n'
                       '[[IMAGE_NEEDED: MCP and A2A together | Show agents communicating '
                       'horizontally through A2A while each agent accesses tools vertically '
                       'through MCP. | MCP connects agents to capabilities; A2A connects agents to '
                       'other agents.]]\n'
                       '\n'
                       '## 38. Hands-On Agent Frameworks\n'
                       '\n'
                       'Different frameworks expose different APIs, but the same architecture '
                       'repeats: define tools, select a model, provide instructions, create state, '
                       'execute the loop, inspect tool results, and return a final answer.\n'
                       '\n'
                       'The framework is therefore not the agent architecture itself. It is one '
                       'implementation of the same reasoning-orchestration-tool pattern.\n'
                       '\n'
                       '## 39. LangChain: Turning a RAG Chain into a Tool\n'
                       '\n'
                       'The LangChain example first builds a small RAG pipeline over the GPT-2 '
                       'paper. That existing pipeline is then exposed as one tool to a ReAct '
                       'agent.\n'
                       '\n'
                       'Conceptually:\n'
                       '\n'
                       '```python\n'
                       '@tool\n'
                       'def rag_gpt_tool(question: str) -> str:\n'
                       '    return rag_chain.invoke(question)\n'
                       '\n'
                       'agent = create_react_agent(llm, [rag_gpt_tool])\n'
                       '```\n'
                       '\n'
                       'For a two-part question, the agent can decompose the task, call the RAG '
                       'tool once for each subquestion, observe the evidence, and synthesize a '
                       'final response.\n'
                       '\n'
                       'The key lesson is **composition**: a deterministic RAG component can '
                       'become one capability inside a more flexible agent.\n'
                       '\n'
                       '{{exercise:M01.L07.EX07}}\n'
                       '\n'
                       '## 40. What the LangChain Demo Still Needs for Production\n'
                       '\n'
                       'A successful notebook run does not make a production agent. The source '
                       'highlights the need for timeouts, retry policies, tracing, logging, and '
                       'monitoring to prevent infinite tool loops and make failures auditable.\n'
                       '\n'
                       'Production reliability comes from the controls around the agent as much as '
                       'from the framework that creates it.\n'
                       '\n'
                       '## 41. LlamaIndex: An Agent with Web, Calculator, and RAG Tools\n'
                       '\n'
                       'The LlamaIndex example gives one agent three distinct tools: web search '
                       'for fresh information, a calculator for deterministic arithmetic, and RAG '
                       'for document-grounded knowledge.\n'
                       '\n'
                       'The `FunctionAgent` receives the tool set, LLM, and system instructions. '
                       'The example then streams events so the developer can observe agent input, '
                       'generated text, tool calls, tool results, and the final answer.\n'
                       '\n'
                       'This makes the workflow concrete. A travel-planning task can require '
                       'several searches followed by a calculator call before the itinerary is '
                       'assembled.\n'
                       '\n'
                       '## 42. Agentic Search Services\n'
                       '\n'
                       'The source distinguishes search services designed for agents from search '
                       'pages designed for humans. Agent-oriented search returns cleaned, '
                       'machine-readable content and links rather than requiring an agent to '
                       'interpret a visually oriented results page.\n'
                       '\n'
                       'The broader design principle is to give agents **structured '
                       'observations**. The less irrelevant interface noise a tool returns, the '
                       'easier it is for the model to reason over the result.\n'
                       '\n'
                       '## 43. Why Agent Event Streaming Matters\n'
                       '\n'
                       "Streaming execution events makes the agent's progress visible while the "
                       'task is running. A developer can observe which tool is called, what '
                       'arguments are used, whether the call succeeds, and how the next decision '
                       'changes.\n'
                       '\n'
                       'This improves debugging and can improve UX. It also creates places to '
                       'insert policy checks, such as pausing before a high-impact action.\n'
                       '\n'
                       '{{exercise:M01.L07.EX08}}\n'
                       '\n'
                       '## 44. Managed Agent Platforms vs Orchestration Libraries\n'
                       '\n'
                       'With an orchestration library, the application team writes the agent and '
                       'still owns hosting, scaling, and operational reliability. A managed agent '
                       'platform abstracts more of the runtime and lets the developer focus on '
                       'tool definitions, model configuration, and business instructions.\n'
                       '\n'
                       'This is the same build-versus-platform trade-off seen earlier in RAG: '
                       'control and flexibility on one side, operational simplicity on the other.\n'
                       '\n'
                       '## 45. Vectara Agents API\n'
                       '\n'
                       "The chapter's managed-platform example first creates a corpus and "
                       "RAG-search tool, then defines the agent's model, description, and "
                       'instructions through an API.\n'
                       '\n'
                       'The execution flow is roughly:\n'
                       '\n'
                       '```text\n'
                       'corpus -> managed RAG tool -> agent definition -> session -> input event '
                       '-> managed execution -> response\n'
                       '```\n'
                       '\n'
                       'The platform manages the orchestration loop, while the developer controls '
                       'which capabilities the agent receives and how it should behave.\n'
                       '\n'
                       '## 46. CrewAI: A Multi-Agent Research and Writing Workflow\n'
                       '\n'
                       'The CrewAI example uses two specialized agents: a market researcher and a '
                       'technology writer. The researcher creates a report; the writing task '
                       'consumes that report and turns it into an article.\n'
                       '\n'
                       'This is a genuine multi-agent workflow because the agents have different '
                       'roles and task objectives. The output of one becomes context for another.\n'
                       '\n'
                       'Specialization is most valuable when subtasks really need different '
                       'prompts, tools, permissions, or ownership—not simply because multiple '
                       'agents sound more advanced.\n'
                       '\n'
                       '{{exercise:M01.L07.EX09}}\n'
                       '\n'
                       '## 47. Why Specialization Can Improve Agent Systems\n'
                       '\n'
                       'The source highlights several reasons specialization can help.\n'
                       '\n'
                       '**Tool bottleneck:** every tool definition consumes context, and too many '
                       'tools can cause selection confusion.\n'
                       '\n'
                       '**Cognitive precision:** smaller contexts and narrower tasks can help each '
                       'worker stay focused.\n'
                       '\n'
                       '**Cost efficiency:** easy subtasks can be routed to cheaper models, '
                       'reserving expensive models for difficult reasoning or synthesis.\n'
                       '\n'
                       'Multi-agent systems can also parallelize independent tasks and make '
                       'specialist capabilities reusable.\n'
                       '\n'
                       '## 48. Agentic Memory\n'
                       '\n'
                       "Memory is an agent's ability to retain and reuse information across steps, "
                       'interactions, or sessions. It is what makes an agent persistent rather '
                       'than a stateless one-shot responder.\n'
                       '\n'
                       'Memory can improve personalization, continuity, and efficiency, but it '
                       'also creates privacy, relevance, and lifecycle responsibilities. Storing '
                       'more history is not automatically better.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Agent memory architecture | Show short-term session memory '
                       'and long-term semantic memory both feeding the active agent context. | '
                       'Short-term memory preserves the current task; long-term memory retrieves '
                       'reusable historical facts.]]\n'
                       '\n'
                       '## 49. Short-Term or Working Memory\n'
                       '\n'
                       'Short-term memory exists for the current reasoning session. It helps the '
                       'agent remember previous tool results, resolve pronouns, and maintain a '
                       'multistep plan.\n'
                       '\n'
                       'A common implementation is a sliding window of recent conversation '
                       'history. Without this working context, a multistep agent becomes '
                       'effectively stateless and cannot reliably connect later instructions to '
                       'earlier steps.\n'
                       '\n'
                       '## 50. Long-Term Memory\n'
                       '\n'
                       'Long-term memory persists across sessions. It can store recurring '
                       'preferences, project history, or other facts that reduce friction in '
                       'future interactions.\n'
                       '\n'
                       'The chapter recommends using long-term memory when knowing the user or '
                       'project creates real cumulative value. A one-off transactional agent may '
                       'not need persistent memory at all, and avoiding it can simplify privacy '
                       'and compliance.\n'
                       '\n'
                       '## 51. Session Consolidation\n'
                       '\n'
                       'Raw session history grows over time. One strategy is **session '
                       'consolidation**: periodically summarize important facts and replace long '
                       'histories with a compressed representation.\n'
                       '\n'
                       'For example, multiple travel conversations might be consolidated into a '
                       'reusable fact such as “prefers window seats.” This reduces token usage and '
                       'noise, but the summary must be accurate because a bad consolidation can '
                       'become a persistent source of future errors.\n'
                       '\n'
                       '## 52. Semantic Retrieval for Long-Term Memory\n'
                       '\n'
                       'Long-term memory is often stored in a database or vector store. When a new '
                       'task begins, the agent semantically retrieves historical memories relevant '
                       'to the current query and inserts them into working context.\n'
                       '\n'
                       'This resembles RAG: the system retrieves only useful history instead of '
                       'loading every past interaction. The quality of memory therefore depends on '
                       'what is stored, how it is indexed, and how relevance is determined.\n'
                       '\n'
                       '{{exercise:M01.L07.EX10}}\n'
                       '\n'
                       '## 53. Memory Governance and Privacy\n'
                       '\n'
                       'Persistent memory turns the agent into a data steward. Enterprise systems '
                       'need the ability to delete memories associated with a user, redact '
                       'sensitive information before storage, and respect applicable privacy '
                       'requirements.\n'
                       '\n'
                       'The design question is not only “Can the agent remember this?” but “Should '
                       'it remember this, for how long, and under whose authorization?”\n'
                       '\n'
                       '## 54. Memory Poisoning\n'
                       '\n'
                       'An agent can accidentally store incorrect or malicious information and '
                       'retrieve it later as if it were trusted history. This is **memory '
                       'poisoning**.\n'
                       '\n'
                       'The source suggests a validation gate before long-term persistence. A '
                       'lightweight secondary check can decide whether a proposed memory is '
                       'factual, safe, and valuable enough to keep.\n'
                       '\n'
                       'Long-term memory should therefore be curated state, not an unfiltered '
                       'transcript dump.\n'
                       '\n'
                       '## 55. Memory Data Lifecycle and Decay\n'
                       '\n'
                       'Information has a shelf life. A preference or project fact that was useful '
                       'months ago may later become irrelevant or incorrect.\n'
                       '\n'
                       'A decay or archival policy helps keep memory current and limits '
                       'unnecessary retention. The right persistence decision depends on whether '
                       'information is reusable and durable or merely transitional.\n'
                       '\n'
                       '{{exercise:M01.L07.EX11}}\n'
                       '\n'
                       '## 56. Why Agent Failures Are Different\n'
                       '\n'
                       'Traditional software failures often map to deterministic bugs. Agent '
                       'failures can instead arise from behavior across an LLM, tool calls, '
                       'memory, and repeated decisions.\n'
                       '\n'
                       'A system can have low CPU usage, fast responses, and zero HTTP errors '
                       "while still failing the user's goal. Production monitoring therefore has "
                       'to evaluate not only infrastructure health but also behavioral '
                       'correctness.\n'
                       '\n'
                       '## 57. Tool Hallucination or Bad Tool Evidence\n'
                       '\n'
                       'A tool can return inaccurate information, and the agent may accept it '
                       'without verification. A RAG tool might return a wrong answer or a Text2SQL '
                       'tool might generate the wrong query.\n'
                       '\n'
                       'The agent can then faithfully propagate the bad evidence. This failure is '
                       'distinct from response hallucination because the error begins in the '
                       'observation supplied by the tool.\n'
                       '\n'
                       '## 58. Response Hallucination\n'
                       '\n'
                       'In response hallucination, the tools provide correct information but the '
                       'agent distorts or adds unsupported content when producing its final '
                       'answer.\n'
                       '\n'
                       'This is similar to generation failure in ordinary RAG. The distinction '
                       'matters because the remediation differs: tool-quality problems require '
                       'fixing the tool; response hallucination requires improving generation, '
                       'grounding, prompting, or post-generation checks.\n'
                       '\n'
                       '## 59. Goal Misinterpretation\n'
                       '\n'
                       'The agent may misunderstand what the user wants and solve a nearby but '
                       'different problem. For example, it might create the wrong destination plan '
                       'even though all tools work correctly.\n'
                       '\n'
                       'This is why evaluating only tool success is insufficient. The entire '
                       'workflow must remain aligned with the original user goal.\n'
                       '\n'
                       '## 60. Plan Generation Failure\n'
                       '\n'
                       'An agent can choose logically plausible steps in the wrong order or omit a '
                       'required step. Scheduling a meeting before checking availability is a '
                       'simple example.\n'
                       '\n'
                       'Planning failures often look reasonable locally. The error becomes obvious '
                       'only when the whole workflow is inspected against task prerequisites and '
                       'constraints.\n'
                       '\n'
                       '{{exercise:M01.L07.EX12}}\n'
                       '\n'
                       '## 61. Incorrect Tool Use\n'
                       '\n'
                       'An agent may select the wrong tool or call the correct tool with bad '
                       'arguments. The risk becomes serious when tools can change state.\n'
                       '\n'
                       'Permissions are a critical defense. If an email tool is read-only, a '
                       'reasoning mistake cannot delete messages. Restricting write capabilities '
                       'and applying least privilege reduces the blast radius of model errors.\n'
                       '\n'
                       '## 62. Verification and Termination Failures\n'
                       '\n'
                       'An agent has to know when the goal is actually complete. It may stop too '
                       'early and return a partial result, or continue calling tools after useful '
                       'work is finished.\n'
                       '\n'
                       'Loop limits, explicit completion criteria, progress checks, and maximum '
                       'cost or step budgets help prevent runaway execution.\n'
                       '\n'
                       '## 63. Prompt Injection in Agentic Systems\n'
                       '\n'
                       'Prompt injection becomes more dangerous when agents can take actions. A '
                       'malicious instruction can try to override the intended role, redirect tool '
                       'use, or cause sensitive information to be exposed.\n'
                       '\n'
                       'Defense requires layered controls: sanitize and classify inputs where '
                       'appropriate, treat external content as untrusted data, enforce permissions '
                       'outside the model, validate tool requests, and keep high-risk actions '
                       'behind approval gates.\n'
                       '\n'
                       '{{exercise:M01.L07.EX13}}\n'
                       '\n'
                       '## 64. Agentic Observability\n'
                       '\n'
                       'Traditional monitoring answers questions such as “Is the server healthy?” '
                       'Agentic observability asks “Did the agent accomplish the task correctly '
                       'and safely?”\n'
                       '\n'
                       'It combines normal logs, metrics, and traces with **evaluation** and '
                       '**governance**. Evaluation measures quality. Governance verifies that the '
                       'agent stayed within rules and permissions.\n'
                       '\n'
                       'The goal is to turn an opaque workflow into a system whose execution can '
                       'be inspected, measured, and improved.\n'
                       '\n'
                       '## 65. Tracing an Agent\n'
                       '\n'
                       'A trace records the end-to-end execution of one request as a hierarchy of '
                       'spans. A span can represent an LLM call, RAG query, Text2SQL invocation, '
                       'or another unit of work.\n'
                       '\n'
                       'A useful trace can answer:\n'
                       '\n'
                       '- Which tool was called?\n'
                       '- What arguments were passed?\n'
                       '- What did it return?\n'
                       '- How long did the step take?\n'
                       '- How many retries occurred?\n'
                       '- Where did the workflow diverge from the expected path?\n'
                       '\n'
                       'For example, repeated calls to the same flight-search tool can reveal poor '
                       'arguments even if the final answer eventually succeeds.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Agent execution trace | A hierarchical trace showing user '
                       'request, LLM decisions, tool-call spans, tool outputs, retries, and final '
                       'response with timings. | The trace exposes hidden inefficiency and the '
                       'first failing step.]]\n'
                       '\n'
                       '## 66. Agentic Observability Metrics\n'
                       '\n'
                       'Useful agent-specific metrics include:\n'
                       '\n'
                       '- **Token usage** — cost and prompt/reasoning efficiency.\n'
                       '- **Inference latency** — time to first token and end-to-end completion '
                       'time.\n'
                       '- **LLM/API call count** — workflow complexity and possible loops.\n'
                       '- **Tool-call success/failure rate** — reliability of agent-tool '
                       'interactions.\n'
                       '- **Response quality** — hallucination, relevance, helpfulness, or domain '
                       'metrics.\n'
                       '- **Human handoff rate** — how often the agent cannot complete a task '
                       'autonomously.\n'
                       '\n'
                       'Agent evaluation also needs dimensions beyond ordinary RAG, such as '
                       'tool-use efficiency, multiturn coherence, and whether autonomous decisions '
                       'remain aligned with user intent.\n'
                       '\n'
                       '{{exercise:M01.L07.EX14}}\n'
                       '\n'
                       '## 67. Traditional vs Agentic Observability\n'
                       '\n'
                       'Traditional observability assumes that operational stability is a useful '
                       'proxy for functional correctness. That assumption is insufficient for '
                       'agents.\n'
                       '\n'
                       'An agent can be perfectly healthy at the infrastructure level and still '
                       'choose the wrong tool, misread the goal, hallucinate a response, or fail '
                       'to terminate.\n'
                       '\n'
                       'Production dashboards therefore need both system-health metrics and '
                       'behavioral metrics.\n'
                       '\n'
                       '## 68. OpenTelemetry for Agent Systems\n'
                       '\n'
                       'The source highlights **OpenTelemetry (OTel)** as a vendor-neutral '
                       'standard for traces, metrics, and logs. AI-specific semantic conventions '
                       'can give different frameworks a shared vocabulary for LLM calls, tool '
                       'calls, and vector-database operations.\n'
                       '\n'
                       'The strategic benefit is interoperability. Instrumentation can remain '
                       'relatively independent from the backend used to visualize or analyze '
                       'telemetry.\n'
                       '\n'
                       '## 69. Agent Observability Platforms\n'
                       '\n'
                       'The chapter mentions tools such as Langfuse, Arize Phoenix, and LangSmith, '
                       'along with agent platforms that include observability directly.\n'
                       '\n'
                       'The exact product is less important than the capabilities: detailed '
                       'traces, latency and cost monitoring, prompt and configuration tracking, '
                       'evaluation datasets, and debugging of routers, planners, retrieval, and '
                       'tool calls.\n'
                       '\n'
                       'Choose tooling that lets you follow one execution deeply and also '
                       'aggregate behavior across many executions.\n'
                       '\n'
                       '## 70. Production Agent Checklist\n'
                       '\n'
                       'Before granting an agent meaningful autonomy, verify that you have:\n'
                       '\n'
                       '- narrow, well-described tools;\n'
                       '- least-privilege permissions;\n'
                       '- schema validation;\n'
                       '- retry and timeout policy;\n'
                       '- loop and cost limits;\n'
                       '- short-term state management;\n'
                       '- deliberate long-term memory policy;\n'
                       '- human approval for irreversible actions;\n'
                       '- tracing and behavior metrics;\n'
                       '- regression evaluation;\n'
                       '- prompt-injection defenses;\n'
                       '- a human escalation path.\n'
                       '\n'
                       'Agent production engineering is primarily about making dynamic behavior '
                       '**bounded, observable, and recoverable**.\n'
                       '\n'
                       '{{exercise:M01.L07.EX15}}\n'
                       '\n'
                       '## 71. Common Misconceptions\n'
                       '\n'
                       '**“An agent is just an LLM with a long prompt.”**  \n'
                       'An agent requires an execution loop, state, and external capabilities.\n'
                       '\n'
                       '**“More agents always means more intelligence.”**  \n'
                       'Multiple agents can increase latency, cost, and failure complexity.\n'
                       '\n'
                       '**“MCP automatically secures tools.”**  \n'
                       'MCP standardizes communication; authentication, authorization, and secret '
                       'management still need deliberate implementation.\n'
                       '\n'
                       '**“Memory means saving the entire transcript.”**  \n'
                       'Useful memory is selected, summarized, retrieved, governed, and expired.\n'
                       '\n'
                       '**“If all tool calls succeeded, the agent succeeded.”**  \n'
                       'The agent can still misunderstand the goal or synthesize the result '
                       'incorrectly.\n'
                       '\n'
                       '**“Low latency and zero server errors prove the agent is healthy.”**  \n'
                       'Agentic systems require behavioral evaluation in addition to '
                       'infrastructure monitoring.\n'
                       '\n'
                       '## 72. Terminology Reference\n'
                       '\n'
                       '| Term | Meaning |\n'
                       '|---|---|\n'
                       '| AI agent | LLM-powered system that can reason, choose actions, use '
                       'tools, and iterate toward a goal |\n'
                       '| Agentic RAG | Agent workflow in which retrieval/RAG is dynamically '
                       'invoked as needed |\n'
                       '| Orchestration | Runtime layer that manages state, tools, and the agent '
                       'loop |\n'
                       '| Tool calling | Structured model request to execute a defined function |\n'
                       '| ReAct | Pattern that alternates action selection and observation |\n'
                       '| MCP | Standardized protocol for exposing tools, resources, and prompts '
                       'to AI applications |\n'
                       '| MCP host | Application environment in which the agent operates |\n'
                       '| MCP client | Protocol component inside the host |\n'
                       '| MCP server | Adapter that exposes capabilities using MCP |\n'
                       '| A2A | Protocol concept for agent-to-agent communication |\n'
                       '| Working memory | State used within the current task/session |\n'
                       '| Long-term memory | Information persisted across sessions |\n'
                       '| Memory poisoning | Persisting harmful or false information that later '
                       'influences the agent |\n'
                       '| Trace | Structured record of one end-to-end execution |\n'
                       '| Span | One unit of work inside a trace |\n'
                       '| Human-in-the-loop | Pattern requiring human review or approval at '
                       'selected stages |\n'
                       '\n'
                       '## 73. Retain This Mental Model\n'
                       '\n'
                       'A reliable agent is not “a smarter chatbot.” Think of it as a **controlled '
                       'software runtime whose planner happens to be probabilistic**.\n'
                       '\n'
                       'The LLM decides what may be useful next. The orchestration layer enforces '
                       'what is actually allowed. Tools provide evidence and actions. Memory '
                       'carries useful state. Observability explains what happened. Governance '
                       'constrains what may happen.\n'
                       '\n'
                       'When an agent fails, inspect the chain in that order: **goal -> plan -> '
                       'tool choice -> tool result -> memory/state -> synthesis -> stopping '
                       'condition**.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Comprehensive self-check\n'
                       '\n'
                       '1. Explain **From Software Agents to LLM Agents** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '2. Give one concrete design decision, trade-off, or failure related to '
                       '**From Software Agents to LLM Agents**.\n'
                       '3. Explain **BDI: Beliefs, Desires, and Intentions** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '4. Give one concrete design decision, trade-off, or failure related to '
                       '**BDI: Beliefs, Desires, and Intentions**.\n'
                       '5. Explain **From Reactive Assistants to Goal-Driven LLM Agents** in your '
                       'own words and state why it matters in an agentic system.\n'
                       '6. Give one concrete design decision, trade-off, or failure related to '
                       '**From Reactive Assistants to Goal-Driven LLM Agents**.\n'
                       '7. Explain **What Is an AI Agent?** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '8. Give one concrete design decision, trade-off, or failure related to '
                       '**What Is an AI Agent?**.\n'
                       '9. Explain **Classic RAG vs Agentic RAG** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '10. Give one concrete design decision, trade-off, or failure related to '
                       '**Classic RAG vs Agentic RAG**.\n'
                       '11. Explain **The Agentic Stack** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '12. Give one concrete design decision, trade-off, or failure related to '
                       '**The Agentic Stack**.\n'
                       '13. Explain **The Reasoning LLM** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '14. Give one concrete design decision, trade-off, or failure related to '
                       '**The Reasoning LLM**.\n'
                       '15. Explain **Agent Orchestration** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '16. Give one concrete design decision, trade-off, or failure related to '
                       '**Agent Orchestration**.\n'
                       "17. Explain **Tools: The Agent's Interface to the World** in your own "
                       'words and state why it matters in an agentic system.\n'
                       '18. Give one concrete design decision, trade-off, or failure related to '
                       "**Tools: The Agent's Interface to the World**.\n"
                       '19. Explain **The Agent Ecosystem** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '20. Give one concrete design decision, trade-off, or failure related to '
                       '**The Agent Ecosystem**.\n'
                       '21. Explain **Single-Agent Systems** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '22. Give one concrete design decision, trade-off, or failure related to '
                       '**Single-Agent Systems**.\n'
                       '23. Explain **Multi-Agent Systems** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '24. Give one concrete design decision, trade-off, or failure related to '
                       '**Multi-Agent Systems**.\n'
                       '25. Explain **Supervisor and Collaborative Topologies** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '26. Give one concrete design decision, trade-off, or failure related to '
                       '**Supervisor and Collaborative Topologies**.\n'
                       '27. Explain **The Multi-Agent Complexity Tax** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '28. Give one concrete design decision, trade-off, or failure related to '
                       '**The Multi-Agent Complexity Tax**.\n'
                       '29. Explain **When Multiple Agents Are Justified** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '30. Give one concrete design decision, trade-off, or failure related to '
                       '**When Multiple Agents Are Justified**.\n'
                       '31. Explain **The Orchestrator-Worker Pattern** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '32. Give one concrete design decision, trade-off, or failure related to '
                       '**The Orchestrator-Worker Pattern**.\n'
                       '33. Explain **Use Case: Customer Service** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '34. Give one concrete design decision, trade-off, or failure related to '
                       '**Use Case: Customer Service**.\n'
                       '35. Explain **Use Case: Financial Services** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '36. Give one concrete design decision, trade-off, or failure related to '
                       '**Use Case: Financial Services**.\n'
                       '37. Explain **Use Case: Healthcare** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '38. Give one concrete design decision, trade-off, or failure related to '
                       '**Use Case: Healthcare**.\n'
                       '39. Explain **Use Case: Coding Agents** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '40. Give one concrete design decision, trade-off, or failure related to '
                       '**Use Case: Coding Agents**.\n'
                       '41. Explain **Human-in-the-Loop for High-Impact Actions** in your own '
                       'words and state why it matters in an agentic system.\n'
                       '42. Give one concrete design decision, trade-off, or failure related to '
                       '**Human-in-the-Loop for High-Impact Actions**.\n'
                       '43. Explain **The Agentic Loop** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '44. Give one concrete design decision, trade-off, or failure related to '
                       '**The Agentic Loop**.\n'
                       '45. Explain **Observation: Building the Current State** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '46. Give one concrete design decision, trade-off, or failure related to '
                       '**Observation: Building the Current State**.\n'
                       '47. Explain **Reasoning and Planning** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '48. Give one concrete design decision, trade-off, or failure related to '
                       '**Reasoning and Planning**.\n'
                       '49. Explain **Action: Executing the Plan** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '50. Give one concrete design decision, trade-off, or failure related to '
                       '**Action: Executing the Plan**.\n'
                       '51. Explain **Unstructured Data: Retrieval Tool or RAG Tool?** in your own '
                       'words and state why it matters in an agentic system.\n'
                       '52. Give one concrete design decision, trade-off, or failure related to '
                       '**Unstructured Data: Retrieval Tool or RAG Tool?**.\n'
                       '53. Explain **Debugging the Iterative Loop** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '54. Give one concrete design decision, trade-off, or failure related to '
                       '**Debugging the Iterative Loop**.\n'
                       '55. Explain **Tool Calling** in your own words and state why it matters in '
                       'an agentic system.\n'
                       '56. Give one concrete design decision, trade-off, or failure related to '
                       '**Tool Calling**.\n'
                       '57. Explain **ReAct: Reason, Act, Observe** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '58. Give one concrete design decision, trade-off, or failure related to '
                       '**ReAct: Reason, Act, Observe**.\n'
                       '59. Explain **Tool Schemas and Descriptions** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '60. Give one concrete design decision, trade-off, or failure related to '
                       '**Tool Schemas and Descriptions**.\n'
                       '61. Explain **Production Controls for Tool Use** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '62. Give one concrete design decision, trade-off, or failure related to '
                       '**Production Controls for Tool Use**.\n'
                       '63. Explain **Model Context Protocol (MCP)** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '64. Give one concrete design decision, trade-off, or failure related to '
                       '**Model Context Protocol (MCP)**.\n'
                       '65. Explain **MCP Primitives: Tools, Resources, and Prompts** in your own '
                       'words and state why it matters in an agentic system.\n'
                       '66. Give one concrete design decision, trade-off, or failure related to '
                       '**MCP Primitives: Tools, Resources, and Prompts**.\n'
                       '67. Explain **MCP Host, Client, and Server** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '68. Give one concrete design decision, trade-off, or failure related to '
                       '**MCP Host, Client, and Server**.\n'
                       '69. Explain **MCP Transports and Security** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '70. Give one concrete design decision, trade-off, or failure related to '
                       '**MCP Transports and Security**.\n'
                       '71. Explain **Enterprise Value of MCP** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '72. Give one concrete design decision, trade-off, or failure related to '
                       '**Enterprise Value of MCP**.\n'
                       '73. Explain **Agent-to-Agent (A2A) Communication** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '74. Give one concrete design decision, trade-off, or failure related to '
                       '**Agent-to-Agent (A2A) Communication**.\n'
                       '75. Explain **Hands-On Agent Frameworks** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '76. Give one concrete design decision, trade-off, or failure related to '
                       '**Hands-On Agent Frameworks**.\n'
                       '77. Explain **LangChain: Turning a RAG Chain into a Tool** in your own '
                       'words and state why it matters in an agentic system.\n'
                       '78. Give one concrete design decision, trade-off, or failure related to '
                       '**LangChain: Turning a RAG Chain into a Tool**.\n'
                       '79. Explain **What the LangChain Demo Still Needs for Production** in your '
                       'own words and state why it matters in an agentic system.\n'
                       '80. Give one concrete design decision, trade-off, or failure related to '
                       '**What the LangChain Demo Still Needs for Production**.\n'
                       '81. Explain **LlamaIndex: An Agent with Web, Calculator, and RAG Tools** '
                       'in your own words and state why it matters in an agentic system.\n'
                       '82. Give one concrete design decision, trade-off, or failure related to '
                       '**LlamaIndex: An Agent with Web, Calculator, and RAG Tools**.\n'
                       '83. Explain **Agentic Search Services** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '84. Give one concrete design decision, trade-off, or failure related to '
                       '**Agentic Search Services**.\n'
                       '85. Explain **Why Agent Event Streaming Matters** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '86. Give one concrete design decision, trade-off, or failure related to '
                       '**Why Agent Event Streaming Matters**.\n'
                       '87. Explain **Managed Agent Platforms vs Orchestration Libraries** in your '
                       'own words and state why it matters in an agentic system.\n'
                       '88. Give one concrete design decision, trade-off, or failure related to '
                       '**Managed Agent Platforms vs Orchestration Libraries**.\n'
                       '89. Explain **Vectara Agents API** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '90. Give one concrete design decision, trade-off, or failure related to '
                       '**Vectara Agents API**.\n'
                       '91. Explain **CrewAI: A Multi-Agent Research and Writing Workflow** in '
                       'your own words and state why it matters in an agentic system.\n'
                       '92. Give one concrete design decision, trade-off, or failure related to '
                       '**CrewAI: A Multi-Agent Research and Writing Workflow**.\n'
                       '93. Explain **Why Specialization Can Improve Agent Systems** in your own '
                       'words and state why it matters in an agentic system.\n'
                       '94. Give one concrete design decision, trade-off, or failure related to '
                       '**Why Specialization Can Improve Agent Systems**.\n'
                       '95. Explain **Agentic Memory** in your own words and state why it matters '
                       'in an agentic system.\n'
                       '96. Give one concrete design decision, trade-off, or failure related to '
                       '**Agentic Memory**.\n'
                       '97. Explain **Short-Term or Working Memory** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '98. Give one concrete design decision, trade-off, or failure related to '
                       '**Short-Term or Working Memory**.\n'
                       '99. Explain **Long-Term Memory** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '100. Give one concrete design decision, trade-off, or failure related to '
                       '**Long-Term Memory**.\n'
                       '101. Explain **Session Consolidation** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '102. Give one concrete design decision, trade-off, or failure related to '
                       '**Session Consolidation**.\n'
                       '103. Explain **Semantic Retrieval for Long-Term Memory** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '104. Give one concrete design decision, trade-off, or failure related to '
                       '**Semantic Retrieval for Long-Term Memory**.\n'
                       '105. Explain **Memory Governance and Privacy** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '106. Give one concrete design decision, trade-off, or failure related to '
                       '**Memory Governance and Privacy**.\n'
                       '107. Explain **Memory Poisoning** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '108. Give one concrete design decision, trade-off, or failure related to '
                       '**Memory Poisoning**.\n'
                       '109. Explain **Memory Data Lifecycle and Decay** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '110. Give one concrete design decision, trade-off, or failure related to '
                       '**Memory Data Lifecycle and Decay**.\n'
                       '111. Explain **Why Agent Failures Are Different** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '112. Give one concrete design decision, trade-off, or failure related to '
                       '**Why Agent Failures Are Different**.\n'
                       '113. Explain **Tool Hallucination or Bad Tool Evidence** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '114. Give one concrete design decision, trade-off, or failure related to '
                       '**Tool Hallucination or Bad Tool Evidence**.\n'
                       '115. Explain **Response Hallucination** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '116. Give one concrete design decision, trade-off, or failure related to '
                       '**Response Hallucination**.\n'
                       '117. Explain **Goal Misinterpretation** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '118. Give one concrete design decision, trade-off, or failure related to '
                       '**Goal Misinterpretation**.\n'
                       '119. Explain **Plan Generation Failure** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '120. Give one concrete design decision, trade-off, or failure related to '
                       '**Plan Generation Failure**.\n'
                       '121. Explain **Incorrect Tool Use** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '122. Give one concrete design decision, trade-off, or failure related to '
                       '**Incorrect Tool Use**.\n'
                       '123. Explain **Verification and Termination Failures** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '124. Give one concrete design decision, trade-off, or failure related to '
                       '**Verification and Termination Failures**.\n'
                       '125. Explain **Prompt Injection in Agentic Systems** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '126. Give one concrete design decision, trade-off, or failure related to '
                       '**Prompt Injection in Agentic Systems**.\n'
                       '127. Explain **Agentic Observability** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '128. Give one concrete design decision, trade-off, or failure related to '
                       '**Agentic Observability**.\n'
                       '129. Explain **Tracing an Agent** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '130. Give one concrete design decision, trade-off, or failure related to '
                       '**Tracing an Agent**.\n'
                       '131. Explain **Agentic Observability Metrics** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '132. Give one concrete design decision, trade-off, or failure related to '
                       '**Agentic Observability Metrics**.\n'
                       '133. Explain **Traditional vs Agentic Observability** in your own words '
                       'and state why it matters in an agentic system.\n'
                       '134. Give one concrete design decision, trade-off, or failure related to '
                       '**Traditional vs Agentic Observability**.\n'
                       '135. Explain **OpenTelemetry for Agent Systems** in your own words and '
                       'state why it matters in an agentic system.\n'
                       '136. Give one concrete design decision, trade-off, or failure related to '
                       '**OpenTelemetry for Agent Systems**.\n'
                       '137. Explain **Agent Observability Platforms** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '138. Give one concrete design decision, trade-off, or failure related to '
                       '**Agent Observability Platforms**.\n'
                       '139. Explain **Production Agent Checklist** in your own words and state '
                       'why it matters in an agentic system.\n'
                       '140. Give one concrete design decision, trade-off, or failure related to '
                       '**Production Agent Checklist**.\n'
                       '141. Explain **Common Misconceptions** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '142. Give one concrete design decision, trade-off, or failure related to '
                       '**Common Misconceptions**.\n'
                       '143. Explain **Terminology Reference** in your own words and state why it '
                       'matters in an agentic system.\n'
                       '144. Give one concrete design decision, trade-off, or failure related to '
                       '**Terminology Reference**.\n'
                       '145. Explain **Retain This Mental Model** in your own words and state why '
                       'it matters in an agentic system.\n'
                       '146. Give one concrete design decision, trade-off, or failure related to '
                       '**Retain This Mental Model**.\n'
                       '147. Draw the full agentic stack and label which layer reasons, which '
                       'layer executes, and which layer provides external capabilities.\n'
                       '148. Compare classic RAG and agentic RAG using the same user request.\n'
                       '149. Describe one workflow where a single agent is superior to multiple '
                       'agents and explain why.\n'
                       '150. Describe one workflow where distinct security domains justify '
                       'multiple agents.\n'
                       '151. Explain how a bad tool result can propagate through later agent-loop '
                       'iterations.\n'
                       '152. Design a tool description that minimizes confusion with a similar '
                       'tool.\n'
                       '153. Explain why tool permission should be enforced outside the LLM.\n'
                       '154. Compare retrieval-as-a-tool and RAG-as-a-tool for a complex research '
                       'workflow.\n'
                       '155. Explain the difference between MCP tools, resources, and prompts.\n'
                       '156. Draw MCP host, client, server, and underlying tool relationships.\n'
                       '157. Explain why MCP does not remove the need for authentication and '
                       'authorization.\n'
                       '158. Explain how A2A and MCP can coexist in one multi-agent enterprise '
                       'architecture.\n'
                       '159. Describe what you would look for in a LangChain ReAct execution '
                       'trace.\n'
                       '160. Explain why event streaming is useful in a LlamaIndex-style '
                       'workflow.\n'
                       '161. Describe the operational trade-off between an orchestration library '
                       'and a managed agent platform.\n'
                       '162. Explain why the CrewAI research/writer example is a legitimate '
                       'multi-agent workflow.\n'
                       '163. Define what information should never automatically become long-term '
                       'memory.\n'
                       '164. Explain how session consolidation reduces cost and how it can '
                       'introduce errors.\n'
                       '165. Describe a validation gate for long-term memory.\n'
                       '166. Explain why a data-decay policy is important for agent memory.\n'
                       '167. Differentiate tool hallucination from response hallucination.\n'
                       '168. Give an example of goal misinterpretation where all tools are '
                       'functioning correctly.\n'
                       '169. Give an example of a plausible but invalid action plan.\n'
                       '170. Explain how least privilege reduces the impact of incorrect tool '
                       'use.\n'
                       '171. Define two stopping conditions that can prevent agent loops.\n'
                       '172. Explain why prompt injection becomes more dangerous when an agent has '
                       'write-capable tools.\n'
                       '173. Describe the difference between traditional infrastructure monitoring '
                       'and agentic observability.\n'
                       '174. List the spans you would expect in a trace for an agent that '
                       'searches, calculates, and sends a draft to a human.\n'
                       '175. Explain how token usage and call count can reveal inefficient '
                       'reasoning.\n'
                       '176. Define a human handoff rate and explain what a sudden increase might '
                       'mean.\n'
                       '177. Explain how OpenTelemetry can reduce observability vendor lock-in.\n'
                       '178. Design a minimal go/no-go checklist before allowing an agent to take '
                       'irreversible actions.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Final takeaway\n'
                       '\n'
                       'The move from RAG to agents is a move from a mostly fixed information '
                       'pipeline to a **dynamic decision-and-action system**. RAG remains '
                       'important, but it becomes one tool among many. The engineering challenge '
                       'shifts from simply retrieving the right context to controlling a '
                       'probabilistic planner that can choose tools, create plans, maintain '
                       'memory, and take actions.\n'
                       '\n'
                       'The safest production mindset is to make autonomy **bounded, observable, '
                       'and reversible wherever possible**. Start simple, give agents only the '
                       'tools and permissions they need, persist only memory that creates durable '
                       'value, trace the execution path, evaluate behavior continuously, and place '
                       'human approval in front of consequential actions.\n',
            'estimated_minutes': 720,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'agent-history',
                          'title': 'From Software Agents to LLM Agents',
                          'order': 1},
                         {'id': 'bdi',
                          'title': 'BDI: Beliefs, Desires, and Intentions',
                          'order': 2},
                         {'id': 'assistants-to-llms',
                          'title': 'From Reactive Assistants to Goal-Driven LLM Agents',
                          'order': 3},
                         {'id': 'what-is-agent', 'title': 'What Is an AI Agent?', 'order': 4},
                         {'id': 'rag-vs-agentic-rag',
                          'title': 'Classic RAG vs Agentic RAG',
                          'order': 5},
                         {'id': 'agentic-stack', 'title': 'The Agentic Stack', 'order': 6},
                         {'id': 'reasoning-llm', 'title': 'The Reasoning LLM', 'order': 7},
                         {'id': 'orchestration', 'title': 'Agent Orchestration', 'order': 8},
                         {'id': 'tools',
                          'title': "Tools: The Agent's Interface to the World",
                          'order': 9},
                         {'id': 'ecosystem', 'title': 'The Agent Ecosystem', 'order': 10},
                         {'id': 'single-agent', 'title': 'Single-Agent Systems', 'order': 11},
                         {'id': 'multi-agent', 'title': 'Multi-Agent Systems', 'order': 12},
                         {'id': 'multi-agent-topologies',
                          'title': 'Supervisor and Collaborative Topologies',
                          'order': 13},
                         {'id': 'complexity-tax',
                          'title': 'The Multi-Agent Complexity Tax',
                          'order': 14},
                         {'id': 'when-multi-agent',
                          'title': 'When Multiple Agents Are Justified',
                          'order': 15},
                         {'id': 'orchestrator-worker',
                          'title': 'The Orchestrator-Worker Pattern',
                          'order': 16},
                         {'id': 'customer-service',
                          'title': 'Use Case: Customer Service',
                          'order': 17},
                         {'id': 'finance', 'title': 'Use Case: Financial Services', 'order': 18},
                         {'id': 'healthcare', 'title': 'Use Case: Healthcare', 'order': 19},
                         {'id': 'coding-agents', 'title': 'Use Case: Coding Agents', 'order': 20},
                         {'id': 'human-in-loop',
                          'title': 'Human-in-the-Loop for High-Impact Actions',
                          'order': 21},
                         {'id': 'agentic-loop', 'title': 'The Agentic Loop', 'order': 22},
                         {'id': 'observation',
                          'title': 'Observation: Building the Current State',
                          'order': 23},
                         {'id': 'reasoning-planning',
                          'title': 'Reasoning and Planning',
                          'order': 24},
                         {'id': 'action', 'title': 'Action: Executing the Plan', 'order': 25},
                         {'id': 'retrieval-vs-rag-tool',
                          'title': 'Unstructured Data: Retrieval Tool or RAG Tool?',
                          'order': 26},
                         {'id': 'debugging-loop',
                          'title': 'Debugging the Iterative Loop',
                          'order': 27},
                         {'id': 'tool-calling', 'title': 'Tool Calling', 'order': 28},
                         {'id': 'react', 'title': 'ReAct: Reason, Act, Observe', 'order': 29},
                         {'id': 'tool-schema',
                          'title': 'Tool Schemas and Descriptions',
                          'order': 30},
                         {'id': 'tool-reliability',
                          'title': 'Production Controls for Tool Use',
                          'order': 31},
                         {'id': 'mcp-overview',
                          'title': 'Model Context Protocol (MCP)',
                          'order': 32},
                         {'id': 'mcp-primitives',
                          'title': 'MCP Primitives: Tools, Resources, and Prompts',
                          'order': 33},
                         {'id': 'mcp-architecture',
                          'title': 'MCP Host, Client, and Server',
                          'order': 34},
                         {'id': 'mcp-security',
                          'title': 'MCP Transports and Security',
                          'order': 35},
                         {'id': 'mcp-enterprise', 'title': 'Enterprise Value of MCP', 'order': 36},
                         {'id': 'a2a', 'title': 'Agent-to-Agent (A2A) Communication', 'order': 37},
                         {'id': 'framework-overview',
                          'title': 'Hands-On Agent Frameworks',
                          'order': 38},
                         {'id': 'langchain-rag-agent',
                          'title': 'LangChain: Turning a RAG Chain into a Tool',
                          'order': 39},
                         {'id': 'langchain-production',
                          'title': 'What the LangChain Demo Still Needs for Production',
                          'order': 40},
                         {'id': 'llamaindex-agent',
                          'title': 'LlamaIndex: An Agent with Web, Calculator, and RAG Tools',
                          'order': 41},
                         {'id': 'agentic-search', 'title': 'Agentic Search Services', 'order': 42},
                         {'id': 'event-streaming',
                          'title': 'Why Agent Event Streaming Matters',
                          'order': 43},
                         {'id': 'managed-platforms',
                          'title': 'Managed Agent Platforms vs Orchestration Libraries',
                          'order': 44},
                         {'id': 'vectara-agent', 'title': 'Vectara Agents API', 'order': 45},
                         {'id': 'crewai',
                          'title': 'CrewAI: A Multi-Agent Research and Writing Workflow',
                          'order': 46},
                         {'id': 'multi-agent-benefits',
                          'title': 'Why Specialization Can Improve Agent Systems',
                          'order': 47},
                         {'id': 'agent-memory', 'title': 'Agentic Memory', 'order': 48},
                         {'id': 'short-term-memory',
                          'title': 'Short-Term or Working Memory',
                          'order': 49},
                         {'id': 'long-term-memory', 'title': 'Long-Term Memory', 'order': 50},
                         {'id': 'session-consolidation',
                          'title': 'Session Consolidation',
                          'order': 51},
                         {'id': 'semantic-memory',
                          'title': 'Semantic Retrieval for Long-Term Memory',
                          'order': 52},
                         {'id': 'memory-privacy',
                          'title': 'Memory Governance and Privacy',
                          'order': 53},
                         {'id': 'memory-poisoning', 'title': 'Memory Poisoning', 'order': 54},
                         {'id': 'memory-decay',
                          'title': 'Memory Data Lifecycle and Decay',
                          'order': 55},
                         {'id': 'agent-failures',
                          'title': 'Why Agent Failures Are Different',
                          'order': 56},
                         {'id': 'tool-hallucination',
                          'title': 'Tool Hallucination or Bad Tool Evidence',
                          'order': 57},
                         {'id': 'response-hallucination',
                          'title': 'Response Hallucination',
                          'order': 58},
                         {'id': 'goal-misinterpretation',
                          'title': 'Goal Misinterpretation',
                          'order': 59},
                         {'id': 'planning-failure',
                          'title': 'Plan Generation Failure',
                          'order': 60},
                         {'id': 'incorrect-tool-use', 'title': 'Incorrect Tool Use', 'order': 61},
                         {'id': 'termination-failure',
                          'title': 'Verification and Termination Failures',
                          'order': 62},
                         {'id': 'prompt-injection-agents',
                          'title': 'Prompt Injection in Agentic Systems',
                          'order': 63},
                         {'id': 'agentic-observability',
                          'title': 'Agentic Observability',
                          'order': 64},
                         {'id': 'tracing', 'title': 'Tracing an Agent', 'order': 65},
                         {'id': 'agent-metrics',
                          'title': 'Agentic Observability Metrics',
                          'order': 66},
                         {'id': 'traditional-vs-agent-observability',
                          'title': 'Traditional vs Agentic Observability',
                          'order': 67},
                         {'id': 'otel', 'title': 'OpenTelemetry for Agent Systems', 'order': 68},
                         {'id': 'observability-tools',
                          'title': 'Agent Observability Platforms',
                          'order': 69},
                         {'id': 'production-checklist',
                          'title': 'Production Agent Checklist',
                          'order': 70},
                         {'id': 'misconceptions', 'title': 'Common Misconceptions', 'order': 71},
                         {'id': 'terminology', 'title': 'Terminology Reference', 'order': 72},
                         {'id': 'retain-mental-model',
                          'title': 'Retain This Mental Model',
                          'order': 73}]},
 'exercises': [{'id': 'M01.L07.EX01',
                'title': 'Classify an Agentic Task',
                'lesson_code': 'M01.L07',
                'section_id': 'what-is-agent',
                'placement': 'after_section',
                'description': 'Given five systems, decide which are simple LLM calls, classic '
                               'RAG, or true agents, and justify each classification.',
                'instructions': 'Given five systems, decide which are simple LLM calls, classic '
                                'RAG, or true agents, and justify each classification.',
                'expected_output': 'A table with classification and evidence from the execution '
                                   'behavior.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX02',
                'title': 'Choose Single vs Multi-Agent',
                'lesson_code': 'M01.L07',
                'section_id': 'when-multi-agent',
                'placement': 'after_section',
                'description': 'Evaluate three workflows and choose a single-agent or multi-agent '
                               'design based on tool surface, security domains, and ownership.',
                'instructions': 'Evaluate three workflows and choose a single-agent or multi-agent '
                                'design based on tool surface, security domains, and ownership.',
                'expected_output': 'Three architecture decisions with explicit trade-offs.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX03',
                'title': 'Design a Coding-Agent Approval Gate',
                'lesson_code': 'M01.L07',
                'section_id': 'coding-agents',
                'placement': 'after_section',
                'description': 'Define which coding-agent actions may run automatically and which '
                               'require human approval.',
                'instructions': 'Define which coding-agent actions may run automatically and which '
                                'require human approval.',
                'expected_output': 'A permission matrix covering read, edit, test, shell, and '
                                   'deploy actions.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX04',
                'title': 'Choose Retrieval Tool vs RAG Tool',
                'lesson_code': 'M01.L07',
                'section_id': 'retrieval-vs-rag-tool',
                'placement': 'after_section',
                'description': 'For research, compliance QA, and exploratory analysis, decide '
                               'whether the agent should receive raw chunks or a grounded RAG '
                               'answer.',
                'instructions': 'For research, compliance QA, and exploratory analysis, decide '
                                'whether the agent should receive raw chunks or a grounded RAG '
                                'answer.',
                'expected_output': 'Three choices with reasoning about where synthesis should '
                                   'live.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX05',
                'title': 'Improve Tool Definitions',
                'lesson_code': 'M01.L07',
                'section_id': 'tool-schema',
                'placement': 'after_section',
                'description': 'Rewrite three vague tool names/descriptions so a model can '
                               'distinguish them reliably.',
                'instructions': 'Rewrite three vague tool names/descriptions so a model can '
                                'distinguish them reliably.',
                'expected_output': 'Clear tool names, purposes, and typed argument descriptions.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX06',
                'title': 'Design an MCP Boundary',
                'lesson_code': 'M01.L07',
                'section_id': 'mcp-enterprise',
                'placement': 'after_section',
                'description': 'Sketch how several agents can share a governed database capability '
                               'through one MCP server.',
                'instructions': 'Sketch how several agents can share a governed database '
                                'capability through one MCP server.',
                'expected_output': 'A host/client/server/tool diagram plus authentication and '
                                   'authorization notes.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX07',
                'title': 'Decompose a Compound RAG Question',
                'lesson_code': 'M01.L07',
                'section_id': 'langchain-rag-agent',
                'placement': 'after_section',
                'description': 'Break a two-part document question into the tool calls a ReAct '
                               'agent should make.',
                'instructions': 'Break a two-part document question into the tool calls a ReAct '
                                'agent should make.',
                'expected_output': 'A short action-observation sequence ending in synthesis.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX08',
                'title': 'Read an Agent Event Stream',
                'lesson_code': 'M01.L07',
                'section_id': 'event-streaming',
                'placement': 'after_section',
                'description': 'Given a sequence of web-search and calculator events, identify the '
                               'purpose of each step and one possible failure point.',
                'instructions': 'Given a sequence of web-search and calculator events, identify '
                                'the purpose of each step and one possible failure point.',
                'expected_output': 'An annotated execution timeline.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX09',
                'title': 'Design a Two-Agent Crew',
                'lesson_code': 'M01.L07',
                'section_id': 'crewai',
                'placement': 'after_section',
                'description': 'Create specialized roles and dependent tasks for producing a '
                               'technical market report.',
                'instructions': 'Create specialized roles and dependent tasks for producing a '
                                'technical market report.',
                'expected_output': 'Two agent definitions, two task definitions, and their '
                                   'dependency.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX10',
                'title': 'Design Memory Retrieval',
                'lesson_code': 'M01.L07',
                'section_id': 'semantic-memory',
                'placement': 'after_section',
                'description': 'Define what should be stored short-term, what should persist '
                               'long-term, and how relevant memories are selected.',
                'instructions': 'Define what should be stored short-term, what should persist '
                                'long-term, and how relevant memories are selected.',
                'expected_output': 'A memory policy with storage and retrieval rules.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX11',
                'title': 'Create a Memory Lifecycle Policy',
                'lesson_code': 'M01.L07',
                'section_id': 'memory-decay',
                'placement': 'after_section',
                'description': 'Define creation, validation, expiration, deletion, and archival '
                               'rules for persistent agent memories.',
                'instructions': 'Define creation, validation, expiration, deletion, and archival '
                                'rules for persistent agent memories.',
                'expected_output': 'A lifecycle policy suitable for an enterprise assistant.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX12',
                'title': 'Diagnose a Planning Failure',
                'lesson_code': 'M01.L07',
                'section_id': 'planning-failure',
                'placement': 'after_section',
                'description': 'Inspect a flawed meeting-scheduling plan and reorder the actions '
                               'correctly.',
                'instructions': 'Inspect a flawed meeting-scheduling plan and reorder the actions '
                                'correctly.',
                'expected_output': 'A corrected plan plus explanation of the dependency error.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX13',
                'title': 'Limit Prompt-Injection Blast Radius',
                'lesson_code': 'M01.L07',
                'section_id': 'prompt-injection-agents',
                'placement': 'after_section',
                'description': 'Design least-privilege permissions for an agent that reads email '
                               'and drafts replies.',
                'instructions': 'Design least-privilege permissions for an agent that reads email '
                                'and drafts replies.',
                'expected_output': 'A tool-permission design that prevents unauthorized '
                                   'send/delete operations.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX14',
                'title': 'Define an Agent Metrics Dashboard',
                'lesson_code': 'M01.L07',
                'section_id': 'agent-metrics',
                'placement': 'after_section',
                'description': 'Select metrics for cost, latency, tool reliability, response '
                               'quality, and autonomy.',
                'instructions': 'Select metrics for cost, latency, tool reliability, response '
                                'quality, and autonomy.',
                'expected_output': 'A dashboard specification with each metric and what failure it '
                                   'detects.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']},
               {'id': 'M01.L07.EX15',
                'title': 'Production Readiness Review',
                'lesson_code': 'M01.L07',
                'section_id': 'production-checklist',
                'placement': 'after_section',
                'description': 'Review a hypothetical agent and identify missing controls before '
                               'deployment.',
                'instructions': 'Review a hypothetical agent and identify missing controls before '
                                'deployment.',
                'expected_output': 'A prioritized readiness checklist with blockers and '
                                   'non-blockers.',
                'difficulty': DifficultyLevel.intermediate,
                'skill_tested': ['ai-agents', 'agentic-rag', 'analysis']}],
 'quiz': {'id': 'M01.L07.QUIZ',
          'title': 'From RAG to AI Agents — Lesson Quiz',
          'lesson_code': 'M01.L07',
          'placement': 'lesson_end',
          'questions': [{'type': 'mcq',
                         'section_id': 'what-is-agent',
                         'question': 'Which property most clearly distinguishes an agent from a '
                                     'single LLM completion?',
                         'options': ['It uses English',
                                     'It can iteratively choose and execute actions toward a goal',
                                     'It always has more parameters',
                                     'It must use a vector database'],
                         'correct': 1,
                         'explanation': 'Agents use iterative decision and action loops rather '
                                        'than only producing one completion.'},
                        {'type': 'mcq',
                         'section_id': 'rag-vs-agentic-rag',
                         'question': 'How does agentic RAG differ from a fixed RAG pipeline?',
                         'options': ['Retrieval becomes a dynamically chosen capability inside a '
                                     'broader loop',
                                     'It eliminates retrieval',
                                     'It forbids generation',
                                     'It requires multiple agents'],
                         'correct': 0,
                         'explanation': 'Agentic RAG lets the agent decide when and how to '
                                        'retrieve as part of a larger task.'},
                        {'type': 'mcq',
                         'section_id': 'agentic-stack',
                         'question': 'Which layer actually executes tool requests?',
                         'options': ['Reasoning LLM alone',
                                     'Orchestration layer',
                                     'User interface only',
                                     'Embedding model'],
                         'correct': 1,
                         'explanation': 'The LLM requests actions; orchestration executes and '
                                        'returns results.'},
                        {'type': 'mcq',
                         'section_id': 'single-agent',
                         'question': 'Why is a single-agent design often the best starting point?',
                         'options': ['It guarantees perfect answers',
                                     'It has fewer moving parts, lower cost, and simpler debugging',
                                     'It can use no tools',
                                     'It removes the need for memory'],
                         'correct': 1,
                         'explanation': 'Single-agent systems avoid inter-agent coordination '
                                        'overhead.'},
                        {'type': 'mcq',
                         'section_id': 'when-multi-agent',
                         'question': 'Which is a strong reason to introduce multiple agents?',
                         'options': ['You want more classes in the codebase',
                                     'Different subtasks require distinct security domains',
                                     'The prompt is short',
                                     'The model supports JSON'],
                         'correct': 1,
                         'explanation': "Security isolation is one of the chapter's explicit "
                                        'justifications for specialization.'},
                        {'type': 'mcq',
                         'section_id': 'retrieval-vs-rag-tool',
                         'question': 'What does retrieval-as-a-tool return?',
                         'options': ['Only a final grounded answer',
                                     'Raw evidence such as chunks for the agent to interpret',
                                     'A deployment manifest',
                                     'Only embeddings'],
                         'correct': 1,
                         'explanation': 'Retrieval tools expose evidence; the agent performs '
                                        'downstream synthesis.'},
                        {'type': 'mcq',
                         'section_id': 'tool-calling',
                         'question': 'Who should ultimately execute a model-requested tool call?',
                         'options': ['The natural-language model without validation',
                                     'Application/orchestration code after validation',
                                     'The user manually every time',
                                     'The embedding model'],
                         'correct': 1,
                         'explanation': 'Execution remains under application control.'},
                        {'type': 'mcq',
                         'section_id': 'react',
                         'question': 'What is the core ReAct pattern?',
                         'options': ['Train, compress, deploy',
                                     'Alternate action selection with observations',
                                     'Only retrieve once',
                                     'Always delegate to another agent'],
                         'correct': 1,
                         'explanation': 'ReAct repeatedly chooses an action and reasons over its '
                                        'observation.'},
                        {'type': 'mcq',
                         'section_id': 'mcp-primitives',
                         'question': 'Which MCP primitive represents contextual data addressable '
                                     'separately from a tool result?',
                         'options': ['Tool', 'Resource', 'Temperature', 'Agent Card'],
                         'correct': 1,
                         'explanation': 'Resources represent contextual data or state.'},
                        {'type': 'mcq',
                         'section_id': 'mcp-architecture',
                         'question': 'What does an MCP server do?',
                         'options': ['It is always the LLM itself',
                                     'It adapts standardized requests to an underlying capability',
                                     'It stores every prompt forever',
                                     'It replaces authentication'],
                         'correct': 1,
                         'explanation': 'The server exposes capabilities and translates MCP '
                                        'requests to the underlying system.'},
                        {'type': 'mcq',
                         'section_id': 'a2a',
                         'question': 'What problem does A2A primarily address?',
                         'options': ['Vector similarity',
                                     'Agent-to-agent collaboration',
                                     'Chunk overlap',
                                     'OCR'],
                         'correct': 1,
                         'explanation': 'A2A standardizes communication and delegation between '
                                        'agents.'},
                        {'type': 'mcq',
                         'section_id': 'crewai',
                         'question': 'Why use a researcher and writer as separate agents?',
                         'options': ['Because every task needs two models',
                                     'They have meaningfully different roles and dependent '
                                     'subtasks',
                                     'To remove the need for tools',
                                     'To guarantee lower latency'],
                         'correct': 1,
                         'explanation': 'Specialization is justified by distinct '
                                        'responsibilities.'},
                        {'type': 'mcq',
                         'section_id': 'long-term-memory',
                         'question': 'When is long-term memory most justified?',
                         'options': ['For every one-off interaction',
                                     'When persistent knowledge of the user or project reduces '
                                     'future friction',
                                     'Only when no database exists',
                                     'Only for calculators'],
                         'correct': 1,
                         'explanation': 'Persistent memory should create cumulative product '
                                        'value.'},
                        {'type': 'mcq',
                         'section_id': 'memory-poisoning',
                         'question': 'What is memory poisoning?',
                         'options': ['Deleting a vector index',
                                     'Persisting false or malicious information that later '
                                     'influences the agent',
                                     'Making a prompt shorter',
                                     'Using a cache'],
                         'correct': 1,
                         'explanation': 'Poisoned memories become trusted future context.'},
                        {'type': 'mcq',
                         'section_id': 'incorrect-tool-use',
                         'question': 'What most directly limits damage from a bad tool decision?',
                         'options': ['Longer prompts',
                                     'Least-privilege tool permissions',
                                     'More temperature',
                                     'More agents'],
                         'correct': 1,
                         'explanation': 'Permissions constrain the blast radius even when model '
                                        'reasoning fails.'},
                        {'type': 'mcq',
                         'section_id': 'termination-failure',
                         'question': 'What is a termination failure?',
                         'options': ['A tool has no API key',
                                     'The agent stops too early or loops too long because it '
                                     'cannot judge completion',
                                     'The model uses Markdown',
                                     'The vector database is empty'],
                         'correct': 1,
                         'explanation': 'Termination is about recognizing when the task is '
                                        'complete.'},
                        {'type': 'mcq',
                         'section_id': 'tracing',
                         'question': 'What does a trace provide that a final answer log does not?',
                         'options': ['Only the final token count',
                                     'The ordered spans of tool/LLM execution and timings',
                                     'A new model',
                                     'Automatic authorization'],
                         'correct': 1,
                         'explanation': 'Traces expose the internal execution path at the '
                                        'system-event level.'},
                        {'type': 'mcq',
                         'section_id': 'agent-metrics',
                         'question': 'Which metric can reveal a simple request stuck in a loop?',
                         'options': ['Number of LLM and API calls per task',
                                     'Screen resolution',
                                     'Embedding dimension alone',
                                     'Corpus file count'],
                         'correct': 0,
                         'explanation': 'Unexpectedly high call counts often indicate inefficient '
                                        'or looping execution.'},
                        {'type': 'open',
                         'section_id': 'retain-mental-model',
                         'question': 'Design a production agent architecture for a task of your '
                                     'choice. Explain the goal, tool boundaries, memory strategy, '
                                     'approval gates, and observability signals you would use.',
                         'expected_points': ['clear goal and agent boundary',
                                             'appropriate tools and permissions',
                                             'short-term/long-term memory choice',
                                             'human approval for risky actions',
                                             'tracing and agent-specific metrics']}],
          'passing_score': 70}}
