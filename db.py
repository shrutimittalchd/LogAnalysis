#!/usr/bin/env python2.7

import psycopg2
# imports psycopg2 module

DB_NAME = "news"


article_views = open('article_views.txt', 'w+')
author_views = open('author_views.txt', 'w+')
errors = open('errors.txt', 'w+')


# gives top 3 most viewed  articles of all time
def que1():
    db = psycopg2.connect(database=DB_NAME)
    cur = db.cursor()
    cur.execute("""select articles.title,
              count(*) as veiws from
              log,articles where
              log.path = '/article/' ||
              articles.slug group by
              articles.title order
              by veiws desc limit 3;
              """)
    views = cur.fetchall()
    for item in views:
        article_views.write(str(item[0]) + ' - ' + str(item[1]) + ' views\n')
        db.close()


# gives the authors name with most views
def que2():
    db = psycopg2.connect(database=DBNAME)
    cur = db.cursor()
    cur.execute("""select authors.name, count(*) as
                sum from log,articles,authors where
                log.path = '/article/' || articles.slug
                and authors.id=articles.author group
                by authors.name order by sum desc;
                """)
    authors = cur.fetchall()
    for i in authors:
        author_views.write('"' + str(i[0]) + '" - ' + str(i[1]) + ' views\n')
    db.close()


# gives the %errors with date
def que3():
    db = psycopg2.connect(database=DBNAME)
    cur = db.cursor()
    cur.execute("""create view totalrequests as
                select count(*) as total,
                date(time) from log group
                by date(time) order
                by date(time);""")
    cur.execute("""create view errors as select
                count(*) as errors,date(time)
                from log where status =
                '404 NOT FOUND' group by date(time)
                order by date(time);""")
    cur.execute("""create view percentage_errors as
                select (cast(errors.errors as float)
                /cast(totalrequests.total as float))
                *100 as percentage,totalrequests.date
                from totalrequests natural join errors;
                """)
    cur.execute("""select * from percentage_errors where
                percentage > 1;""")
    percentage = cur.fetchall()
    for item in percentage:
        errors.write(str(item[1]) + ' - ' + '%0.2f' % item[0] + '%errors\n')
    db.close()

que1()
que2()
que3()
