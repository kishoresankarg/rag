"""
Sakthi Textiles Smart RAG Assistant
A Retrieval-Augmented Generation system for textile order management
"""

import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import os
from datetime import datetime


class SakthiTextilesRAG:
    """RAG system for Sakthi Textiles order management"""
    
    def __init__(self, csv_path: str = "textile_orders_5000.csv", db_path: str = "./chroma_db"):
        """
        Initialize the RAG system
        
        Args:
            csv_path: Path to the CSV file containing order data
            db_path: Path to store ChromaDB database
        """
        self.csv_path = csv_path
        self.db_path = db_path
        
        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        print("Initializing vector database...")
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="textile_orders",
            metadata={"description": "Sakthi Textiles order records"}
        )
        
        print(f"RAG system initialized. Current records in DB: {self.collection.count()}")
    
    def create_document_from_order(self, order: Dict[str, Any]) -> str:
        """
        Convert an order record to a structured text document
        
        Args:
            order: Dictionary containing order data
            
        Returns:
            Formatted text document
        """
        doc = f"""Order ID: {order['order_id']}
Invoice: {order['invoice_no']}
Vendor: {order['vendor_name']} (ID: {order['vendor_id']})
GST Number: {order['gst_number']}
State: {order['vendor_state']}
Contact: {order['vendor_contact']}
Item: {order['item_name']} ({order['item_category']})
Item ID: {order['item_id']}
HSN Code: {order['hsn_code']}
Quantity: {order['quantity']} {order['unit']}
Unit Price: ₹{order['unit_price']}
Taxable Amount: ₹{order['taxable_amount']}
Total Tax: ₹{order['total_tax']}
Total Invoice Amount: ₹{order['total_invoice_amount']}
Order Date: {order['order_date']}
Invoice Date: {order['invoice_date']}
Delivery Date: {order['delivery_date']}
Payment Status: {order['payment_status']}
Payment Mode: {order['payment_mode']}
Transaction ID: {order['transaction_id']}
Transport Mode: {order['transport_mode']}
E-way Bill: {order['eway_bill_no']}
Received By: {order['received_by']}
Quality Check: {order['quality_check_status']}"""
        
        return doc
    
    def load_csv_data(self) -> pd.DataFrame:
        """Load order data from CSV file"""
        print(f"Loading data from {self.csv_path}...")
        df = pd.read_csv(self.csv_path)
        print(f"✅ Loaded {len(df)} orders from CSV")
        return df
    
    def add_orders_to_db(self, df: pd.DataFrame, batch_size: int = 100):
        """
        Add orders to the vector database
        
        Args:
            df: DataFrame containing order data
            batch_size: Number of records to process at once
        """
        print(f"Processing {len(df)} orders...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            # Create document
            doc = self.create_document_from_order(row.to_dict())
            documents.append(doc)
            
            # Create metadata
            metadata = {
                "order_id": str(row['order_id']),
                "invoice_no": str(row['invoice_no']),
                "vendor_id": str(row['vendor_id']),
                "vendor_name": str(row['vendor_name']),
                "gst_number": str(row['gst_number']),
                "item_id": str(row['item_id']),
                "item_name": str(row['item_name']),
                "item_category": str(row['item_category']),
                "order_date": str(row['order_date']),
                "payment_status": str(row['payment_status']),
                "total_invoice_amount": float(row['total_invoice_amount']),
            }
            metadatas.append(metadata)
            
            # Create unique ID
            ids.append(f"order_{row['order_id']}")
            
            # Add in batches
            if len(documents) >= batch_size:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"  Added batch of {len(documents)} orders...")
                documents = []
                metadatas = []
                ids = []
        
        # Add remaining documents
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"  Added final batch of {len(documents)} orders...")
        
        print(f"✅ Successfully added all orders to database!")
        print(f"   Total records in DB: {self.collection.count()}")
    
    def query(self, query_text: str, n_results: int = 10, vendor_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            query_text: Natural language query
            n_results: Number of results to retrieve
            vendor_filter: Optional vendor name to filter by
            
        Returns:
            Dictionary containing results and metadata
        """
        # Build where clause for filtering
        where_clause = None
        if vendor_filter:
            where_clause = {"vendor_name": {"$eq": vendor_filter}}
        
        # Query the collection
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_clause
        )
        
        return results
    
    def get_vendor_orders(self, vendor_name: str) -> List[Dict[str, Any]]:
        """Get all orders for a specific vendor"""
        results = self.collection.get(
            where={"vendor_name": {"$eq": vendor_name}}
        )
        return results
    
    def get_vendor_items(self, vendor_name: str) -> List[str]:
        """Get unique item names for a vendor"""
        results = self.get_vendor_orders(vendor_name)
        
        if not results['metadatas']:
            return []
        
        items = set()
        for metadata in results['metadatas']:
            items.add(metadata['item_name'])
        
        return sorted(list(items))
    
    def calculate_vendor_total(self, vendor_name: str) -> float:
        """Calculate total amount spent by a vendor"""
        results = self.get_vendor_orders(vendor_name)
        
        if not results['metadatas']:
            return 0.0
        
        total = sum(metadata['total_invoice_amount'] for metadata in results['metadatas'])
        return total
    
    def get_vendor_gst(self, vendor_name: str) -> Optional[str]:
        """Get GST number for a vendor"""
        results = self.get_vendor_orders(vendor_name)
        
        if not results['metadatas']:
            return None
        
        return results['metadatas'][0]['gst_number']
    
    def search_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Search orders by date"""
        results = self.collection.get(
            where={"order_date": {"$eq": date}}
        )
        return results
    
    def add_new_order(self, order_data: Dict[str, Any]) -> bool:
        """
        Add a new order to the database
        
        Args:
            order_data: Dictionary containing order information
            
        Returns:
            True if successful
        """
        try:
            # Create document
            doc = self.create_document_from_order(order_data)
            
            # Create metadata
            metadata = {
                "order_id": str(order_data['order_id']),
                "invoice_no": str(order_data['invoice_no']),
                "vendor_id": str(order_data['vendor_id']),
                "vendor_name": str(order_data['vendor_name']),
                "gst_number": str(order_data['gst_number']),
                "item_id": str(order_data['item_id']),
                "item_name": str(order_data['item_name']),
                "item_category": str(order_data['item_category']),
                "order_date": str(order_data['order_date']),
                "payment_status": str(order_data['payment_status']),
                "total_invoice_amount": float(order_data['total_invoice_amount']),
            }
            
            # Add to collection
            self.collection.add(
                documents=[doc],
                metadatas=[metadata],
                ids=[f"order_{order_data['order_id']}"]
            )
            
            return True
        except Exception as e:
            print(f"Error adding order: {e}")
            return False
    
    def get_all_vendor_names(self) -> List[str]:
        """Get all unique vendor names from the database"""
        try:
            # Get all records
            all_records = self.collection.get()
            if not all_records['metadatas']:
                return []
            
            # Extract unique vendor names
            vendors = set()
            for metadata in all_records['metadatas']:
                vendors.add(metadata['vendor_name'])
            
            return sorted(list(vendors))
        except Exception as e:
            print(f"Error getting vendor names: {e}")
            return []
    
    def find_vendor_in_query(self, query: str) -> Optional[str]:
        """
        Find vendor name in query by checking against all known vendors
        
        Args:
            query: User query string
            
        Returns:
            Matched vendor name or None
        """
        query_lower = query.lower()
        
        # Get all vendor names from database
        all_vendors = self.get_all_vendor_names()
        
        # Check for exact or partial matches
        for vendor in all_vendors:
            vendor_lower = vendor.lower()
            
            # Check if vendor name or significant part is in query
            vendor_words = vendor_lower.split()
            
            # Check for full vendor name match
            if vendor_lower in query_lower:
                return vendor
            
            # Check for partial match (at least 2 words or single significant word)
            if len(vendor_words) >= 2:
                # Check if any 2+ consecutive words match
                for i in range(len(vendor_words) - 1):
                    partial = ' '.join(vendor_words[i:i+2])
                    if partial in query_lower and len(partial) > 5:  # Avoid short matches
                        return vendor
            
            # Check for single word match if it's significant (>4 chars)
            for word in vendor_words:
                if len(word) > 4 and word in query_lower:
                    # Verify it's not a common word
                    common_words = ['textiles', 'traders', 'mills', 'fabrics', 'spinning', 'yarn', 'tech']
                    if word not in common_words:
                        return vendor
        
        return None
    
    def answer_query(self, user_query: str) -> str:
        """
        Process user query and return answer
        
        Args:
            user_query: Natural language question
            
        Returns:
            Answer string
        """
        query_lower = user_query.lower()
        
        # Try to find vendor name in query
        vendor_name = self.find_vendor_in_query(user_query)
        
        # Detect if user wants specific vendor details
        show_keywords = ['show', 'details', 'get', 'find', 'list']
        is_show_query = any(keyword in query_lower for keyword in show_keywords)
        
        # Handle different query types
        if "item" in query_lower and vendor_name:
            items = self.get_vendor_items(vendor_name)
            if not items:
                return f"No records found for {vendor_name}."
            return f"Items ordered by {vendor_name}:\n" + "\n".join(f"• {item}" for item in items)
        
        elif "total" in query_lower or "amount" in query_lower or "spent" in query_lower:
            if vendor_name:
                total = self.calculate_vendor_total(vendor_name)
                if total == 0:
                    return f"No records found for {vendor_name}."
                return f"Total amount spent by {vendor_name}: ₹{total:,.2f}"
        
        elif "gst" in query_lower and vendor_name:
            gst = self.get_vendor_gst(vendor_name)
            if not gst:
                return f"No records found for {vendor_name}."
            return f"GST Number of {vendor_name}: {gst}"
        
        elif ((("order" in query_lower or "detail" in query_lower or is_show_query) and vendor_name) or 
              ("payment" in query_lower and vendor_name)):
            results = self.get_vendor_orders(vendor_name)
            if not results['metadatas']:
                return f"No records found for {vendor_name}."
            
            # Get full document for detailed info
            documents = results.get('documents', [])
            metadatas = results['metadatas']
            count = len(metadatas)
            
            # Check for specific question types (with typo tolerance)
            payment_keywords = ['payment', 'payemnt', 'paymnt', 'pymnt']
            status_keywords = ['status', 'sttaus', 'staus', 'stat']
            
            has_payment = any(keyword in query_lower for keyword in payment_keywords)
            has_status = any(keyword in query_lower for keyword in status_keywords)
            
            if has_payment and has_status:
                # Only show payment status
                response = f"💳 Payment Status for {vendor_name}:\n\n"
                for i, metadata in enumerate(metadatas[:5]):
                    response += f"{i+1}. Order {metadata['order_id']} - Payment: {metadata['payment_status']}\n"
                return response
            
            elif "gst" in query_lower and "number" in query_lower:
                # Only show GST
                gst = metadatas[0]['gst_number']
                return f"🏢 GST Number of {vendor_name}: {gst}"
            
            elif "date" in query_lower:
                # Only show dates
                response = f"📅 Order Dates for {vendor_name}:\n\n"
                for i, metadata in enumerate(metadatas[:5]):
                    response += f"{i+1}. Order {metadata['order_id']} - Date: {metadata['order_date']}\n"
                return response
            
            # Check if user wants full/all details
            full_keywords = ['full', 'all', 'complete', 'everything', 'comprehensive']
            show_full = any(keyword in query_lower for keyword in full_keywords)
            
            # Check if user wants detailed view
            detailed_keywords = ['detail', 'payment', 'status', 'show']
            show_detailed = any(keyword in query_lower for keyword in detailed_keywords)
            
            if show_full:
                # Show ALL fields from the document
                response = f"📋 COMPLETE Details for {vendor_name} ({count} total orders):\n\n"
                
                max_show = min(count, 3)
                for i in range(max_show):
                    response += f"{'='*70}\n"
                    response += f"ORDER #{i+1}\n"
                    response += f"{'='*70}\n"
                    
                    # Parse the document to show all fields
                    if documents and i < len(documents):
                        doc = documents[i]
                        response += doc + "\n\n"
                    else:
                        # Fallback to metadata
                        metadata = metadatas[i]
                        for key, value in metadata.items():
                            response += f"{key}: {value}\n"
                        response += "\n"
                
                if count > max_show:
                    response += f"... and {count - max_show} more orders\n"
                    
            elif show_detailed:
                # Show key details (enhanced version)
                response = f"📋 Detailed Orders for {vendor_name} ({count} total):\n\n"
                
                max_show = min(count, 5)
                for i, metadata in enumerate(metadatas[:max_show]):
                    response += f"{'='*60}\n"
                    response += f"Order #{i+1} - ID: {metadata['order_id']}\n"
                    response += f"{'='*60}\n"
                    response += f"📦 Item: {metadata['item_name']} ({metadata['item_category']})\n"
                    response += f"💰 Amount: ₹{metadata['total_invoice_amount']:,.2f}\n"
                    response += f"💳 Payment Status: {metadata['payment_status']}\n"
                    response += f"📅 Order Date: {metadata['order_date']}\n"
                    response += f"🏢 GST Number: {metadata['gst_number']}\n"
                    response += f"📄 Invoice: {metadata['invoice_no']}\n\n"
                
                if count > max_show:
                    response += f"... and {count - max_show} more orders\n"
                    
                response += f"\n💡 Tip: Use 'full details' or 'all details' to see every field"
            else:
                # Show summary view
                response = f"Found {count} orders for {vendor_name}:\n\n"
                
                max_show = min(count, 10)
                for i, metadata in enumerate(metadatas[:max_show]):
                    response += f"{i+1}. Order {metadata['order_id']} - {metadata['item_name']} - ₹{metadata['total_invoice_amount']:,.2f}\n"
                
                if count > max_show:
                    response += f"\n... and {count - max_show} more orders"
                
                response += f"\n\n💡 Tip: Add 'details' to see more, or ask specific questions like 'payment status'"
            
            return response
        
        # If vendor is mentioned but no specific query type, show vendor orders with details
        elif vendor_name:
            results = self.get_vendor_orders(vendor_name)
            if not results['metadatas']:
                return f"No records found for {vendor_name}."
            
            count = len(results['metadatas'])
            response = f"📋 Orders for {vendor_name} ({count} total):\n\n"
            
            # Show detailed information for first 3 orders
            max_show = min(count, 3)
            for i, metadata in enumerate(results['metadatas'][:max_show]):
                response += f"{'='*60}\n"
                response += f"Order #{i+1} - ID: {metadata['order_id']}\n"
                response += f"{'='*60}\n"
                response += f"📦 Item: {metadata['item_name']} ({metadata['item_category']})\n"
                response += f"💰 Amount: ₹{metadata['total_invoice_amount']:,.2f}\n"
                response += f"💳 Payment Status: {metadata['payment_status']}\n"
                response += f"📅 Order Date: {metadata['order_date']}\n"
                response += f"🏢 GST Number: {metadata['gst_number']}\n"
                response += f"📄 Invoice: {metadata['invoice_no']}\n\n"
            
            if count > max_show:
                response += f"... and {count - max_show} more orders\n"
            
            return response
        
        # Default: semantic search (only if no vendor found)
        results = self.query(user_query, n_results=5)
        
        if not results['metadatas'] or len(results['metadatas'][0]) == 0:
            return "No records found for the requested information."
        
        # Format response
        response = "Here are the relevant orders:\n\n"
        for i, metadata in enumerate(results['metadatas'][0]):
            response += f"{i+1}. {metadata['vendor_name']} - {metadata['item_name']} - ₹{metadata['total_invoice_amount']:,.2f}\n"
        
        return response


def initialize_database(csv_path: str = "textile_orders_5000.csv", interactive: bool = True):
    """Initialize the database with CSV data"""
    rag = SakthiTextilesRAG(csv_path=csv_path)
    
    # Check if database is already populated
    if rag.collection.count() > 0:
        print(f"Database already contains {rag.collection.count()} records.")
        
        if interactive:
            response = input("Do you want to reload all data? (yes/no): ")
            if response.lower() != 'yes':
                return rag
        else:
            print("Skipping reload in non-interactive mode.")
            return rag
        
        # Clear existing data
        print("Clearing existing data...")
        rag.client.delete_collection("textile_orders")
        rag.collection = rag.client.create_collection(
            name="textile_orders",
            metadata={"description": "Sakthi Textiles order records"}
        )
    
    # Load and add data
    df = rag.load_csv_data()
    rag.add_orders_to_db(df)
    
    return rag


if __name__ == "__main__":
    # Initialize database
    rag = initialize_database()
    
    # Test queries
    print("\n" + "="*60)
    print("Testing RAG System")
    print("="*60)
    
    test_queries = [
        "Show orders for Sakthi Traders",
        "What items did ABC Textiles order?",
        "Total amount spent by Vijay Spinning",
        "GST number of Lakshmi Fabrics"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        answer = rag.answer_query(query)
        print(answer)
