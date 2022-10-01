import marko
import os
import sys
import sqlite3
from jinja2 import Environment, FileSystemLoader

class Converter:
    def __init__(self,path):
        self.path = path
        self.con = sqlite3.connect("index.db")
        self.cur = self.con.cursor()

    def start(self):
        self.list_files()

    def close(self):
        self.con.close()

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
        self.cur.execute("select last_modification from files where name = :file_name", {"file_name": str(file_name)})
        rows = self.cur.fetchone()
        if rows is None:
            print("couldnt find this file name in the db\n")
            self.insert(file_name, detail)
            self.md_to_html(self.path,file_name)
        else:
            print("i could find this file name in the db\n")
            print("db timestamp = ",rows[0])
            db_timestamp = rows[0]
            if int(detail.st_mtime) != db_timestamp:
                print("the timestamps were different, updating")
                self.update(file_name, detail)
                self.md_to_html(self.path,file_name)

    def insert(self, file_name, detail):
        print("inserting values ", file_name, " with modification time ", int(detail.st_mtime))
        self.cur.execute("insert into files values(?,?)",(file_name, int(detail.st_mtime)))
        self.con.commit()
        print("finished inserting values ", file_name, " with modification time ", detail.st_mtime)

    def update(self, file_name, detail):
        print("updating values ", file_name, " with modification time ", int(detail.st_mtime))
        self.cur.execute("update files set last_modification = ?",(int(detail.st_mtime)))
        self.con.commit()
        print("finished updating values ", file_name, " with modification time ", detail.st_mtime)

    def md_to_html(self,directory,file):
        path = os.path.join(directory, file)
        file_name = file
        with open(path, 'r') as file:
            data = file.read()
        print(".md file: \n",data)
        converted_data = marko.convert(data)
        print("converted md file: \n",converted_data)
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template('base.html')
        html_out = template.render({"content":converted_data})
        print("templated file with content inserted\n",html_out)
        sep = '.'
        base_file_name = file_name.split(sep, 1)[0]
        file_name = base_file_name + ".html"
        print("saving content to file: ",file_name)
        with open('html/'+file_name, 'w') as file:
            file.write(html_out)

# Main part:
n = len(sys.argv)
if len(sys.argv) != 2:
    print("correct usage: python3 ./app.py path_of_dir_to_be_inspected\n")
    sys.exit()

path = sys.argv[1]

converter = Converter(path)
converter.start()
converter.close()
