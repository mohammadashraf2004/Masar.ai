"""COURSE-007 AI Agents with MCP: example answers (part a)."""

EXAMPLES = {
    "COURSE-007.M01.L01.EX01": (
        """| # | Label | Why |
| 1 | Agentic workflow | The LLM does one step, but the program's fixed if/else decides the path |
| 2 | Agent | The LLM chooses which tool to call and when to stop, in a loop |
| 3 | Neither | A single prompt-response call, no tools or iterations |
| 4 | Agentic workflow | The model classifies, but application code controls the routing |
| 5 | (cycles below) | |

Agentic workflows are the cases where code controls the path (1 and 4); the agent (2) controls its own path. Example cycle for scenario 2: Reason - "The tests failed in test_parser; I should read parser.py." Act - call read_file("parser.py"). Observe - the file shows a missing None check. Reason - "Add the check." Act - write_file(...). Observe - file saved. Act - run_tests(). Observe - all tests pass, so the agent stops and reports.""",
        """| # | التصنيف | السبب |
| 1 | agentic workflow | الـ LLM ينفذ خطوة واحدة، لكن if/else الثابتة في البرنامج تحدد المسار |
| 2 | agent | الـ LLM يختار الأداة التي يستدعيها ومتى يتوقف، في حلقة |
| 3 | لا هذا ولا ذاك | استدعاء واحد prompt ثم رد، بلا أدوات أو تكرار |
| 4 | agentic workflow | النموذج يصنّف، لكن كود التطبيق يتحكم في التوجيه |

الحالتان 1 و4 workflows يتحكم فيها الكود في المسار؛ أما الحالة 2 فـ agent يتحكم في مساره. مثال دورة للحالة 2: Reason - "فشلت الاختبارات في test_parser؛ يجب أن أقرأ parser.py". Act - استدعاء read_file("parser.py"). Observe - يظهر الملف فحص None مفقودًا. Reason - "أضيف الفحص". Act - write_file(...). Observe - حُفظ الملف. Act - run_tests(). Observe - نجحت كل الاختبارات، فيتوقف الـ agent ويقدم تقريره.""",
    ),
    "COURSE-007.M01.L01.EX02": (
        """1. Host: the engineering assistant application (for example an IDE or chat app) that runs the LLM and talks to the user.
2. MCP client: inside the host, one client per server; it opens the connection, negotiates capabilities, lists and calls tools, reads resources and fetches prompts, and passes results back to the host.
3. Tool: create_deployment_ticket(service, version, environment, notes) -> returns the ticket ID and URL. Resource: docs://project/deployment-guide (read-only documentation). Prompt: deployment_review(service, change_summary) - a reusable template that asks the model to review risks, rollback plan and checks.
4. stdio for the first version: the server runs locally next to the host, needs no network setup or authentication, and is simplest to develop; move to Streamable HTTP when it becomes a shared remote service.
5. User -> Host (LLM decides to use a tool) -> MCP Client -> transport (stdio: JSON-RPC over stdin/stdout) -> MCP Server -> ticket system API; the result travels back Server -> transport -> Client -> Host -> LLM -> answer to the user.
6. Security: creating tickets is a write action - require user confirmation and scope the server's credentials to the ticket project only. Tool choice: if tool names or descriptions are vague, the model may call the wrong tool or invent parameters - keep few, clearly described tools.
7. Dozens of low-level endpoints flood the model's context, make it chain many calls correctly by itself, and increase errors; a few task-level tools that do the whole job (like create_deployment_ticket) are easier for the model to choose and use safely.""",
        """1. الـ host: تطبيق المساعد الهندسي (مثل IDE أو تطبيق محادثة) الذي يشغّل الـ LLM ويتحدث مع المستخدم.
2. الـ MCP client: داخل الـ host، عميل لكل server؛ يفتح الاتصال ويتفاوض على القدرات ويسرد الأدوات ويستدعيها ويقرأ الـ resources ويجلب الـ prompts ويعيد النتائج إلى الـ host.
3. Tool: ‏create_deployment_ticket(service, version, environment, notes) -> يعيد رقم التذكرة ورابطها. Resource: ‏docs://project/deployment-guide ‏(وثائق للقراءة فقط). Prompt: ‏deployment_review(service, change_summary) - قالب قابل لإعادة الاستخدام يطلب من النموذج مراجعة المخاطر وخطة التراجع والفحوص.
4. stdio للإصدار الأول: يعمل الـ server محليًا بجوار الـ host، ولا يحتاج إعداد شبكة أو مصادقة، وهو الأبسط في التطوير؛ ثم الانتقال إلى Streamable HTTP عندما يصبح خدمة بعيدة مشتركة.
5. المستخدم -> الـ Host ‏(يقرر الـ LLM استخدام أداة) -> الـ MCP Client -> الـ transport ‏(stdio: ‏JSON-RPC عبر stdin/stdout) -> الـ MCP Server -> API نظام التذاكر؛ وتعود النتيجة Server -> transport -> Client -> Host -> LLM -> الإجابة للمستخدم.
6. الأمان: إنشاء التذاكر عملية كتابة - تتطلب تأكيد المستخدم وتقييد صلاحيات الـ server بمشروع التذاكر فقط. اختيار الأداة: إذا كانت أسماء الأدوات أو أوصافها مبهمة فقد يستدعي النموذج الأداة الخطأ أو يخترع معاملات - لذا أبقي أدوات قليلة موصوفة بوضوح.
7. عشرات الـ endpoints منخفضة المستوى تُغرق سياق النموذج وتجعله مسؤولًا عن ربط استدعاءات كثيرة بنفسه وتزيد الأخطاء؛ أما أدوات قليلة على مستوى المهمة تنجز العمل كله (مثل create_deployment_ticket) فيسهل على النموذج اختيارها واستخدامها بأمان.""",
    ),
    "COURSE-007.M02.L01.EX01": (
        """| Scenario | Transport | Why |
| 1. Local filesystem server tied to the IDE | stdio | The host launches it as a subprocess and it dies with the IDE; no network exposure |
| 2. One SaaS endpoint for thousands of customers | Streamable HTTP | A remote, always-on service shared by many clients |
| 3. Local Python calculator in the project | stdio | Launched locally by the assistant, simplest setup |
| 4. Authenticated internal ticketing service | Streamable HTTP | Hosted centrally in the private network and reached over HTTP with authentication |

Security notes for scenario 2 (and 4): authenticate and authorize every request (OAuth tokens with scopes, per-tenant isolation so one customer can never reach another's data), and protect the endpoint itself (TLS, Origin header validation against DNS rebinding, rate limiting, and validation of all tool inputs).""",
        """| الحالة | الـ transport | السبب |
| 1. server محلي لنظام الملفات مرتبط بالـ IDE | stdio | يشغّله الـ host كعملية فرعية وينتهي بانتهاء الـ IDE؛ بلا تعرض للشبكة |
| 2. نقطة SaaS واحدة لآلاف العملاء | Streamable HTTP | خدمة بعيدة تعمل دائمًا ويشترك فيها عملاء كثيرون |
| 3. حاسبة Python محلية في المشروع | stdio | يشغّلها المساعد محليًا، أبسط إعداد |
| 4. خدمة تذاكر داخلية بمصادقة | Streamable HTTP | مستضافة مركزيًا في الشبكة الخاصة ويُوصل إليها عبر HTTP مع المصادقة |

ملاحظات أمنية للحالة 2 (و4): مصادقة كل طلب وتفويضه (OAuth tokens مع scopes، وعزل لكل عميل حتى لا يصل أحد إلى بيانات غيره أبدًا)، وحماية النقطة نفسها (TLS، والتحقق من Origin header ضد DNS rebinding، وحدود المعدل، والتحقق من كل مدخلات الأدوات).""",
    ),
    "COURSE-007.M02.L01.EX02": (
        """1. Host -> LLM: messages = [user: "What is 5 x 3 + 7?"], tools = [multiply_two_numbers(a, b), add_two_numbers(a, b)] (descriptions and schemas from tools/list).
2. LLM -> Host: tool_use multiply_two_numbers {"a": 5, "b": 3}.
3. Host -> MCP Client -> Server: JSON-RPC tools/call {name: "multiply_two_numbers", arguments: {a: 5, b: 3}}.
4. Server -> Client -> Host: result "15"; the host appends the assistant's tool request and a tool_result (15) to the conversation and calls the LLM again.
5. LLM -> tool_use add_two_numbers {"a": 15, "b": 7} -> Client -> Server -> result "22" -> appended to the history -> LLM called again.
6. The LLM now has everything it needs and returns text instead of a tool request: "5 x 3 + 7 = 22." The host shows it to the user.
7. The outer loop handles each user message; the inner loop must keep calling the LLM and executing tools until the LLM stops asking for tools, because one question can need several dependent tool calls (the addition needs the multiplication's result).""",
        """1. الـ Host -> الـ LLM: ‏messages = [user: "What is 5 x 3 + 7?"]، وtools = [multiply_two_numbers(a, b), add_two_numbers(a, b)] (الأوصاف والمخططات من tools/list).
2. الـ LLM -> الـ Host: ‏tool_use multiply_two_numbers {"a": 5, "b": 3}.
3. الـ Host -> الـ MCP Client -> الـ Server: ‏JSON-RPC tools/call {name: "multiply_two_numbers", arguments: {a: 5, b: 3}}.
4. الـ Server -> الـ Client -> الـ Host: النتيجة "15"؛ يضيف الـ host طلب الأداة ونتيجتها tool_result ‏(15) إلى المحادثة ويستدعي الـ LLM مرة أخرى.
5. الـ LLM -> tool_use add_two_numbers {"a": 15, "b": 7} -> Client -> Server -> النتيجة "22" -> تُضاف إلى السجل -> يُستدعى الـ LLM مجددًا.
6. صار لدى الـ LLM كل ما يحتاجه فيعيد نصًا بدل طلب أداة: "5 x 3 + 7 = 22." ويعرضه الـ host للمستخدم.
7. الحلقة الخارجية تعالج كل رسالة مستخدم؛ والحلقة الداخلية يجب أن تستمر في استدعاء الـ LLM وتنفيذ الأدوات حتى يتوقف عن طلب أدوات، لأن سؤالًا واحدًا قد يحتاج عدة استدعاءات متتابعة (فالجمع يحتاج نتيجة الضرب).""",
    ),
    "COURSE-007.M02.L01.EX03": (
        """1. "How should I deploy this service?" -> deployment-guide.md (plus architecture.md for the service's components).
2. "What failed in yesterday's deployment?" -> incident-log.txt (the build-artifact image only if the log points to it).
3. Strategy: an LLM selector - send the model the list of resource names and descriptions (not their contents) and ask which are needed; fall back to a user picker when it is unsure.
4. Trade-off: one extra, small LLM call adds some latency and tokens, but saves many more tokens than loading every resource into every prompt, and keeps irrelevant context from distracting the model.
5. Text resources are added as text blocks labelled with their URI (for example "<resource uri='docs://deployment-guide.md'> ... </resource>"); images are added as image content blocks (base64 with their MIME type) so a vision-capable model can see them.
6. Only accept names that exactly match a URI from resources/list; if the selector returns an unknown name, drop it (or ask the model again with the valid list) instead of trying to read it.""",
        """1. "How should I deploy this service?" -> deployment-guide.md (مع architecture.md لمكونات الخدمة).
2. "What failed in yesterday's deployment?" -> incident-log.txt (وصورة الـ build artifact فقط إذا أشار إليها السجل).
3. الاستراتيجية: LLM selector - أرسل للنموذج قائمة أسماء الـ resources وأوصافها (لا محتواها) وأسأله أيها مطلوب؛ مع الرجوع إلى اختيار المستخدم عندما لا يكون متأكدًا.
4. المقايضة: استدعاء LLM إضافي صغير يضيف بعض الزمن والـ tokens، لكنه يوفر tokens أكثر بكثير من تحميل كل الـ resources في كل prompt، ويمنع السياق غير المهم من تشتيت النموذج.
5. تُضاف الـ resources النصية ككتل نصية موسومة بالـ URI (مثل "<resource uri='docs://deployment-guide.md'> ... </resource>")؛ وتُضاف الصور ككتل محتوى صورة (base64 مع نوع MIME) ليراها نموذج يدعم الرؤية.
6. لا أقبل إلا الأسماء المطابقة تمامًا لـ URI من resources/list؛ وإذا أعاد المختار اسمًا غير معروف أتجاهله (أو أسأل النموذج مجددًا مع القائمة الصحيحة) بدل محاولة قراءته.""",
    ),
    "COURSE-007.M02.L02.EX01": (
        """1. Show the user: which server is asking, the full messages it wants sent (including the private document excerpt), its requested system prompt, model preferences and max tokens.
2. The user can approve, edit, or reject the request; and later approve, edit, or discard the model's output.
3. No. The server's system prompt is only a suggestion; the host keeps its own policies and may ignore or restrict the server's prompt so a server cannot change the model's behaviour silently.
4. Rate limit: at most N sampling requests per server per minute (for example 5), and a token budget per session; excess requests are rejected with an error.
5. Yes - the user should see the summary before it is returned, because it contains information derived from the private document that will leave the host.
6. Flow: client sends tools/call to the server -> the server, mid-operation, sends sampling/createMessage to the client -> the client shows the request to the user -> user approves (or edits/rejects) -> the client calls the host's LLM -> the client shows the result to the user -> user approves -> the client returns the result to the server -> the server finishes the tool operation and sends its final tools/call response.""",
        """1. أعرض على المستخدم: أي server يطلب، والرسائل الكاملة التي يريد إرسالها (بما فيها مقتطف المستند الخاص)، والـ system prompt المطلوب، وتفضيلات النموذج، وحد الـ tokens.
2. يستطيع المستخدم الموافقة على الطلب أو تعديله أو رفضه؛ ثم لاحقًا الموافقة على مخرج النموذج أو تعديله أو تجاهله.
3. لا. الـ system prompt الخاص بالـ server مجرد اقتراح؛ ويحتفظ الـ host بسياساته وقد يتجاهل prompt الـ server أو يقيده حتى لا يستطيع server تغيير سلوك النموذج بصمت.
4. حد المعدل: N طلبات sampling على الأكثر لكل server في الدقيقة (مثل 5)، مع ميزانية tokens لكل جلسة؛ وتُرفض الطلبات الزائدة بخطأ.
5. نعم - يجب أن يرى المستخدم الملخص قبل إعادته، لأنه يحتوي معلومات مشتقة من المستند الخاص ستغادر الـ host.
6. التدفق: يرسل العميل tools/call إلى الـ server -> يرسل الـ server أثناء العملية sampling/createMessage إلى العميل -> يعرض العميل الطلب على المستخدم -> يوافق المستخدم (أو يعدّل أو يرفض) -> يستدعي العميل الـ LLM الخاص بالـ host -> يعرض العميل النتيجة على المستخدم -> يوافق المستخدم -> يعيد العميل النتيجة إلى الـ server -> يُكمل الـ server عملية الأداة ويرسل رد tools/call النهائي.""",
    ),
    "COURSE-007.M02.L02.EX02": (
        """| OAuth role | Who |
| End user | The person using the host app who owns the project-management account |
| OAuth client | The host's MCP client |
| Resource server | The remote MCP server with the protected tools |
| Authorization server | The project-management identity provider that issues tokens |

1-2. When the MCP server returns 401 with a WWW-Authenticate challenge: (1) the client reads the protected-resource metadata to find the authorization server; (2) it fetches the authorization server's metadata (and registers if needed); (3) it opens the browser to the authorization URL with PKCE and the requested scopes; (4) the user logs in and consents; (5) the authorization server redirects back with a code, which the client exchanges for access and refresh tokens; (6) the client retries the MCP request with "Authorization: Bearer <token>".
3. Scopes: projects:read, tasks:read (read); tasks:write, tasks:assign (write).
4. Tokens are stored by the client in secure storage (the OS keychain or an encrypted store), never in the prompt, the model's context or logs.
5. The redirect URI is where the authorization server sends the user back with the code; it must be pre-registered so codes cannot be delivered to an attacker's address.
6. Authorization is a property of the connection, not of each tool: the HTTP client layer attaches tokens, refreshes them and handles 401s once for every request, instead of duplicating (and risking mistakes in) that logic in every tool wrapper.""",
        """| دور OAuth | من هو |
| المستخدم النهائي | الشخص الذي يستخدم تطبيق الـ host ويملك حساب إدارة المشاريع |
| OAuth client | الـ MCP client في الـ host |
| resource server | الـ MCP server البعيد صاحب الأدوات المحمية |
| authorization server | مزود الهوية لنظام إدارة المشاريع الذي يصدر الـ tokens |

1-2. عندما يعيد الـ MCP server الرمز 401 مع تحدي WWW-Authenticate: (1) يقرأ العميل protected-resource metadata ليعرف الـ authorization server؛ (2) يجلب metadata الـ authorization server (ويسجّل إن لزم)؛ (3) يفتح المتصفح على رابط التفويض مع PKCE والـ scopes المطلوبة؛ (4) يسجّل المستخدم دخوله ويوافق؛ (5) يعيده الـ authorization server مع code يستبدله العميل بـ access وrefresh tokens؛ (6) يعيد العميل طلب الـ MCP مع "Authorization: Bearer <token>".
3. الـ scopes: ‏projects:read وtasks:read (قراءة)؛ وtasks:write وtasks:assign (كتابة).
4. يخزن العميل الـ tokens في تخزين آمن (keychain النظام أو مخزن مشفر)، ولا توضع أبدًا في الـ prompt أو سياق النموذج أو السجلات.
5. الـ redirect URI هو المكان الذي يعيد إليه الـ authorization server المستخدم مع الـ code؛ ويجب تسجيله مسبقًا حتى لا تُسلَّم الأكواد إلى عنوان مهاجم.
6. التفويض خاصية للاتصال لا لكل أداة: طبقة عميل HTTP ترفق الـ tokens وتجددها وتعالج الـ 401 مرة واحدة لكل الطلبات، بدلًا من تكرار هذا المنطق (والمخاطرة بأخطاء فيه) داخل كل غلاف أداة.""",
    ),
    "COURSE-007.M02.L02.EX03": (
        """1. ClientSessionGroup connects to all three servers, keeps one ClientSession per server and aggregates their tools, resources and prompts into combined collections the host can present to the model.
2. Collision: both GitHub and Linear expose a tool named create_issue (or search).
3. Namespacing: prefix every primitive with its server: github__create_issue, linear__create_issue, docs__search (using the group's component-name hook to apply the prefix).
4. Keep a dictionary from the namespaced name to (server ID, session, original tool name); when the model calls github__create_issue, the host looks it up and calls create_issue on the GitHub session.
5. On disconnect, remove that server's tools, resources and prompts from the aggregated lists (and the mapping), refresh the tool list sent to the model, and return a clear error for any in-flight call - other servers keep working.
6. New problems: a malicious or compromised server can inject instructions through its tool descriptions or results that influence calls to other servers (cross-server prompt injection / data exfiltration from GitHub to Linear); and the growing number of tool definitions consumes context and makes the model more likely to choose the wrong tool.""",
        """1. يتصل ClientSessionGroup بالخوادم الثلاثة ويحتفظ بـ ClientSession لكل server ويجمع أدواتها وresources والـ prompts في مجموعات موحدة يعرضها الـ host على النموذج.
2. التصادم: كل من GitHub وLinear يعرض أداة اسمها create_issue (أو search).
3. التسمية بنطاقات (namespacing): بادئة باسم الـ server لكل عنصر: github__create_issue وlinear__create_issue وdocs__search (باستخدام خطاف أسماء المكونات في المجموعة لتطبيق البادئة).
4. أحتفظ بقاموس من الاسم ذي النطاق إلى (معرّف الـ server والجلسة واسم الأداة الأصلي)؛ وعندما يستدعي النموذج github__create_issue يبحث الـ host فيه ويستدعي create_issue على جلسة GitHub.
5. عند الانفصال أزيل أدوات ذلك الـ server وresources والـ prompts من القوائم المجمعة (ومن القاموس)، وأحدّث قائمة الأدوات المرسلة للنموذج، وأعيد خطأ واضحًا لأي استدعاء جارٍ - بينما تستمر الخوادم الأخرى في العمل.
6. مشكلات جديدة: server خبيث أو مخترق قد يحقن تعليمات عبر أوصاف أدواته أو نتائجها تؤثر في استدعاءات خوادم أخرى (cross-server prompt injection أو تسريب بيانات من GitHub إلى Linear)؛ وتزايد عدد تعريفات الأدوات يستهلك السياق ويزيد احتمال اختيار النموذج للأداة الخطأ.""",
    ),
    "COURSE-007.M02.L02.EX04": (
        """| | A. Full list every turn | B. search_tools + progressive loading | C. Sandboxed code with typed stubs |
| Token usage | Very high (180 schemas every turn) | Low (only matched tools) | Lowest in context; intermediate data stays in the sandbox |
| Latency / round trips | Fewest round trips, but large prompts | Extra search round trips | Few model turns, but code generation and execution add time |
| Complexity | Simplest | Moderate (search index, dynamic tool list) | Highest (sandbox, stub generation, runtime) |
| Tool freshness | Always current (refreshed each turn) | Current if the index refreshes | Stubs must be regenerated when tools change |
| Security | Standard tool-call approval | Standard, plus search must not expose hidden tools | Executing model-written code needs strong isolation and egress limits |

1. Small internal prototype: A - few tools, simplicity matters most.
2. Production assistant with 180 tools: B - keeps context small and accuracy high without the risk and cost of running generated code.
3. Automation environment with a hardened sandbox: C - the isolation already exists, and composing many tool calls in code saves the most tokens and round trips.""",
        """| | A. القائمة كاملة كل دور | B. أداة search_tools مع تحميل تدريجي | C. كود في sandbox مع stubs بأنواع |
| استهلاك الـ tokens | مرتفع جدًا (180 مخططًا كل دور) | منخفض (الأدوات المطابقة فقط) | الأقل في السياق؛ وتبقى البيانات الوسيطة في الـ sandbox |
| الزمن والرحلات | أقل رحلات لكن prompts كبيرة | رحلات بحث إضافية | أدوار نموذج قليلة، لكن توليد الكود وتنفيذه يضيفان وقتًا |
| التعقيد | الأبسط | متوسط (فهرس بحث وقائمة أدوات ديناميكية) | الأعلى (sandbox وتوليد stubs وبيئة تشغيل) |
| حداثة الأدوات | حديثة دائمًا (تُحدَّث كل دور) | حديثة إذا حُدّث الفهرس | يجب إعادة توليد الـ stubs عند تغير الأدوات |
| الأمان | موافقة استدعاء الأدوات المعتادة | معتاد، مع ألا يكشف البحث أدوات مخفية | تنفيذ كود كتبه النموذج يحتاج عزلًا قويًا وتقييدًا للاتصال الخارجي |

1. نموذج أولي داخلي صغير: A - أدوات قليلة والبساطة أهم شيء.
2. مساعد إنتاجي بـ 180 أداة: B - يبقي السياق صغيرًا والدقة عالية دون مخاطر وتكلفة تشغيل كود مولَّد.
3. بيئة أتمتة بها sandbox محصّن: C - العزل موجود أصلًا، وتركيب استدعاءات كثيرة في الكود يوفر أكبر قدر من الـ tokens والرحلات.""",
    ),
    "COURSE-007.M03.L01.EX01": (
        """| Scenario | Server API | Transport | Why |
| 1. Local calculator for one developer | MCPServer | stdio | Typed decorators are the fastest way; launched locally by the IDE |
| 2. Hosted company service for many users | MCPServer | Streamable HTTP | Normal tools/prompts/resources, but remote and multi-user |
| 3. Research prototype customizing tools/list per client | Low-level API | stdio (or HTTP if remote) | Needs direct control over request handlers that the high-level API hides |
| 4. Normal production server with a few typed tools | MCPServer | Streamable HTTP (stdio if it is a local server) | The high-level API covers it with less code and fewer mistakes |

Security for the remote case: authenticate and authorize every request (OAuth tokens, scopes per user, never trusting client-supplied identities), and protect the transport and inputs (TLS, Origin validation, rate limiting, strict validation of tool arguments, least-privilege credentials for the backends the tools call).""",
        """| الحالة | واجهة الـ server | الـ transport | السبب |
| 1. حاسبة محلية لمطور واحد | MCPServer | stdio | الـ decorators ذات الأنواع أسرع طريقة؛ ويشغّله الـ IDE محليًا |
| 2. خدمة شركة مستضافة لمستخدمين كثيرين | MCPServer | Streamable HTTP | أدوات وprompts وresources عادية، لكنها بعيدة ومتعددة المستخدمين |
| 3. نموذج بحثي يخصص tools/list لكل عميل | الواجهة منخفضة المستوى | stdio (أو HTTP إن كانت بعيدة) | يحتاج تحكمًا مباشرًا في معالجات الطلبات التي تخفيها الواجهة عالية المستوى |
| 4. server إنتاجي عادي ببضع أدوات ذات أنواع | MCPServer | Streamable HTTP (أو stdio إن كان محليًا) | الواجهة عالية المستوى تغطيه بكود أقل وأخطاء أقل |

الأمان للحالة البعيدة: مصادقة كل طلب وتفويضه (OAuth tokens وscopes لكل مستخدم وعدم الثقة بهويات يرسلها العميل)، وحماية الـ transport والمدخلات (TLS، والتحقق من Origin، وحدود المعدل، والتحقق الصارم من معاملات الأدوات، وأقل الصلاحيات لبيانات اعتماد الأنظمة التي تستدعيها الأدوات).""",
    ),
    "COURSE-007.M03.L01.EX02": (
        """Tool 1: tickets__create_bug_for_user
Description: "Create a bug ticket, assign it to a person found by name or email, and set its status (default: ready for triage). Use this whenever the user wants a new bug filed for someone."
Inputs: {"title": string, "description": string, "assignee": string (name or email), "project": string, "status": enum ["ready_for_triage", "in_progress"] (default "ready_for_triage")}
Output: {"ticket_id": string, "url": string, "assignee": {"id": string, "name": string}, "status": string}
Tool 2 (optional): tickets__find_user(query) -> [{"id", "name", "email"}] for when the assignee is ambiguous.
5. Private helpers inside tool 1: search_user (resolve "Bob"), fetch_project, create_ticket, assign_ticket, change_status; add_comment stays internal unless a separate "comment on ticket" story needs it.
6. The model makes one call that matches the user's intent instead of planning and ordering six calls, passing IDs between them correctly; fewer tools mean less context, fewer wrong choices, and the server handles errors (for example "Bob" not found or several Bobs) with a clear message.""",
        """الأداة 1: ‏tickets__create_bug_for_user
الوصف: "Create a bug ticket, assign it to a person found by name or email, and set its status (default: ready for triage). Use this whenever the user wants a new bug filed for someone."
المدخلات: {"title": string، "description": string، "assignee": string (الاسم أو البريد)، "project": string، "status": enum ["ready_for_triage", "in_progress"] (الافتراضي "ready_for_triage")}
المخرج: {"ticket_id": string، "url": string، "assignee": {"id": string، "name": string}، "status": string}
الأداة 2 (اختيارية): ‏tickets__find_user(query) -> [{"id", "name", "email"}] عندما يكون المكلَّف غامضًا.
5. مساعدات خاصة داخل الأداة 1: ‏search_user (لتحديد "Bob")، وfetch_project، وcreate_ticket، وassign_ticket، وchange_status؛ ويبقى add_comment داخليًا ما لم تحتجه قصة منفصلة "comment on ticket".
6. يجري النموذج استدعاءً واحدًا يطابق قصد المستخدم بدلًا من التخطيط وترتيب ستة استدعاءات وتمرير المعرّفات بينها بشكل صحيح؛ والأدوات الأقل تعني سياقًا أقل واختيارات خاطئة أقل، ويعالج الـ server الأخطاء (مثل عدم وجود "Bob" أو وجود أكثر من Bob) برسالة واضحة.""",
    ),
    "COURSE-007.M03.L01.EX03": (
        """Prompt name: code_review. Arguments: language (required), code (required), review_focus (optional: "security", "performance", "readability"; default "general").
Template: "You are reviewing {language} code. Review the code below with a focus on {review_focus}. Identify real problems only; do not invent issues. For each problem give its location, why it matters, and a concrete fix. Then list anything done well.
Code:
{code}
Output format:
## Summary (2-3 sentences)
## Issues (severity: high/medium/low - location - problem - fix)
## Strengths"
4. No full example by default: an example review anchors the model to the same kinds of issues and wording; a short format example is enough. An example could be offered as a separate variant.
5. A multiturn prompt helps: a user message with the code, then an assistant prefill starting with "## Summary" nudges the model straight into the structure - but keep it optional, because not every client/model supports prefill.
6. The client calls prompts/list to discover code_review with its argument descriptions, shows it to the user (for example as a slash command), collects the arguments, calls prompts/get with them, and inserts the returned messages into the conversation.
7. Avoid making provider-specific tricks mandatory - for example a particular model's XML tag conventions or a required assistant prefill - since the server's prompts must work with whatever model the host uses.""",
        """اسم الـ prompt: ‏code_review. المعاملات: language (إلزامي)، وcode (إلزامي)، وreview_focus (اختياري: "security" أو "performance" أو "readability"؛ والافتراضي "general").
القالب: "You are reviewing {language} code. Review the code below with a focus on {review_focus}. Identify real problems only; do not invent issues. For each problem give its location, why it matters, and a concrete fix. Then list anything done well.
Code:
{code}
Output format:
## Summary (2-3 sentences)
## Issues (severity: high/medium/low - location - problem - fix)
## Strengths"
4. لا مثال كاملًا افتراضيًا: مثال مراجعة يثبّت النموذج على أنواع المشكلات والصياغة نفسها (anchoring)؛ ويكفي مثال قصير للشكل. ويمكن تقديم مثال كنسخة منفصلة.
5. الـ prompt متعدد الأدوار مفيد: رسالة مستخدم بالكود ثم assistant prefill يبدأ بـ "## Summary" يدفع النموذج مباشرة إلى البنية - لكن أبقيه اختياريًا لأن ليس كل عميل أو نموذج يدعم الـ prefill.
6. يستدعي العميل prompts/list فيكتشف code_review مع أوصاف معاملاته، ويعرضه على المستخدم (مثلًا كأمر slash)، ويجمع المعاملات، ويستدعي prompts/get بها، ويدرج الرسائل العائدة في المحادثة.
7. أتجنب جعل حيل مزود معين إلزامية - مثل اصطلاحات وسوم XML لنموذج بعينه أو prefill إلزامي - لأن prompts الـ server يجب أن تعمل مع أي نموذج يستخدمه الـ host.""",
    ),
}
