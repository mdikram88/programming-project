from flask_restful import reqparse, fields


REGREX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
EMAIL = "mohdikram888@yahoo.com"
PASSWORD = "njunpafqajljsrga"
# -------------------------------------- For user Object -----------------------------------

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')
create_user_parser.add_argument('name')
create_user_parser.add_argument('age')
create_user_parser.add_argument('backup')
create_user_parser.add_argument('gender')


update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('email')
update_user_parser.add_argument('password')
update_user_parser.add_argument('name')
update_user_parser.add_argument('age')
update_user_parser.add_argument('backup')
update_user_parser.add_argument('gender')


user_re = {
            "user_id": fields.Integer,
            "email": fields.String,
            "password": fields.String,
            "name": fields.String,
            "age": fields.Integer,
            "backup": fields.String,
            "gender": fields.String

}
# --------------------------------------------- End of User object ------------------------------

# ----------------------------------------------- Tracker Object --------------------------------
create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument("tracker_name")
create_tracker_parser.add_argument("description")
create_tracker_parser.add_argument("tracker_type")
create_tracker_parser.add_argument("setting")
create_tracker_parser.add_argument("user_id")
create_tracker_parser.add_argument("last_time")

update_tracker_parser = reqparse.RequestParser()
update_tracker_parser.add_argument("tracker_name")
update_tracker_parser.add_argument("description")
update_tracker_parser.add_argument("tracker_type")
update_tracker_parser.add_argument("setting")
update_tracker_parser.add_argument("user_id")
update_tracker_parser.add_argument("last_time")

tracker_re = {
                "tracker_id": fields.Integer,
                "tracker_name": fields.String,
                "description": fields.String,
                "tracker_type": fields.String,
                "setting": fields.String,
                "user_id": fields.Integer,
                "last_time": fields.String
}
# ------------------------------------------ End of Tracker Object ------------------------------

# ------------------------------------------- Logs Object ---------------------------------------
log_re = {
        "log_id": fields.Integer,
        "time": fields.String,
        "value": fields.String,
        "note": fields.String,
        "tracker_id": fields.Integer
}

create_log_parser = reqparse.RequestParser()
create_log_parser.add_argument("time")
create_log_parser.add_argument("value")
create_log_parser.add_argument("note")
create_log_parser.add_argument("tracker_id")

update_log_parser = reqparse.RequestParser()
update_log_parser.add_argument("time")
update_log_parser.add_argument("value")
update_log_parser.add_argument("note")
update_log_parser.add_argument("tracker_id")

# ------------------------------------------- End of Log Object ------------------------------------

TRACKER_HEADERS = {'tracker_name': 'Tracker Name',
                   'description': 'Description',
                   'tracker_type': 'Tracker Type',
                   'setting': 'Setting',
                   'last_time': 'Last visited'}

TRACKER_INFO = ["tracker_name", "description", "tracker_type", "setting", "last_time"]

LOG_INFO = ["time", "value", "note", "tracker_id"]

LOG_HEADER = {"time": "Time",
              "value": "Value",
              "note": "Note"}
