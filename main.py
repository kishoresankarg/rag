"""
Sakthi Textiles Smart RAG Assistant - Interactive CLI
"""

from rag_system import SakthiTextilesRAG, initialize_database
import sys
from datetime import datetime


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("  🧵 SAKTHI TEXTILES SMART RAG ASSISTANT 🧵")
    print("="*70)
    print("  Your intelligent textile order management system")
    print("="*70 + "\n")


def print_help():
    """Print help information"""
    help_text = """
📋 AVAILABLE COMMANDS:

  Query Examples:
  • "Show orders for [Vendor Name]"
  • "What items did [Vendor Name] order?"
  • "Total amount spent by [Vendor Name]"
  • "GST number of [Vendor Name]"
  
  Supported Vendors:
  • Sakthi Traders
  • ABC Textiles
  • Sri Yarn Mills
  • Lakshmi Fabrics
  • Vijay Spinning
  
  Special Commands:
  • add      - Add a new order (guided entry)
  • help     - Show this help message
  • exit     - Exit the application
  • quit     - Exit the application

"""
    print(help_text)


def add_new_order_interactive(rag):
    """Interactive function to add a new order"""
    print("\n" + "="*70)
    print("  📝 ADD NEW ORDER")
    print("="*70 + "\n")
    
    try:
        # Get next order ID
        current_count = rag.collection.count()
        next_order_id = current_count + 1
        
        print("Please enter the order details:")
        print("(Press Ctrl+C to cancel at any time)\n")
        
        # Collect order information
        order_data = {}
        
        # Required fields
        order_data['order_id'] = next_order_id
        order_data['invoice_no'] = input("Invoice Number (e.g., INV-10001): ").strip() or f"INV-{10000 + next_order_id}"
        
        # Vendor information
        print("\n--- Vendor Information ---")
        order_data['vendor_name'] = input("Vendor Name: ").strip()
        order_data['vendor_id'] = input("Vendor ID (e.g., V001): ").strip() or "V999"
        order_data['gst_number'] = input("GST Number: ").strip() or "33XXXXX0000Z0"
        order_data['vendor_state'] = input("Vendor State (default: Tamil Nadu): ").strip() or "Tamil Nadu"
        order_data['vendor_contact'] = input("Vendor Contact: ").strip() or "+919999999999"
        
        # Item information
        print("\n--- Item Information ---")
        order_data['item_name'] = input("Item Name (e.g., Cotton Yarn): ").strip()
        order_data['item_id'] = input("Item ID (e.g., I001): ").strip() or "I999"
        order_data['item_category'] = input("Item Category (e.g., Yarn/Fabric): ").strip() or "Yarn"
        order_data['hsn_code'] = input("HSN Code (e.g., 5205): ").strip() or "0000"
        
        # Quantity and pricing
        print("\n--- Quantity & Pricing ---")
        order_data['quantity'] = float(input("Quantity: ").strip() or "0")
        order_data['unit'] = input("Unit (e.g., Kg): ").strip() or "Kg"
        order_data['unit_price'] = float(input("Unit Price (₹): ").strip() or "0")
        
        # Calculate amounts
        taxable_amount = order_data['quantity'] * order_data['unit_price']
        order_data['taxable_amount'] = taxable_amount
        
        cgst_rate = 9
        sgst_rate = 9
        cgst_amount = (taxable_amount * cgst_rate) / 100
        sgst_amount = (taxable_amount * sgst_rate) / 100
        total_tax = cgst_amount + sgst_amount
        
        order_data['cgst_rate'] = cgst_rate
        order_data['cgst_amount'] = cgst_amount
        order_data['sgst_rate'] = sgst_rate
        order_data['sgst_amount'] = sgst_amount
        order_data['total_tax'] = total_tax
        order_data['total_invoice_amount'] = taxable_amount + total_tax
        
        # Dates
        print("\n--- Dates ---")
        today = datetime.now().strftime("%Y-%m-%d")
        order_data['order_date'] = input(f"Order Date (YYYY-MM-DD, default: {today}): ").strip() or today
        order_data['invoice_date'] = input(f"Invoice Date (default: {today}): ").strip() or today
        order_data['delivery_date'] = input("Delivery Date (optional): ").strip() or today
        order_data['payment_due_date'] = input("Payment Due Date (optional): ").strip() or today
        
        # Payment information
        print("\n--- Payment Information ---")
        order_data['payment_status'] = input("Payment Status (Paid/Pending/Partial): ").strip() or "Pending"
        order_data['payment_mode'] = input("Payment Mode (NEFT/UPI/RTGS/Cheque): ").strip() or "NEFT"
        order_data['payment_date'] = input("Payment Date (optional): ").strip() or ""
        order_data['transaction_id'] = input("Transaction ID (optional): ").strip() or f"TXN{next_order_id}"
        
        # Logistics
        print("\n--- Logistics ---")
        order_data['transport_mode'] = input("Transport Mode (Road/Courier): ").strip() or "Road"
        order_data['eway_bill_no'] = input("E-way Bill Number (optional): ").strip() or f"EWB{next_order_id}"
        order_data['received_by'] = input("Received By: ").strip() or "Staff"
        order_data['quality_check_status'] = input("Quality Check (Approved/Rejected/Pending): ").strip() or "Pending"
        order_data['remarks'] = input("Remarks (optional): ").strip() or ""
        
        # Show summary
        print("\n" + "="*70)
        print("  📋 ORDER SUMMARY")
        print("="*70)
        print(f"Order ID: {order_data['order_id']}")
        print(f"Invoice: {order_data['invoice_no']}")
        print(f"Vendor: {order_data['vendor_name']}")
        print(f"Item: {order_data['item_name']}")
        print(f"Quantity: {order_data['quantity']} {order_data['unit']}")
        print(f"Total Amount: ₹{order_data['total_invoice_amount']:,.2f}")
        print("="*70)
        
        # Confirm
        confirm = input("\nAdd this order to the database? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            success = rag.add_new_order(order_data)
            if success:
                print("\n✅ Data successfully added to Sakthi Textiles knowledge base")
                print(f"   Total records in database: {rag.collection.count()}")
            else:
                print("\n❌ Failed to add order to database")
        else:
            print("\n❌ Order cancelled")
            
    except KeyboardInterrupt:
        print("\n\n❌ Order entry cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize RAG system
    print("🔄 Initializing RAG system...\n")
    try:
        rag = initialize_database()
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        print("\nMake sure:")
        print("1. The file 'textile_orders_5000.csv' exists in the current directory")
        print("2. All dependencies are installed (run: pip install -r requirements.txt)")
        sys.exit(1)
    
    print("\n✅ System ready! Type 'help' for usage examples or 'exit' to quit.\n")
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("💬 Your question: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Thank you for using Sakthi Textiles RAG Assistant!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'add':
                add_new_order_interactive(rag)
                continue
            
            # Detect if user is trying to add/update/delete with natural language
            add_keywords = ['add an order', 'add new order', 'create order', 'new order', 'insert order']
            update_keywords = ['update', 'edit', 'modify', 'change']
            delete_keywords = ['delete', 'remove']
            
            # Detect conversational/non-query phrases
            conversational_phrases = [
                'thank you', 'thanks', 'thank u', 'thankyou',
                'ok', 'okay', 'got it', 'understood',
                'bye', 'goodbye', 'see you',
                'hi', 'hello', 'hey',
                'yes', 'no', 'maybe',
                'cool', 'nice', 'great', 'awesome', 'perfect'
            ]
            
            query_lower = user_input.lower().strip()
            
            # Check for conversational phrases
            if query_lower in conversational_phrases or len(user_input.strip()) < 3:
                print("\n😊 You're welcome! Ask me anything about textile orders.\n")
                continue
            
            if any(keyword in query_lower for keyword in add_keywords):
                print("\n💡 To add a new order, please type: add")
                print("   This will start the guided data entry process.\n")
                continue
            
            if any(keyword in query_lower for keyword in update_keywords):
                print("\n💡 Update/Edit functionality:")
                print("   Currently, the system supports adding new orders only.")
                print("   To add a new order, type: add\n")
                continue
            
            if any(keyword in query_lower for keyword in delete_keywords):
                print("\n💡 Delete functionality:")
                print("   Currently, the system supports adding new orders only.")
                print("   Delete operations require programmatic access.\n")
                continue
            
            # Process query
            print("\n🔍 Searching...")
            answer = rag.answer_query(user_input)
            
            print("\n📊 Answer:")
            print("-" * 70)
            print(answer)
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Sakthi Textiles RAG Assistant!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
