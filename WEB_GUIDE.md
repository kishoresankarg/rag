# 🌐 Sakthi Infra Tech Web Assistant - User Guide

## 🚀 Getting Started

### 1. Start the Server
Open your terminal and run:
```bash
python app.py
```

### 2. Open in Browser
Go to: **[http://localhost:5000](http://localhost:5000)**

---

## ✨ Features

### 💬 Chat Interface
Ask questions naturally, just like in the CLI:
- _"Show orders for Infra Tech"_
- _"Infra Tech payment status"_
- _"What items did ABC Textiles order?"_

### ➕ Add New Orders
1. Click the **"Add New Order"** button (top right).
2. Fill in the form (Vendor, Item, Quantity, Price, etc.).
3. Click "Add Order".
4. The assistant picks up the new data immediately!

### 🎨 Visuals
- **Dark Mode**: Professional dark theme for low-light usage.
- **Glassmorphism**: Modern, semi-transparent cards.
- **Responsive**: Works on mobile and desktop.

---

## 🔧 Troubleshooting

**Q: Server won't start?**
A: Make sure you installed Flask: `pip install flask`

**Q: "Address already in use"?**
A: Another instance applies running. Close it first or kill the python process.

**Q: Browser shows error?**
A: Ensure the terminal says `Running on http://127.0.0.1:5000`.

---

## 📝 API Reference (For Developers)

- `POST /api/query`: Send JSON `{ "query": "your question" }`
- `POST /api/add`: Send JSON with order fields.
