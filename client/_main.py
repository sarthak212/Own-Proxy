from .connections import connection 
def run():
    print("Starting Client")
    config = {'hostname': '127.0.0.1',
              'portname':8080,
              'buffer_size':4096
              }
    k = connection(config)
