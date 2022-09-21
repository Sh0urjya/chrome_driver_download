import os
import re
import time
import zipfile
import requests
import wget

os.chdir("D:\\my_python_files")
chromedriver_path = ".\\chromedriver"


def get_driver_latest_version(version):
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + str(version)
    response = requests.get(url)
    version_number = response.text
    return version_number

def download_chromedriver_zip(download_url, driver_binaryname, target_name):
        # downloading the zip file
        latest_driver_zip = wget.download(download_url, out=chromedriver_path)

        # extract the zip file
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(path = chromedriver_path)
        # delete the zip file downloaded above
        os.remove(latest_driver_zip)
        time.sleep(1)
        os.rename(driver_binaryname, target_name)
        time.sleep(1)
        os.chmod(target_name, 755)

def chromedriver_download_automation():
    if os.name == 'nt':
        replies = os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
        replies = replies.split('\n')
        for reply in replies:
            if 'version' in reply:
                reply = reply.rstrip()
                reply = reply.lstrip()
                tokens = re.split(r"\s+", reply)
                fullversion = tokens[len(tokens) - 1]
                tokens = fullversion.split('.')
                version = tokens[0]
                break
        target_name = chromedriver_path +'\\chromedriver-win-' + version + '.exe'
        found = os.path.exists(target_name)
        if not found:
            version_number = get_driver_latest_version(version)
            # build the donwload url
            download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
            download_chromedriver_zip(download_url, chromedriver_path +'\\chromedriver.exe', target_name)
            return os.path.abspath(target_name)
        else:
            return "Already latest version exist!"

    elif os.name == 'posix':
        reply = os.popen(r'chromium --version').read()

        if reply != '':
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[1]
            tokens = fullversion.split('.')
            version = tokens[0]
        else:
            reply = os.popen(r'google-chrome --version').read()
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[2]
            tokens = fullversion.split('.')
            version = tokens[0]

        target_name = chromedriver_path +'\\chromedriver-linux-' + version
        found = os.path.exists(target_name)
        if not found:
            version_number = get_driver_latest_version(version)
            download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_linux64.zip"
            download_chromedriver_zip(download_url, chromedriver_path +'\\chromedriver.exe', target_name)
            return os.path.abspath(target_name)
        else:
            return "Already latest version exist!"

if __name__ == "__main__":
    print(chromedriver_download_automation())