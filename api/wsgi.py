import os
import subprocess
from index import app

# Run prestart script if it exists
prestart_script = os.path.join(os.path.dirname(__file__), 'prestart.sh')
if os.path.exists(prestart_script):
    subprocess.call(['bash', prestart_script])

if __name__ == "__main__":
    app.run()
