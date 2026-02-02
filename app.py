from flask import Flask, render_template, request, jsonify
from rag_system import initialize_database
from datetime import datetime
import os

app = Flask(__name__)

# Initialize RAG system
print("Initializing RAG system for web server...")
rag = initialize_database(interactive=False)
print("Web server RAG system ready!")

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    """Handle chat queries"""
    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Process query using RAG system
    try:
        # Check for conversational phrases (simple version for web)
        conversational_phrases = ['hi', 'hello', 'hey', 'thank you', 'thanks', 'thank u', 'hii', 'heyy', 'hlo', 'hola']
        
        # Check for exact match or short greeting
        clean_query = user_query.lower().strip()
        if clean_query in conversational_phrases or (len(clean_query) < 5 and any(g in clean_query for g in ['hi', 'hey'])):
            answer = "😊 Hello! I'm your Sakthi Infra Tech Assistant.\n\nI can help you with:\n• Order details\n• Payment status\n• Vendor information\n\nWhat would you like to know?"
        else:
            answer = rag.answer_query(user_query)
            
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/add', methods=['POST'])
def add_order():
    """Handle adding new orders"""
    data = request.json
    
    try:
        # Calculate derived fields
        # Note: In a real app, this logic should be shared/centralized
        # Simplified for demo: just ensuring required fields exist
        
        # Determine Order ID (simplified)
        current_count = rag.collection.count()
        next_id = current_count + 1
        
        # Prepare order data with defaults
        order_data = {
            'order_id': next_id,
            'invoice_no': f"INV-{10000 + next_id}",
            'vendor_name': data.get('vendor_name'),
            'vendor_id': "V999", # Placeholder
            'gst_number': data.get('gst_number', "33XXXXX0000Z0"),
            'vendor_state': "Tamil Nadu",
            'vendor_contact': "+919999999999",
            'item_name': data.get('item_name'),
            'item_id': "I999",
            'item_category': "General",
            'hsn_code': "0000",
            'quantity': float(data.get('quantity', 0)),
            'unit': data.get('unit', 'Kg'),
            'unit_price': float(data.get('unit_price', 0)),
            'order_date': data.get('order_date', datetime.now().strftime("%Y-%m-%d")),
            'invoice_date': datetime.now().strftime("%Y-%m-%d"),
            'delivery_date': datetime.now().strftime("%Y-%m-%d"),
            'payment_status': "Pending",
            'payment_mode': "NEFT",
            'transaction_id': "PENDING",
            'transport_mode': "Road",
            'eway_bill_no': "-",
            'received_by': "Staff",
            'quality_check_status': "Pending"
        }
        
        # Calculate totals
        taxable = order_data['quantity'] * order_data['unit_price']
        tax = taxable * 0.18 # 18% GST assumption
        total = taxable + tax
        
        order_data['taxable_amount'] = taxable
        order_data['total_tax'] = tax
        order_data['total_invoice_amount'] = total
        
        # Add to RAG
        success = rag.add_new_order(order_data)
        
        if success:
            return jsonify({'success': True, 'order_id': next_id})
        else:
            return jsonify({'success': False, 'error': 'Failed to add to database'}), 500
            
    except Exception as e:
        print(f"Error adding order: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
