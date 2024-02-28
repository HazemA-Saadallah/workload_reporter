#! /bin/python3

import psutil
import subprocess
import datetime
import time
import signal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import variables


class signals_handler:
    shutdown_request = False

    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.shutdown_request)
        signal.signal(signal.SIGTERM, self.shutdown_request)

    def request_shutdown(self, *args):
        self.shutdown_request = True

    def can_run(self):
        return not self.shutdown_request


def send_mail():
    body = """
        Please find the attached workload file. The file contains workload reports generated every hour.
        Note: this email is automaticly sent.
    """
    attachment = open(variables.filedir + '/' + variables.filename)

    msg = MIMEMultipart()
    msg['From'] = variables.src_mail
    msg['To'] = variables.dist_mail
    msg['subject'] = "Workload report"
    msg.attach(MIMEText(body, 'plain'))

    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= workload_file.txt")
    msg.attach(attachment_package)

    casted_string = msg.as_string()

    TIE_server = smtplib.SMTP("smtp.gmail.com", 587)
    TIE_server.starttls()
    TIE_server.login(variables.src_mail, variables.src_mail_password)

    TIE_server.sendmail(variables.src_mail, variables.dist_mail, casted_string)
    TIE_server.quit()


def get_data():
    cpu_name_command = "lscpu | grep \"Model name:\" | cut -d \":\" -f 2"
    directory = "/"

    data = {
        "CPU": [
            cpu_name := f"CPU: {subprocess.check_output(cpu_name_command, shell=True, text=True).strip()}\n",
            cpu_freq := f"CPU frequancy: {round(psutil.cpu_freq()[0])} Hz\n",
            cpu_usage_percen := f"CPU usage: {psutil.cpu_percent()}%\n",
            cpu_usage_percore := "\n".join(f"CPU {core}: {value}%" for core, value in enumerate(psutil.cpu_percent(percpu=True))) + "\n"
        ],

        "RAM": [
            ram_capacity := f"capacity: {round(psutil.virtual_memory()[0]/1048576)} MB\n",
            ram_used := f"Used: {round(psutil.virtual_memory()[3]/1048576)} MB ({psutil.virtual_memory()[2]}%)\n",
            ram_free := f"Free: {round(psutil.virtual_memory()[1]/1048576)} MB\n"
        ],

        "Swap": [
            swap_capacity := f"capacity: {round(psutil.swap_memory()[0]/1048576)} MB\n",
            swap_used := f"Used: {round(psutil.swap_memory()[1]/1048576)} MB ({psutil.swap_memory()[3]}%)\n",
            swap_free := f"Free: {round(psutil.swap_memory()[2]/1048576)} MB\n"
        ],

        "Disk": [
            disk_space := f"Space: {round(psutil.disk_usage(directory)[0]/(2**30))} GB\n",
            disk_used := f"Used: {round(psutil.disk_usage(directory)[1]/(2**30))} GB ({round(psutil.disk_usage(directory)[3])}%)\n",
            disk_usage := f"Free: {round(psutil.disk_usage(directory)[2]/(2**30))} GB\n"
        ],
        "Network": [
            total_recived := f"Total recived bytes: {round(psutil.net_io_counters()[1])} bytes\n",
            total_recived := f"Total recived packets: {round(psutil.net_io_counters()[3])} packets\n",
            total_recived := f"Total sent bytes: {round(psutil.net_io_counters()[0])} bytes\n",
            total_recived := f"Total sent packets: {round(psutil.net_io_counters()[2])} packets\n"
        ]

    }
    return data


def write_data(mode: bool) -> None:
    data = get_data()
    if mode == 1:
        wa = "a"
    else:
        wa = "w"

    with open(variables.filedir + '/' + variables.filename, wa) as workload_file:
        workload_file.write("Time stamp: " + str(datetime.datetime.now()) + "\n\n")
        for data_catagory, data_list in data.items():
            workload_file.write("".join(['-' for _ in range(20)]) + " " + data_catagory + " Status" + " " + "".join(['-' for _ in range(20)]) + "\n")
            for info in data_list: workload_file.write(info)
            workload_file.write("\n")
        workload_file.write("".join(['-' for _ in range(100)]) + "\n\n\n")


if __name__ == "__main__":
    signals = signals_handler()
    mail_time = 6
    frequancy = 1
    first_launch = True

    while signals.can_run():
        if first_launch: write_data(0)
        send_mail()

        for _ in range(round(mail_time/frequancy)):
            write_data(1)
            time.sleep(frequancy*3600)

        first_launch = False
