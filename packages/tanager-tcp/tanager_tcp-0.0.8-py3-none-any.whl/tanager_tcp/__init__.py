import socket
import sys
import time
from email.base64mime import header_length

global HEADER_LEN
HEADER_LEN=12
global ADDRESS_LEN
ADDRESS_LEN=25

class TanagerServer():
    def __init__(self, port): #Port is the port to listen on
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        hostname=socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Bind the socket to the port
        self.server_address = (ip_address, port)
        self.server_address = ('', port)
        self.sock.bind(self.server_address)
        self.queue=[]
        self.header_len=12 #needs to match client header len
        self.address_len=25 #needs to match client address len
        
        
    def listen(self):
        print('Listening on %s port %s.\n\n' % self.server_address)
        # Listen for incoming connections
        self.sock.listen(1)
        while True:
            # Wait for a connection
            connection, client_address = self.sock.accept()
            
            try:        
                # Receive the header telling the length of the message
                header=b''
                remaining_len=self.header_len-len(header)
                while remaining_len>0:
                    next_message=connection.recv(remaining_len)
                    header+=next_message
                    remaining_len=self.header_len-len(header)
                    if not next_message:
                        raise Exception('Message does not include full header.')
                
                # Receive the address where the remote computer will be listening for other messages  
                remote_server_address=b''
                remaining_len=self.address_len-len(remote_server_address)
                while remaining_len>0:
                    next_message=connection.recv(remaining_len)
                    remote_server_address+=next_message
                    remaining_len=self.address_len-len(remote_server_address)
                    if not next_message:
                        raise Exception('Message does not include full address of remote computer.')
                    
                decoded_remote_server_address=remote_server_address.decode('utf-8').split('&')
                self.remote_server_address=(decoded_remote_server_address[0], int(decoded_remote_server_address[1]))
                
                #Receive the actual message
                message=b''
                while len(message)<int(header):
                    data = connection.recv(1024)
                    message+=data
                    if not data:
                        raise Exception('Message shorter than expected')
                    
                self.queue.append(str(message, 'utf-8'))
                
                #Send a return message containing the header and address info
                connection.sendall(header+remote_server_address)
            
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
            next_message=self.sock.recv(self.header_len+self.address_info_len)
            self.return_message=b''
            while next_message:
                self.return_message+=next_message
                next_message=self.sock.recv(self.header_len+self.address_info_len) #If all is as expected, should be b''. If full message didn't make it through in first sock.recv could have content.
                if len(self.return_message)>self.header_len+self.address_info_len:
                    raise Exception('Return message longer than expected.')

            #Check that the remote server received the correct message length                
            if str(self.return_message[0:self.header_len])!=header:
                print(self.return_message)
                raise Exception('Message length different than expected.')
            
            #Check that the remote server received the address to listen on
            if str(self.return_message)[self.header_len:]!=address_info:
                print(self.return_message)
                raise Exception('Wrong address returned.')
            
            print('Return message: '+str(self.return_message))
                

        except ConnectionResetError: #Happens when one computer is restarted.
            print('Connection reset.')
            self.__init__(server_address, base_message, listening_port, timeout)   
            
        finally:
            self.sock.close()