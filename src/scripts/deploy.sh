cd /path/to/project
git pull origin develop
source venv/bin/activate
pip install -r requirements.txt
export $(xargs < .env)
python ./src/manage.py migrate
sudo systemctl restart drf_starter
sudo systemctl restart nginx