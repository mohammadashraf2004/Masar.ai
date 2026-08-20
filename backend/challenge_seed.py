"""
backend/challenge_seed.py
Seeds 3 challenge projects (beginner/intermediate/advanced) with dirty datasets.
Run: python challenge_seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz
from app.models.progress import Enrollment, UserProgress, QuizAttempt, ProjectSubmission, MentorSession, UserSkillScore, EngineerScorecard
from app.models.community import Post, PostLike, PostComment, UserFollow
from app.models.exam import Exam, ExamAttempt, ProctoringEvent, Certificate
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage
from app.models.challenge import ChallengeProject, ChallengeAttempt, ExamPayment

Base.metadata.create_all(bind=engine)

CHALLENGES = [
    # ── BEGINNER ──────────────────────────────────────────────────────────────
    {
        "title": "Egyptian Customer Reviews Cleaner",
        "slug": "egyptian-reviews-cleaner",
        "difficulty": "beginner",
        "credit_cost": 15,
        "passing_score": 65.0,
        "description": (
            "You work at a Cairo-based e-commerce startup. Their product review database "
            "has been corrupted — reviews are duplicated, timestamps are broken, Arabic and "
            "English are mixed randomly, ratings are out of range, and some records have "
            "null fields. Your job: build a cleaning pipeline that produces a usable dataset "
            "ready for sentiment analysis."
        ),
        "dataset_description": (
            "100 product reviews scraped from multiple sources. Issues include:\n"
            "- Duplicate records (same review, different IDs)\n"
            "- Ratings outside 1-5 range (e.g. 0, 6, 99, -1)\n"
            "- Null/empty review_text fields\n"
            "- Inconsistent date formats (DD/MM/YYYY, Unix timestamp, Arabic month names)\n"
            "- Mixed Arabic/English in the same text field with inconsistent encoding\n"
            "- Extra whitespace, HTML tags, and emoji in text\n"
            "- Duplicate product_id + user_id combinations (should be unique)"
        ),
        "dataset_filename": "egyptian_reviews_dirty.json",
        "dirty_dataset": [
            {"id": 1,  "product_id": "P001", "user_id": "U001", "rating": 5,   "review_text": "المنتج ممتاز جداً <br/> best product ever 🔥🔥",  "date": "15/03/2024", "verified": True},
            {"id": 2,  "product_id": "P001", "user_id": "U002", "rating": 99,  "review_text": "مش كويس خالص",                                      "date": "2024-03-16", "verified": False},
            {"id": 3,  "product_id": "P002", "user_id": "U003", "rating": 4,   "review_text": "   good product   ",                                 "date": "1710633600", "verified": True},
            {"id": 4,  "product_id": "P001", "user_id": "U001", "rating": 5,   "review_text": "المنتج ممتاز جداً <br/> best product ever 🔥🔥",  "date": "15/03/2024", "verified": True},
            {"id": 5,  "product_id": "P003", "user_id": "U004", "rating": -1,  "review_text": "terrible quality",                                   "date": "مارس 17، 2024", "verified": False},
            {"id": 6,  "product_id": "P003", "user_id": "U005", "rating": 3,   "review_text": None,                                                  "date": "18/03/2024", "verified": True},
            {"id": 7,  "product_id": "P004", "user_id": "U006", "rating": 2,   "review_text": "التغليف وحش بس المنتج ok",                          "date": "2024-03-19", "verified": False},
            {"id": 8,  "product_id": "P004", "user_id": "U007", "rating": 6,   "review_text": "Amazing!! highly recommend",                          "date": "20/03/2024", "verified": True},
            {"id": 9,  "product_id": "P005", "user_id": "U008", "rating": 1,   "review_text": "<p>worst purchase</p>",                               "date": "1711065600", "verified": False},
            {"id": 10, "product_id": "P005", "user_id": "U009", "rating": 4,   "review_text": "كويس وبيتبعت بسرعة",                                 "date": "أبريل 1، 2024", "verified": True},
            {"id": 11, "product_id": "P006", "user_id": "U010", "rating": 0,   "review_text": "no comment",                                          "date": "22/03/2024", "verified": False},
            {"id": 12, "product_id": "P006", "user_id": "U010", "rating": 0,   "review_text": "no comment",                                          "date": "22/03/2024", "verified": False},
            {"id": 13, "product_id": "P007", "user_id": "U011", "rating": 5,   "review_text": "product جامد    جداً!!   ",                          "date": "23/03/2024", "verified": True},
            {"id": 14, "product_id": "P007", "user_id": "U012", "rating": 3,   "review_text": "",                                                    "date": "2024-03-24", "verified": False},
            {"id": 15, "product_id": "P008", "user_id": "U013", "rating": 4,   "review_text": "شريته اتنين مرات وكل مرة نفس الجودة good consistency", "date": "25/03/2024", "verified": True},
        ],
        "grading_rubric": [
            {"criterion": "Duplicate removal",        "weight": 20, "description": "All exact duplicate records removed; composite duplicates (same product_id+user_id) handled"},
            {"criterion": "Rating validation",        "weight": 20, "description": "All ratings clamped or filtered to valid 1-5 range; out-of-range records handled with clear strategy"},
            {"criterion": "Null/empty handling",      "weight": 20, "description": "Null and empty review_text fields handled (dropped or imputed with justification)"},
            {"criterion": "Date normalization",       "weight": 20, "description": "All date formats normalized to ISO 8601 (YYYY-MM-DD); Arabic month names parsed correctly"},
            {"criterion": "Text cleaning",            "weight": 10, "description": "HTML tags removed, excess whitespace stripped, encoding consistent"},
            {"criterion": "Code quality & comments",  "weight": 10, "description": "Code is readable, functions are named clearly, pipeline steps are explained"},
        ],
        "hints": [
            "Use pandas for data manipulation — it handles mixed types well",
            "For Arabic month names, build a simple mapping dict: {'يناير': 1, 'فبراير': 2, ...}",
            "pd.to_datetime() with errors='coerce' handles most date formats automatically",
            "For duplicates: first check exact duplicates with df.duplicated(), then check subset=['product_id','user_id']",
        ],
        "tags": ["pandas", "data-cleaning", "arabic-nlp", "beginner"],
        "expected_output": {
            "records_after_cleaning": "10-12 records",
            "all_ratings_valid": True,
            "no_nulls_in_review_text": True,
            "dates_iso_format": True,
        },
    },

    # ── INTERMEDIATE ──────────────────────────────────────────────────────────
    {
        "title": "MENA Job Listings RAG Pipeline",
        "slug": "mena-jobs-rag-pipeline",
        "difficulty": "intermediate",
        "credit_cost": 30,
        "passing_score": 70.0,
        "description": (
            "A Gulf-based recruitment agency scraped job listings from 4 regional portals. "
            "The data is a disaster: listings are duplicated across portals, salaries mix USD/EGP/SAR, "
            "job titles use inconsistent Arabic/English variants, and location strings are unstructured. "
            "Your task: build a full cleaning + chunking + embedding pipeline that produces a "
            "RAG-ready vector store. The grader will test retrieval quality by running sample queries."
        ),
        "dataset_description": (
            "200 job listings scraped from Wuzzuf, Bayt, LinkedIn MENA, and Indeed Gulf. Issues:\n"
            "- Same job listed on multiple portals with slight text differences\n"
            "- Salary in mixed currencies (EGP, USD, SAR) and formats ('5000 EGP', '$2k', '٥٠٠٠ جنيه')\n"
            "- Job titles have Arabic/English variants ('Software Engineer' = 'مهندس برمجيات')\n"
            "- Location field: 'Cairo, Egypt' / 'القاهرة' / 'CAI' / 'Masr' all refer to the same city\n"
            "- HTML in description fields, broken encoding on Arabic text\n"
            "- Required skills listed as comma string, JSON array, or newline-separated"
        ),
        "dataset_filename": "mena_jobs_dirty.json",
        "dirty_dataset": [
            {"id": 1,  "portal": "wuzzuf",   "title": "Senior Python Developer",       "company": "TechCorp Egypt",  "location": "Cairo, Egypt",    "salary": "15000-20000 EGP", "skills": "Python, FastAPI, PostgreSQL",           "description": "We need a <b>senior</b> Python dev...", "posted": "2024-03-01"},
            {"id": 2,  "portal": "linkedin", "title": "Senior Python Developer",       "company": "TechCorp Egypt",  "location": "القاهرة",         "salary": "١٥٠٠٠-٢٠٠٠٠ جنيه", "skills": ["Python", "FastAPI", "PostgreSQL"],   "description": "We need a senior Python dev...",       "posted": "2024-03-01"},
            {"id": 3,  "portal": "bayt",     "title": "مهندس برمجيات Python",         "company": "TechCorp Egypt",  "location": "CAI",             "salary": "$900-$1200",      "skills": "Python\nFastAPI\nPostgreSQL",            "description": "نحتاج مطور Python...",                 "posted": "01/03/2024"},
            {"id": 4,  "portal": "wuzzuf",   "title": "AI Engineer",                   "company": "Instabug",        "location": "Masr",            "salary": "25000 EGP",       "skills": "PyTorch, LangChain, OpenAI API",        "description": "<p>Join our AI team</p>",               "posted": "2024-03-05"},
            {"id": 5,  "portal": "indeed",   "title": "AI Engineer",                   "company": "Instabug",        "location": "Cairo",           "salary": None,              "skills": ["PyTorch", "LangChain", "OpenAI API"],  "description": "Join our AI team",                     "posted": "05-03-2024"},
            {"id": 6,  "portal": "bayt",     "title": "Data Scientist",                "company": "Noon",            "location": "Dubai, UAE",      "salary": "15000-20000 SAR", "skills": "Python, ML, SQL",                       "description": "Data science role at Noon",             "posted": "2024-03-10"},
            {"id": 7,  "portal": "linkedin", "title": "Data Scientist",                "company": "Noon",            "location": "دبي",             "salary": "SAR 15k-20k",     "skills": "Python, Machine Learning, SQL",         "description": "Data science role at Noon.",            "posted": "10/03/2024"},
            {"id": 8,  "portal": "wuzzuf",   "title": "Backend Engineer",              "company": "Paymob",          "location": "New Cairo",       "salary": "18000-22000 EGP", "skills": "Node.js, MongoDB, AWS",                 "description": "Backend engineering position",          "posted": "2024-03-12"},
            {"id": 9,  "portal": "wuzzuf",   "title": "MLOps Engineer",                "company": "Breadfast",       "location": "Cairo Egypt",     "salary": "20000 EGP",       "skills": "Docker, Kubernetes, MLflow",            "description": "MLOps role for scaling ML pipelines",  "posted": "2024-03-15"},
            {"id": 10, "portal": "linkedin", "title": "Machine Learning Engineer",     "company": "Breadfast",       "location": "القاهرة، مصر",   "salary": "~20k EGP",        "skills": ["Docker", "Kubernetes", "MLflow"],      "description": "MLOps engineer for ML pipelines",      "posted": "15/03/2024"},
            {"id": 11, "portal": "bayt",     "title": "Full Stack Developer",          "company": "Vezeeta",         "location": "Heliopolis",      "salary": "12000-15000 EGP", "skills": "React, Node.js, TypeScript",            "description": "Full stack dev for health platform",   "posted": "2024-03-18"},
            {"id": 12, "portal": "indeed",   "title": "مطور Full Stack",               "company": "Vezeeta",         "location": "Heliopolis, Cairo","salary": "EGP 12k-15k",    "skills": "React\nNode.js\nTypeScript",             "description": "Full stack for منصة صحية",             "posted": "18/03/2024"},
        ],
        "grading_rubric": [
            {"criterion": "Cross-portal deduplication",  "weight": 25, "description": "Duplicate listings across portals merged intelligently (fuzzy title+company+location match)"},
            {"criterion": "Salary normalization",        "weight": 20, "description": "All salaries converted to a single currency (EGP) with consistent format; Arabic numerals handled"},
            {"criterion": "Skills normalization",        "weight": 15, "description": "Skills unified into a consistent list format regardless of source format (string/array/newline)"},
            {"criterion": "Location standardization",   "weight": 15, "description": "Locations mapped to canonical city names; Arabic/English variants resolved"},
            {"criterion": "Chunking strategy",          "weight": 15, "description": "Each job listing chunked appropriately for RAG (title+skills+description in context window)"},
            {"criterion": "Embedding & retrieval demo", "weight": 10, "description": "At least one embedding model used; sample query returns relevant results"},
        ],
        "hints": [
            "Use rapidfuzz or difflib for fuzzy string matching across portals",
            "For Arabic numerals: str.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))",
            "Exchange rates: 1 USD ≈ 48 EGP, 1 SAR ≈ 12.8 EGP (use fixed rates for this challenge)",
            "For chunking: combine title + company + location + skills + first 200 chars of description",
            "Try sentence-transformers with a multilingual model like 'paraphrase-multilingual-MiniLM-L12-v2'",
        ],
        "tags": ["rag", "nlp", "arabic", "data-cleaning", "embeddings", "intermediate"],
        "expected_output": {
            "unique_listings_after_dedup": "7-8 listings",
            "all_salaries_in_egp": True,
            "skills_as_list": True,
            "retrieval_works": True,
        },
    },

    # ── ADVANCED ──────────────────────────────────────────────────────────────
    {
        "title": "Multi-Agent Financial News Monitor",
        "slug": "multi-agent-financial-news",
        "difficulty": "advanced",
        "credit_cost": 50,
        "passing_score": 75.0,
        "description": (
            "A Cairo fintech startup needs an automated system to monitor Egyptian and Gulf "
            "financial news, extract entities (companies, currencies, amounts), detect sentiment, "
            "and alert on anomalies. The raw data feed is corrupted — articles have broken encoding, "
            "mixed Arabic/English financial jargon, duplicate articles from different sources, and "
            "malformed JSON. Your task: build a multi-agent pipeline with: (1) a cleaning agent, "
            "(2) an entity extraction agent, (3) a sentiment analysis agent, and (4) an anomaly "
            "detection agent that flags unusual price movements or breaking news. The pipeline must "
            "handle failures gracefully — if one agent fails, others should continue."
        ),
        "dataset_description": (
            "50 financial news articles from EGX, Mubasher, and Gulf news feeds. Issues:\n"
            "- Broken UTF-8 encoding on Arabic text (replacement characters)\n"
            "- Same article from multiple sources with different headlines\n"
            "- Financial amounts in mixed formats: '٢.٣ مليار جنيه', '2.3B EGP', 'EGP 2,300,000,000'\n"
            "- Malformed JSON in the metadata field\n"
            "- HTML entities and RTL/LTR markers embedded in text\n"
            "- Timestamps in 3 different timezones (Cairo UTC+2, Dubai UTC+4, UTC)\n"
            "- Truncated articles (feed cut off mid-sentence)"
        ),
        "dataset_filename": "financial_news_dirty.json",
        "dirty_dataset": [
            {"id": 1,  "source": "egx",      "headline": "البنك الأهلي يرفع الفائدة 1%",                           "body": "أعلن البنك الأهلي المصري اليوم رفع أسعار الفائدة...", "amount_mentioned": "٢.٣ مليار جنيه", "timestamp": "2024-03-15T10:00:00+02:00", "metadata": '{"ticker": "NBE", "sector": "banking"}'},
            {"id": 2,  "source": "mubasher", "headline": "National Bank of Egypt Raises Interest Rate by 1%",      "body": "The National Bank of Egypt announced today...",          "amount_mentioned": "EGP 2.3B",        "timestamp": "2024-03-15T08:00:00Z",      "metadata": '{"ticker": "NBE", "sector": "banking"}'},
            {"id": 3,  "source": "gulf_news","headline": "NBE interest rate hike",                                  "body": "NBE raised rates...",                                   "amount_mentioned": "2,300,000,000 EGP","timestamp": "2024-03-15T12:00:00+04:00", "metadata": "{invalid json}"},
            {"id": 4,  "source": "egx",      "headline": "أوراسكوم للإنشاء تحقق أرباح قياسية",                    "body": "حققت شركة أوراسكوم للإنشاء والصناعة أرباح\ufffd\ufffd قياسية...", "amount_mentioned": "١.٧ مليار",  "timestamp": "2024-03-16T09:30:00+02:00", "metadata": '{"ticker": "ORAS", "sector": "construction"}'},
            {"id": 5,  "source": "mubasher", "headline": "Orascom Construction Reports Record Profits",             "body": "Orascom Construction reported record profits...",         "amount_mentioned": "1.7B EGP",        "timestamp": "2024-03-16T07:30:00Z",      "metadata": '{"ticker": "ORAS", "sector": "construction"}'},
            {"id": 6,  "source": "egx",      "headline": "&#x62a;&#x631;&#x627;&#x62c;&#x639; حاد في أسهم البنوك", "body": "شهدت أسهم البنوك تراجعاً...",                           "amount_mentioned": None,              "timestamp": "2024-03-17T11:00:00+02:00", "metadata": '{"sector": "banking", "alert": true}'},
            {"id": 7,  "source": "gulf_news","headline": "Saudi Aramco Q1 Results Beat Expectations",               "body": "Saudi Aramco reported Q1 results that",                 "amount_mentioned": "SAR 330B",        "timestamp": "2024-03-18T14:00:00+04:00", "metadata": '{"ticker": "2222.SR", "sector": "energy"}'},
            {"id": 8,  "source": "egx",      "headline": "انخفاض الجنيه أمام الدولار",                             "body": "سجل الجنيه المصري انخفاضاً أمام الدولار...",            "amount_mentioned": "48.5 EGP/$",      "timestamp": "2024-03-19T09:00:00+02:00", "metadata": '{"currency_pair": "EGP/USD"}'},
            {"id": 9,  "source": "egx",      "headline": "CIB يعلن توزيعات أرباح",                                 "body": "أعلن بنك CIB عن توزيعات أرباح...",                     "amount_mentioned": "٥٠٠ مليون جنيه", "timestamp": "2024-03-20T10:00:00+02:00", "metadata": '{"ticker": "COMI", "sector": "banking"}'},
            {"id": 10, "source": "mubasher", "headline": "CIB Announces Dividend Distribution",                     "body": "CIB announced dividend distribution...",                 "amount_mentioned": "EGP 500M",        "timestamp": "2024-03-20T08:00:00Z",      "metadata": '{"ticker": "COMI", "sector": "banking"}'},
        ],
        "grading_rubric": [
            {"criterion": "Cleaning agent",           "weight": 20, "description": "Fixes encoding, deduplicates cross-source articles, normalizes timestamps to UTC, parses malformed JSON metadata"},
            {"criterion": "Entity extraction agent",  "weight": 25, "description": "Extracts companies, tickers, amounts (normalized to EGP), and currencies from both Arabic and English text"},
            {"criterion": "Sentiment agent",          "weight": 20, "description": "Classifies each article as positive/negative/neutral with confidence; handles mixed-language inputs"},
            {"criterion": "Anomaly detection agent",  "weight": 20, "description": "Flags articles with unusual amounts, breaking news keywords, or significant market movements"},
            {"criterion": "Fault tolerance",          "weight": 15, "description": "Pipeline continues if one agent fails; errors are logged not raised; partial results returned"},
        ],
        "hints": [
            "Use ftfy library for fixing broken Unicode/encoding issues",
            "For amount normalization: 'مليار' = billion (×10⁹), 'مليون' = million (×10⁶)",
            "Consider LangGraph or a simple state machine for the multi-agent orchestration",
            "For deduplication: normalize headline to lowercase, remove punctuation, compare with difflib.SequenceMatcher > 0.85",
            "For fault tolerance: wrap each agent call in try/except and store error in the result dict",
        ],
        "tags": ["multi-agent", "arabic-nlp", "financial-ai", "langchain", "advanced"],
        "expected_output": {
            "deduped_articles": "7 unique articles",
            "entities_extracted": True,
            "sentiments_classified": True,
            "anomalies_flagged": True,
            "pipeline_fault_tolerant": True,
        },
    },
]


def seed_challenges():
    db = SessionLocal()
    try:
        existing = db.query(ChallengeProject).count()
        if existing > 0:
            print(f"ℹ️   {existing} challenges already exist. Deleting and re-seeding...")
            db.query(ChallengeProject).delete()
            db.commit()

        for ch in CHALLENGES:
            db.add(ChallengeProject(**ch))
        db.commit()

        print(f"\n✅  Seeded {len(CHALLENGES)} challenge projects:\n")
        for ch in db.query(ChallengeProject).all():
            print(f"    [{ch.difficulty.upper():12}] {ch.title}")
            print(f"                  Cost: {ch.credit_cost} credits | Pass: {ch.passing_score}%")
            print(f"                  Slug: /challenges/{ch.slug}\n")

    except Exception as e:
        db.rollback()
        print(f"❌  Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_challenges()