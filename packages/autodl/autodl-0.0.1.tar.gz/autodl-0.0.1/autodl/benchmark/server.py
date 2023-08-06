# Author: Herilalaina Rakotoarison

#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#db_connect = create_engine('sqlite:///opendl.db')
db_connect = create_engine('postgresql://dbuser:dbmdp@localhost:5432/opendldb')
app = Flask(__name__)
api = Api(app)


class Dataset(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from dataset")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        name = request.json['dataset_name']
        try:
            query = conn.execute(
                "insert into Dataset(dataset_name) values('{0}') returning dataset_id".format(name))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]
            return {'status': 'success', "dataset_id": result["dataset_id"]}
        except Exception as e:
            query = conn.execute(
                "select dataset_id from Dataset where dataset_name='{0}'".format(name))
            return {'status': 'success', "dataset_id": [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]["dataset_id"]}


class Grammar(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select grammar_id, grammar_name from grammar")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        name = request.json['grammar_name']
        try:
            query = conn.execute(
                "insert into grammar(grammar_name) values('{0}') returning grammar_id".format(name))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]
            return {'status': 'success', "grammar_id": result["grammar_id"]}
        except Exception as e:
            query = conn.execute(
                "select grammar_id from grammar where grammar_name='{0}'".format(name))
            return {'status': 'success', "grammar_id": [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]["grammar_id"]}


class String(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
            "select string_id, string_name, grammar_id, timestamp from string")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        string_name = request.json['string_name']
        grammar_id = request.json['grammar_id']
        query = conn.execute("insert into string(string_name, grammar_id) values('{0}', {1}) returning string_id".format(
            string_name, grammar_id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]
        return {'status': 'success', "string_id": result["string_id"]}


class Performance(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
            "select performance_id, epoch, value, runtime, subset, string_id from performance")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        epoch = request.json['epoch']
        value = request.json['value']
        subset = request.json['subset']
        string_id = request.json['string_id']
        metric_name = request.json["metric_name"]
        dataset_id = request.json["dataset_id"]

        query = conn.execute("insert into performance(epoch, value, subset, string_id, metric_name, dataset_id) values({0}, {1}, {2}, {3}, '{4}', {5}) returning performance_id".format(
            epoch, value, subset, string_id, metric_name, dataset_id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor][0]
        return {'status': 'success', "inserted_id": result["performance_id"]}


class Performances(Resource):
    def post(self):
        performances = request.json['performances']
        dataset_id = request.json['dataset_id']
        string_id = request.json['string_id']
        conn = db_connect.connect()

        for val in performances:
            query = conn.execute("insert into performance(epoch, value, subset, string_id, metric_name, dataset_id, runtime) values({0}, {1}, {2}, {3}, '{4}', {5}, {6})".format(
                val["epoch"], val["value"], val["subset"], string_id, val["metric_name"], dataset_id, val["runtime"]))
        return {'status': 'success'}


class SearchGrammar(Resource):
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        grammar_id = request.json['grammar_id']
        name_string = request.json['word']
        max_results = request.json['limit']

        query = conn.execute("""SELECT string_id
        FROM Grammar
        INNER JOIN String ON Grammar.grammar_id=String.grammar_id
        WHERE String.string_name='{0}'
        AND Grammar.Grammar_id={1} {2}""".format(name_string, grammar_id, "" if max_results == -1 else "LIMIT {0}".format(max_results)))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        for index, val in enumerate(result):
            query = conn.execute(
                "select epoch, value, runtime, subset, metric_name from performance where string_id={0} ORDER BY epoch ASC".format(val["string_id"]))
            result[index]["performance"] = [
                dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return jsonify(result)


api.add_resource(Grammar, '/grammar')
api.add_resource(String, '/string')
api.add_resource(Dataset, '/dataset')
api.add_resource(Performance, '/performance')
api.add_resource(Performances, '/performances')
api.add_resource(SearchGrammar, '/check_grammar_string')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
