# Django task scheduler
This is an app for scheduling tasks
## run
To run this project, follow these steps:
### create the virtual environment
```
source venv/bin/activate
pip install -r requirements.txt
```
### configuration
If you want to configure database and ssl settings, create a file named `local_settings.py` under the `wishtasks` directory:
``` 
cd wishtasks/
touch local_settings.py
vim local_settings.py
```
### database
By default, Wishtasks works on a postgres database named `wishtasks` with the same password as it name. you can change this configuration. But for this database
