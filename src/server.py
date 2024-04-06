# remote server that the client will communicate to by MQTT (or UDP/TCP)
"""
Steps (after a scan and a password input):
- Client sends an encrypted message containing "user:input_password" 
- Server verifies the encrypted message using a symmetric key (symmetric key changes with the counter)
- If correct, server will send appropriate response and increment counter/change symmetric key
- Client will then unlock the door and increment counter/change symmetric key

The counter will prevent any relayed attacks because if an attack is relayed, nothing will happen since the symmetric key has already changed.
"""

# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
import socket
from security import encrypt, decrypt, change_key
import time 



if __name__ == "__main__":

    # load the key
    count = 1
    with open('key.txt', 'r') as file:
        key = str(file.read().replace('\n', ''))

    # load the credentials as a text file
    with open('stored_credentials.txt', 'r') as f:
        entries = [entry.strip() for entry in f.readlines()]

    # connect over tcp
    HOST = '0.0.0.0'  # localhost
    PORT = 1024        # port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.close()

    time.sleep(0.5)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print('Server is listening for connections...')
    client_socket, client_address = server_socket.accept()
    print('Connected to:', client_address)

    while True:
        # wait for data *****
        data = client_socket.recv(1024)
        print('Received from client:', data.decode())
        message_received = data.decode()

        # decrypt the message using the symmetric key, if correct:
        # send the encrypted server response
        
        decrypted_message = decrypt(message_received, key).rstrip(":").strip()
        print("Decrypted message:{}|".format(decrypted_message))
        print(entries)

        if (decrypted_message in entries):
            print("Authenticated user:", message_received.split(":")[0])
            response = encrypt(str("V3r1f13D-" + decrypted_message + "!"), key)
            client_socket.sendall(response.encode())
            # change the symmetric key
            key, count = change_key(key, count)
        else:
            print("Failed to authenticate user:", message_received.split(":")[0])
            response = encrypt(str("Unable to authenticate" + message_received + "!"), key)
            client_socket.sendall(response.encode())



        # # Close client socket
        # client_socket.close()

        # # Close server socket
        # server_socket.close()
        
        # print(entries)

        # continuously check:
        #   once a message is received:
        #       decrypt the message using the symmetric key, if correct:
        #           send the encrypted server response
        #           change the symmetric key

