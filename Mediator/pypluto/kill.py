from pypluto import pluto

if __name__ == '__main__':
    client = pluto()
    client.connect()
    print('killing')
    client.disarm()
