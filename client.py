# This is the client from lab 2
import socket
import sys
import tqdm
import os

def client_program():
    if(len(sys.argv) != 3):
        print("Usage: python client.py <server_(IP)_address> <server_port_number>")
        sys.exit()
    SEPARATOR = "<SEPARATOR>"
    buf = 1024
    port = int(sys.argv[2])
    server_addr = (sys.argv[1], port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_addr)

    message = raw_input(" -> ")
    while message.lower().strip() != ';;;':
        str_arr = message.split()
        if len(str_arr) < 2:
             print("The command is incorrect")
             print("Re-enter the command")
             message = raw_input(" -> ") # iwant ldfja;lsdkjfa
             continue
	filename = str_arr[1]
        if str_arr[0] == "iwant":
	    print("Please specify the desired directory:")
	    partial_path = raw_input(" -> ")
	    if partial_path.strip() == "default":
	       completename = "/home/csse/CSSE432/Lab2/client/received_files/"+ filename
	    else:
 	       completename = partial_path +"/" + filename
            send_str = "iwant"+ " " + filename+ " "+ "0"
	    client_socket.sendall(send_str)
	    handshake = client_socket.recv(buf).decode()
	    print(handshake)
	    if str(handshake) == "end":
		print("Server aint got no file, Willis!:", filename)
		message = raw_input(" -> ")
		continue
	    temp = handshake.split()
	    filesize = int(temp[1])
	    file_byte_track = 0
	    client_socket.sendall("Ready")
	    try:
	    	with open(completename,"wb") as f:
		   while file_byte_track < filesize:
		       byte_val = client_socket.recv(buf)
		       file_byte_track+=len(bytearray(byte_val)) # I want apples
		       f.write(byte_val)
	    except Exception:
		print("Willis... that aint no directory!")
		client_socket.close()
		break
        elif str_arr[0] == "utake":
         # need to check if file is here
	    path= "/home/csse/CSSE432/Lab2/client/store/" + filename

	    try:
                filesize = os.path.getsize(path)

            except OSError:
                print("Path '%s' does not exist or inaccessible" % path)
                message = raw_input(" -> ")
		continue

            print("The file size in bytes is:", filesize)
            #sendf file
	    send_str =  "utake" + " " + filename + " " + str(filesize)
	    print(send_str)
            client_socket.sendall(send_str)
	    data = client_socket.recv(buf).decode()
	    if data:
	            #progress = tqdm.tqdm(range(filesize), "Sending {filename}", unit="B", unit_scale=True, unit_divisor=buf)
	            with open(path, "rb") as f:
	              while True:
	                  # read the bytes from the file
	                  bytes_read = f.read(buf)
	                  if not bytes_read:
	                    # file transmitting is done
	                      break
	                  # we use sendall to assure transimission in
	                  # busy networks sending binary data pymotw
			  # bytearray() to change data binary
	                  client_socket.sendall(bytearray(bytes_read))
	                  # update the progress bar
	                  #progress.update(len(bytes_read))

        elif str_arr[0] == "close":
	    print("HERE PLS")
	    client_socket.sendall("close x 0")
	else:
	    print("Incorrect Command")
	    message = raw_input(" -> ")

        message = raw_input(" -> ")

    client_socket.close()


if __name__ == '__main__':
    client_program()

