from .grader import PythonGrader, GradingResult, SUPPORTED_TEST_TYPES as PYTHON_TEST_TYPES
from .sql_grader import SQLGrader, SQL_TEST_TYPES
from .text_grader import TextGrader, TEXT_TEST_TYPES

SUPPORTED_TEST_TYPES = PYTHON_TEST_TYPES | TEXT_TEST_TYPES | SQL_TEST_TYPES

__all__ = [
    "PythonGrader", "SQLGrader", "TextGrader", "GradingResult",
    "SUPPORTED_TEST_TYPES", "TEXT_TEST_TYPES", "SQL_TEST_TYPES",
]
