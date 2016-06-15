import json

import os
from bro.models import Bro
from flask_script import Command
from main.extensions import db


class PopulateBrosCommand(Command):
    def run(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = file_dir + '/fixtures/bros.json'

        with open(file_path) as bros_file:
            data = json.loads(bros_file.read())
            for line in data:
                bro = Bro.query.filter_by(email=line['email'].lower()).all()
                if not bro:
                    bro = Bro(line['username'], line['username'], line['email'].lower(), line['birthday'])
                    db.session.add(bro)
                    db.session.commit()
                    print("Bro {0} has been added.".format(bro))
