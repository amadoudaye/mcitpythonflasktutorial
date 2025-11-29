from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# ---------- Fake menu data ----------
MENU = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "description": "Classic pizza with fresh mozzarella, basil & tomato sauce.",
        "price": 12.99,
    },
    {
        "id": 2,
        "name": "Pepperoni Pizza",
        "category": "Pizza",
        "description": "Mozzarella, tomato sauce & crispy pepperoni slices.",
        "price": 14.49,
    },
    {
        "id": 3,
        "name": "Butter Chicken Bowl",
        "category": "Indian",
        "description": "Creamy tomato-based curry with tender chicken & basmati rice.",
        "price": 16.99,
    },
    {
        "id": 4,
        "name": "Paneer Tikka Wrap",
        "category": "Indian",
        "description": "Grilled paneer, veggies & mint chutney in a warm wrap.",
        "price": 11.50,
    },
    {
        "id": 5,
        "name": "Classic Cheeseburger",
        "category": "Burgers",
        "description": "Beef patty, cheddar, lettuce, tomato & secret sauce.",
        "price": 13.25,
    },
    {
        "id": 6,
        "name": "Crispy Chicken Burger",
        "category": "Burgers",
        "description": "Crispy chicken fillet, mayo, pickles & lettuce.",
        "price": 12.75,
    },
    {
        "id": 7,
        "name": "Caesar Salad",
        "category": "Salads",
        "description": "Romaine, parmesan, croutons & creamy Caesar dressing.",
        "price": 9.99,
    },
    {
        "id": 8,
        "name": "Greek Salad",
        "category": "Salads",
        "description": "Tomato, cucumber, olives, feta & olive oil dressing.",
        "price": 10.50,
    },
    {
        "id": 9,
        "name": "Tiramisu",
        "category": "Desserts",
        "description": "Coffee-soaked ladyfingers with mascarpone cream.",
        "price": 7.25,
    },
    {
        "id": 10,
        "name": "Chocolate Lava Cake",
        "category": "Desserts",
        "description": "Warm chocolate cake with gooey molten center.",
        "price": 7.75,
    },
]


def find_menu_item(item_id: int):
    for item in MENU:
        if item["id"] == item_id:
            return item
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU)


@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(force=True) or {}

    customer = data.get("customer", {})
    items = data.get("items", [])

    name = (customer.get("name") or "").strip()
    address = (customer.get("address") or "").strip()
    phone = (customer.get("phone") or "").strip()

    if not name or not address or not phone:
        return jsonify({"error": "Please fill name, address and phone."}), 400

    if not items:
        return jsonify({"error": "Your cart is empty."}), 400

    # calculate total based on menu prices on backend
    total = 0.0
    detailed_items = []
    for item in items:
        item_id = int(item.get("id"))
        qty = int(item.get("quantity", 0))
        if qty <= 0:
            continue
        menu_item = find_menu_item(item_id)
        if not menu_item:
            continue
        line_total = menu_item["price"] * qty
        total += line_total
        detailed_items.append({
            "id": menu_item["id"],
            "name": menu_item["name"],
            "quantity": qty,
            "price": menu_item["price"],
            "line_total": round(line_total, 2),
        })

    if not detailed_items:
        return jsonify({"error": "No valid items in cart."}), 400

    order_id = f"FD-{int(time.time())}"

    # In a real app you would save to DB, send email, etc.
    # Here we just respond with a success message.
    response = {
        "orderId": order_id,
        "customer": {
            "name": name,
            "address": address,
            "phone": phone,
            "notes": customer.get("notes", ""),
        },
        "items": detailed_items,
        "total": round(total, 2),
        "message": "Order placed successfully. This is a demo, not a real order.",
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
