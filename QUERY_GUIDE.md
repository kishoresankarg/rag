# 🎯 Query Guide - Sakthi Textiles RAG Assistant

## 📝 How to Ask Questions

### 1️⃣ **Specific Questions** (Get Specific Answers)

| What You Want | Example Query | What You Get |
|---------------|---------------|--------------|
| **Payment Status Only** | `infra tech payment status` | Just payment info |
| **GST Number Only** | `infra tech gst number` | Just GST |
| **Order Dates Only** | `infra tech order dates` | Just dates |

**Example Output:**
```
💳 Payment Status for infra tech:
1. Order 901 - Payment: pending
```

---

### 2️⃣ **Summary View** (Quick Overview)

| Query | Output |
|-------|--------|
| `infra tech orders` | Order ID, Item, Amount |
| `show infra tech` | Simple list |

**Example Output:**
```
Found 1 orders for infra tech:
1. Order 901 - cottton - ₹1,062.00
```

---

### 3️⃣ **Detailed View** (Key Information)

| Query | Output |
|-------|--------|
| `infra tech details` | 6 key fields |
| `show infra tech details` | Item, Amount, Payment, Date, GST, Invoice |

**Example Output:**
```
📋 Detailed Orders for infra tech (1 total):

============================================================
Order #1 - ID: 901
============================================================
📦 Item: cottton (yarn)
💰 Amount: ₹1,062.00
💳 Payment Status: pending
📅 Order Date: 500
🏢 GST Number: 123g3
📄 Invoice: inv006
```

---

### 4️⃣ **Full Details** (ALL 34 Fields!)

| Query | Output |
|-------|--------|
| `infra tech full details` | Every single field |
| `infra tech all details` | Complete order info |
| `show infra tech everything` | All 34 fields |

**Example Output:**
```
📋 COMPLETE Details for infra tech (1 total orders):

======================================================================
ORDER #1
======================================================================
Order ID: 901
Invoice: inv006
Vendor: infra tech (ID: v003)
GST Number: 123g3
State: tamilnadu
Contact: 923032034
Item: cottton (yarn)
Item ID: i002
HSN Code: 54
Quantity: 9.0 2
Unit Price: ₹100
Taxable Amount: ₹900.0
Total Tax: ₹162.0
Total Invoice Amount: ₹1062.0
Order Date: 500
Invoice Date: 2/10/25
Delivery Date: 2/11/25
Payment Status: pending
Payment Mode: neft
Transaction ID: io
Transport Mode: corier
E-way Bill: 
Received By: 
Quality Check: pending
... (and more fields)
```

---

## 🎯 Quick Reference

### Specific Questions
```
payment status
gst number  
order dates
```

### Summary
```
orders
show [vendor]
```

### Detailed (6 fields)
```
details
show details
```

### Full (ALL fields)
```
full details
all details
everything
complete details
```

---

## 💡 Pro Tips

1. **Be specific** - Ask for exactly what you need
2. **Use keywords** - "payment", "gst", "date", "full", "all"
3. **Vendor name first** - Start with vendor name for best results
4. **Try variations** - Different phrasings work!

---

## ✅ Examples

```
💬 infra tech payment status          → Payment only
💬 infra tech orders                  → Summary
💬 infra tech details                 → 6 key fields
💬 infra tech full details            → ALL 34 fields
💬 what did infra tech order?         → Items list
💬 total spent by infra tech          → Total amount
```

**Enjoy your smart RAG assistant!** 🚀
