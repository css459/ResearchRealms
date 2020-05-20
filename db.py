from pymongo import MongoClient
from bson.objectid import ObjectId
from util.config import MONGO_CONNECTION_STRING
from core.snippets import format_snippet_list, format_snippet, format_save


class DBClient:
    def __init__(self):
        self.db = MongoClient(MONGO_CONNECTION_STRING).rr

    def save_snippet(self, author, code, snippet_name=None):
        name = snippet_name if snippet_name else ''

        new_snippet = {
            'author': author,
            'code': code,
            'name': name
        }
        snippet_id = self.db.snippets.insert_one(new_snippet)

        if snippet_name:
            return format_save(snippet_name)
        else:
            return format_save(snippet_id.inserted_id)

    def find_snippets(self, author):
        return format_snippet_list(list(self.db.snippets.find({'author': author}, {'_id': 1})))

    def find_snippet(self, author, snippet_id):
        return format_snippet(self.db.snippets.find_one({'author': author, '_id': ObjectId(snippet_id)}, {'code': 1}))
