from os import system
import ngrok, struct, socket, json, time
import asyncio, clipboard

ip = None

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def check_connection(host, port):
    try:
        socket.socket().connect((host, port))
        return True
    except:
        return False

def search_server():
    multicast_group = '224.0.2.60'
    server_address = ('', 4445)

    sock = create_socket()
    sock.bind(server_address)

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def find(a, string):
        string = string.split(f"[{a}]")[1]
        string = string.split(f"[/{a}]")[0]
        return string

    while True:
        data, address = sock.recvfrom(1024)
        data = data.decode("utf-8")
        return f"{address[0]}:{find('AD', data)}"

def setup_ngrok_connection(apiKey):
    global ip
    ip = search_server()
    ngrok.set_auth_token(apiKey)
    ngrok_listener = ngrok.forward(ip, 'tcp')
    return ngrok_listener
            
async def main():
    global ip
    with open('settings.json') as f:
        data = json.load(f)

    print('+----------------------------+')
    print('|IP| |Loading...             |')
    print('+----------------------------+')

    ngrok_listener = await setup_ngrok_connection(data['API-KEY'])
    url = ngrok_listener.url().replace("tcp://", "")
    if data['auto-copy']: clipboard.copy(url)

    print('+----------------------------+')
    print('|IP| |' + url + '|')
    print('+----------------------------+')
    
    working = True
    while working:
        working = check_connection(ip.split(":")[0], int(ip.split(":")[1]))
        await asyncio.sleep(1)

    ngrok_listener.close()
    if data['auto-restart']:
        asyncio.run(await main())
    else:
        exit()
    
if __name__ == "__main__":
    system('mode 30,4')
    system('cls')
    asyncio.run(main())