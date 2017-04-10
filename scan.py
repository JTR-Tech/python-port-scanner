import socket
import sys
from multiprocessing.dummy import Pool as ThreadPool

socket.setdefaulttimeout(0.001)
pool = ThreadPool(20)

def tryport(address):
    """tryport(address) uses the socket module to test a given IP, Port
       tuple for a successful connection, indicating that IP,port is open
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(s.connect_ex(address) == 0):
        return address
    s.close()

def scanport(port, subnet="192.168"):
    """scanport() calls tryport() on all possible addresses of the (default: 192.168)
       subnet in a multi-threaded implimentation to quickly detect if the port
       is up on a reachable local network.
    """
    try:
	port = int(port)
    except:
	print("port argument must be an interger")
	return
    addresses = []
    port_hosts = []
    for i in range(0, 255):
    	for k in range(1, 255):
    		addresses.append(('{0}.{1}.{2}'.format(subnet, i, k), port))
    result = pool.map(tryport, addresses)
    pool.close()
    pool.join()
    port_hosts = [x for x in result if not x is None]
    return port_hosts

if __name__ == '__main__':
    if(len(sys.argv) == 2):
	print(scanport(sys.argv[1]))
    elif(len(sys.argv) == 3):
	print(scanport(sys.argv[1], sys.argv[2]))
    else:
	print("port argument required")
