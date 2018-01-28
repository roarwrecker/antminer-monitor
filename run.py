import os
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('ANT_MON_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
