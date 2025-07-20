# 🛒 E-Commerce Backend with FastAPI & MongoDB

This is a simple e-commerce backend project built with **FastAPI** and **MongoDB**, created as part of the **HROne Backend Intern Hiring Task**.

It lets you:

- Add products
- List products (with filters)
- Create orders
- View orders by user

---

## 🚀 Tech Stack

- **Python 3.10+**
- **FastAPI** for building APIs
- **MongoDB Atlas** for storing product and order data
- **Motor** (async MongoDB client)
- **httpx + pytest** for testing APIs

---

## 📁 Project Structure

```
app/
├── models/         # Pydantic schemas for request & response
├── routes/         # All API endpoints
├── database.py     # MongoDB connection
├── main.py         # App entry point
tests/
├── test_api.py     # Automated tests using httpx
.env                # Environment variables (MongoDB URI etc.)
requirements.txt    # All dependencies
```

---

## ⚙️ How to Run Locally

### 1. Clone the project
```bash
git clone https://github.com/your-username/ecom-fastapi.git
cd ecom-fastapi
```

### 2. Set up environment variables

Create a `.env` file (or copy `.env.example`) and add your MongoDB URI:

```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Now visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try the APIs.

---

## 🔬 Running Tests

To run API tests locally:

```bash
pytest tests/ -v
```

> Make sure the server is running locally at `http://127.0.0.1:8000` before running the tests.

---

## ✅ APIs Implemented

### 1. Create Product
- `POST /products`
- Request Body:
```json
{
  "name": "T-shirt",
  "price": 299.0,
  "sizes": [
    {"size": "M", "quantity": 10},
    {"size": "L", "quantity": 5}
  ]
}
```
- Returns: `{ "id": "..." }`

---

### 2. List Products
- `GET /products?name=shirt&size=M&limit=5&offset=0`
- Returns:
```json
{
  "data": [ ... ],
  "page": { "next": ..., "previous": ..., "limit": ... }
}
```

---

### 3. Create Order
- `POST /orders`
```json
{
  "userId": "user123",
  "items": [
    {
      "productId": "product_id_here",
      "qty": 2
    }
  ]
}
```
- Returns: `{ "id": "..." }`

---

### 4. Get Orders by User
- `GET /orders/user123`
- Returns:
```json
{
  "data": [
    {
      "id": "order_id",
      "items": [
        {
          "productDetails": {
            "name": "T-shirt",
            "id": "product_id"
          },
          "qty": 2
        }
      ],
      "total": 598.0
    }
  ],
  "page": { "next": ..., "previous": ..., "limit": ... }
}
```

---

## 🧠 Notes

- All product and order IDs are **custom numeric strings** (not Mongo ObjectId).
- Products don't show their `sizes` in the `/products` GET response — as per spec.
- Pagination is supported on both listing APIs.

---

## 🤝 Submission Notes

- Hosted on **Render**: [https://ecom-fastapi-wnzl.onrender.com](https://ecom-fastapi-wnzl.onrender.com)
- Base URL submitted correctly
- Code pushed and public
- Follows all format guidelines in the assignment

---

## 🙋‍♂️ Author

Built with ❤️ by **Dev Rathore**  
For HROne Backend Intern 2025
