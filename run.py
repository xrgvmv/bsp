#from bsp import create_app

#app = create_app()

#if __name__ == '__main__':
    #app.run(app.run(debug=True, host='0.0.0.0', port=5000))


import threading
from bsp import create_app
from bsp.task import periodic_task
import asyncio

app = create_app()

def start_periodic_task():
    with app.app_context():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(periodic_task())

if __name__ == '__main__':
    task_thread = threading.Thread(target=start_periodic_task)
    task_thread.daemon = True
    task_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)
