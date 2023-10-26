import logging
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

def get_fields_nearby(lon, lat, distance, crop=None):
    conn = psycopg2.connect(
        database="mydb",
        user="myuser",
        password="mypassword",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
    query = """
        SELECT id, coordinates, crop, productivity, region, area_ha
        FROM geo
        WHERE ST_DWithin(ST_Transform(geometry, 2154), ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s),
        2154), 2154), %s)
    """
    if crop is not None:
        query += " AND crop = %s"
    cur.execute(query, (lon, lat, distance, crop) if crop is not None else (lon, lat, distance))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_fields_inside(lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, crop=None):
    conn = psycopg2.connect(
        database="mydb",
        user="myuser",
        password="mypassword",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
    query = """
            SELECT id, coordinates, crop, productivity, region, area_ha
            FROM geo
            WHERE ST_Within(geometry, ST_GeomFromText('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))', 2154))
        """

    if crop is not None:
        query += " AND crop = %s"
    cur.execute(query, (lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, lon1, lat1, crop) if crop is not None else (lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, lon1, lat1,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_fields_intersect(lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, crop=None):
    conn = psycopg2.connect(
        database="mydb",
        user="myuser",
        password="mypassword",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
    query = """
            SELECT id, coordinates, crop, productivity, region, area_ha
            FROM geo WHERE ST_Intersects(geometry, ST_Transform(ST_GeomFromText('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))', 2154), 2154))
"""

    if crop is not None:
        query += " AND crop = %s"
    cur.execute(query, (lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, lon1, lat1, crop) if crop is not None else (lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, lon1, lat1,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_fields_data(region):
    conn = psycopg2.connect(
        database="mydb",
        user="myuser",
        password="mypassword",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()
    query = """
        SELECT SUM(area_ha) as total_area, SUM(productivity) as total_yield,
        SUM(productivity * area_ha) / SUM(area_ha) as weighted_average_yield
        FROM geo
        WHERE region = %s;
    """
    cur.execute(query, (region,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result[0]



@app.route('/fields_nearby', methods=['GET'])
def query_nearby():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    distance = float(request.args.get('distance'))
    crop = request.args.get('crop')


    results_nearby = get_fields_nearby(lon, lat, distance, crop)

    if not results_nearby:
        return "There are no fields!"

    if len(results_nearby) >= 10000:
        return jsonify({"message": "Result limit exceeded. Please refine your query."})

    features = []
    for row in results_nearby:
        feature = {
            "type": "Feature",
            "id": row[0],
            "properties": {
                "crop": row[2],
                "productivity_estimation": row[3],
                "region_code": row[4],
                "area_ha": row[5],
            },
            "geometry": {
                "type": row[1]['type'],
                "coordinates": row[1]['coordinates'],
            }
        }

        features.append(feature)

    response = {"type": "FeatureCollection", "features": features}
    app.logger.info("Number of features in response: %d", len(features))
    return jsonify(response)


@app.route('/fields_inside', methods=['GET'])
def query_inside():
    lon1 = float(request.args.get('lon1'))
    lat1 = float(request.args.get('lat1'))
    lon2 = float(request.args.get('lon2'))
    lat2 = float(request.args.get('lat2'))
    lon3 = float(request.args.get('lon3'))
    lat3 = float(request.args.get('lat3'))
    lon4 = float(request.args.get('lon4'))
    lat4 = float(request.args.get('lat4'))
    crop = request.args.get('crop')

    results_inside = get_fields_inside(lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, crop)

    if not results_inside:
        return "There are no fields!"

    if len(results_inside) >= 10000:
        return jsonify({"message": "Result limit exceeded. Please refine your query."})

    features = []
    for row in results_inside:
        feature = {
            "type": "Feature",
            "id": row[0],
            "properties": {
                "crop": row[2],
                "productivity_estimation": row[3],
                "region_code": row[4],
                "area_ha": row[5],
            },
            "geometry": {
                "type": row[1]['type'],
                "coordinates": row[1]['coordinates'],
            }
        }

        features.append(feature)

    response = {"type": "FeatureCollection", "features": features}
    app.logger.info("Number of features in response: %d", len(features))
    return jsonify(response)


@app.route('/fields_intersect', methods=['GET'])
def query_intersect():
    lon1 = float(request.args.get('lon1'))
    lat1 = float(request.args.get('lat1'))
    lon2 = float(request.args.get('lon2'))
    lat2 = float(request.args.get('lat2'))
    lon3 = float(request.args.get('lon3'))
    lat3 = float(request.args.get('lat3'))
    lon4 = float(request.args.get('lon4'))
    lat4 = float(request.args.get('lat4'))
    crop = request.args.get('crop')

    results_intersect = get_fields_intersect(lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4, crop)

    if not results_intersect:
        return jsonify("There are no fields!")

    if len(results_intersect) >= 10000:
        return jsonify({"message": "Result limit exceeded. Please refine your query."})

    features = []
    for row in results_intersect:
        feature = {
            "type": "Feature",
            "id": row[0],
            "properties": {
                "crop": row[2],
                "productivity_estimation": row[3],
                "region_code": row[4],
                "area_ha": row[5],
            },
            "geometry": {
                "type": row[1]['type'],
                "coordinates": row[1]['coordinates'],
            }
        }

        features.append(feature)

    response = {"type": "FeatureCollection", "features": features}
    app.logger.info("Number of features in response: %d", len(features))
    return jsonify(response)

@app.route('/fields_data', methods=['GET'])
def query_fields_data():
    region = request.args.get('region')

    if region is None:
        return jsonify({"error": "Region parameter is required."})

    result = get_fields_data(region)


    response_data = {}
    if result[0] is not None:
        response_data["total_area"] = result[0]
    if result[1] is not None:
        response_data["total_yield"] = result[1]
    if result[2] is not None:
        response_data["average_yield"] = result[2]
    if response_data == {}:
        return "Region not found or no data available if no result"
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)