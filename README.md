# Pasclepius (Pa)

Pa for personal assistant or Pasclepius is a simple medical billing system running on Flask 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. I am running develop on my Mac but have a production server running on Ubuntu 18.04. However, the following instructions only apply to Mac

### Prerequisites
```
LibreOffice 6+
MySql Server 8
python3 
```

### Installing

1. Set global variables as following:
    * DB_CONN_STRING=mysql+pymysql://<username>:<password>@localhost/<database_name>
    * DATABASE_USER
    * DATABASE_PASSWORD
    * DATABASE_NAME
    * TEST_USER_EMAIL=<email>
    * TEST_USER_NAME=<name>
    * TEST_USER_SURNAME=<surname>
    * FLASK_ENV=development
    * SYSTEM_URL (eg. /User/me/)
    * SECRET_KEY (for the flask server)
    * APP_URL (URL to root directory of project)
    * LIBPYTHON (Path to LibreOffice python binary)
    * INVOICE_URL (path to save odt invoices)
    * CSV_URL_NAMAF_TARIFFS (path to project/pasclepius/data/namaf_tariffs.csv)

&nbsp;
&nbsp;
2. Install dependencies: 
```
pip install -r requirements.txt
```
&nbsp;
&nbsp;
3. Create database and run database_setup.py
```
python application/database_setup.py
```
&nbsp;
&nbsp;
4. Run LibreOffice socket:
```
/Applications/LibreOffice.app/Contents/MacOS/soffice "--accept=socket,host=localhost,port=2002;urp;"
```
&nbsp;
&nbsp;
5. Start core application:
```
python development.py
```


## License

This project is licensed under the MIT License






