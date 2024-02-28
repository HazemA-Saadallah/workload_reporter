#! /bin/python3

import subprocess


if __name__ == "__main__":
    username = str(subprocess.check_output("whoami", shell=True, text=True)).strip()
    execdir = str(subprocess.check_output("pwd", shell=True, text=True)).strip()+"/daemon.py"

    if username != "root":
        print("The program must be setup as root.\nRun: root python setup.py")
        exit()

    src_mail_inp = input("sourse e-mail address: ")
    src_mail_password_inp = input("sourse e-mail password (app password): ")
    dist_mail_inp = input("distnation e-mail address: ")
    filedir_inp = input("where to place the log file(default is '/tmp'): ").strip() or "/tmp"
    filename_inp = input("file name (default is 'workload_report.txt') ").strip() or "workload_report.txt"
    freq_inp = input("when to add a new reading to the file (default = 1 hour): ").strip() or '1'
    mail_time_inp = input("when to send the email (default = 12 hours): ").strip() or "12"

    with open("/etc/systemd/system/workload_reporter.service", "w") as service_file:
        service_file.write("[Unit]\n" +
                            "Description=workload reporter\n\n" +
                            "[Service]\n" +
                            "type=simple\n" +
                            f"ExecStart={execdir}\n" +
                            "Restart=always\n" +
                            "RestartSec=60\n\n" +
                            "[Install]\n" +
                            "WantedBy=multi-user.target"
                           )

    with open("variables.py", "w") as varibales_file:
        varibales_file.write(f"src_mail = '{src_mail_inp}'\n" +
                             f"src_mail_password = '{src_mail_password_inp}'\n" +
                             f"dist_mail = '{dist_mail_inp}'\n" +
                             f"filedir = '{filedir_inp}'\n" +
                             f"filename = '{filename_inp}'\n" +
                             f"freq = {freq_inp}\n" +
                             f"mail_time = {mail_time_inp}"
                             )

    subprocess.Popen("sudo systemctl start workload_reporter", shell=True)
