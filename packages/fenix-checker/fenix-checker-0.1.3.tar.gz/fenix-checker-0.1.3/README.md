# [![Fenix](https://fe.nix.cz/images/logo_fenix.png)](https://fe.nix.cz/) `fenix-checker`

A small server which checks if user's IP is in a trusted [Fenix](https://fe.nix.cz/) network. Used by [`ipv6widget`](https://gitlab.labs.nic.cz/labs/ipv6widget) and [standard-konektivity.cz](https://www.standardkonektivity.cz/).

## Dependencies

- Python >= 3.6
- pyaml >= 17
- psycopg2 >= 2.7.4

## Installation

```
$ virtualenv -p `which python3.6` .venv
$ source .venv/bin/activate
$ pip install fenix_checker
$ cp config.example.yml config.yml
$ $EDITOR config.yml # set DB credentials
```

### Running in production

uWSGI:

```
$ uwsgi --master --single-interpreter --threads 2 --http :5000 -H .venv -w fenix_checker.server
```

GUnicorn:

```
$ gunicorn -w 2 -k gevent --timeout 160 -n netmetr-proxy fenix_checker:server:app
```

## Usage

```
GET /
-> 200
   {"result": 1}
```

Result is:

- `0` for non-Fenix networks
- `>= 1` for Fenix networks

IP is validated with Python's [`ipaddress`](https://docs.python.org/3/library/ipaddress.html) module before passing it to DB:

```
GET /  # with client IP somehow spoofed to eg. "127.0.0.1'); DROP TABLE networks;"
-> 400
  {"error": "Invalid IP"}
```

## Development

Starting server with auto reload on file changes:

```
$ FLASK_APP=fenix_checker/server.py FLASK_DEBUG=1 flask run
```

Linting Python code:

```
$ flake8 --config=.flake8rc *py
```

## License

GPLv3
