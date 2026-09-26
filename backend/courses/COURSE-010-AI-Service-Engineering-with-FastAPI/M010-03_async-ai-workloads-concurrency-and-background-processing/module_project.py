MODULE_ID = 'M010-03'
MODULE_PROJECT = {'title': 'Concurrent Multi-User AI Service',
 'description': 'Remove blocking paths, add bounded async provider calls, isolate heavy inference, '
                'and expose a background-job workflow.',
 'objectives': ['Protect event loop',
                'Bound external concurrency',
                'Separate inference tier',
                'Implement job status flow'],
 'tech_stack': ['FastAPI', 'asyncio', 'HTTPX', 'optional worker queue'],
 'estimated_hours': 7}
