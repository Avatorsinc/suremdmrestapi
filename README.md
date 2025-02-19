Edit .env with your credentials +api
edit paths inside movetogrouptest.py (folder paths)
this project is using numbers as folder names (first XXXX) -> you can change that
built it as an exe :
  windows : pyinstaller --onefile --add-data ".env;." movetogroupTest.py
  linux : pyinstaller --onefile --add-data ".env:." movetogroupTest.py

*How it works*

type in XXXX (or something you specified) in storeid field this will find anything similar and resolve Group ID
in device name just paste device name it will resolve Device ID
Assign -> device moved to specified group from point 10
