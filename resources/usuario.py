from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from secrets import compare_digest

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blink.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blink.")

class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return  {'message': 'An error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted'}
        return{'message': 'User not found'}, 404

class UserRegister(Resource):
    #/cadastro
    def post(self):
        
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}
        
        user = UserModel(**dados)
        user.save_user()
        return {"message": "User created successfully!"}, 201 #created
    
class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and compare_digest(user.senha.encode('utf-8'), dados['senha'].encode('utf-8')):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': "The username or password is incorrect."}, 401 #unauthorized