List of files
==============
1. bar_only.htm
2. script_bar.js
3. bar&line.htm
4. script_barline.js
5. cors_server.py
6. readme.txt 

Pre-requisites
==============
1. Rename the *.js1 files to *.js
2. Execute "pip install cors" from command prompt
3. To launch and keep the listener running, execute "python cors_server.py" from same directory as htm and js files


Execution
=========
1. Invoke "http://localhost:8000/bar_only.htm" from Chrome
	- This displays a chart with only bars by calling the js file "script_bar.js"

2. Invoke "http://localhost:8000/bar&line.htm" from Chrome
	- This displays a chart with only bars by calling the js file "script_barline.js"

