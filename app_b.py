from flask import Flask
from datetime import datetime
from model import get_main_runner, check_or_change_runner
import threading
import time

pool_instance = "B"
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

def run_task(pool_instance):
    print(f"Running task in {pool_instance}")
    for i in range(10):
        print(i)
        time.sleep(1)
    print(f"Task completed in {pool_instance}")

def loop_check_or_change_runner(pool_instance, pool_time_limit):
    while True:
        # with app.app_context():
        if check_or_change_runner(pool_instance, pool_time_limit):
            run_task(pool_instance)
        time.sleep(check_frequency_seconds)

# create daemon to check runner
threading.Thread(target=loop_check_or_change_runner, args=[pool_instance, pool_time_limit], daemon=True).start()



if __name__ == "__main__":
    app.run(port=3000, debug=False)