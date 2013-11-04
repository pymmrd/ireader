#!/bin/sh
export PATH=$PATH:/usr/bin

#screen_shot_task
pgrep init_feature_book.py || python /var/www/wwwroot/ireader/ireader/bin/init_feature_book.py >> /data/log/init_feature_book.log
