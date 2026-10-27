# data

Datasets and sample inputs, for example prompt injection samples, PII test cases and evaluation sets.

Find the folder from code with:

```python
from guardrails_lab.config import DATA_DIR
```

Commit only small, hand-made samples. Keep large or downloaded datasets, and anything with real personal data, out of git. Local databases, vector stores and caches are already in `.gitignore`.
