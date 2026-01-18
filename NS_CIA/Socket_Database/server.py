import socket
import threading
import database

HOST = '0.0.0.0'
PORT = 6000

def handle_waiter(client_socket, addr):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message: break

            print(f"[{addr}] Incoming: {message}")
            
            response = "Error"
            
            if "|" in message:
                parts = message.split("|")
                command = parts[0]

                if command == "NEW_ORDER":
                    _, table, food = parts
                    confirmation = database.save_order(table, food)
                    print(f"!!! NEW ORDER: Table {table} - {food}")
                    response = confirmation
                
                elif command == "CHECK_STATUS":
                    response = database.get_kitchen_view()

                # Order completed
                elif command == "ORDER_DONE":
                    #ORDER_DONE|Order_ID
                    order_id = parts[1]
                    response = database.mark_order_done(order_id)
                    print(f"Order #{order_id} Completed.")
            
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_kitchen():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("--- KITCHEN SERVER READY ---")
    print(f"Listening on Port {PORT}")
    
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_waiter, args=(client, addr)).start()

if __name__ == "__main__":
    start_kitchen()