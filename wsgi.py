from portal import app

if __name__ == '__main__':
    #app.run() #descomentar cuando el comando : uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app
    app.run('0.0.0.0', 8080, debug=True) #comentar cuando el comando : uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app