import socket

def get_server_stats(ip,port,request):
    try:
        dongle = ip, port
        BUFFER_SIZE = 10000
        request = request.encode('utf-8')
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(dongle)
        conn.send(request)
        data = conn.recv(BUFFER_SIZE)
        conn.close()
        return(data.decode('utf-8'))
    except:
        return('Error')
