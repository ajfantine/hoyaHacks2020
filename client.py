# Import socket module 
import socket 
  
  
def Main(): 
    host = '10.150.242.200'
  
    # Define the port on which you want to connect 
    port = 5056
  
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    # connect to server on local computer 
    server_socket.connect((host, port))

  
    while True: 
  
        message = str(['chicken', 'pork', 'steak', 'cream cheese','bacon', 'eggs', 'olive oil', 'cheddar cheese', 'salt', 'pepper', 'milk', 'butter', 'green onions', 'spinach', 'pimento', 'dough', 'tomatoes'])
        # message sent to server 
        server_socket.send(message.encode('ascii', 'ignore'))
        print("Searching for recipes...")
  
        # messaga received from server 
        data = server_socket.recv(8192)
        
        recipes_str = str(data.decode('ascii'))
        recipes = eval(recipes_str)
  
        print(recipes)
  
        # ask the client whether he wants to continue 
        ans = input('\nDo you want to continue(y/n) :') 
        if ans == 'y': 
            continue
        else: 
            break
    # close the connection 
    server_socket.close()
  
if __name__ == '__main__': 
    Main()
