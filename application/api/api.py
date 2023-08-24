from flask import Flask
from flask_restful import Resource, Api

api = Api(app)

class Product(Resource):
    #CREATE
    def post(self):
    
    #READ
    def get(self,product_id):
    
    #UPDATE
    def patch(self,product_id):
    
    #DELETE
    def delete(self, category_id):


class Category(Resource):
    #CREATE
    def post(self):
        
    #READ
    def get(self, category_id):
    
    #UPDATE
    def patch(self, category_id):
    
    #DELETE
    def delete(self, category_id):
        
api.add_resource(Product,'/product','/product/<product_id>')
api.add_resource(Category,'/category','/category/<category_id>')