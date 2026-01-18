import socket
import tkinter as tk
from tkinter import messagebox

SERVER_IP = '192.168.X.X' # Place your server IP here
SERVER_PORT = 6000

class WaiterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Waiter Pad")
        self.root.geometry("400x600")
        self.root.configure(bg="#8D6E63")

        tk.Label(root, text="RESTAURANT ORDER", font=("Impact", 20), bg="#8D6E63", fg="white").pack(pady=20)

        # Table Number
        tk.Label(root, text="Table Number:", bg="#8D6E63", fg="white").pack(pady=5)
        self.ent_table = tk.Entry(root, font=("Arial", 14), justify='center')
        self.ent_table.pack(padx=50, fill=tk.X)

        # Order Items
        tk.Label(root, text="Items (comma separated):", bg="#8D6E63", fg="white").pack(pady=5)
        self.ent_items = tk.Entry(root, font=("Arial", 14))
        self.ent_items.pack(padx=20, fill=tk.X)
        
        self.btn_frame = tk.Frame(root, bg="#8D6E63")
        self.btn_frame.pack(pady=10)
        
        # Send Button
        self.btn_send = tk.Button(root, text="SEND TO KITCHEN", command=self.send_order, 
                                  bg="#FF5722", fg="white", font=("Arial", 12, "bold"), height=2)
        self.btn_send.pack(pady=20, padx=20, fill=tk.X)
        
        # Check Kitchen Status
        self.btn_check = tk.Button(root, text="View Active Orders", command=self.check_kitchen, bg="#FFCCBC")
        self.btn_check.pack(pady=10)

        #Mark Order as Done 
        tk.Label(root, text="--- Update Status ---", bg="#8D6E63", fg="#D7CCC8").pack(pady=(20, 5))
        
        self.frame_update = tk.Frame(root, bg="#8D6E63")
        self.frame_update.pack(pady=5)
        
        tk.Label(self.frame_update, text="Order ID:", bg="#8D6E63", fg="white").pack(side=tk.LEFT)
        self.ent_id = tk.Entry(self.frame_update, width=5, font=("Arial", 14), justify='center')
        self.ent_id.pack(side=tk.LEFT, padx=10)
        
        self.btn_done = tk.Button(self.frame_update, text="MARK SERVED", command=self.mark_served, 
                                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_done.pack(side=tk.LEFT)

    def mark_served(self):
        order_id = self.ent_id.get()
        if not order_id:
            messagebox.showwarning("Error", "Enter Order ID")
            return
            
        # ORDER_DONE | ID
        response = self.connect_and_send(f"ORDER_DONE|{order_id}")
        messagebox.showinfo("Status Update", response)
        self.ent_id.delete(0, tk.END)

    def connect_and_send(self, msg):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((SERVER_IP, SERVER_PORT))
            client.send(msg.encode('utf-8'))
            response = client.recv(4096).decode('utf-8')
            client.close()
            return response
        except Exception as e:
            return f"Conn Error: {e}"

    def send_order(self):
        tbl = self.ent_table.get()
        items = self.ent_items.get()
        
        if not tbl or not items:
            messagebox.showwarning("Error", "Table and Items required")
            return
            
        # NEW_ORDER | Table | Items
        payload = f"NEW_ORDER|{tbl}|{items}"
        response = self.connect_and_send(payload)
        
        if "Conn Error" in response:
            messagebox.showerror("Failed", "Kitchen is Offline")
        else:
            messagebox.showinfo("Success", response)
            self.ent_items.delete(0, tk.END)

    def check_kitchen(self):
        resp = self.connect_and_send("CHECK_STATUS|")
        messagebox.showinfo("Kitchen Display", resp)

if __name__ == "__main__":
    root = tk.Tk()
    app = WaiterApp(root)
    root.mainloop()