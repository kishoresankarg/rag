"""
Quick diagnostic script to check vendor names in database
"""

from rag_system import SakthiTextilesRAG

# Initialize RAG system
print("Initializing RAG system...")
rag = SakthiTextilesRAG()

# Get all vendor names
print("\n" + "="*70)
print("ALL VENDORS IN DATABASE:")
print("="*70)

vendors = rag.get_all_vendor_names()
for i, vendor in enumerate(vendors, 1):
    # Get count for each vendor
    results = rag.get_vendor_orders(vendor)
    count = len(results['metadatas']) if results['metadatas'] else 0
    print(f"{i}. {vendor} ({count} orders)")

print("\n" + "="*70)
print(f"Total unique vendors: {len(vendors)}")
print("="*70)

# Test vendor search
print("\n" + "="*70)
print("TESTING VENDOR DETECTION:")
print("="*70)

test_queries = [
    "infra tech orders",
    "show infra tech details",
    "what did infra tech order?",
]

for query in test_queries:
    vendor = rag.find_vendor_in_query(query)
    print(f"\nQuery: '{query}'")
    print(f"Detected vendor: {vendor}")
