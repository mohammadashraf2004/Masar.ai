"""
app/content/legal_documents.py

The text of the Terms of Service and the Privacy Policy, in English and Arabic.

The text and its version number live in one package on purpose: changing a
document without bumping `app.core.legal` (or the reverse) is exactly the
mistake that lets people "accept" something they were never shown. Each
document is a list of sections, each section a heading plus paragraphs; the
frontend renders them and never holds a copy of the wording.

DRAFT NOTICE
    This wording describes what the platform does today (accounts, learning
    content, AI-assisted features, credits, certification exams, community).
    It is a working draft and has not been reviewed by a lawyer. It must be
    reviewed by qualified counsel for the operating jurisdiction before it is
    relied on. Any material change means bumping the version in
    `app.core.legal` so existing learners are asked to accept again.
"""
from typing import Dict, List, Optional, TypedDict

from app.core import legal


class Section(TypedDict):
    heading: str
    body: List[str]


class Document(TypedDict):
    title: str
    intro: str
    sections: List[Section]


TERMS: Dict[str, Document] = {
    "en": {
        "title": "Terms of Service",
        "intro": "These terms govern your use of Masar. By creating an account you agree to them.",
        "sections": [
            {"heading": "1. Who we are and what Masar is", "body": [
                "Masar is an online learning platform for AI careers. It offers courses, lessons, exercises, "
                "personalised learning paths, an AI mentor, community spaces, certification exams and related tools.",
            ]},
            {"heading": "2. Your account", "body": [
                "You must give accurate information and keep your password secret. You are responsible for what "
                "happens under your account. You must be old enough to enter a binding agreement where you live.",
                "You can delete your account at any time from your profile. Deleting it removes your personal details; "
                "records we must keep for accounting, such as payment receipts, are retained without your personal details.",
            ]},
            {"heading": "3. Learning content and your roadmap", "body": [
                "Your roadmap is generated from what you tell us: your level, your fields of interest, your career goal "
                "and the skills you say you already know. Skills you declare are self-reported. They shape your "
                "roadmap but are not a verified qualification and are never shown to others as one.",
                "Content is provided for education. We do not promise a job, a salary or a particular outcome.",
            ]},
            {"heading": "4. AI-assisted features", "body": [
                "The AI mentor and answer evaluation use third-party AI providers to produce responses. Responses can be "
                "wrong or incomplete; check anything important before relying on it. Do not submit anything to these "
                "features that you are not allowed to share.",
            ]},
            {"heading": "5. Credits, payments and exams", "body": [
                "Some features use credits, and certification exams may carry a fee. Prices and the way credits are "
                "spent are shown before you pay. Payments are handled by a payment provider; we do not store your card "
                "details. Subscription refund requests are handled under the published Refund Policy. Fees and credits "
                "already spent on other delivered services are not refundable unless the law says otherwise or we "
                "decide to refund an error on our side.",
            ]},
            {"heading": "6. Acceptable use", "body": [
                "Do not attack, overload or probe the service; do not share your account; do not copy or resell course "
                "content; do not cheat in exams or post unlawful, abusive or misleading material in the community. We "
                "may remove content and suspend accounts that break these rules.",
            ]},
            {"heading": "7. Your content", "body": [
                "You keep the rights to what you submit (code, answers, posts). You allow us to store and display it as "
                "needed to run the service, for example to show your post to other learners or to evaluate your answer.",
            ]},
            {"heading": "8. Availability and liability", "body": [
                "We work to keep Masar available but do not guarantee uninterrupted service. To the extent the law "
                "allows, we are not liable for indirect or consequential loss, and our total liability to you is "
                "limited to the amount you paid us in the twelve months before the claim.",
            ]},
            {"heading": "9. Changes to these terms", "body": [
                "When we change these terms in a material way we publish a new version and ask you to accept it. "
                "Continuing to use the parts of the service that require acceptance depends on you accepting it.",
            ]},
        ],
    },
    "ar": {
        "title": "شروط الخدمة",
        "intro": "تنظّم هذه الشروط استخدامك لمنصة مسار. بإنشاء حساب فإنك توافق عليها.",
        "sections": [
            {"heading": "١. من نحن وما هي مسار", "body": [
                "مسار منصة تعلّم عبر الإنترنت لمهن الذكاء الاصطناعي. تقدّم دورات ودروساً وتمارين ومسارات تعلّم مخصصة "
                "ومرشداً بالذكاء الاصطناعي ومساحات مجتمعية واختبارات شهادات وأدوات مرتبطة بها.",
            ]},
            {"heading": "٢. حسابك", "body": [
                "عليك تقديم معلومات صحيحة والحفاظ على سرية كلمة المرور. أنت مسؤول عمّا يحدث عبر حسابك، ويجب أن تكون "
                "في السن التي تسمح لك قانوناً بإبرام اتفاق ملزم في بلدك.",
                "يمكنك حذف حسابك في أي وقت من صفحة ملفك الشخصي. يؤدي الحذف إلى إزالة بياناتك الشخصية، أما السجلات "
                "التي يلزمنا الاحتفاظ بها لأغراض المحاسبة مثل إيصالات الدفع فتبقى دون بياناتك الشخصية.",
            ]},
            {"heading": "٣. المحتوى التعليمي ومسارك", "body": [
                "يُبنى مسارك مما تخبرنا به: مستواك ومجالات اهتمامك وهدفك المهني والمهارات التي تقول إنك تعرفها. "
                "المهارات التي تعلنها هي إفادة ذاتية؛ تؤثر في مسارك لكنها ليست مؤهلاً موثّقاً ولا تُعرض لغيرك على "
                "أنها كذلك.",
                "المحتوى مقدَّم لأغراض التعليم. لا نعد بوظيفة أو راتب أو نتيجة بعينها.",
            ]},
            {"heading": "٤. الميزات المدعومة بالذكاء الاصطناعي", "body": [
                "يستخدم المرشد الذكي وتقييم الإجابات مزوّدي ذكاء اصطناعي من أطراف ثالثة لتوليد الردود. قد تكون الردود "
                "خاطئة أو ناقصة، فتحقّق من أي أمر مهم قبل الاعتماد عليه. لا ترسل إلى هذه الميزات ما لا يحق لك مشاركته.",
            ]},
            {"heading": "٥. الرصيد والمدفوعات والاختبارات", "body": [
                "تستهلك بعض الميزات رصيداً، وقد تكون لاختبارات الشهادات رسوم. تُعرض الأسعار وطريقة استهلاك الرصيد قبل "
                "الدفع. تتولى الدفعَ جهةُ دفع مستقلة ولا نخزّن بيانات بطاقتك. تخضع طلبات استرداد الاشتراكات لسياسة "
                "الاسترداد المنشورة. أما الرسوم والرصيد المنفقان على خدمات أخرى قُدِّمت فعلاً فلا يُستردان إلا إذا "
                "أوجب القانون ذلك أو قررنا رد مبلغ بسبب خطأ من جانبنا.",
            ]},
            {"heading": "٦. الاستخدام المقبول", "body": [
                "لا تهاجم الخدمة أو تثقلها أو تفحصها، ولا تشارك حسابك، ولا تنسخ محتوى الدورات أو تبِعه، ولا تغشّ في "
                "الاختبارات، ولا تنشر في المجتمع مواد غير قانونية أو مسيئة أو مضللة. يجوز لنا إزالة المحتوى وتعليق "
                "الحسابات المخالفة.",
            ]},
            {"heading": "٧. محتواك", "body": [
                "تحتفظ بحقوقك في ما تقدّمه (الشيفرة والإجابات والمنشورات). وتسمح لنا بتخزينه وعرضه بالقدر اللازم "
                "لتشغيل الخدمة، كعرض منشورك على متعلمين آخرين أو تقييم إجابتك.",
            ]},
            {"heading": "٨. التوفّر والمسؤولية", "body": [
                "نعمل على إبقاء مسار متاحة لكننا لا نضمن خدمة دون انقطاع. وبالقدر الذي يسمح به القانون لا نتحمل "
                "الخسائر غير المباشرة أو التبعية، وتقتصر مسؤوليتنا الإجمالية تجاهك على ما دفعته لنا في الاثني عشر "
                "شهراً السابقة للمطالبة.",
            ]},
            {"heading": "٩. تعديل هذه الشروط", "body": [
                "عند تعديل هذه الشروط تعديلاً جوهرياً ننشر إصداراً جديداً ونطلب منك قبوله. ويتوقف استمرارك في "
                "استخدام الأجزاء التي تتطلب القبول على موافقتك عليه.",
            ]},
        ],
    },
}

