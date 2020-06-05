# Pasclepius (Pa)

Pa for personal assistant or Pasclepius is a simple medical billing system running on Flask 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. I am running develop on my Mac but have a production server running on Ubuntu 18.04. However, the following instructions only apply to Mac

### Prerequisites
```
LibreOffice 6+
OwnCloud 10.4.1 (production)
MySql Server 8
python3 
pip3
```

### Installing

1. Set global variables as following:
    * DATABASE_USER
    * DATABASE_PASSWORD
    * DATABASE_NAME
    * SYSTEM_URL (eg. /User/me/)
    * SECRET_KEY (for the flask server)
    * APP_URL (URL to root directory of project)
    * LIBPYTHON (Path to LibreOffice python binary)
    * OWNCLOUD_URL (if no Owncloud just use SYSTEM_URL)
    * CSV_URL_NAMAF_ORTHOPAEDIC_SURGOENS (this is a sample CSV data to be found in the data direcotry)

&nbsp;
&nbsp;
2. Install dependencies: 
```
pip3 install -r requirements.txt
```
&nbsp;
&nbsp;
3. Run LibreOffice socket:
```
/Applications/LibreOffice.app/Contents/MacOS/soffice "--accept=socket,host=localhost,port=2002;urp;"
```
&nbsp;
&nbsp;
4. Start flask server (when on Ubuntu no need to use the LibreOffice python):
```
/Applications/LibreOffice.app/Contents/MacOS/python start.py
```

Now you can register at [localhost:4003/register](localhost:4003/register)


## License

This project is licensed under the MIT License






