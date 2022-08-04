cd /path/to/project
git pull origin develop
source venv/bin/activate
pip install -r requirements.txt
export $(xargs < .env)
python ./src/manage.py migrate
sudo systemctl restart legalcrm
sudo systemctl restart nginx