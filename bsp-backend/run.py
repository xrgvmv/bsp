from bsp import create_app
from bsp.packets_generator import packets_generator

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    
    packets_generator.start_generating_packets()
    app.run(debug=False, host='0.0.0.0', port=5000)
