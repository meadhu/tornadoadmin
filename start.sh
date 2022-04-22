#python app.py
# python app.py --env=prod --port=3001
# https://github.com/vishnubob/wait-for-it
#./wait-for-it.sh tornadoadmin-mysql:3306 -- python app.py
./wait-for-it.sh tornadoadmin-mysql:3306 -- python app.py --env=prod --port=3001
#./wait-for-it.sh tornadoadmin-mysql:3306 -- python app.py --env=prod --port=3002