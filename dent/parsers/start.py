from parsers import El_dent, WStorm, Aveldent, Rocada
import threading
import asyncio

def start_eldent():
    item = El_dent()
    asyncio.run(item.start())

def start_aveldent():
    item = Aveldent()
    item.start()


def start_rocada():
    item = Rocada()
    item.start()

def start_wstorm():
    item = WStorm()
    asyncio.run(item.main())

if __name__ == '__main__':
    #eldent = threading.Thread(target=start_eldent)
    #aveldent = threading.Thread(target=start_aveldent)
    rocada = threading.Thread(target=start_rocada)
    #wstorm = threading.Thread(target=start_wstorm)
    
    #eldent.start()
    #aveldent.start()
    rocada.start()
    #wstorm.start()
