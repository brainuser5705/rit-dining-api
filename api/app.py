from sqlite3 import DatabaseError
from sre_parse import SPECIAL_CHARS
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import db

app = Flask(__name__)
api = Api(app)

class SpecialToday(Resource):
    def get(self):
        try:
            specials = db.execute_db_query("SELECT * FROM special WHERE day=date('now', 'localtime')")
        except DatabaseError:
            return 500

        special_jsons = []
        for special in specials:
            special_jsons.append(
                {
                    'day':special['day'],
                    'name':special['name'],
                    'location':special['location'],
                    'station':special['station'],
                    'category':special['category']
                }
            )

        return jsonify({ 'specials' : special_jsons })
    

    def post(self):
        data = request.get_json()

        try:
            day = data['day']
            name = data['name']
            location = data['location']
            station = data['station']
            category = data['category']
        except AttributeError:
            return 400

        try:
            db.execute_db_command(
                'INSERT INTO special (day, name, location, station, category)'
                'VALUES(date(?,"localtime"),?,?,?,?)', 
                    (day, name, location, station, category)
            )   
        except DatabaseError:
            return 500

        return 200

class SpecialDate(Resource):
    def get(self, year, date, day):
        return 200

api.add_resource(SpecialToday, '/specials/today')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()