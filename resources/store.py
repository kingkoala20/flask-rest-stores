import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort # type:ignore
from models import StoreModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations in stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}
            
@blp.route("/store")
class StoreList(MethodView):
    
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists."
            )
        
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the store.")
        
        return store