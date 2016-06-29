import json

import os
from application.bro.models import Bro
from flask_script import Command
from application.main.extensions import db


class PopulateBrosCommand(Command):
    def run(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = file_dir + '/fixtures/bros.json'

        with open(file_path) as bros_file:
            data = json.loads(bros_file.read())
            for line in data:
                bro = Bro.query.filter_by(email=line['email'].lower()).all()
                if not bro:
                    bro = Bro(username=line['username'], password=line['username'],
                              email=line['email'].lower(), birthdate=line['birthday'])
                    db.session.add(bro)
                    db.session.commit()
                    print("Bro {0} has been added.".format(bro))
