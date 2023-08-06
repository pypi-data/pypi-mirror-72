# CSI4930 Frontiersman

A clone of Settlers of CATAN (base game, 3-4 players local multiplayer)
The game rules are included in the directory

## README Requirements for class

Gitlab Link: [https://gitlab.com/csi4930-frontiersman/csi4930-frontiersman](https://gitlab.com/csi4930-frontiersman/csi4930-frontiersman)

Package Name on PyPI: Frontiersman

Executable Line to Run Server: py server.py 127.0.0.1 1233

Executable Line to Run Clients: py ClientMain.py 127.0.0.1 1233 Zander 2

Notes: 
>127.0.0.1 1233 is for the local host local IP, and the client's IP must match the server's  
>server.py args are host IP and port  
>ClientMain.py args are address, port, name, and the number of players  
>Run the client line for each player, so for two players:  
>>py server.py 127.0.0.1 1233  
>>py ClientMain.py 127.0.0.1 1233 Zander 2  
>>py ClientMain.py 127.0.0.1 1233 Bob 2  

