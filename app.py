import marko
import os
import sys
import sqlite3

class Converter:
    def __init__(self,path):
        self.path = path
        self.con = sqlite3.connect("index.db")
        self.cur = self.con.cursor()

    def start(self):
        self.list_files()

    def list_files(self):
        for x in os.listdir(self.path):
            if x.endswith(".md"):
                print("evaluating file: ", x)
                self.file_details(x)

    def file_details(self,i):
        print("getting file details", i)
        details = os.stat(os.path.join(self.path, i))
        self.aligned(details, i)
        print("end of getting file details \n", i)
    
    def aligned(self, detail, file_name):
        print("checking if file", file_name, " with details: ", detail, " is aligned\n")
        rows = self.cur.execute("select last_modification from files where name = :file_name", {"file_name": str(file_name)})
        if self.cur.fetchone() is None:
            print("couldnt find this file name in the db\n")
            self.insert(file_name, detail)
            #md_to_html(file)
        else:
            print("i could find this file name in the db\n")
            for r in rows:
                print(r)

    def insert(self, file_name, detail):
        print("inserting values ", file_name, " with modification time ", int(detail.st_mtime))
        self.cur.execute("insert into files values(?,?)",(file_name, int(detail.st_mtime)))
        self.con.commit()
        print("finished inserting values ", file_name, " with modification time ", detail.st_mtime)

    def md_to_html(file):
        with open('markdown_files/text1.md', 'r') as file:
            data = file.read()
        return render_template('index.html', data = marko.convert(data))

# Main part:
n = len(sys.argv)
if len(sys.argv) != 2:
    print("correct usage: python3 ./app.py path_of_dir_to_be_inspected\n")
    sys.exit()

path = sys.argv[1]

converter = Converter(path)
converter.start()
