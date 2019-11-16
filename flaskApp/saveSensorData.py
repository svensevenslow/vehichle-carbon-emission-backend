from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskApp.db import connection
import jwt

from flaskApp.handlers import get_email_from_token

bp = Blueprint('saveSensorData', __name__, url_prefix='/saveSensorData')


@bp.route('/saveAirVedaData', methods=['POST'])
def save_air_veda_data():
    try:
        # email = get_email_from_token(request, jwt)
        # if email is None:
        #     return make_response({"message": "Token not sent, authentication failed"},401)
        # mysql_fetch_vid_query = """Select vid from user where email = (%s)"""
        # fetch_vid_tuple = [email]

        c, conn = connection()
        # c.execute(mysql_fetch_vid_query, fetch_vid_tuple)
        # result_set = c.fetchall()

        # if len(result_set) is 0:
        #     return make_response({"message": "user is not registered"},401)

        # vid = result_set[0][0]
        if 'AirVedaData' not in request.files:
            return make_response({"message": "file not sent"},500)
        file = request.files['AirVedaData']
        data_list = file.read().splitlines()

        mysql_insert_airveda_data_query = """INSERT INTO airvedadata (TIMESTAMP,AQI,PM25,PM10,CO2,Temperature,Humidity,VID,SID) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        insert_airveda_data_query_list = []
        for row in data_list:
            r = row.decode("utf-8").split(",")
            r.extend([request.form.get('VID'), request.form.get('SID')])
            insert_airveda_data_query_list.append(tuple(r))

        # remove the headers
        insert_airveda_data_query_list.pop(0)
        c.executemany(mysql_insert_airveda_data_query, insert_airveda_data_query_list)
        conn.commit()
        c.close()
        conn.close()
        return make_response({"message":"succesfully inserted airveda data"},200)

    except jwt.exceptions.InvalidTokenError as e:
        return make_response({"message": "Invalid token error, authentication failed", "error": e}, 401)
    except Exception as e:
        return make_response({"message": "encountered exception","error": e},500)


@bp.route('/saveAndroSensorData', methods=['POST'])
def save_andro_sensor_data():

    try:
        if 'AndroSensorData' not in request.files:
            return make_response({"message": "file not sent"}, 500)

        file = request.files['AndroSensorData']
        vid = request.form.get('VID')
        sid = request.form.get('SID')
        mileage= request.form.get('mileage')
        if vid is None:
            return make_response({"message": "vid missing from form"},500)
        if sid is None:
            return make_response({"message": "sid missing from form"}, 500)
        if mileage is None:
            return make_response({"message": "mileage missing from form"}, 500)

        mysql_insert_androsensor_data = """INSERT INTO AndroSensorData
                                        (AccX , AccY , AccZ , GravityX , GravityY , GravityZ , LAccX , LAccY, LAccZ
                                        ,GyroX, GyroY, GyroZ, Light, MFieldX , MFieldY , MFieldZ , OrientationZ , OrientationX , OrientationY, 
                                        Proximity, SoundLevel, Latitude, Longitude, Alt, AltGoogle, Speed , Accuracy, Orientation ,Satelites,TimeSinceStart, 
                                        TIMESTAMP,VID, SID ,mileage) VALUES
                                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data_list = file.read().splitlines()
        insert_androsensor_data_query_list= []
        for row in data_list:
            r = str(row.decode("utf-8")).split(",")
            r.extend([vid,sid,mileage])
            # ensure speed column is not empty
            if r[25] is '':
                r[25]='0'
            # remove milliseconds from timestamp
            r[30] = r[30][:19]
            insert_androsensor_data_query_list.append(tuple(r))

        # remove the headers
        insert_androsensor_data_query_list.pop(0)
        c, conn = connection()
        c.executemany(mysql_insert_androsensor_data,insert_androsensor_data_query_list)
        conn.commit()
        c.close()
        conn.close()
        return make_response({"message": "succesfully inserted androsensor data"}, 200)
    except Exception as e:
        return make_response({"message": "encountered exception","error": [str(x) for x in e.args]},500)
