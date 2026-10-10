"""COURSE-007 AI Agents with MCP: example answers (part b)."""

EXAMPLES = {
    "COURSE-007.M03.L01.EX04": (
        """1. Resource template: logs://app/{date}{?level,start,end,offset,limit} - for example logs://app/2026-10-09?level=ERROR&limit=500.
2. Parameters: date (one daily file), level (ERROR/WARN/INFO), start/end time within the day, offset and limit (lines per page, capped e.g. at 1,000) so clients fetch manageable slices.
3. Only return data: filtering by the requested parameters is fine, but analysis belongs to a tool (e.g. summarize_errors) or to the model; resources are read-only context, and mixing analysis into them hides logic from the client.
4. URL indirection is better when the content is too large for the transport and context (a whole day's 500 MB file): return a link the client can download or stream outside the MCP message, instead of inlining it.
5. Metadata: name and description (date, service), mimeType (text/plain), size in bytes and line count, time range covered, and last-modified time - so a client can decide before loading.
6. Flow: the client calls resources/list (and resources/templates/list) to discover the template and available dates -> fills in the template -> calls resources/read with the URI -> the server returns contents with uri, mimeType and text.
7. The client subscribes with resources/subscribe for a URI; when the current day's log grows, the server sends notifications/resources/updated with that URI, and the client re-reads it (notifications/resources/list_changed announces new daily files).""",
        """1. قالب الـ resource: ‏logs://app/{date}{?level,start,end,offset,limit} - مثل logs://app/2026-10-09?level=ERROR&limit=500.
2. المعاملات: date (ملف يوم واحد)، وlevel ‏(ERROR/WARN/INFO)، وstart/end للوقت داخل اليوم، وoffset وlimit (أسطر لكل صفحة بحد أقصى مثل 1,000) ليجلب العملاء أجزاء يمكن التعامل معها.
3. إعادة البيانات فقط: الترشيح حسب المعاملات المطلوبة مقبول، لكن التحليل مكانه أداة (مثل summarize_errors) أو النموذج؛ فالـ resources سياق للقراءة فقط، وخلط التحليل فيها يخفي المنطق عن العميل.
4. الإحالة بالرابط (URL indirection) أفضل عندما يكون المحتوى أكبر من الـ transport والسياق (ملف يوم كامل 500 MB): أعيد رابطًا يستطيع العميل تنزيله أو بثّه خارج رسالة الـ MCP بدل تضمينه.
5. الـ metadata: الاسم والوصف (التاريخ والخدمة)، وmimeType ‏(text/plain)، والحجم بالـ bytes وعدد الأسطر، والفترة الزمنية المغطاة، ووقت آخر تعديل - ليقرر العميل قبل التحميل.
6. التدفق: يستدعي العميل resources/list (وresources/templates/list) لاكتشاف القالب والتواريخ المتاحة -> يملأ القالب -> يستدعي resources/read بالـ URI -> يعيد الـ server المحتوى مع uri وmimeType وtext.
7. يشترك العميل عبر resources/subscribe في URI؛ وعندما يكبر سجل اليوم الحالي يرسل الـ server ‏notifications/resources/updated بذلك الـ URI فيعيد العميل قراءته (وتعلن notifications/resources/list_changed عن ملفات أيام جديدة).""",
    ),
    "COURSE-007.M03.L03.EX01": (
        """1. Connect the Inspector (stdio command or the remote URL). Expect a successful initialize, the server name/version and capabilities (tools, resources, prompts, elicitation); the Tools and Resources tabs list create_ticket and the project://{id} template.
2. Call create_ticket with valid arguments (title, project, description). Expect a result with the ticket ID and URL (structuredContent matching the output schema) and no isError.
3. Call it with a missing title and with a wrong type. Expect a clear validation error - a protocol-level invalid-params error or a tool result with isError: true - not a crash or a created ticket.
4. List resources/templates, fill project://42 and read it. Expect JSON/text content for project 42; reading a nonexistent ID returns a clear error.
5. Trigger the confirmation: answer Accept (ticket created), Decline (no ticket, a polite declined result) and Cancel (operation aborted, no ticket); each response appears in the history.
6. Connect remotely without a token: expect 401 with a WWW-Authenticate challenge; complete the OAuth flow in the Inspector's auth settings; then the same calls succeed, and a token without write scope cannot call create_ticket.
7. Open the history/notifications pane: check request/response pairs and IDs, progress or logging notifications, and list_changed notifications if tools change.
8. Remote failure case: after deployment behind a proxy, requests fail with 403 because of Origin/host validation (or the session ID is lost between replicas); expect a clear error and confirm the fix by re-running steps 1-2.""",
        """1. أوصل الـ Inspector (أمر stdio أو الرابط البعيد). المتوقع: initialize ناجح، واسم الـ server وإصداره وقدراته (tools وresources وprompts وelicitation)؛ وتسرد تبويبات Tools وResources الأداة create_ticket والقالب project://{id}.
2. أستدعي create_ticket بمعاملات صحيحة (العنوان والمشروع والوصف). المتوقع: نتيجة برقم التذكرة ورابطها (structuredContent مطابق لمخطط المخرج) بلا isError.
3. أستدعيها بعنوان مفقود ونوع خاطئ. المتوقع: خطأ تحقق واضح - خطأ invalid params على مستوى البروتوكول أو نتيجة أداة بـ isError: true - لا انهيار ولا تذكرة منشأة.
4. أسرد resources/templates وأملأ project://42 وأقرؤه. المتوقع: محتوى JSON/نص للمشروع 42؛ وقراءة رقم غير موجود تعيد خطأ واضحًا.
5. أطلق التأكيد: أجيب Accept (تُنشأ التذكرة)، وDecline (لا تذكرة مع نتيجة رفض مهذبة)، وCancel (تُلغى العملية بلا تذكرة)؛ ويظهر كل رد في السجل.
6. أتصل عن بُعد بلا token: المتوقع 401 مع تحدي WWW-Authenticate؛ أكمل تدفق OAuth في إعدادات المصادقة في الـ Inspector؛ ثم تنجح الاستدعاءات نفسها، ولا يستطيع token بلا scope الكتابة استدعاء create_ticket.
7. أفتح لوحة السجل والإشعارات: أتحقق من أزواج الطلب والرد ومعرّفاتها، وإشعارات التقدم أو التسجيل، وإشعارات list_changed إذا تغيرت الأدوات.
8. حالة فشل بعد النشر: خلف proxy تفشل الطلبات بـ 403 بسبب التحقق من Origin/host (أو يضيع session ID بين النسخ)؛ المتوقع خطأ واضح، ثم أتأكد من الإصلاح بإعادة الخطوتين 1-2.""",
    ),
    "COURSE-007.M03.L03.EX02": (
        """| # | User request | Expected tool |
| 1 | "Open a bug: login button does nothing on Safari" | github_create_issue |
| 2 | "Add a note to issue #42 that it also happens on Firefox" | github_comment_issue |
| 3 | "Close #57, it was fixed in the last release" | github_close_issue |
| 4 | "Are there any open issues about dark mode?" | github_search_issues |
| 5 | "Report that the export crashes with large files" | github_create_issue |
| 6 | "Tell the people on #12 the fix is deployed" | github_comment_issue |
| 7 | "Find issues assigned to Sara labelled urgent" | github_search_issues |
| 8 | "Mark issue 88 as done" | github_close_issue |
| 9 (ambiguous) | "There's a problem with payments" | github_search_issues first (it may already exist), not create |
| 10 (ambiguous) | "#42 is a duplicate of #40" | github_comment_issue on #42 (closing too is acceptable only with confirmation) |

3. Tool-choice accuracy = requests where the first tool called equals the expected tool / all requests (multi-step cases scored on the full expected sequence).
4. Structured assertion: for github_close_issue the arguments must validate against the schema and issue_number must equal the number in the request (57).
5. Cost: average input + output tokens (and dollars) per task, including retries.
6. Different model families and sizes interpret descriptions differently; a tool set that only works with one large model is fragile, and the results show whether a cheaper model is reliable enough.
7. Group failures by confused tool pairs; rewrite names and descriptions to state when to use and when not to use each tool (for example "search before creating to avoid duplicates"), add parameter descriptions, re-run the suite and keep the change only if accuracy improves without regressions.""",
        """| # | طلب المستخدم | الأداة المتوقعة |
| 1 | "Open a bug: login button does nothing on Safari" | github_create_issue |
| 2 | "Add a note to issue #42 that it also happens on Firefox" | github_comment_issue |
| 3 | "Close #57, it was fixed in the last release" | github_close_issue |
| 4 | "Are there any open issues about dark mode?" | github_search_issues |
| 5 | "Report that the export crashes with large files" | github_create_issue |
| 6 | "Tell the people on #12 the fix is deployed" | github_comment_issue |
| 7 | "Find issues assigned to Sara labelled urgent" | github_search_issues |
| 8 | "Mark issue 88 as done" | github_close_issue |
| 9 (غامض) | "There's a problem with payments" | github_search_issues أولًا (قد تكون موجودة)، لا الإنشاء |
| 10 (غامض) | "#42 is a duplicate of #40" | github_comment_issue على #42 (والإغلاق مقبول فقط بتأكيد) |

3. دقة اختيار الأداة = الطلبات التي كانت أول أداة مستدعاة فيها هي المتوقعة ÷ كل الطلبات (وتُقيَّم الحالات متعددة الخطوات على التسلسل المتوقع كاملًا).
4. تأكيد منظم: لـ github_close_issue يجب أن تتحقق المعاملات من المخطط وأن يساوي issue_number الرقم المذكور في الطلب (57).
5. التكلفة: متوسط tokens المدخل والمخرج (والدولارات) لكل مهمة، شاملة إعادة المحاولات.
6. عائلات النماذج وأحجامها تفسر الأوصاف بشكل مختلف؛ ومجموعة أدوات لا تعمل إلا مع نموذج كبير واحد هشة، والنتائج توضح هل نموذج أرخص موثوق بما يكفي.
7. أجمع الأخطاء حسب أزواج الأدوات المخلوطة؛ وأعيد كتابة الأسماء والأوصاف لتوضيح متى تُستخدم كل أداة ومتى لا (مثل "search before creating to avoid duplicates")، وأضيف أوصافًا للمعاملات، ثم أعيد التشغيل ولا أحتفظ بالتغيير إلا إذا تحسنت الدقة دون تراجعات.""",
    ),
    "COURSE-007.M03.L03.EX03": (
        """1. Lethal trifecta: access to private data (project documents) + exposure to untrusted content (public web pages) + external communication (messages to external users). A web page can inject instructions that make the agent send private documents out.
2. Vulnerability classes: prompt injection through fetched content (indirect injection); tool poisoning (malicious instructions in tool descriptions or results); data exfiltration through the messaging tool; excessive permissions / confused deputy (the server acts with more rights than the user); token or credential theft; SSRF through the fetch tool (fetching internal URLs).
3. Layer 1 (infrastructure): run the server in an isolated container with egress allow-listing; the fetch tool cannot reach internal network ranges (blocks SSRF).
4. Layer 2 (access): OAuth with per-user scopes so the server only reads documents the user can read; separate, narrowly scoped credentials for the messaging API with an allow-list of recipients.
5. Layer 3 (operations): audit logging of every tool call with arguments and results; monitoring and rate limits on outgoing messages (alerts on unusual volume or new recipients).
6. MCP Colors: fetch_web_page - red (brings in untrusted content); send_external_message - blue (critical action that can exfiltrate or cause harm); read_project_document - neither (private data, but it neither brings untrusted content nor acts externally).
7. Redesign: never allow red and blue tools in the same session - when a conversation has fetched untrusted web content, the send_external_message tool is removed for that session (or outgoing messages are restricted to fixed templates without document content). Sessions that need to message users work only with internal documents.
8. Human approval for every external message (showing recipient and full content), and for any action that combines web-derived content with private documents.""",
        """1. الثالوث القاتل (lethal trifecta): الوصول إلى بيانات خاصة (مستندات المشروع) + التعرض لمحتوى غير موثوق (صفحات الويب العامة) + التواصل الخارجي (رسائل لمستخدمين خارجيين). فقد تحقن صفحة ويب تعليمات تجعل الـ agent يرسل المستندات الخاصة للخارج.
2. فئات الثغرات: prompt injection عبر المحتوى المجلوب (حقن غير مباشر)؛ وtool poisoning (تعليمات خبيثة في أوصاف الأدوات أو نتائجها)؛ وتسريب البيانات عبر أداة المراسلة؛ والصلاحيات الزائدة / confused deputy (يتصرف الـ server بصلاحيات أكثر من المستخدم)؛ وسرقة الـ tokens أو بيانات الاعتماد؛ وSSRF عبر أداة الجلب (جلب روابط داخلية).
3. الطبقة 1 (البنية التحتية): تشغيل الـ server في حاوية معزولة مع قائمة سماح للاتصال الخارجي؛ وأداة الجلب لا تصل إلى نطاقات الشبكة الداخلية (منع SSRF).
4. الطبقة 2 (الوصول): OAuth بصلاحيات لكل مستخدم فلا يقرأ الـ server إلا المستندات التي يحق للمستخدم قراءتها؛ وبيانات اعتماد منفصلة ومحدودة لـ API المراسلة مع قائمة مستلمين مسموحين.
5. الطبقة 3 (التشغيل): تسجيل تدقيقي لكل استدعاء أداة بمعاملاته ونتائجه؛ ومراقبة الرسائل الصادرة وحدود معدلها (تنبيهات على الحجم غير المعتاد أو المستلمين الجدد).
6. ألوان MCP: ‏fetch_web_page - أحمر (يدخل محتوى غير موثوق)؛ وsend_external_message - أزرق (إجراء حرج قد يسرّب أو يضر)؛ وread_project_document - لا هذا ولا ذاك (بيانات خاصة لكنها لا تدخل محتوى غير موثوق ولا تتصرف خارجيًا).
7. إعادة التصميم: لا يُسمح أبدًا بأدوات حمراء وزرقاء في الجلسة نفسها - فعندما تجلب المحادثة محتوى ويب غير موثوق تُزال أداة send_external_message من تلك الجلسة (أو تُقيَّد الرسائل الصادرة بقوالب ثابتة بلا محتوى مستندات). والجلسات التي تحتاج مراسلة المستخدمين تعمل بالمستندات الداخلية فقط.
8. موافقة بشرية على كل رسالة خارجية (مع عرض المستلم والمحتوى كاملًا)، وعلى أي إجراء يجمع محتوى مأخوذًا من الويب مع مستندات خاصة.""",
    ),
    "COURSE-007.M03.L03.EX04": (
        """A. Local distribution
1. Repository: src/<package>/server.py, pyproject.toml with a console-script entry point, README, LICENSE, CHANGELOG, tests/, examples/ with client config snippets.
2. Install: "uvx <package>" (or "pip install <package>"), plus a ready-to-paste client configuration: {"command": "uvx", "args": ["<package>"], "env": {...}}.
3. Document every environment variable (API keys, base URLs, allowed directories), what each tool can read/write, and the minimum permissions/scopes the credentials need.
4. Optionally build an MCPB bundle (manifest plus server) so desktop clients can install it with one click, with user-configurable settings in the manifest.
5. Offer a Docker image that runs the server over stdio as a non-root user with a read-only filesystem, no extra network access and only the needed volumes mounted.
B. Remote distribution
1. Run with Streamable HTTP on one endpoint (for example /mcp), stateless mode if possible for easier scaling, with correct host/Origin validation.
2. Authentication at the HTTP layer: the server acts as an OAuth resource server validating bearer tokens (audience, scopes) before any MCP handling; per-tool scope checks for write actions.
3. Mount the MCP ASGI app inside a Starlette/FastAPI application alongside /health and metadata routes, behind a reverse proxy that terminates TLS.
4. Container: small pinned base image, non-root user, dependencies locked, image scanned and signed, configuration only via environment and secrets manager.
5. Scaling: stateless servers behind a load balancer, or sticky sessions/shared session storage when sessions are stateful; long-running operations moved to a task store.
6. Limits and observability: maximum request body size and tool output size, timeouts, rate limits; structured logs, metrics (latency, errors per tool) and traces with request IDs.
7. Publish the package to PyPI and the server entry to the MCP Registry with a server.json, proving namespace ownership (for example via the GitHub account or DNS for a domain-based name).""",
        """أ. التوزيع المحلي
1. المستودع: src/<package>/server.py، وpyproject.toml مع نقطة دخول console script، وREADME وLICENSE وCHANGELOG، ومجلد tests/، ومجلد examples/ بمقتطفات إعداد العملاء.
2. التثبيت: "uvx <package>" (أو "pip install <package>")، مع إعداد عميل جاهز للصق: {"command": "uvx", "args": ["<package>"], "env": {...}}.
3. توثيق كل متغير بيئة (مفاتيح API والروابط الأساسية والمجلدات المسموحة)، وما تستطيع كل أداة قراءته وكتابته، وأقل الصلاحيات/الـ scopes اللازمة لبيانات الاعتماد.
4. اختياريًا حزمة MCPB ‏(manifest مع الـ server) ليثبّتها عملاء سطح المكتب بنقرة واحدة، مع إعدادات يضبطها المستخدم في الـ manifest.
5. تقديم صورة Docker تشغّل الـ server عبر stdio بمستخدم غير root ونظام ملفات للقراءة فقط وبلا وصول شبكي إضافي ومع تركيب المجلدات اللازمة فقط.
ب. التوزيع البعيد
1. التشغيل بـ Streamable HTTP على نقطة واحدة (مثل /mcp)، وبوضع stateless إن أمكن لتسهيل التوسع، مع تحقق صحيح من host/Origin.
2. المصادقة في طبقة HTTP: يعمل الـ server كـ OAuth resource server يتحقق من bearer tokens ‏(الجمهور والـ scopes) قبل أي معالجة MCP؛ مع فحص scope لكل أداة كتابة.
3. تركيب تطبيق MCP ASGI داخل تطبيق Starlette/FastAPI بجوار مسارات /health والـ metadata، خلف reverse proxy ينهي TLS.
4. الحاوية: صورة أساس صغيرة بإصدار مثبت، ومستخدم غير root، واعتماديات مقفلة، وصورة مفحوصة وموقعة، والإعداد عبر البيئة ومدير الأسرار فقط.
5. التوسع: خوادم stateless خلف موازن حمل، أو sticky sessions/تخزين جلسات مشترك عندما تكون الجلسات ذات حالة؛ ونقل العمليات الطويلة إلى مخزن مهام.
6. الحدود والمراقبة: حد أقصى لحجم جسم الطلب ومخرجات الأدوات، ومهلات، وحدود معدل؛ مع سجلات منظمة ومقاييس (الزمن والأخطاء لكل أداة) وتتبع بمعرّفات الطلبات.
7. نشر الحزمة على PyPI وإدراج الـ server في MCP Registry بملف server.json، مع إثبات ملكية النطاق (مثلًا عبر حساب GitHub أو DNS للأسماء القائمة على نطاق).""",
    ),
    "COURSE-007.M04.L01.EX01": (
        """| Scenario | Layer | Message type | ID behaviour | Reasoning |
| 1. Unknown required parameter in tools/call | Protocol (JSON-RPC) | Error response, -32602 Invalid params | Same id as the request | The request itself is malformed for the protocol |
| 2. Tool runs, project does not exist | Application | Successful result with isError: true and an explanatory message | Same id | The protocol worked; the tool reports a business error the model can read and react to |
| 3. Connection times out | Transport | No JSON-RPC message at all | Pending entry fails locally with a timeout | Nothing came back; the client raises an error and cleans up the request |
| 4. Tool list changed | Protocol notification | notifications/tools/list_changed | No id (no response expected) | The client should call tools/list again |
| 5. Progress 60/100 | Protocol notification | notifications/progress with the request's progressToken, progress 60, total 100 | No id; linked through the progressToken | Informs about a running request without completing it |
| 6. Content + structuredContent | Result | Successful tools/call result | Same id | Human-readable content plus machine-readable data matching the output schema |

7. Request {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {...}} -> response {"jsonrpc": "2.0", "id": 7, "result": {...}}: the client matches the response to its pending request by id 7.""",
        """| الحالة | الطبقة | نوع الرسالة | سلوك الـ ID | التعليل |
| 1. معامل إلزامي غير معروف في tools/call | البروتوكول (JSON-RPC) | رد خطأ -32602 Invalid params | نفس id الطلب | الطلب نفسه غير صالح للبروتوكول |
| 2. الأداة تعمل والمشروع غير موجود | التطبيق | نتيجة ناجحة بـ isError: true مع رسالة توضيحية | نفس الـ id | البروتوكول عمل؛ والأداة تبلغ عن خطأ عمل يستطيع النموذج قراءته والتصرف بناءً عليه |
| 3. انتهاء مهلة الاتصال | الـ transport | لا رسالة JSON-RPC إطلاقًا | يفشل الطلب المعلق محليًا بانتهاء المهلة | لم يعد شيء؛ فيطلق العميل خطأ وينظف الطلب |
| 4. تغيّر قائمة الأدوات | إشعار بروتوكول | notifications/tools/list_changed | بلا id (لا يُنتظر رد) | يجب أن يستدعي العميل tools/list مجددًا |
| 5. تقدم 60/100 | إشعار بروتوكول | notifications/progress مع progressToken الطلب وprogress 60 وtotal 100 | بلا id؛ ويرتبط عبر progressToken | يخبر عن طلب جارٍ دون إنهائه |
| 6. content مع structuredContent | نتيجة | نتيجة tools/call ناجحة | نفس الـ id | محتوى مقروء للبشر مع بيانات آلية تطابق مخطط المخرج |

7. الطلب {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {...}} -> الرد {"jsonrpc": "2.0", "id": 7, "result": {...}}: يطابق العميل الرد مع طلبه المعلق عبر الـ id رقم 7.""",
    ),
    "COURSE-007.M04.L01.EX02": (
        """1. When the client sends requests 10, 11 and 12, each gets an entry in the pending table (id -> a future/stream waiting for the response). On the server, each incoming request is recorded as in flight (id -> its task and cancel scope).
2. The server dispatcher starts a separate task for each request, each inside its own cancel scope; slow request 11 only blocks its own task, so 10 and 12 run and finish independently.
3. Response 12 arrives first: the client looks up id 12 in the pending table and resolves that future; then response 10 resolves future 10. Matching is by id, so order does not matter.
4. The client sends notifications/cancelled with requestId 11 (and a reason); the server finds 11 in its in-flight table, cancels its cancel scope (the task stops) and removes the entry; on the client side, the pending entry for 11 is completed with a cancellation error.
5. A late result for 11 that arrives after cancellation no longer matches any pending entry, so the client ignores it (optionally logging it); it must not be delivered to anyone.
6. If the connection closes, every pending entry still waiting (for example 11 if not yet resolved) is failed with a connection-closed error so callers do not wait forever, and the server cancels the in-flight tasks for that session.""",
        """1. عندما يرسل العميل الطلبات 10 و11 و12 يحصل كل منها على مدخل في جدول الطلبات المعلقة (id -> future أو stream ينتظر الرد). وعلى الـ server يُسجَّل كل طلب وارد كطلب جارٍ (id -> مهمته وcancel scope الخاص به).
2. يبدأ موزّع الـ server مهمة منفصلة لكل طلب، كلٌّ داخل cancel scope خاص؛ فالطلب البطيء 11 لا يعطّل إلا مهمته، فيعمل 10 و12 وينتهيان باستقلال.
3. يصل الرد 12 أولًا: يبحث العميل عن id ‏12 في جدول المعلقات ويحلّ ذلك الـ future؛ ثم يحل الرد 10 الـ future رقم 10. فالمطابقة بالـ id، والترتيب لا يهم.
4. يرسل العميل notifications/cancelled مع requestId ‏11 (وسبب)؛ فيجد الـ server الطلب 11 في جدول الجارية ويلغي cancel scope الخاص به (تتوقف المهمة) ويحذف المدخل؛ وعلى جانب العميل يُنهى المدخل المعلق 11 بخطأ إلغاء.
5. نتيجة متأخرة للطلب 11 تصل بعد الإلغاء لا تطابق أي مدخل معلق، فيتجاهلها العميل (مع تسجيلها اختياريًا)؛ ولا يجب تسليمها لأحد.
6. إذا أُغلق الاتصال يفشل كل مدخل معلق ما زال ينتظر (مثل 11 إن لم يُحل) بخطأ إغلاق الاتصال حتى لا ينتظر المستدعون إلى الأبد، ويلغي الـ server المهام الجارية لتلك الجلسة.""",
    ),
    "COURSE-007.M04.L01.EX04": (
        """1. Local code-indexing server launched by the IDE - stdio. Boundary: a child process on the user's machine, no network. Auth: none (the OS user is the boundary). TLS: not needed. Secrets: passed as environment variables by the host, never in arguments or logs. Least privilege: restrict it to the project directory, no network if not needed. Scaling: not applicable. Failure: the server writes logs to stdout and corrupts the JSON-RPC stream.
2. Hosted CRM integration for thousands of customers - Streamable HTTP. Boundary: public network between client and server. Auth: OAuth with per-tenant scopes. TLS: mandatory. Secrets: tenants' CRM tokens in a secrets manager, encrypted, never exposed to the model. Least privilege: per-tenant isolation, minimal CRM scopes. Scaling: stateless replicas behind a load balancer. Failure: a token or tenant mix-up leaking one customer's data to another.
3. Local Docker container on localhost - Streamable HTTP (bound to 127.0.0.1). Boundary: container and localhost port. Auth: still use a token - other local programs and web pages can reach localhost. TLS: optional on loopback. Secrets: Docker secrets/env files, not baked into the image. Least privilege: non-root, minimal mounts. Scaling: single instance. Failure: DNS-rebinding attack from a malicious web page if Origin is not validated (or binding to 0.0.0.0 exposes it to the LAN).
4. Internal production service behind a load balancer - Streamable HTTP. Boundary: internal network and the LB. Auth: OAuth/SSO tokens or mTLS between services. TLS: yes, even internally. Secrets: secrets manager, rotated. Least privilege: service account with only the needed backend permissions, network policies. Scaling: multiple replicas; sticky sessions or shared session state if stateful. Failure: session ID routed to a different replica that does not know the session (lost state).""",
        """1. server فهرسة كود محلي يشغّله الـ IDE - stdio. الحد: عملية فرعية على جهاز المستخدم بلا شبكة. المصادقة: لا شيء (مستخدم النظام هو الحد). TLS: غير مطلوب. الأسرار: يمررها الـ host كمتغيرات بيئة، لا في المعاملات ولا السجلات. أقل الصلاحيات: حصره في مجلد المشروع وبلا شبكة إن لم تلزم. التوسع: لا ينطبق. الفشل: يكتب الـ server سجلات على stdout فيفسد تدفق JSON-RPC.
2. تكامل CRM مستضاف لآلاف العملاء - Streamable HTTP. الحد: شبكة عامة بين العميل والـ server. المصادقة: OAuth بـ scopes لكل عميل. TLS: إلزامي. الأسرار: tokens الـ CRM للعملاء في مدير أسرار ومشفرة ولا تُكشف للنموذج. أقل الصلاحيات: عزل لكل عميل وأقل scopes للـ CRM. التوسع: نسخ stateless خلف موازن حمل. الفشل: خلط tokens أو عملاء يسرّب بيانات عميل لآخر.
3. حاوية Docker محلية على localhost - Streamable HTTP (مربوطة بـ 127.0.0.1). الحد: الحاوية ومنفذ localhost. المصادقة: token مع ذلك - فبرامج محلية أخرى وصفحات ويب تستطيع الوصول إلى localhost. TLS: اختياري على الـ loopback. الأسرار: Docker secrets أو ملفات env لا داخل الصورة. أقل الصلاحيات: غير root وأقل تركيبات. التوسع: نسخة واحدة. الفشل: هجوم DNS rebinding من صفحة ويب خبيثة إذا لم يُتحقق من Origin (أو الربط بـ 0.0.0.0 يكشفه للشبكة المحلية).
4. خدمة إنتاج داخلية خلف موازن حمل - Streamable HTTP. الحد: الشبكة الداخلية والموازن. المصادقة: tokens عبر OAuth/SSO أو mTLS بين الخدمات. TLS: نعم حتى داخليًا. الأسرار: مدير أسرار مع تدوير. أقل الصلاحيات: حساب خدمة بالصلاحيات اللازمة فقط وسياسات شبكة. التوسع: نسخ متعددة؛ sticky sessions أو حالة جلسات مشتركة إذا كانت ذات حالة. الفشل: توجيه session ID إلى نسخة لا تعرف الجلسة (فقدان الحالة).""",
    ),
    "COURSE-007.M05.L01.EX01": (
        """1. Import from the official Registry: server name and namespace, description, version, repository URL, package/remote endpoints (package type, transport), required environment variables/headers, and publisher information.
2. Organization _meta fields (under a company namespace, e.g. com.acme/*): approval_status, risk_level (low/medium/high), data_classification_allowed, allowed_departments, security_review_date and reviewer, pinned_approved_version, internal_owner.
3. Workflow: discovered (synced from upstream, not visible to employees) -> security-reviewed (code/package scan, permissions and data-flow review, licence check) -> approved (visible, with a pinned version and allowed scope) -> blocked (vulnerability, policy violation or abandoned upstream; removed from discovery, clients warned). Approved entries are re-reviewed on version changes.
4. Yes, internal servers appear in the same subregistry so employees have one place to search, but with internal visibility and access control, never synced back upstream.
5. Clients and agents query only the subregistry's API (filtered by approval_status=approved and the user's department), not the public registry; client configuration points to it by policy.
6. It guarantees which servers and versions were reviewed and approved and their metadata; it does not guarantee that an approved server is free of bugs or vulnerabilities, that its behaviour cannot change at runtime (remote servers), or that it is used safely - runtime controls are still needed.
7. A scheduled sync job pulls upstream changes by updated timestamp, stores new versions as "discovered", flags changed metadata for re-review, and never auto-promotes a new version past the approved pin.""",
        """1. ما يُستورد من الـ Registry الرسمي: اسم الـ server ونطاقه، والوصف، والإصدار، ورابط المستودع، ونقاط الحزمة أو الـ remote ‏(نوع الحزمة والـ transport)، ومتغيرات البيئة أو الـ headers المطلوبة، ومعلومات الناشر.
2. حقول _meta خاصة بالمؤسسة (تحت نطاق الشركة مثل com.acme/*): ‏approval_status، وrisk_level ‏(منخفض/متوسط/عالٍ)، وdata_classification_allowed، وallowed_departments، وsecurity_review_date والمراجِع، وpinned_approved_version، وinternal_owner.
3. سير العمل: مُكتشَف (مزامن من المصدر وغير ظاهر للموظفين) -> مراجَع أمنيًا (فحص الكود والحزمة، ومراجعة الصلاحيات وتدفق البيانات، وفحص الترخيص) -> معتمد (ظاهر بإصدار مثبت ونطاق مسموح) -> محظور (ثغرة أو مخالفة سياسة أو مصدر مهجور؛ يُزال من الاكتشاف ويُنبَّه العملاء). وتُعاد مراجعة المعتمد عند تغيير الإصدار.
4. نعم، تظهر الخوادم الداخلية في الـ subregistry نفسه ليكون للموظفين مكان بحث واحد، لكن بظهور داخلي وتحكم في الوصول، ولا تُزامن إلى المصدر أبدًا.
5. يستعلم العملاء والـ agents من API الـ subregistry فقط (مرشحًا بـ approval_status=approved وقسم المستخدم) لا من الـ registry العام؛ ويشير إعداد العملاء إليه بالسياسة.
6. يضمن أي الخوادم والإصدارات رُوجعت واعتُمدت مع بياناتها الوصفية؛ ولا يضمن خلو الـ server المعتمد من الأخطاء أو الثغرات، ولا عدم تغير سلوكه وقت التشغيل (الخوادم البعيدة)، ولا استخدامه بأمان - فما زالت ضوابط وقت التشغيل لازمة.
7. مهمة مزامنة مجدولة تسحب التغييرات من المصدر حسب وقت التحديث، وتخزن الإصدارات الجديدة كـ "مُكتشَف"، وتعلّم البيانات الوصفية المتغيرة لإعادة المراجعة، ولا ترفع أبدًا إصدارًا جديدًا تلقائيًا فوق الإصدار المثبت المعتمد.""",
    ),
    "COURSE-007.M05.L01.EX02": (
        """| Scenario | Approach | Tokens / context | Round trips | Security / sandbox | Testing |
| A. 6 well-designed tools | Normal tools | Small, fixed tool list - no problem | One call per action | Standard tool approval | Inspector for each tool; model eval of tool choice on realistic tasks |
| B. 2,000+ operations | Search/execute progressive disclosure | Only search + found tools enter context | Extra search calls | Search must respect permissions; execute validates arguments | Inspector tests of search ranking and execute; model eval of finding the right operation |
| C. Each step depends on interpreting natural-language results | Normal tools (or progressive disclosure) - the model must read each result | Results enter context, which is needed here | One round trip per step | Standard | Model-connected eval of multi-step tasks; trace review |
| D. Deterministic 30-call batch with a hardened sandbox | Code Mode | Intermediate results stay in the sandbox; only the final summary returns | Few model turns | Generated code runs only inside the existing isolated sandbox with limited egress | Direct protocol tests of the typed stubs; eval that generated code completes the batch correctly |

For every interface: direct protocol tooling (MCP Inspector, scripted client calls, schema validation) checks that it works as specified; model-connected evaluation checks that real models use it correctly.""",
        """| الحالة | النهج | الـ tokens والسياق | الرحلات | الأمان والـ sandbox | الاختبار |
| A. ست أدوات مصممة جيدًا | أدوات عادية | قائمة أدوات صغيرة ثابتة - لا مشكلة | استدعاء لكل إجراء | موافقة الأدوات المعتادة | Inspector لكل أداة؛ وتقييم نموذجي لاختيار الأداة على مهام واقعية |
| B. أكثر من 2,000 عملية | إفصاح تدريجي search/execute | لا يدخل السياق إلا البحث والأدوات الموجودة | استدعاءات بحث إضافية | يجب أن يحترم البحث الصلاحيات، وexecute يتحقق من المعاملات | اختبارات Inspector لترتيب البحث وexecute؛ وتقييم نموذجي لإيجاد العملية الصحيحة |
| C. كل خطوة تعتمد على تفسير نتائج لغوية | أدوات عادية (أو إفصاح تدريجي) - يجب أن يقرأ النموذج كل نتيجة | تدخل النتائج السياق، وهذا مطلوب هنا | رحلة لكل خطوة | معتاد | تقييم نموذجي لمهام متعددة الخطوات؛ ومراجعة التتبع |
| D. دفعة حتمية من 30 استدعاءً مع sandbox محصّن | Code Mode | تبقى النتائج الوسيطة في الـ sandbox ولا يعود إلا الملخص | أدوار نموذج قليلة | يعمل الكود المولَّد داخل الـ sandbox المعزول الموجود فقط مع اتصال خارجي محدود | اختبارات بروتوكول مباشرة للـ stubs ذات الأنواع؛ وتقييم أن الكود المولَّد يكمل الدفعة بشكل صحيح |

لكل واجهة: أدوات البروتوكول المباشرة (MCP Inspector واستدعاءات عميل مبرمجة والتحقق من المخططات) تتأكد أنها تعمل كما وُصفت؛ والتقييم المتصل بالنماذج يتأكد أن النماذج الحقيقية تستخدمها بشكل صحيح.""",
    ),
    "COURSE-007.M05.L01.EX03": (
        """1. tools/call (with task creation requested) returns immediately with a task object: {taskId, status: "working", createdAt, pollInterval, ttl} instead of the final result.
2. The client writes the taskId (with server identity, tool name and arguments, creation time) to durable local storage - a database or file - before showing "started" to the user.
3. working -> input_required (the server needs a decision, e.g. "dataset has 12% missing labels - continue or abort?"; the client fetches the pending request and asks the user) -> working (after the answer is provided).
4. Success: working -> completed; the client calls tasks/result to retrieve the training report. Failure: working -> failed with an error message (for example out of GPU memory); tasks/result returns the error details.
5. The client calls tasks/cancel with the taskId; the server stops the job and the task moves to the terminal state cancelled - it is not reported as failed.
6. After restart, the client reloads stored taskIds and calls tasks/get for each to read the current status, then resumes polling, answers any input_required request, or fetches the result if completed - no connection had to stay open.
7. Progress notifications only flow over a live connection tied to the original request; if the client disconnects or restarts they are lost and cannot report completion, results or required input. A durable task with its own ID can be queried at any time.""",
        """1. يعيد tools/call (مع طلب إنشاء مهمة) فورًا كائن مهمة: {taskId، status: "working"، createdAt، pollInterval، ttl} بدلًا من النتيجة النهائية.
2. يكتب العميل الـ taskId (مع هوية الـ server واسم الأداة ومعاملاتها ووقت الإنشاء) في تخزين محلي دائم - قاعدة بيانات أو ملف - قبل عرض "بدأ" للمستخدم.
3. working -> input_required (يحتاج الـ server قرارًا، مثل "في البيانات 12% تسميات مفقودة - استمرار أم إلغاء؟"؛ فيجلب العميل الطلب المعلق ويسأل المستخدم) -> working (بعد تقديم الإجابة).
4. النجاح: working -> completed؛ ويستدعي العميل tasks/result لجلب تقرير التدريب. الفشل: working -> failed مع رسالة خطأ (مثل نفاد ذاكرة الـ GPU)؛ ويعيد tasks/result تفاصيل الخطأ.
5. يستدعي العميل tasks/cancel بالـ taskId؛ فيوقف الـ server المهمة وتنتقل إلى الحالة النهائية cancelled - ولا تُبلَّغ كفشل.
6. بعد إعادة التشغيل يعيد العميل تحميل الـ taskIds المخزنة ويستدعي tasks/get لكل منها لقراءة الحالة الحالية، ثم يستأنف الاستطلاع أو يجيب أي input_required أو يجلب النتيجة إن اكتملت - دون حاجة لبقاء أي اتصال مفتوح.
7. إشعارات التقدم تمر فقط عبر اتصال حي مرتبط بالطلب الأصلي؛ فإذا انقطع العميل أو أعيد تشغيله ضاعت ولا تستطيع الإبلاغ عن الاكتمال أو النتائج أو المدخلات المطلوبة. أما المهمة الدائمة بمعرّفها الخاص فيمكن الاستعلام عنها في أي وقت.""",
    ),
    "COURSE-007.M05.L01.EX04": (
        """1. Track: Standards Track - it changes protocol messages and behaviour that implementations must support (an extension of the specification, not just guidance or process).
2. Abstract: "This SEP adds resumable streamed results to MCP. Servers can attach monotonically increasing event IDs to streamed result chunks so that a client whose connection drops can reconnect and resume from the last received chunk instead of re-running the operation."
3. Motivation: long tool outputs (large file reads, generated reports) streamed over unreliable networks are lost on disconnect; repeating expensive or non-idempotent operations wastes cost and can duplicate side effects.
4. Specification changes: a capability flag for resumable results; chunk/event ID format and ordering guarantees; the resume request (reconnect with Last-Event-ID or a resume method referencing the request and last chunk); server retention rules (how long chunks are kept); errors when resumption is no longer possible; interaction with cancellation and tasks.
5. Compatibility risks: older clients and servers without the capability must keep working (feature negotiated, never assumed); intermediaries (proxies) that buffer streams; ambiguity with existing SSE resumability behaviour.
6. Security: resume tokens must be bound to the authenticated session so another user cannot resume and read someone's results; stored chunks may contain sensitive data and need retention limits and encryption; resumption attempts must be rate-limited to prevent resource exhaustion.
7. Reference implementation: a prototype in the Python SDK (server retains chunks in a bounded buffer; client reconnects and resumes), plus an example server demonstrating a dropped connection.
8. Conformance tests: resume after disconnect delivers each chunk exactly once and in order; resuming with an expired or unknown ID returns the specified error; peers without the capability behave exactly as before.
9. Open a GitHub discussion in the specification repository and present at a community/working-group meeting, ask a maintainer or core contributor to sponsor the SEP, then submit it as a pull request following the SEP template and iterate on review feedback.""",
        """1. المسار: Standards Track - فهو يغير رسائل البروتوكول وسلوكًا يجب أن تدعمه التطبيقات (امتداد للمواصفة لا مجرد إرشاد أو إجراء).
2. الملخص: "يضيف هذا الـ SEP نتائج متدفقة قابلة للاستئناف إلى MCP. تستطيع الخوادم إلحاق معرّفات أحداث متزايدة بأجزاء النتيجة المتدفقة، فيتمكن العميل الذي انقطع اتصاله من إعادة الاتصال والاستئناف من آخر جزء استلمه بدلًا من إعادة تشغيل العملية."
3. الدافع: مخرجات الأدوات الطويلة (قراءة ملفات كبيرة وتقارير مولدة) المتدفقة عبر شبكات غير مستقرة تضيع عند الانقطاع؛ وتكرار العمليات المكلفة أو غير الـ idempotent يهدر التكلفة وقد يكرر الآثار الجانبية.
4. تغييرات المواصفة: علامة قدرة للنتائج القابلة للاستئناف؛ وصيغة معرّفات الأجزاء/الأحداث وضمانات الترتيب؛ وطلب الاستئناف (إعادة الاتصال مع Last-Event-ID أو طريقة استئناف تشير إلى الطلب وآخر جزء)؛ وقواعد احتفاظ الـ server (مدة حفظ الأجزاء)؛ والأخطاء عندما يتعذر الاستئناف؛ والتفاعل مع الإلغاء والمهام.
5. مخاطر التوافق: يجب أن يستمر عمل العملاء والخوادم الأقدم التي لا تملك القدرة (الميزة بالتفاوض لا بالافتراض)؛ والوسطاء (proxies) الذين يخزنون التدفقات مؤقتًا؛ والالتباس مع سلوك استئناف SSE الحالي.
6. الأمان: يجب ربط رموز الاستئناف بالجلسة المصادَق عليها حتى لا يستأنف مستخدم آخر ويقرأ نتائج غيره؛ والأجزاء المخزنة قد تحتوي بيانات حساسة وتحتاج حدود احتفاظ وتشفيرًا؛ ويجب تحديد معدل محاولات الاستئناف لمنع استنزاف الموارد.
7. التطبيق المرجعي: نموذج أولي في Python SDK ‏(يحتفظ الـ server بالأجزاء في مخزن محدود؛ ويعيد العميل الاتصال ويستأنف)، مع server مثال يوضح انقطاع الاتصال.
8. اختبارات المطابقة: الاستئناف بعد الانقطاع يسلم كل جزء مرة واحدة بالترتيب؛ والاستئناف بمعرّف منتهٍ أو غير معروف يعيد الخطأ المحدد؛ والأطراف التي لا تملك القدرة تتصرف تمامًا كما قبل.
9. أفتح نقاشًا على GitHub في مستودع المواصفة وأعرضه في اجتماع للمجتمع أو مجموعة العمل، وأطلب من maintainer أو مساهم أساسي رعاية الـ SEP، ثم أقدمه كـ pull request وفق قالب الـ SEP وأطوره حسب ملاحظات المراجعة.""",
    ),
}
