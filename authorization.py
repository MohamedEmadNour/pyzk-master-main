from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from sqlalchemy import  text


class UserService:
    def __init__(self, engine):
        self.engine = engine

    def user_has_access(self, user_id, function_name):
        sql = """
            SELECT COUNT(*)
            FROM tbFunctions AS f
            JOIN tbFunctionRoles AS fr ON f.Id = fr.FunctionId
            JOIN AspNetUserRoles AS ur ON fr.RoleId = ur.RoleId
            WHERE ur.UserId = :user_id
              AND f.FunctionName = :function_name
              AND f.IsDeleted = 0
              AND fr.IsDeleted = 0;
        """

        with self.engine.connect() as connection:
            result = connection.execute(text(sql), {'user_id': user_id, 'function_name': function_name})
            count = result.scalar()
            has_access = count > 0
            return has_access

user_service = UserService(db.session)

def dynamic_function_authorize(function_name):
    def wrapper(fn):
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_service.user_has_access(user_id, function_name):
                return jsonify({"msg": "Unauthorized"}), 401
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper