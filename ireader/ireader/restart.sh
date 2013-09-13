ps aux | grep uwsgi | awk {'print $2'} | xargs kill -9

echo "start"
uwsgi --ini ireader_uwsgi.ini