PRIVACY: Dict[str, Document] = {
    "en": {
        "title": "Privacy Policy",
        "intro": "This policy explains what Masar collects about you, why, who else handles it, and your choices.",
        "sections": [
            {"heading": "1. What we collect", "body": [
                "Account details: your name, email address and a hashed password (we never store your password itself).",
                "Learning data: your level, fields, career goal, the skills you say you know, your progress, quiz, "
                "exercise and project submissions, exam attempts and certificates.",
                "Payment records: credit balance and transactions, and payment references from our payment provider. "
                "We do not receive or store your card number.",
                "Community content you post, and technical logs (such as IP address and request details) used to keep "
                "the service secure.",
            ]},
            {"heading": "2. Why we use it", "body": [
                "To run your account, build and update your roadmap, track your progress, provide AI-assisted "
                "feedback, process payments, issue certificates, keep the service secure and prevent abuse, and send "
                "essential emails such as email verification and password reset.",
            ]},
            {"heading": "3. Who else handles it", "body": [
                "AI providers receive the text you send to AI features so they can respond. An email provider delivers "
                "our messages, and a payment provider processes payments. They handle data only to provide those "
                "services to us. We do not sell your personal data.",
            ]},
            {"heading": "4. Skills you declare", "body": [
                "The skills you mark as known are stored against your account and used only to personalise your "
                "roadmap. They are recorded as self-declared and are not published to other users.",
            ]},
            {"heading": "5. How long we keep it", "body": [
                "We keep your data while your account exists. If you delete your account we remove your personal "
                "details; records we must keep for accounting are kept without them.",
            ]},
            {"heading": "6. Your choices", "body": [
                "You can view and edit your profile and your skills in the app, and delete your account from your "
                "profile. You can ask us about the data we hold on you through the contact details published on the platform.",
            ]},
            {"heading": "7. Security", "body": [
                "We use hashed passwords, encrypted connections and access controls, and we limit what we log. No "
                "system is perfectly secure, and we cannot guarantee absolute security.",
            ]},
            {"heading": "8. Changes to this policy", "body": [
                "When we change this policy in a material way we publish a new version and ask you to accept it.",
            ]},
        ],
    },
    "ar": {
        "title": "سياسة الخصوصية",
        "intro": "توضّح هذه السياسة ما تجمعه مسار عنك ولماذا ومن يتعامل معه غيرنا وما هي خياراتك.",
        "sections": [
            {"heading": "١. ما الذي نجمعه", "body": [
                "بيانات الحساب: اسمك وبريدك الإلكتروني وكلمة مرور مشفّرة (لا نخزّن كلمة المرور نفسها أبداً).",
                "بيانات التعلّم: مستواك ومجالاتك وهدفك المهني والمهارات التي تقول إنك تعرفها وتقدّمك وإجاباتك في "
                "الاختبارات القصيرة والتمارين والمشاريع ومحاولات الاختبارات والشهادات.",
                "سجلات الدفع: رصيدك ومعاملاتك ومراجع الدفع من جهة الدفع. لا نستلم رقم بطاقتك ولا نخزّنه.",
                "ما تنشره في المجتمع، والسجلات التقنية (مثل عنوان IP وتفاصيل الطلبات) التي نستخدمها لحماية الخدمة.",
            ]},
            {"heading": "٢. لماذا نستخدمها", "body": [
                "لتشغيل حسابك وبناء مسارك وتحديثه وتتبّع تقدّمك وتقديم ملاحظات مدعومة بالذكاء الاصطناعي ومعالجة "
                "المدفوعات وإصدار الشهادات وحماية الخدمة ومنع إساءة استخدامها وإرسال رسائل أساسية مثل تأكيد البريد "
                "وإعادة تعيين كلمة المرور.",
            ]},
            {"heading": "٣. من يتعامل معها غيرنا", "body": [
                "يستلم مزوّدو الذكاء الاصطناعي النصوص التي ترسلها إلى ميزات الذكاء الاصطناعي ليتمكنوا من الرد. "
                "ويوصل مزوّد البريد رسائلنا، وتعالج جهة الدفع المدفوعات. يتعاملون مع البيانات لتقديم هذه الخدمات لنا "
                "فقط. لا نبيع بياناتك الشخصية.",
            ]},
            {"heading": "٤. المهارات التي تعلنها", "body": [
                "المهارات التي تحددها بأنك تعرفها تُخزَّن مع حسابك وتُستخدم فقط لتخصيص مسارك. وتُسجَّل على أنها "
                "إفادة ذاتية ولا تُعرض لمستخدمين آخرين.",
            ]},
            {"heading": "٥. مدة الاحتفاظ", "body": [
                "نحتفظ ببياناتك ما دام حسابك قائماً. إذا حذفت حسابك أزلنا بياناتك الشخصية، وتبقى السجلات التي يلزمنا "
                "الاحتفاظ بها للمحاسبة دونها.",
            ]},
            {"heading": "٦. خياراتك", "body": [
                "يمكنك عرض ملفك ومهاراتك وتعديلها داخل التطبيق، وحذف حسابك من صفحة ملفك الشخصي. ويمكنك أن تسألنا عن "
                "البيانات التي نحتفظ بها عنك عبر وسائل التواصل المنشورة على المنصة.",
            ]},
            {"heading": "٧. الأمان", "body": [
                "نستخدم كلمات مرور مشفّرة واتصالات مشفّرة وضوابط وصول، ونحدّ مما نسجّله. لا يوجد نظام آمن تماماً، ولا "
                "يمكننا ضمان أمان مطلق.",
            ]},
            {"heading": "٨. تعديل هذه السياسة", "body": [
                "عند تعديل هذه السياسة تعديلاً جوهرياً ننشر إصداراً جديداً ونطلب منك قبوله.",
            ]},
        ],
    },
}

