# Purpose
This project is to test how two distributed app instances can check a central database, and if their own value aligns with the database value, the (single) app will carry out the job function.

# How to run
Install dependencies using `poetry install`.
Run the first instance using `poetry run python app_a.py`.
Then for the second instance, run using `poetry run python app_b.py`.

See that the first instance is maintaining the database value as "A", at http://localhost:2000/model
But when we stop the first instance, the second instance will change the value to "B" after the specified pool_time_limit (180 seconds), at http://localhost:3000/model

