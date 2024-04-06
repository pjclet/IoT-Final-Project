# encryption and decryption functions

"""
Notes:
- Use MD5 or SHA-1 like algorithm, or take features from RSA using prime numbers as authenticators
- Need QoS of 1 or 2 to guarantee the message for the algorithm
"""

# encrypt a message to send
def encrypt(msg, key):

    msg_nums = [str(ord(char)) for char in msg]
    # print(msg_nums)
    msg_encr = []
    for num in msg_nums:
        temp = ""
        for char in num:
            temp = temp + key[int(char)]
        msg_encr.append(temp)
    # msg_encr = [key[int(char)] for char in msg_nums]
    final_msg = "/".join(msg_encr)
    
    # print(final_msg)
    return final_msg

# decrypt a received message
def decrypt(msg, key):
    # print(type(key.index(str(1))))
    msg_encry = msg.split("/")
    msg_dec = []
    for num in msg_encry:
        temp = ""
        for char in num:
            temp = temp + str(key.index(str(char)))
        msg_dec.append(temp)
    # print(msg_dec)
    msg_chars = [str(chr(int(char))) for char in msg_dec]

    # print(msg_chars)
    final_msg = "".join(msg_chars)
    return final_msg

# a successful key has been sent/received, we can change the key now
def change_key(key, count):

    # temp = key
    for i in range((count * 3) % 7):
        index1, index2 = count % 10, ((count * 7) + 17) % 10
        # print(index1, index2)

        char_list = list(key)
        
        char_list[index1], char_list[index2] = char_list[index2], char_list[index1]
        
        key = ''.join(char_list)
        count += 1
    # print(key)

    return key, count



# test the encryption and decryption
if __name__ == "__main__":
    
    count = 1
    with open('key.txt', 'r') as file:
        key = str(file.read().replace('\n', ''))

    m = "username:4321"
    print("Original Message: {}".format(m))
    encrypted_m = encrypt(m, key)
    print("Encrypted Message: {}".format(encrypted_m))
    decrypted_m = decrypt(encrypted_m, key)
    print("Decrypted Message: {}".format(decrypted_m))
    print()

    key, count = change_key(key, count)

    m = "user2:9989"
    print("Original Message: {}".format(m))
    encrypted_m = encrypt(m, key)
    print("Encrypted Message: {}".format(encrypted_m))
    decrypted_m = decrypt(encrypted_m, key)
    print("Decrypted Message: {}".format(decrypted_m))
    print()


    key, count = change_key(key, count)

    m = "username_number_3:6789"
    print("Original Message: {}".format(m))
    encrypted_m = encrypt(m, key)
    print("Encrypted Message: {}".format(encrypted_m))
    decrypted_m = decrypt(encrypted_m, key)
    print("Decrypted Message: {}".format(decrypted_m))
    print()
    