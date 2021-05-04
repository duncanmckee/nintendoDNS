# THis is the server code from lab 2
import socket
import sys
import tqdm
import os

def server_program():
    # get the hostname and print it
    host = socket.gethostname()
    print("Host name: " + str(host))
    buf = 1024
    if(len(sys.argv) != 2):
        print("Usage: python server.py <port_number>")
        sys.exit()

    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(2)

    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))

        #receive data
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print("from connected user: " + str(data))
	    str_arr = str(data).split()
	    command = str_arr[0].lower().strip()
	    filename = str_arr[1].lower().strip()
	    filesize = str_arr[2].lower().strip()
	    # remove absolute path if there is
	    filename = os.path.basename(filename)
	    temp_name ="/home/csse/CSSE432/Lab2/server/received_files"
	    completename = os.path.join(temp_name, filename)
	    # convert to integer
	    filesize = int(filesize)
	    file_byte_track = 0
	    if command == "utake":
		conn.sendall("Ready to take")
		#progress = tqdm.tqdm(range(filesize), "Receiving {filename}", unit="B", unit_scale=True, unit_divisor=buf)
		with open(completename, "wb") as f:
		    while file_byte_track < filesize:
		        # read 1024 bytes from the socket (receive)
			print("Before byteval")
			my_bytes = bytearray()
		        byte_val= conn.recv(buf)
			print("Here are the bytes", byte_val)
			my_bytes = bytearray(byte_val)
			file_byte_track += len(my_bytes)
		        # write to the file the bytes we just received
			print("writing")
		        f.write(byte_val)
		        # update the progress bar
		        #progress.update(len(bytes_read))
		print("Task completed " + filename + " taken")
	    elif command == "iwant":
		path = "/home/csse/CSSE432/Lab2/server/store/" + filename
		try:
		      filesize= os.path.getsize(path)
		except OSError:
		      print("Path '%s' does not exist or inaccessible" % path)
		      conn.sendall("end")
		      print("Make that file boss")
		      continue
   		print("Requested file size: ", filesize)
		send_str = filename + " " + str(filesize)
		conn.sendall(send_str)
		data = conn.recv(buf).decode()
		if data:
		      with open(path, "rb") as f:
			while True:
			    bytes_read = f.read(buf)
			    if not bytes_read:
				break
			    conn.sendall(bytearray(bytes_read))
	    else:
		print("Aight see ya")
		break
		# do fiel
            #data = str(data).upper()
        print("HEre is the end")
        conn.close()
	sys.exit()



if __name__ == '__main__':
    server_program()
