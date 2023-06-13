from main import app, db, cache
from flask_restful import Resource, Api, marshal
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import datetime as dt
import jwt
from application.models import *
from application.additional_variables import create_user_parser, update_user_parser, user_re, tracker_re, \
    update_tracker_parser, create_tracker_parser, log_re, update_log_parser, create_log_parser
from application.additional_functions import token_required, validate_user_data, validate_tracker_data, \
    validate_log_data, validate_email, update_headers, clean_json
from application.keys import SECRET_KEY

api = Api(app)


@cache.memoize(timeout=10)
def get_user(email):
    return Users.query.filter_by(email=email).first()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if validate_email(data["email"]):
        record = get_user(data["email"])

    else:
        resp = make_response(jsonify({"message": "Invalid Email Address"}), 400)
        resp = update_headers(resp)
        return resp

    if record:
        if check_password_hash(record.password, data["password"]):

            record = clean_json(record)  # clean_json() is from application.additional_functions
            # print(record)
            payload = {
                'user': data["email"],
                'exp': dt.datetime.utcnow() + dt.timedelta(hours=24)
            }
            token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

            # making response
            resp = make_response(record, 200)
            resp = update_headers(resp, token, status=True)  # update_headers is from application.additional_functions
            return resp

        else:
            resp = make_response(jsonify({'message': "Incorrect Password"}), 401)
            resp = update_headers(resp)
            return resp

    resp = make_response(jsonify({'message': "Email doesn't exist"}), 404)
    resp = update_headers(resp)
    return resp


@app.route("/reset_password", methods=["POST"])
def reset():
    data = request.get_json()
    user = get_user(data["email"])

    if user:
        if hashlib.sha256(data["backup"].encode("utf-8")).hexdigest() == user.backup:
            if len(data["password"].strip()) < 8:
                return make_response(jsonify({"message": "Password Should be at least 8 characters"}), 400)

            if not check_password_hash(user.password, data["password"]):
                user.password = generate_password_hash(password=data["password"],
                                                       method="pbkdf2:sha256:2",
                                                       salt_length=8)

            try:
                db.session.commit()
            except:
                return make_response(jsonify({"message": "Something went wrong, try again later"}), 400)

            cache.delete_memoized(get_user, user.email)

            return make_response(jsonify({"message": "Password Reset Successfully"}), 200)
        else:
            return make_response(jsonify({"message": "Backup code does not match"}), 400)
    else:
        return make_response(jsonify({"message": "Email does not exists."}), 404)


# Pure Flask-Restful APIs

class UserAPI(Resource):
    @staticmethod
    def post():

        args = create_user_parser.parse_args()
        user_record = Users.query.filter_by(email=args["email"]).first()
        if user_record:
            return make_response(jsonify({"message": "Email Already Taken"}), 400)

        # Validating user Data
        resp, status = validate_user_data(args)
        if not status:
            return resp

        email = args.get('email')
        password = args.get('password')
        name = args.get('name').title()
        age = int(float(args.get('age')))
        backup = hashlib.sha256(args.get('backup').encode("utf-8")).hexdigest()
        gender = args.get('gender')

        # Creating User Object
        user = Users(email=email,
                     password=generate_password_hash(password=password,
                                                     method="pbkdf2:sha256:2",
                                                     salt_length=8),
                     name=name,
                     age=age,
                     backup=backup,
                     gender=gender)

        # Committing New User Record
        try:
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({"message": "Congratulations! \n\nYour Account is Created Successfully."}),
                                 201)
        except:
            return make_response(jsonify({"message": "Something went wrong.Please try again later"}), 400)

    @staticmethod
    @token_required
    def put(user_id):
        user = Users.query.filter_by(user_id=user_id).first()
        # checking is user id exists in the database
        if user is not None:
            args = update_user_parser.parse_args()
            # Validate Data
            resp, status = validate_user_data(args)

            if not status:
                return resp

            # Updating Data
            new_password = generate_password_hash(password=args.get("password"),
                                                  method="pbkdf2:sha256:2",
                                                  salt_length=8)
            if new_password != user.password:
                user.password = new_password
            user.name = args.get('name')
            user.age = args.get('age')
            user.backup = hashlib.sha256(str(args.get('backup')).encode("utf-8")).hexdigest()
            user.gender = args.get('gender')

            # Committing all updates
            try:
                db.session.commit()
            except:
                return make_response(jsonify({"message": "Something went wrong, try again later"}), 400)
            # extracting updated user record and returning
            user = Users.query.filter_by(user_id=user_id).first()
            cache.delete_memoized(get_user, user.email)
            return marshal(user, user_re), 200

        else:
            return make_response(jsonify({"message": "User Doesn't Exist"})), 404

    @staticmethod
    @token_required
    def delete(user_id):
        user = Users.query.filter_by(user_id=user_id).first()

        if user is not None:
            # Deleting Trackers of the user and logs of each Tracker
            trackers = Trackers.query.filter_by(user_id=user_id)
            for tracker in trackers:
                logs = Logs.query.filter_by(tracker_id=tracker.tracker_id)
                for log in logs:
                    db.session.delete(log)
                db.session.delete(tracker)

            try:
                db.session.delete(user)
                db.session.commit()
            except:
                return make_response(jsonify({"message": "Something went Wrong"}), 400)

            return make_response(jsonify({"message": "User Deleted Successfully"}), 200)
        else:
            return make_response(jsonify({"message": "User Doesn't Exist"}), 404)


