import customtkinter as ctk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

item_details = {
    "item_name": "Apple",
    "category": "Fruits",
    "price": 0.0,
    "amount": 0
}

info = {}
orders = []

def readInFile():
    global info
    try:
        with open('project.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                item_name, category, price, amount = line.strip().split(',')
                info[item_name] = {
                    'category': category,
                    'price': float(price),
                    'amount': int(amount)
                }
    except FileNotFoundError:
        pass

def writeInFile():
    global info
    with open('project.txt', 'w') as file:
        for item_name, details in info.items():
            file.write(f"{item_name},{details['category']},{details['price']},{details['amount']}\n")

def writeOrdersInFile():
    global orders
    with open('orders.txt', 'w') as file:
        for order in orders:
            file.write(f"{order['order_id']},{order['item_name']},{order['quantity']},{order['status']}\n")

def add_item():
    global info
    item_name = simpledialog.askstring("Input", "Enter item name:")
    category = simpledialog.askstring("Input", "Enter item category:")
    price = simpledialog.askfloat("Input", "Enter item price:")
    amount = simpledialog.askinteger("Input", "Enter item amount:")
    
    if item_name and category and price is not None and amount is not None:
        info[item_name] = {
            "category": category,
            "price": price,
            "amount": amount
        }
        writeInFile()
        messagebox.showinfo("Info", f"Item '{item_name}' added successfully!")

def edit_item():
    global info
    item_name = simpledialog.askstring("Input", "Enter the name of the item you want to edit:")
    
    if item_name in info:
        category = simpledialog.askstring("Input", "Enter the new category:")
        price = simpledialog.askfloat("Input", "Enter the new price:")
        amount = simpledialog.askinteger("Input", "Enter the new amount:")
        
        if category and price is not None and amount is not None:
            info[item_name] = {
                "category": category,
                "price": price,
                "amount": amount
            }
            writeInFile()
            messagebox.showinfo("Info", f"Item '{item_name}' updated successfully!")
    else:
        messagebox.showerror("Error", f"Item '{item_name}' not found in the inventory.")

def remove_item():
    global info
    item_name = simpledialog.askstring("Input", "Enter the name of the item you want to remove:")
    
    if item_name in info:
        del info[item_name]
        writeInFile()
        messagebox.showinfo("Info", f"Item '{item_name}' removed successfully!")
    else:
        messagebox.showerror("Error", f"Item '{item_name}' not found in the inventory.")

def display_inventory():
    global info
    inventory_text = "\n".join([f"{item_name}: {details}" for item_name, details in info.items()])
    messagebox.showinfo("Inventory", inventory_text)

def display_Terminal():
    global info
    inventory_text = "\n".join([f"{item_name}: {details}" for item_name, details in info.items()])
    print(inventory_text)

def create_html_file():
    global info, orders
    with open("project.html", 'w') as html:
        html.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Table</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        ::selection {
            background-color: #333;
            color: white;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        thead tr {
            background-color: #007BFF;
            color: #fff;
            text-align: left;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
        }
        tbody tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tbody tr:hover {
            background-color: #f1f1f1;
        }
        tbody tr td {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Inventory List</h1>
        <table>
            <thead>
                <tr>
                    <th>Item Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
""")
        for item_name, details in info.items():
            html.write(f"""
                <tr>
                    <td>{item_name}</td>
                    <td>{details['category']}</td>
                    <td>{details['price']}</td>
                    <td>{details['amount']}</td>
                </tr>
""")
        html.write("""
            </tbody>
        </table>
        <h1>Orders</h1>
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Item Name</th>
                    <th>Quantity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
""")
        for order in orders:
            html.write(f"""
                <tr>
                    <td>{order['order_id']}</td>
                    <td>{order['item_name']}</td>
                    <td>{order['quantity']}</td>
                    <td>{order['status']}</td>
                </tr>
""")
        html.write("""
            </tbody>
        </table>
    </div>
</body>
</html>
""")
    messagebox.showinfo("Info", "HTML file generated successfully!")

def create_order():
    global orders, info
    order_id = simpledialog.askstring("Input", "Enter order ID:")
    item_name = simpledialog.askstring("Input", "Enter item name for the order:")
    quantity = simpledialog.askinteger("Input", "Enter quantity:")
    
    if order_id and item_name and quantity is not None:
        if item_name in info:
            if quantity <= info[item_name]['amount']:
                orders.append({
                    "order_id": order_id,
                    "item_name": item_name,
                    "quantity": quantity,
                    "status": "Pending"
                })
                info[item_name]['amount'] -= quantity
                writeInFile()
                writeOrdersInFile()
                messagebox.showinfo("Info", f"Order '{order_id}' created successfully!")
            else:
                messagebox.showerror("Error", f"Quantity '{quantity}' is not available. Available: {info[item_name]['amount']}")
        else:
            messagebox.showerror("Error", f"Item '{item_name}' not found in the inventory.")

def update_order():
    global orders
    order_id = simpledialog.askstring("Input", "Enter order ID to update:")
    
    for order in orders:
        if order["order_id"] == order_id:
            new_item_name = simpledialog.askstring("Input", "Enter the name of the item you want to edit:")
            new_status = simpledialog.askstring("Input", "Enter new status:")
            new_order_quantity = simpledialog.askinteger("Input", "Enter new quantity:")
            if new_item_name and new_status is not None and new_order_quantity is not None:
                order["item_name"] = new_item_name
                order['quantity'] = new_order_quantity
                order["status"] = new_status
                writeOrdersInFile()
                messagebox.showinfo("Info", f"Order '{order_id}' updated successfully!")
            return
    
    messagebox.showerror("Error", f"Order '{order_id}' not found.")

def delete_order():
    global orders
    order_id = simpledialog.askstring("Input", "Enter order ID to delete:")
    
    for order in orders:
        if order["order_id"] == order_id:
            orders.remove(order)
            writeOrdersInFile()
            messagebox.showinfo("Info", f"Order '{order_id}' deleted successfully!")
            return
    
    messagebox.showerror("Error", f"Order '{order_id}' not found.")

def generate_report():
    global info

    categories = [details['category'] for details in info.values()]
    prices = [details['price'] for details in info.values()]
    amounts = [details['amount'] for details in info.values()]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Inventory Amount Distribution')

    plt.subplot(1, 2, 2)
    plt.bar(categories, prices)
    plt.title('Price by Category')
    plt.xlabel('Category')
    plt.ylabel('Price')

    plt.tight_layout()
    plt.show()

def open_inventory_window():
    inventory_window = ctk.CTkToplevel()
    inventory_window.title("Inventory Management")
    inventory_window.geometry("300x600")
    ctk.CTkButton(inventory_window, text="Add Item", command=add_item).pack(fill='x')
    ctk.CTkButton(inventory_window, text="Edit Item", command=edit_item).pack(fill='x')
    ctk.CTkButton(inventory_window, text="Remove Item", command=remove_item).pack(fill='x')
    ctk.CTkButton(inventory_window, text="Display Inventory", command=display_inventory).pack(fill='x')
    ctk.CTkButton(inventory_window, text="Display In Terminal", command=display_Terminal).pack(fill='x')
    ctk.CTkButton(inventory_window, text="Generate HTML", command=create_html_file).pack(fill='x')

def open_order_window():
    order_window = ctk.CTkToplevel()
    order_window.title("Order Management")
    order_window.geometry("300x400")
    ctk.CTkButton(order_window, text="Create Order", command=create_order).pack(fill='x')
    ctk.CTkButton(order_window, text="Update Order", command=update_order).pack(fill='x')
    ctk.CTkButton(order_window, text="Delete Order", command=delete_order).pack(fill='x')
    ctk.CTkButton(order_window, text="Generate Report", command=generate_report).pack(fill='x')

def main():
    readInFile()
    
    root = ctk.CTk()
    root.title("Inventory System")
    root.geometry("300x500") 
    
    ctk.CTkButton(root, text="Inventory", command=open_inventory_window).pack(fill='x')
    ctk.CTkButton(root, text="Order", command=open_order_window).pack(fill='x')
    
    root.mainloop()

if __name__ == "__main__":
    main()
