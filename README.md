# Game King

> Hub for Web Page Based Social Games

> Modification from [codenames](https://github.com/joshporter1/codenames).

## Tech Stack
#### Front End
* Vue
* Vuex
* Vuetify
* Webpack

#### Back End
* Flask + Socketio

## Development

The app uses flask as its back-end and webpack as a front-end dev server.

### Prerequesites

* npm
* python
* pip
* _(optional)_ Gunicorn
* _(optional)_ nginx
* _(optional)_ Foreman (development only)

### Install Dependencies
```bash
# create a virtualenv
virtualenv venv
source venv/bin/activate

# install python and js dependencies
npm run setup

# install dependencies separately
pip install -r requirements.txt
npm install
# or
yarn install
```

### Development Servers

I recommend using Foreman. Foreman allows us to run both servers simultaneously in one terminal window.

```bash
# install foreman
npm i -g foreman
# start foreman
nf start
# both flask and webpack-dev-server should be running

# run servers separately...
# start the flask server on port 5000
npm run flask

# start webpack dev server with hot reload at localhost:8080
npm run serve
# navigate to localhost:8080 in browser
```

## Production

### Build

``` bash
# install dependencies
npm install
pip install -r requirements.txt

# or install both at once
npm run setup

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

#### Running with nginx + Gunicorn

After installing Gunicorn and nginx...

* Add your username and/or project folder path to the configs in the `deploy` directory.
* Copy `deploy/gunicorn.service` to `/etc/systemd/system`
* Copy `deploy/codenames.nginx.conf` to `/etc/nginx/sites-available`
* Create a symbolic link from the new config to `sites-enabled`
