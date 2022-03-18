from sqlite3 import DatabaseError
from sre_parse import SPECIAL_CHARS
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import db

app = Flask(__name__)
api = Api(app)

def _format_specials(specials_list):
    special_json = []
    for special in specials_list:
        special_json.append(
            {
                'day':special['day'],
                'name':special['name'],
                'location':special['location'],
                'station':special['station'],
                'category':special['category']
            }
        )
    return special_json

class SpecialToday(Resource):
    def get(self):
        try:
            specials = db.execute_db_query("SELECT * FROM special WHERE day=date('now', 'localtime')")
        except DatabaseError:
            return 500

        return jsonify({ 'specials' : _format_specials(specials) })
    

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
    def get(self, year, month, day):
        try:
            # url will automatically strip month and day
            if month < 10:
                month = "0" + str(month)
            if day < 10:
                day = "0" + str(day)
            specials = db.execute_db_query('SELECT * FROM special WHERE day = "{}-{}-{}"'.format(year,month,day));
        except DatabaseError:
            return 500

        return jsonify({ 'specials' : _format_specials(specials) })
    

api.add_resource(SpecialToday, '/specials/today')
api.add_resource(SpecialDate, '/specials/<int:year>/<int:month>/<int:day>')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()