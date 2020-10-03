# Online Tank Game

Online Tank Game is a game where players can connect to the same server and play AZ-Tanks against each other.

![image](https://user-images.githubusercontent.com/54172854/94990644-ff776e00-057d-11eb-9720-1fcc471160c3.png)

## Installation

This project requires ```pygame```. To install run:\
```$ pip install pygame```


### Play Locally
To play 1v1 on one machine just run the file ```client.py```.\
```$ python3 client.py```\
\
Player one moves with ```WASD``` and fires with ```SPACE```.\
Player two moves with ```arrow keys``` and fires with ```M```.

### Play Online
#### Host:
Spin up a server by running ```server.py``` from the host machine:\
```$ python3 server.py```.
#### Join:
Run ```client.py``` from any machine with internet access to connect:\
```$ python3 client.py```.\
\
You move your tank with ```WASD``` and fire with ```SPACE```.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
Developed by Kasper Skov Hansen\
kasper@skovhansen.net

## License
[MIT](https://choosealicense.com/licenses/mit/)