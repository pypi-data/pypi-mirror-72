import psycopg2
import psycopg2.extras

class Orca:

    def __init__(self, connection):
        self.connection = connection


    def get_schema_properties(self, schema):
        try:
            conn = psycopg2.connect(**self.connection)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT schema FROM orca.schema WHERE name = '"+schema+"'")
            rows = cur.fetchall()[0][0]['properties']
            cur.close()
            conn.close()
            return rows
        except psycopg2.Error as e:
            raise { 'error': e }


    def is_valid_key(self, schema_properties, key):
        for id in schema_properties:
            name = schema_properties[id]['name']
            type = schema_properties[id]['type']
            if key == name and type == 'string':
                return True
        return False

    def get_properties_names(self, schema_properties, names):
        for id in schema_properties:
            names[id] = schema_properties[id]['name']
            if 'items' in schema_properties[id] and 'properties' in schema_properties[id]['items']:
                self.get_properties_names(schema_properties[id]['items']['properties'], names)

    def get_data(self, schema, schema_properties):
        names = {}
        self.get_properties_names(schema_properties, names)
        try:
            conn = psycopg2.connect(**self.connection)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            #TODO TURN THIS INTO A VIEW
            cur.execute("SELECT json_agg(i.data) FROM orca.schemaItem i JOIN orca.schema s ON s.id = i.schemaId WHERE s.name = '"+schema+"'")
            rows = cur.fetchall()[0][0]
            data = []
            self.get_data_helper(rows, names, data)
            cur.close()
            conn.close()
            return data
        except psycopg2.Error as e:
            raise { 'error': e }


    def get_data_helper(self, rows, names, data):
        if not rows:
            return
        for r in rows:
            temp = {}
            for id in r:
                name = names[id]
                if (isinstance(r[id], list)):
                    innerData = []
                    self.get_data_helper(r[id], names, innerData)
                    temp[name] = innerData
                else:
                    temp[name] = r[id]

            data.append(temp)
