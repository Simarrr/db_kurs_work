from flask import Flask,render_template,request,redirect,url_for
import mysql.connector


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def do_search():

    if request.method == 'POST':

        if 'send' in request.form and request.form['send']=='Запрос 1':

            year = request.form['year']

            month = request.form['month']

            conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')


            cursor = conn.cursor()

            _SQL = f"""select film.name,count(session.id_film) - count(ticket.id_ticket) + 1, sum(ticket.status)
                       from film left join session on film.id_film = session.id_film
                       left join ticket on session.id_session = ticket.id_session
                       where year(session.date) = {year} and month(session.date) = {month}
                       group by film.name"""

            cursor.execute(_SQL)

            result = cursor.fetchall()

            res = []

            schema = ['name', 'session_count','ticket_count']

            for blank in result:
                res.append(dict(zip(schema,blank)))
            return render_template('result.html',year=year, month=month, blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Запрос 2':

                         year = request.form['year2']

                         month = request.form['month2']

                         name = request.form['name2']

                         conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')


                         cursor = conn.cursor()

                         _SQL = f"""select session.date,sum(ticket.price) * session.margin
                                    from film left join session on film.id_film = session.id_film
                                    left join ticket on session.id_session = ticket.id_session
                                    where year(session.date) = {year} and month(session.date) = {month}
                                    and film.name = '{name}' and ticket.status = 1
                                    group by session.date"""

                         cursor.execute(_SQL)

                         result = cursor.fetchall()

                         res = []

                         schema = ['date', 'money']

                         for blank in result:
                             res.append(dict(zip(schema,blank)))
                         return render_template('result.html',year=year, month=month, name = name, blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Запрос 3':
            conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')
            cursor = conn.cursor()
            _SQL = f"""SELECT * FROM film
                       order by duration desc
                       limit 1;"""
            cursor.execute(_SQL)
            result = cursor.fetchall()
            res = []
            schema = ['id', 'name','country', 'year', 'director', 'production', 'duration']
            for blank in result:
                res.append(dict(zip(schema,blank)))
            return render_template('result.html', blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Запрос 4':
                    conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')
                    cursor = conn.cursor()
                    _SQL = f"""select film.id_film, film.name, film.country,
                               film.year, film.director, film.production, film.duration
                               from film left join session on film.id_film = session.id_film
                               where session.id_session is NULL"""
                    cursor.execute(_SQL)
                    result = cursor.fetchall()
                    res = []
                    schema = ['id', 'name','country', 'year', 'director', 'production', 'duration']
                    for blank in result:
                        res.append(dict(zip(schema,blank)))
                    return render_template('result.html', blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Запрос 5':
                            conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')
                            cursor = conn.cursor()
                            _SQL = f"""select film.name
                                       from film left join session on film.id_film = session.id_film
                                       where session.id_session is NULL"""
                            cursor.execute(_SQL)
                            result = cursor.fetchall()
                            res = []
                            schema = ['name']
                            for blank in result:
                                res.append(dict(zip(schema,blank)))
                            return render_template('result.html', blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Запрос 6':
                    conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')
                    cursor = conn.cursor()
                    _SQL = f"""SELECT * FROM many_sessions"""
                    cursor.execute(_SQL)
                    result = cursor.fetchall()
                    res = []
                    schema = ['id', 'name','country', 'year', 'director', 'production', 'duration']
                    for blank in result:
                        res.append(dict(zip(schema,blank)))
                    return render_template('result.html', blanks = res, schema = schema)
        elif 'send' in request.form and request.form['send']=='Процедура':

                                 year = request.form['year7']

                                 month = request.form['month7']

                                 conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')

                                 cursor = conn.cursor()

                                 args = (month, year)

                                 cursor.callproc('film_data',args)

                                 conn.commit()

                                 conn = mysql.connector.connect(user='root', password='Smileng11', host='localhost', database='cinema')

                                 cursor = conn.cursor()

                                 _SQL = f"""select * from report where D_Year = {year} and D_Month = {month};"""

                                 cursor.execute(_SQL)

                                 result = cursor.fetchall()

                                 res = []

                                 schema = ['id', 'name', 'duration', 'session_count', 'ticket_count', 'year', 'month']

                                 for blank in result:
                                     res.append(dict(zip(schema,blank)))
                                 return render_template('result.html',year=year, month=month, blanks = res, schema = schema)
    else:
        return render_template('entry.html')

app.run(debug=True)

