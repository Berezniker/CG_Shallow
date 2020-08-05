# Shallow Water

inspired by [Evan](http://madebyevan.com/webgl-water/) ([git](https://github.com/evanw/webgl-water))  
guide: [learnopengl.com](learnopengl.com) ([RU](https://habr.com/ru/post/310790/))

<img src="https://github.com/Berezniker/CG_Shallow/blob/master/pool.png">

### Load:
```sh
$ git clone https://github.com/Berezniker/CG_Shallow.git
$ cd CG_Shallow
```

### Activation of virtual environment:
```sh
$ source venv/bin/activate
```
or you can install the libraries yourself:
```sh
$ pip3 install --upgrade -r requirements.txt
```
deactivate virtual environment:
```sh
$ deactivate
```

### Run:
```sh
$ python3 main.py
```

### Control:
  - W/A/S/D -- camera movement
  - mouse -- camera rotation
  - scrool -- zoom
  - Q -- on/off wireframe water visualization
  - E -- add random drop
  - R -- on/off rain
  - B -- on/off skybox
  - F1, F2, F3 -- change camera position
  - F5 -- stop simulation
