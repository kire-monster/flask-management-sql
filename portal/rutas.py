
from portal import app
from flask import render_template, session, request, json, redirect, url_for
from ms import mssql
import re



@app.route('/')
def Index():
    error = ''
    dblit = []
    
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    try:
        
        con = mssql.SqlConnection(session['driver'],session['host'], session['usuario'], session['contrasenia'], '')
        con.open()
        if con.StatusError:
            error = str(err)
        
        con.cursor.execute("SELECT [name] FROM [sys].[databases]")
        dblit = [list(i) for i in con.cursor.fetchall()]
        con.close()
            
    except Exception as err:
        error = str(err)

    return render_template('home.html', error=error, database=dblit)

@app.route('/help')
def help_html():
    return render_template('help.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',mensaje_error='')

    elif request.method == 'POST':

        host = request.form['host']
        usuario = request.form['usr']
        driver = request.form['driver']
        contrasenia = request.form['pwd']
        
                
        try:
            con = mssql.SqlConnection(driver,host, usuario, contrasenia, '')
            con.open()
            if con.StatusError:
                return render_template('login.html',mensaje_error=con.MessageError)
            else:
                session['host']=host
                session['usuario']=usuario
                session['contrasenia']=contrasenia
                session['driver']=driver
                con.close()
                return redirect(url_for('Index'))
        except Exception as err:
            return render_template('login.html',mensaje_error=str(err))

        #return "host: %s - usuario: %s - contraseña: %s - driver: %s " % (host , usuario , contrasenia , host)
    else:
        return 'Metodo no valido'
    




@app.route('/sql', methods=['POST'])
def sql_func():
    
    response_json={'Status': False,'Mensaje': '', 'Columns':[], 'Resultado': [], 'Query': '' }

    try:
        CONTROLADOR=session['driver']
        HOST=session['host']
        USUARIO=session['usuario']
        CONTRASENIA=session['contrasenia']
        DBNAME=request.form['db']

        con = mssql.SqlConnection(CONTROLADOR,HOST, USUARIO, CONTRASENIA, DBNAME)
        con.open()

        if con.StatusError:
            response_json['Mensaje']=str(con.MessageError)
        else:
            
            query = response_json['Query']  = request.form['query']

            if re.search(r'^SELECT(.*)', query.upper().lstrip()):
                con.cursor.execute(query)
                response_json['Columns'] = [i[0] for i in con.cursor.description]
                response_json['Resultado'] = [list(i) for i in con.cursor.fetchall()]
                response_json['Status']=True

            elif re.search(r'^EXEC(.*)', query.upper().lstrip()):
                con.cursor.execute(query)
                
                response_json['Columns'] = [i[0] for i in con.cursor.description]
                response_json['Resultado'] = [list(i) for i in con.cursor.fetchall()]
                response_json['Status']=True

                con.cnx.commit()

            elif re.search(r'^UPDATE(.*)', query.upper().lstrip()) or re.search(r'^DELETE(.*)', query.upper().lstrip()):                
                
                if re.search(r'WHERE(.*)', query.upper().lstrip()):
                    con.cursor.execute(query)
                    con.cnx.commit()
                    response_json['Status']=True
                else:
                    response_json['Mensaje']='Es obligatoria la clausula WHERE'
            elif re.search(r'^INSERT(.*)', query.upper().lstrip()):

                if re.search(r'INTO(.*)', query.upper().lstrip()):

                    con.cursor.execute(query)
                    con.cnx.commit()
                    response_json['Status']=True
                else:
                    response_json['Mensaje']='sin clausula INSERT INTO'
            else:
                response_json['Mensaje']='Query no valido: ' + query
        
        con.close()
    except Exception as err:
        response_json['Resultado'] = []
        response_json['Mensaje']='Exception: ' + str(err)
        response_json['Status']=False

    
    return app.response_class(
        response=json.dumps(response_json),
        status=200,
        mimetype='application/json'
    )

