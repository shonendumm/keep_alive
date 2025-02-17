from flask import Flask
from datetime import datetime
from model import get_main_runner, check_runner
import threading
import time

pool_instance = "A"
pool_time_limit = 30
check_frequency_seconds = 10

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to Soo's website!"


@app.route("/model")
def model():
    runner = get_main_runner()
    return f"runner pool: {runner.pool}, updated: {runner.updated}"

def loop_check_runner(pool_instance, pool_time_limit):
    while True:
        with app.app_context():
            check_runner(pool_instance, pool_time_limit)
            time.sleep(check_frequency_seconds)

# create daemon to check runner
threading.Thread(target=loop_check_runner, args=[pool_instance, pool_time_limit], daemon=True).start()



if __name__ == "__main__":
    app.run(port=2000, debug=False)