from os import system
import ngrok, struct, socket, json

def search_server():
    multicast_group = '224.0.2.60'
    server_address = ('', 4445)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    ngrok.set_auth_token(apiKey)
    ngrok_listener = ngrok.forward(search_server(), 'tcp')
    return ngrok_listener

def main():
    with open('settings.json') as f:
        data = json.load(f)

    ngrok_listener = setup_ngrok_connection(data['API-KEY'])
    url = ngrok_listener.url().replace("tcp://", "")

    print('+' + '-' * 28 + '+')
    print('|IP| |' + url + '|')
    print('+' +'-' * 28 + '+')

    while True:
        pass
    
if __name__ == "__main__":
    # system('mode 30,4')
    main()