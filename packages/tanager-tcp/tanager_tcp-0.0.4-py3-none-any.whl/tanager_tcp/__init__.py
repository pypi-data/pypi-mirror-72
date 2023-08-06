import socket
import sys
import time

class TanagerServer():
    def __init__(self, port): #Port is the port to listen on
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        hostname=socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Bind the socket to the port
        self.server_address = (ip_address, port)
        self.server_address = ('', port)
        print('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)
        self.queue=[]
        self.header_len=12
        
        
    def listen(self):
        print('TCP server listening.\n\n')
        # Listen for incoming connections
        self.sock.listen(1)
        while True:
            # Wait for a connection
            connection, client_address = self.sock.accept()
            
            try:        
                # Receive the data in small chunks and retransmit it
                next_message=b''
                header=connection.recv(self.header_len)
                remote_server_address=connection.recv(25)
                remote_server_address=remote_server_address.decode('utf-8').split('&')
                self.remote_server_address=(remote_server_address[0], int(remote_server_address[1]))
                
                while len(next_message)<int(header):
                    data = connection.recv(16)
                    next_message+=data
                    if not data:
                        raise Exception('Message shorter than expected')
                        break
                self.queue.append(str(next_message, 'utf-8'))
                connection.sendall(next_message)
            
            except ConnectionResetError: #Happens on restart of other computer
                self.listen()
                    
            finally:
                # Clean up the connection
                connection.close()
                
class TanagerClient():
    def __init__(self, server_address, base_message, listening_port, timeout=None): #Server address is where you will send your message, listening port is the port you have a server listening for additional messages on.
        self.header_len=12 #Length of message, not including header or address info
        self.address_info_len=25 #Number of digits in the address including IP address and port info.
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if timeout!=None:
            self.sock.settimeout(timeout)
            
        #base message may be passed as string or bytes-like object
        if isinstance(base_message, (bytes, bytearray)):
            print('Message passed as bytes')
            base_message=base_message.decode('utf-8')
        
        #Make sure the header is the right length
        header=str(len(base_message))
        while len(header)<self.header_len:
            header='0'+header
            
        #Get address info to send with message
        hostname=socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        address_info=ip_address+'&'+str(listening_port)
        while len(address_info)<self.address_info_len:
            address_info+='&'
        
        #Concatenate various parts of the message and convert to bytes
        full_message=header+address_info+base_message
        full_message=full_message.encode('utf-8')
        
        # Connect the socket to the port where the server is listening
        self.server_address = server_address
        self.sock.connect(self.server_address)
        
        try: 
            # Send data
            self.sock.sendall(full_message)
        
            # Look for the response
            amount_received = 0
            amount_expected = len(base_message)
            
            self.return_message=''
            while amount_received < amount_expected:
                data = self.sock.recv(10)
                self.return_message+=str(data)
                amount_received += len(data)
                if not data:
                    print(self.return_message)
                    raise Exception('Message shorter than expected')

        except ConnectionResetError: #Happens when one computer is restarted.
            print('CONNECTION RESET')
            self.__init__(server_address, base_message, listening_port, timeout)   
            
        finally:
            self.sock.close()