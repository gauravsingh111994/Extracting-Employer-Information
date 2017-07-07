Steps to run the webapp :
	- Install Python 3.5 (Use python ide like spyder or pycharm).
	- Run 'pip' command in the terminal for installing requirements from requirements.txt file as :
		'pip install -r requirements.txt'
	- Once all the required package has been installed run 'main_run.py' in the terminal as :
		python main_run.py 
	- You can also use the ide for running 'main_run.py'.
	- When main_run.py is running if any popup of phantomjs comes do not close that popup,just minimize it.
	- Go to the link provided, generally it is '127.0.0.1:5000'.
	- Type the company name for which you want make the search.
	- Result shows(takes around 15 secs) :
		email id, employee strength, industry category, revenue, profit, number of opening on naukri.
		
Source of error :
	- Added phantomjs(for windows) along the webapp but in case code is not able read the location of phantomjs just change the location in config.ini file to the exact location of phantomjs.exe
	- If error comes as 'Import error: module not found' just use pip command for installing that modules as :
		'pip install package_name'
	- If frequent search is made there is a possibility that linkedin may block the bot for certain period of time.
