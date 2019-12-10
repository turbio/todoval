import requests

class QueryException(Exception):
  pass

class DB():
  def __init__(self, key=None, host='evaldb.turb.io'):
    self.key = key
    self.host = host
  
  def read(self, query, **args):
    return self.query(query, args, True)

  def write(self, query, **args):
    return self.query(query, args, False)

  def query(self, query, args, readonly):
    httpres = requests.post(
      'https://' + self.host + '/eval/' + self.key,
      json={
        'code': query,
        'readonly': readonly,
        'args': args,
      },
    )

    dbres = httpres.json()

    if 'error' in dbres:
      raise QueryException(dbres['error'])
    
    return dbres['object']