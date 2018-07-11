OVERVEW
-------

The project is running ok. Video theme is case sensitive.
Mongo uri is the default(host: localhost, port: 27017),
If you want, you can change it updating development.ini file replacing
mongo_uri attribute.


Getting Started
---------------

- Clone project

    git clone https://github.com/anderson89marques/deepersystem.git

- Change directory into your newly created project.

    cd deepersystem

- Create a Python virtual environment.

   Ex:  python3 -m venv env

- Activate your virtual enviroment

   Ex: source env/bin/activate

- Upgrade packaging tools.

    pip install --upgrade pip setuptools

- Install the project.

    pip install -e .

- Run your project.

    pserve development.ini