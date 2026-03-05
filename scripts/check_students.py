import os, sys
sys.path.append(os.getcwd())
from database.db import student_collection
import numpy as np

count = student_collection.count_documents({})
print(f"Student documents count: {count}")

sample = student_collection.find_one()
print("Sample student:")
print(sample)

# Analyze embeddings
all_docs = list(student_collection.find({}))
for i, d in enumerate(all_docs[:5]):
    emb = np.array(d.get('embedding', []))
    if emb.size == 0:
        print(i, "embedding missing or empty")
    else:
        print(i, "embedding length", emb.size, "all zeros:", np.allclose(emb, 0))
