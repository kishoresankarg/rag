# 🚨 IMPORTANT: How to Add New Data

## ❌ WRONG WAY (What you tried)
```
💬 Your question: Add an order of 500 Cotton Yarn from Sakthi Infra Tech...
```
This treats your input as a SEARCH QUERY, not an add command!

---

## ✅ CORRECT WAY

### Step 1: Type just the word "add"
```
💬 Your question: add
```

### Step 2: Follow the guided prompts
The system will ask you for each field one by one:
```
📝 ADD NEW ORDER
======================================================================

Invoice Number (e.g., INV-10001): INV-15001

--- Vendor Information ---
Vendor Name: Sakthi Infra Tech Textile Pvt Ltd
Vendor ID (e.g., V001): V006
GST Number: 33ABCDE1234F1Z2
...
```

### Step 3: Enter your data
- Vendor Name: **Sakthi Infra Tech Textile Pvt Ltd**
- GST: **33ABCDE1234F1Z2**
- Item: **Cotton Yarn**
- Quantity: **500**
- Unit Price: **1560** (to get ₹7,80,000)
- Order Date: **18-03-2025** (or 2025-03-18)

### Step 4: Confirm
```
Add this order to the database? (yes/no): yes

✅ Data successfully added to Sakthi Textiles knowledge base
```

---

## 📝 Quick Reference

| What You Want | Command to Type |
|---------------|-----------------|
| **Add new order** | `add` |
| **Search orders** | Type your question normally |
| **Get help** | `help` |
| **Exit** | `exit` or `quit` |

---

## ⚠️ Current Limitations

### ✅ Supported
- ✅ **Add new orders** - Type `add`
- ✅ **Search/Query** - Ask questions naturally

### ❌ Not Supported (Yet)
- ❌ **Update/Edit** - Cannot modify existing orders
- ❌ **Delete** - Cannot remove orders
- ❌ **Natural language add** - Must use `add` command

---

## 🎯 Example Session

```
💬 Your question: add

📝 ADD NEW ORDER
======================================================================

Invoice Number: INV-15001
Vendor Name: Sakthi Infra Tech Textile Pvt Ltd
Vendor ID: V006
GST Number: 33ABCDE1234F1Z2
...
Item Name: Cotton Yarn
Quantity: 500
Unit: Kg
Unit Price: 1560

✅ Data successfully added!

💬 Your question: Show orders for Sakthi Infra Tech Textile Pvt Ltd

📊 Answer:
----------------------------------------------------------------------
Found 1 orders for Sakthi Infra Tech Textile Pvt Ltd:
1. Order 5001 - Cotton Yarn - ₹9,09,080.00
----------------------------------------------------------------------
```

---

## 🆘 Troubleshooting

**Q: I typed "Add an order..." but it searched instead**
**A:** Type just `add` (one word), not a full sentence

**Q: Can I add data in one line?**
**A:** No, you must use the interactive `add` command

**Q: How do I update an existing order?**
**A:** Currently not supported. You can only add new orders.

**Q: How do I delete an order?**
**A:** Currently not supported through the CLI.

---

## 💡 Remember

**To add data:**
1. Type: `add`
2. Fill in the prompts
3. Confirm with `yes`

**That's it!** 🎉
