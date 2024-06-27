from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserRole(db.Model):
    __tablename__ = 'AspNetUserRoles'
    UserId = db.Column(db.String(450), nullable=False, primary_key=True)
    RoleId = db.Column(db.String(450), nullable=False, primary_key=True)

class FunctionRole(db.Model):
    __tablename__ = 'tbFunctionRoles'
    Id = db.Column(db.BigInteger, primary_key=True)
    FunctionId = db.Column(db.BigInteger, nullable=False)
    RoleId = db.Column(db.String(450), nullable=False)
    IsDeleted = db.Column(db.Boolean, default=False)

class Function(db.Model):
    __tablename__ = 'tbFunctions'
    Id = db.Column(db.BigInteger, primary_key=True)
    FunctionName = db.Column(db.String(100), nullable=False)
    IsDeleted = db.Column(db.Boolean, default=False)