@cache.memoize(timeout=3600)
def get_tracker(tk_id):
    return Trackers.query.get(tk_id)


class TrackersAPI(Resource):
    @staticmethod
    @token_required
    def get(tracker_id):

        tracker = get_tracker(tracker_id)
        if tracker:
            return marshal(tracker, tracker_re), 200
        return make_response(jsonify({"message": "Tracker Id does not exists"}))

    @staticmethod
    @token_required
    def post():
        args = create_tracker_parser.parse_args()
        tracker = Trackers.query.filter_by(tracker_name=args["tracker_name"], user_id=args["user_id"]).first()
        user = Users.query.get(args["user_id"])

        if tracker:
            return make_response(jsonify({"message": "Tracker Name already exists for the user"}), 400)
        if not user:
            return make_response(jsonify({"message": "user_id is invalid"}), 400)

        # Validating Tracker Data
        resp, status = validate_tracker_data(args)
        if not status:
            return resp

        tracker_name = args.get("tracker_name")
        description = args.get('description')
        tracker_type = args.get("tracker_type")
        setting = args.get("setting")
        user_id = int(float(args.get("user_id")))
        last_time = args.get("last_time")

        try:
            new_tracker = Trackers(tracker_name=tracker_name,
                                   description=description,
                                   tracker_type=tracker_type,
                                   setting=setting,
                                   user_id=user_id,
                                   last_time=last_time)
            db.session.add(new_tracker)
            db.session.commit()
        except:
            db.session.rollback()
            return make_response(jsonify({"message": "Something went wrong, Try again..."}), 400)

        tracker = Trackers.query.filter_by(tracker_name=tracker_name, user_id=user_id).first()
        # Deleting Cache of user
        cache.delete_memoized(get_user, tracker.tracker_user.email)

        return marshal(tracker, tracker_re), 201

    @staticmethod
    @token_required
    def put(tracker_id):

        tracker = Trackers.query.filter_by(tracker_id=tracker_id).first()

        if tracker is not None:

            cache.delete_memoized(get_tracker, tracker_id)

            args = update_tracker_parser.parse_args()
            resp, status = validate_tracker_data(args)
            if not status:
                return resp

            # To Check if New Tracker Name already exist for this user
            if tracker.tracker_name != args.get("tracker_name"):
                duplicate_record = Trackers.query.filter_by(tracker_name=args.get("tracker_name"),
                                                            user_id=args.get("user_id")).first()

                if duplicate_record:
                    print(duplicate_record)
                    return make_response(jsonify({"message": "This Tracker name already exist"}), 400)

            tracker.tracker_name = args.get("tracker_name")
            tracker.description = args.get('description')
            tracker.setting = args.get("setting")
            tracker.last_time = args.get("last_time")

            db.session.commit()
            # delete user cache
            cache.delete_memoized(get_user, tracker.tracker_user.email)
            return make_response(jsonify({"message": "Tracker Updated Successfully"}), 200)
        else:
            return make_response(jsonify({"message": "Tracker Id is Invalid"}), 404)

    @staticmethod
    @token_required
    def delete(tracker_id):

        tracker = Trackers.query.filter_by(tracker_id=tracker_id).first()

        if tracker is not None:

            cache.delete_memoized(get_tracker, tracker_id)

            logs = Logs.query.filter_by(tracker_id=tracker_id)
            for log in logs:
                db.session.delete(log)
            try:
                db.session.delete(tracker)
                db.session.commit()
            except:
                return make_response(jsonify({"message": "Something went wrong, try again later"}), 400)

            # cache.delete_memoized(get_user, tracker.tracker_user.email)
            return make_response(jsonify({"message": "Tracker delete Successfully!"}), 200)
        else:
            return make_response(jsonify({"message": "Tracker id doesn't exists"}), 404)


@cache.memoize(timeout=3600)
def get_log(lg_id):
    return Logs.query.get(lg_id)


class LogsAPI(Resource):
    @staticmethod
    @token_required
    def get(log_id):

        log = get_log(log_id)

        if log:
            return marshal(log, log_re), 200
        return make_response(jsonify({"message": "Log Id does not exist.."}))


    @staticmethod
    @token_required
    def post():
        args = create_log_parser.parse_args()
        resp, status = validate_log_data(args)

        if not status:
            return resp

        time = args.get("time")
        value = args.get("value")
        note = args.get("note")
        tracker_id = args.get("tracker_id")

        tracker = Trackers.query.filter_by(tracker_id=tracker_id).first()
        if not tracker:
            return make_response(jsonify({"message": "Tracker id doesn't exist"}))

        duplicate = Logs.query.filter_by(time=time,
                                         value=value,
                                         note=note,
                                         tracker_id=tracker_id).first()
        if duplicate:
            return make_response(jsonify({"message": "Log already exist"}))

        try:
            new_log = Logs(time=time,
                           value=value,
                           note=note,
                           tracker_id=tracker_id)
            db.session.add(new_log)
            db.session.commit()
        except:
            return make_response(jsonify({"message": "Something went Wrong, Please try again later..."}), 400)

        log = Logs.query.filter_by(time=time,
                                   value=value,
                                   note=note,
                                   tracker_id=tracker_id).first()
        cache.delete_memoized(get_user, log.tracker.tracker_user.email)
        return marshal(log, log_re), 201

    @staticmethod
    @token_required
    def put(log_id):
        log = Logs.query.filter_by(log_id=log_id).first()
        if log is not None:

            cache.delete_memoized(get_log, log_id)

            args = update_log_parser.parse_args()
            resp, status = validate_log_data(args)
            if not status:
                return resp

            time = args.get("time")
            value = args.get("value")
            note = args.get("note")

            log.time = time
            log.value = value
            log.note = note

            try:
                db.session.commit()
            except:
                return make_response(jsonify({"message": "Something went wrong"}), 400)

            log = Logs.query.filter_by(log_id=log_id).first()
            cache.delete_memoized(get_user, log.tracker.tracker_user.email)
            return marshal(log, log_re), 200
        else:
            return make_response(jsonify({"message": "Log id doesn't exist"}), 404)

    @staticmethod
    @token_required
    def delete(log_id):
        log = Logs.query.filter_by(log_id=log_id).first()

        if log is not None:
            cache.delete_memoized(get_log, log_id)
            db.session.delete(log)
            db.session.commit()
            return make_response(jsonify({"message": "Log deleted successfully!"}))
        else:
            return make_response(jsonify({"message": "Log id doesn't exist"}), 404)


api.add_resource(UserAPI, "/api/user", "/api/user/<int:user_id>")
api.add_resource(TrackersAPI, "/api/tracker", "/api/tracker/<int:tracker_id>")
api.add_resource(LogsAPI, "/api/log", "/api/log/<int:log_id>")
