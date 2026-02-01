"""
Test script to verify vendor detection is working
"""

from rag_system import SakthiTextilesRAG

# Initialize
print("Initializing RAG system...")
rag = SakthiTextilesRAG()

print("\n" + "="*70)
print("TESTING VENDOR DETECTION")
print("="*70)

test_queries = [
    "show the infra tech details",
    "infra tech orders",
    "what did infra tech order?",
    "total spent by infra tech",
    "get orders for infra tech",
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    vendor = rag.find_vendor_in_query(query)
    print(f"Detected vendor: '{vendor}'")
    
    if vendor:
        print(f"✅ Vendor detected correctly!")
    else:
        print(f"❌ NO VENDOR DETECTED - will use semantic search")

print("\n" + "="*70)
print("ACTUAL QUERY RESULTS")
print("="*70)

# Test one query
query = "show the infra tech details"
print(f"\nQuery: '{query}'")
answer = rag.answer_query(query)
print(f"\nAnswer:\n{answer}")
