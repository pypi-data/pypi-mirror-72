import random
import socket
import time
import sys

from frontiersman.client import ClientHelper


class client:
    def __init__(self, name, address, socket, color):
        self.name = name
        self.address = address
        self.socket = socket
        self.color = color


class server:
    def __init__(self, host, port):

        sep = '\n'

        def dice_roll():
            return (str(random.randint(1, 6)) + ',' + str(random.randint(1, 6)))

        def readfromBuffer(sock):
            totalMessage = ""
            while sep not in totalMessage:
                totalMessage += sock.recv(1).decode('utf-8')
            return totalMessage[:-1]

        clients = []
        Colors = ['red', 'cyan', 'orange', 'blue', 'green', 'pink', 'yellow']
        random.shuffle(Colors)
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        def sendToAll(message):
            for cli in clients:
                cli.socket.send(str.encode(message + "\n"))

        def sendToAllButOne(message, cli2):
            for cli in clients:
                if (cli != cli2):
                    cli.socket.send(str.encode(message + "\n"))

        print('Waitiing for a Connection..')
        ServerSocket.listen(5)

        Client, address = ServerSocket.accept()
        res = readfromBuffer(Client)
        name = res
        print(name)
        Client.send(str.encode("host\n"))
        clients.append(client(name, address, Client, Colors[0]))
        Colors.pop(0)
        numplayers = readfromBuffer(Client)
        print(int(numplayers))
        for x in range(int(numplayers) - 1):
            Client, address = ServerSocket.accept()
            res = readfromBuffer(Client)
            name = res
            print(name)
            # for cli in clients:
            #    i =0
            #    cli.socket.send(str.encode(name+" connected\n"))
            clients.append(client(name, address, Client, Colors[0]))
            Colors.pop(0)
        for cli in clients:
            sendToAllButOne("enemy," + cli.name + "," + cli.color, cli)
        for i in range(0, len(clients)):
            sendstring = "color,"
            sendstring = sendstring + clients[i].color+','+str(i) + '\n'
            clients[i].socket.send(str.encode(sendstring))
        # board randomizer
        resource_list = ['Wheat'] * 4 + \
                        ['Sheep'] * 4 + \
                        ['Ore'] * 3 + \
                        ['Brick'] * 3 + \
                        ['Wood'] * 4 + \
                        ['Desert'] * 1
        number_list = [2, 12]
        for index in range(3, 12):
            if index == 7:
                pass
            else:
                number_list.append(index)
                number_list.append(index)
        port_list = ['Wheat'] + \
                    ['Sheep'] + \
                    ['Ore'] + \
                    ['Brick'] + \
                    ['Wood'] + \
                    ['None'] * 4
        developmentDeck = ['knight'] * 15 + \
                          ['roadBuilding'] * 2 + \
                          ['yearOfPlenty'] * 2 + \
                          ['monopoly'] * 2 + \
                          ['victoryPoint'] * 5
        random.shuffle(developmentDeck)
        random.shuffle(number_list)
        random.shuffle(resource_list)
        random.shuffle(port_list)
        numberstring = 'board|' + ','.join([str(elem) for elem in number_list]) + '|' + ','.join(
            resource_list) + '|' + ','.join(port_list)
        sendToAll(numberstring)
        for cli in clients:
            cli.socket.send(str.encode("startgui\n"))
            readfromBuffer(cli.socket)
        winner = False
        # setup
        random.shuffle(clients)
        for cli in clients:
            cli.socket.send(str.encode("set\n"))
            coordinates = readfromBuffer(cli.socket)
            sendToAllButOne("set," + coordinates + "," + cli.color, cli)
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)
            cli.socket.send(str.encode('startroad\n'))
            coordinates = readfromBuffer(cli.socket)
            sendToAllButOne("road," + coordinates + "," + cli.color, cli)
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)
        for cli in reversed(clients):
            cli.socket.send(str.encode("set\n"))
            coordinates = readfromBuffer(cli.socket)
            sendToAllButOne("set," + coordinates + "," + cli.color, cli)
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)
            cli.socket.send(str.encode('startroad\n'))
            coordinates = readfromBuffer(cli.socket)
            sendToAllButOne("road," + coordinates + "," + cli.color, cli)
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)
        for cli in clients:
            cli.socket.send(str.encode('getstart\n'))
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)
            message = readfromBuffer(cli.socket)
            sendToAllButOne(message, cli)

        while (not winner):
            for cli in clients:
                dice = dice_roll()
                sendToAll('dice,' + dice)
                for cli2 in clients:
                    message = readfromBuffer(cli2.socket)
                    sendToAllButOne(message, cli2)
                    message = readfromBuffer(cli2.socket)
                    sendToAllButOne(message, cli2)
                if (int(dice.split(',')[0]) + int(dice.split(',')[1]) == 7):
                    cli.socket.send(str.encode('robber\n'))
                else:
                    cli.socket.send(str.encode('turn\n'))
                while True:
                    message = readfromBuffer(cli.socket)
                    #print(message)
                    if (message == "end"):
                        break
                    if (message.split(',')[0] == "winner"):
                        #print(message)
                        break
                    elif (message == "dev"):
                        card = developmentDeck.pop(0)
                        cli.socket.send(str.encode(card + '\n'))
                    else:
                        sendToAllButOne(message, cli)
                cli.socket.send(str.encode('notturn\n'))
                # message=readfromBuffer(cli.socket)
                # print(message)
                # sendToAllButOne(message, cli)

        time.sleep(10)
        # game loop

        for cli in clients:
            cli.socket.send(str.encode("quit\n"))
        ServerSocket.close()

def main():
    address='127.0.0.1'
    port=1233
    if(len(sys.argv)==3):
        address=sys.argv[1]
        try:
            port=sys.argv[2]
        except ValueError:
            print("invalid port")
        else:
            server(address, int(port))
    else:
        print("please put the address and port of the server")
    


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 1233
    test = server(host, port)
#     host = sys.argv[1]
#     port = int(sys.argv[2])
#     test = server(host, port)
