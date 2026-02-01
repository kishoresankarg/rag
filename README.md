# Sakthi Textiles Smart RAG Assistant - Quick Start Guide

## 🚀 Getting Started

### 1. Run the Interactive Assistant
```bash
cd d:\rag
python main.py
```

### 2. Try These Queries
```
Show orders for Sakthi Traders
What items did ABC Textiles order?
Total amount spent by Vijay Spinning
GST number of Lakshmi Fabrics
```

### 3. Get Help
```
Type: help
```

### 4. Exit
```
Type: exit
```

---

## 📝 Supported Query Types

| Query Type | Example |
|------------|---------|
| **Vendor Orders** | "Show orders for [Vendor Name]" |
| **Item Names** | "What items did [Vendor] order?" |
| **Total Amount** | "Total spent by [Vendor]" |
| **GST Number** | "GST number of [Vendor]" |
| **General Search** | Any natural language question |

---

## 🏢 Supported Vendors

- Sakthi Traders
- ABC Textiles
- Sri Yarn Mills
- Lakshmi Fabrics
- Vijay Spinning

---

## ⚡ System Status

✅ **Database**: 5,000 orders loaded  
✅ **Vector Store**: ChromaDB initialized  
✅ **Embeddings**: Generated and stored  
✅ **Ready**: System operational  

---

## 📁 Files

- `main.py` - Interactive CLI
- `rag_system.py` - Core RAG engine
- `textile_orders_5000.csv` - Data source
- `chroma_db/` - Vector database

---

**Need help?** Type `help` in the interactive mode!