REFUND_POLICY: Dict[str, Document] = {
    "en": {
        "title": "Refund Policy",
        "intro": "This policy explains when and how you may request a refund for a paid Masar subscription.",
        "sections": [
            {"heading": "1. Seven-day free trial", "body": [
                "A new Masar subscription includes a seven-day free trial before the first subscription charge. "
                "The price and billing cycle are shown before you start.",
            ]},
            {"heading": "2. Request window and review", "body": [
                "After a successful paid subscription charge, you may submit a refund request within seven days of "
                "the payment date. Submitting a request does not guarantee approval; Masar reviews eligibility, the "
                "reason, and use of paid platform resources before deciding.",
                "Requests may be rejected where a substantial part of the paid service or AI resources has already "
                "been consumed, subject to applicable law. Duplicate or incorrect charges are eligible for correction "
                "or refund after verification.",
            ]},
            {"heading": "3. How approved refunds are returned", "body": [
                "When the active payment provider supports it, an approved refund is returned through the original "
                "payment method. Provider and bank processing times may apply after Masar initiates or confirms it. "
                "Your order and its Masar reference number remain in the audit history.",
            ]},
            {"heading": "4. Cancellation is different", "body": [
                "Cancelling a subscription prevents future renewals. It does not automatically refund a payment that "
                "has already completed. A refund must be requested separately from the relevant payment details.",
            ]},
            {"heading": "5. Access and credits after a refund", "body": [
                "A completed subscription refund ends the Pro access purchased by that payment. Paid Pro subscriptions "
                "currently grant access but do not add wallet or AI credits, so no wallet credits are removed. Credits "
                "bought separately are governed by their own payment record.",
            ]},
            {"heading": "6. Contacting support", "body": [
                "Use the Masar Reference Number shown in payment history, receipts, and refund details when contacting "
                "support. It is separate from the payment provider's transaction identifier.",
            ]},
        ],
    },
    "ar": {
        "title": "سياسة الاسترداد",
        "intro": "توضح هذه السياسة متى وكيف يمكنك طلب استرداد قيمة اشتراك مدفوع في مسار.",
        "sections": [
            {"heading": "١. التجربة المجانية لمدة سبعة أيام", "body": [
                "يتضمن الاشتراك الجديد في مسار تجربة مجانية لمدة سبعة أيام قبل أول خصم للاشتراك، ويظهر السعر "
                "ودورة الفوترة قبل البدء.",
            ]},
            {"heading": "٢. مهلة الطلب والمراجعة", "body": [
                "بعد نجاح خصم اشتراك مدفوع، يمكنك تقديم طلب استرداد خلال سبعة أيام من تاريخ الدفع. لا تعني مجرد "
                "تقديم الطلب الموافقة عليه؛ تراجع مسار الأهلية والسبب ومدى استخدام موارد المنصة المدفوعة قبل القرار.",
                "قد يُرفض الطلب عند استهلاك جزء جوهري من الخدمة المدفوعة أو موارد الذكاء الاصطناعي، مع مراعاة القانون "
                "المطبق. وتكون الدفعات المكررة أو المبالغ المخصومة بالخطأ مؤهلة للتصحيح أو الاسترداد بعد التحقق.",
            ]},
            {"heading": "٣. طريقة إعادة المبلغ المعتمد", "body": [
                "عندما يدعم مزوّد الدفع المستخدم ذلك، يُعاد المبلغ المعتمد عبر طريقة الدفع الأصلية. وقد تستغرق "
                "معالجة مزوّد الدفع أو البنك وقتاً بعد بدء الاسترداد أو تأكيده. يبقى الطلب ورقمه المرجعي في سجل التدقيق.",
            ]},
            {"heading": "٤. الإلغاء مختلف عن الاسترداد", "body": [
                "يمنع إلغاء الاشتراك التجديدات المستقبلية، لكنه لا يسترد تلقائياً دفعة مكتملة. يجب طلب الاسترداد "
                "بشكل منفصل من تفاصيل عملية الدفع المعنية.",
            ]},
            {"heading": "٥. الوصول والرصيد بعد الاسترداد", "body": [
                "يُنهي اكتمال استرداد الاشتراك وصول Pro الذي اشترته الدفعة. اشتراك Pro المدفوع يمنح الوصول حالياً "
                "ولا يضيف رصيد محفظة أو رصيد ذكاء اصطناعي، لذلك لا يُسحب رصيد من المحفظة. ويخضع الرصيد المشترى "
                "بشكل منفصل لسجل دفعه الخاص.",
            ]},
            {"heading": "٦. التواصل مع الدعم", "body": [
                "استخدم الرقم المرجعي لمسار الظاهر في سجل الدفع والإيصالات وتفاصيل الاسترداد عند التواصل مع الدعم. "
                "وهو منفصل عن معرّف معاملة مزوّد الدفع.",
            ]},
        ],
    },
}

DOCUMENTS = {"terms": TERMS, "privacy": PRIVACY, "refund": REFUND_POLICY}


def versions() -> Dict[str, str]:
    """Read from `app.core.legal` on every call, so there is one number and it
    is never a stale copy."""
    return {
        "terms": legal.TERMS_VERSION,
        "privacy": legal.PRIVACY_VERSION,
        "refund": legal.REFUND_POLICY_VERSION,
    }


def get_document(kind: str, lang: str = "en") -> Optional[Document]:
    docs = DOCUMENTS.get(kind)
    if docs is None:
        return None
    return docs.get(lang) or docs["en"]
