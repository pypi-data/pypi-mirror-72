import os
from elasticsearch import Elasticsearch


class Elastic(object):

	def __init__(self):

		self.es = Elasticsearch(
			hosts=[{'host': os.environ.get('ELASTIC_HOST'), 'port': 9243}],
			http_auth=(os.environ.get('ELASTIC_USER'), os.environ.get('ELASTIC_PASS')),
			use_ssl=True
		)

	def insertData(self, index, id_doc, data):
		result = self.es.index(index=index, doc_type='_doc', id=id_doc, body=data)
		try:
			return result['result']
		except BaseException as e:
			print(e)
			return False

	def searchDatabox(self, databoxId, query, init=0, size=10):
		try:
			result = self.es.search(index="mdb_{}".format(databoxId),body=query,size=size,from_=init)
			return result
		except Exception as e:
			return False

if __name__ == '__main__':
	print('*** Welcome to Minerva 4R. Social Data Mining S.A. 2020 ***')
