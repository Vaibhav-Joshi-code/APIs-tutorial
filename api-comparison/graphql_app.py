from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

# Same data
users_data = [
    {"id": 1, "name": "Vijay", "email": "vijay@example.com", "age": 22, "city": "Jaipur"},
    {"id": 2, "name": "Bhumika", "email": "bhumika@example.com", "age": 21, "city": "Delhi"},
]

posts_data = [
    {"id": 1, "user_id": 1, "title": "REST API Basics"},
    {"id": 2, "user_id": 1, "title": "Docker Intro"},
    {"id": 3, "user_id": 2, "title": "GraphQL Guide"},
]

class Post(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()

class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    age = graphene.Int()
    city = graphene.String()
    posts = graphene.List(Post)

    def resolve_posts(self, info):
        return [p for p in posts_data if p['user_id'] == self['id']]

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())
    users = graphene.List(User)

    def resolve_user(self, info, id):
        user = next((u for u in users_data if u['id'] == id), None)
        return user

    def resolve_users(self, info):
        return users_data

schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(port=5001, debug=True)