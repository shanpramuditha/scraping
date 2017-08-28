import sqlite3

conn = sqlite3.connect('test.db')
def setup():
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";

    conn.execute("CREATE TABLE IF NOT EXISTS images \
             (image           TEXT    NOT NULL, \
             link            TEXT     NOT NULL)");
    print "Table created successfully";
    return conn
    # conn.close()

def insertImage(image,link):
    cur = conn.cursor()
    cur.execute("INSERT INTO images(image,link) VALUES (?,?)",(image,link))
    conn.commit()
    print "added"

def isImageAvailable(image):
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE image=?", (image,))

    rows = cur.fetchall()
    if(len(rows) == 1):
        return True
    else:
        return False



