# selenium-project
- Create a virtual env

    **virtualenv selenium

    source selenium/bin/activate**
    
- Steps to install selenium;

    **pip install selenium**

- Download the driver to interface with the chosen browser;

    for firefox -> **geckodriver**.

    **wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz**


- Unzip the tarball file;

    **tar -xvzf PATH_TO_DRIVER/geckodriver-v0.21.0-linux64.tar.gz geckodriver**

- Make it executable:

    **chmod +x geckodriver**

- move the unzipped file to /usr/local/bin

    **sudo mv geckodriver /usr/local/bin/**

- And then go about writing your scripts to interact with the browser.