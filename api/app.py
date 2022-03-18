from sqlite3 import DatabaseError
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
                'name':special['name'],
                'location':special['location'],
                'station':special['station'],
                'category':special['category']
            }
        )
    return special_json

def _format_menus(menus_list):
    menu_json = []
    for menu in menus_list:
        menu_json.append(
            {
                'name':menu['name'],
                'location':menu['location'],
                'category':menu['category']
            }
        )
    return menu_json

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
            specials = db.execute_db_query('SELECT * FROM special WHERE day = "{}-{}-{}"'.format(year,month,day))
        except DatabaseError:
            return 500

        return jsonify({ 'specials' : _format_specials(specials) })
    
class GeneralLocation(Resource):
    def get(self, location):
        try:
            menus = db.execute_db_query('SELECT * FROM general WHERE location = "{}"'.format(location))
        except DatabaseError:
            return 500

        return jsonify({ 'menus' : _format_menus(menus) })

class General(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            name = data['name']
            location = data['location']
            category = data['category']
        except AttributeError:
            return 400

        try:
            db.execute_db_command(
                'INSERT INTO general (name, location, category)'
                'VALUES(?,?,?)', 
                    (name, location, category)
            )   
        except DatabaseError:
            return 500

        return 200


api.add_resource(SpecialToday, '/specials/today')
api.add_resource(SpecialDate, '/specials/<int:year>/<int:month>/<int:day>')
api.add_resource(GeneralLocation, '/general/<string:location>')
api.add_resource(General, '/general')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()