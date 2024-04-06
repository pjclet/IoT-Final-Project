# user-facing RPi used to communicate with the server
#   encrypt the message using the symmetric key
#   wait for server response (add timeout here)
#   decrypt server response using symmetric key, if correct:
#       open the door, change the symmetric key

"""
Steps (after a scan and a password input):
- Client sends an encrypted message containing "user:input_password" 
- Server verifies the encrypted message using a symmetric key (symmetric key changes with the counter)
- If correct, server will send appropriate response and increment counter/change symmetric key
- Client will then unlock the door and increment counter/change symmetric key

The counter will prevent any relayed attacks because if an attack is relayed, nothing will happen since the symmetric key has already changed.
"""

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from security import encrypt, decrypt, change_key
import socket

if __name__ == "__main__":

    # load the key
    count = 1
    with open('key.txt', 'r') as file:
        key = str(file.read().replace('\n', ''))

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SERVER_HOST, SERVER_PORT = "129.161.117.229", 1024

    # Connect to server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    # create the card reader object
    reader = SimpleMFRC522()

    while True:

        # # Close client socket
        # client_socket.close()

        # once a scan happens:
        try:
            id, text = reader.read()
            print("ID:",id)
            print()
            print("Text:", text)

            # now wait for password input HERE 
            # -----
            # *****
            password_input = "4321" # temp password

            # ------ 

            # once we have the password input, we put it in the message form: "<rfid tag username>:<keypad password>"
            message = "{}:{}".format(text.strip(), password_input).rstrip(":").strip()

            # encrypt using symmetric key
            encrypted_message = encrypt(message)

            # send the message to the server
            # Send message to server
            client_socket.sendall(encrypted_message.encode())

            # Receive response from server
            try:
                data = client_socket.recv(1024)
                print('Received from server:', data.decode())
                message_received = data.decode()
                decrypted_message = decrypt(message_received, key).rstrip(":").strip()
                print("Decrupted message:{}|".format(decrypted_message))

                if (decrypted_message == "V3r1f13D-" + message + "!"):
                    print("[SUCCESS] Received valid authentication!")
                    key, count = change_key(key, count)
                else:
                    print(message)
                    print("[ERROR] Failed to validate the user.")
            except:
                print("[ERROR] No data received from the server.")
            
        # # after the scan
        finally:
            print("scanned")
            # GPIO.cleanup()
