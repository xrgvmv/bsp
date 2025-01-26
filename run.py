#from bsp import create_app

#app = create_app()

#if __name__ == '__main__':
    #app.run(app.run(debug=True, host='0.0.0.0', port=5000))


import threading
from bsp import create_app
from bsp.packets_generator import global_generator

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    
    global_generator.start_generating_packets()
    print("Program start")
    app.run(debug=True, host='0.0.0.0', port=5000)
