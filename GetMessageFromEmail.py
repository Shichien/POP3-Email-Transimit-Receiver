# -*- coding: utf-8 -*-
# coding: unicode_escape
# 命名规则：content_ 表示MIME格式的原始数据，decoded_ 表示通过解析后的数据

import base64
import os
import poplib
import re
import warnings
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.quoprimime import decode as q_decode
warnings.filterwarnings("ignore")

class EmailSender:

    def __init__(self):
        self.sender = "deralive@qq.com"
        self.receivers = ["2642136260@qq.com"]
        self.message = MIMEText("This is a test email", "plain", "utf-8")
        self.message["From"] = formataddr(SMTP_FROM, 'utf-8')
        self.message["To"] = formataddr(SMTP_TO,'utf-8')
        self.message["Subject"] = Header("Test Email",'utf-8')

    # 连接至 SMTP 服务器
    def stmp_connect(self):
        try:
            self.smtp_obj = smtplib.SMTP_SSL(SMTP_HOST, 465)
            self.smtp_obj.login(SMTP_USER, SMTP_PASS)
        except Exception as e:
            print(f"SMTP Connect Error:{e}")
            exit()

    # 选择开启 DEBUG 模式，实时获取交互回应
    def open_stmp_debug(self):
        self.smtp_obj.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息

    # 发送纯文本邮件
    def stmp_send_text_email(self):
        self.stmp_connect()
        self.smtp_obj.sendmail(self.sender, self.receivers, self.message.as_string())

    # 发送带附件的邮件
    def stmp_send_attachments_email(self):
        self.stmp_connect()
        pass
        self.smtp_obj.sendmail(self.sender, self.receivers, self.message.as_string())

class EmailPatterns:
    """邮件常用正则表达式"""
    PAT_FROM = re.compile(b'^From:')
    PAT_TO = re.compile(b'^To:')
    PAT_DATE = re.compile(b'^Date:')
    PAT_SUBJECT = re.compile(b'^Subject:')
    PAT_ATTACHMENT_FILENAME = re.compile(b'filename="?(.+)"?') # Fix Bug (1): 双引号是可选的 使用 "? 表示可选
    PAT_DECODED_ATTACHMENT_FILENAME = re.compile(r'filename="?(.+)"?') # Fix Bug (1): 双引号是可选的 使用 "? 表示可选
    PAT_MIME_FORMAT = re.compile(b'=\?[A-Za-z0-9_-]+\?[BQbq]\?[A-Za-z0-9+/=]+\?=')

class EmailDecoder:
    @staticmethod
    # 解码 Base64 编码的附件
    def decode_attachment_base64(attachment_bin_data: bytes, attachment_name: str) -> None: # Return File Output
        attachment_name = attachment_name.replace('"', '')  # 去除文件名中的双引号
        output_dir = "Output_Attachment"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, attachment_name)

        with open(output_path, "wb") as file:
            file.write(attachment_bin_data)

    @staticmethod
    # 解码 Base64 编码的内容
    def decode_content_base64(content_base64_data: bytes, charset: str) -> str:
        return base64.b64decode(content_base64_data).decode(f"{charset}")

    @staticmethod
    # 解码 MIME 头文件
    def decode_mime_header(header: bytes) -> str:
        # 解析出编码片段，形如 "=?编码格式?编码方式?数据?="
        start = header.find(b'=?')
        end = header.find(b'?=', start) + 2
        mime_encoded_part = header[start:end]

        # 将其分割为不同的部分: 编码格式、编码方式、编码数据
        parts = mime_encoded_part.split(b'?')
        charset = parts[1].decode('utf-8')
        encoding = parts[2].decode('utf-8')
        encoded_data = parts[3].decode('utf-8')

        # 解码 Base64 数据
        if encoding.upper() == 'B':
            decoded_bytes = base64.b64decode(encoded_data)
            decoded_string = decoded_bytes.decode(charset)
            decoded_header = header.replace(mime_encoded_part, decoded_string.encode('utf-8'))  # 替换回原来的部分
            return decoded_header.decode('utf-8')
        elif encoding.upper() == 'Q':
            decoded_string = q_decode(encoded_data)
            return decoded_string
        else:
            raise ValueError("不支持的编码方式")

    @staticmethod
    def check_mime_format(PAT: [bytes],line: bytes) -> str:
        if PAT.search(line):
            if EmailPatterns.PAT_MIME_FORMAT.search(line):
                decoded_result = EmailDecoder.decode_mime_header(line)
            else:
                decoded_result = line.decode('utf-8')
            return decoded_result

    @staticmethod
    # 从字符串解析出 (Real Name, Email Address)
    def parse_email_tuple(env_value: str) -> tuple | None:
        if env_value:
            env_value = env_value.strip('"')
            name, email = env_value.split(',')
            return (name.strip(), email.strip())
        return None

class CommandReceiver:

    @staticmethod # 对电脑作出控制指令
    def do_specific_command(command: str) -> None:
        if command == 'close':
            print("即将关机")
            os.system("shutdown -s -t 100")
        elif command == 'reset':
            os.system("shutdown -r -t -100")
        elif command == 'VPN':
            os.system("taskkill /f /im vpnui.exe")
        elif command == 'Sunshine':
            os.system("C:\\Users\\26421\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\RunSideSunshine.pyw")
        else:
            try:
                os.system(command)
            except Exception as error:
                print(f"Error Command:{error}")

class EmailReceiver:

    def __init__(self, EMAIL_ADDRESS, PASSWORD, POP_SERVER):
        self._email_address = EMAIL_ADDRESS
        self._password = PASSWORD
        self._pop_server = POP_SERVER

    # 获取邮箱当前邮件数与总字节数 Tuple(Count, Size)
    def get_emailbox_state(self) -> tuple:
        try:
            welcome_massage = self.read_email.getwelcome()
            print("\n")
            print(f"Welcome Message:{welcome_massage}")
        except Exception as e:
            print(f"Get Welcome Message Error:{e}")

        # Get the state of the email
        self.all_email = self.read_email.stat()  # 获取邮箱状态
        print("\nBasic Situation:\n")
        print("Message Count:{0},Mailbox Size:{1}".format(*self.all_email))

        self.email_list = self.read_email.list()
        print("\nEmail List:\n")
        print(f"{self.email_list[1]}")

        return self.all_email[0], self.all_email[1]

    # 连接到 POP3 服务器
    def pop_connect(self):
        try:
            self.read_email = poplib.POP3_SSL(self._pop_server, 995)
            self.read_email.user(self._email_address)
            self.read_email.pass_(self._password)
        except Exception as e:
            print("Reading The Email Error:{e}")
            exit()

    # 获取某邮件中所有的附件
    def get_attachment_content(self, email_index):
        email_content = self.read_email.retr(email_index)[1] # response, contents(list), octets

        decoded_attachment_file_header_list = [] # 文件可能有多个，所以用列表存储

        # 读取文件头信息
        for line in email_content:
            if EmailPatterns.PAT_ATTACHMENT_FILENAME.search(line):
                content_attachment_file_header = line
                if EmailPatterns.PAT_MIME_FORMAT.search(content_attachment_file_header):
                    decoded_attachment_file_header = EmailDecoder.decode_mime_header(content_attachment_file_header)
                else:
                    decoded_attachment_file_header = content_attachment_file_header.decode('utf-8')
                decoded_attachment_file_header_list.append(decoded_attachment_file_header)

        start = False
        collected_lines = []
        list_index = 0
        # 遍历每一行，找到文件名行并从空行开始收集数据
        for i, line in enumerate(email_content):
            # 如果找到文件名行，则继续查找直到空行
            if b"filename" in line:
                # 从文件名行开始，继续往下找空行
                for j in range(i + 1, len(email_content)):
                    next_line = email_content[j].strip()
                    if next_line == b"":  # 空行，代表 Base64 数据的开始
                        start = True
                        continue

                    # 开始收集 Base64 数据，直到遇到下一个分隔符
                    if start:
                        if b"------=" in email_content[j]:
                            # 拼接并解码 Base64 数据
                            attachment_base64_data = b''.join(collected_lines).decode('utf-8')
                            attachment_bin_data = base64.b64decode(attachment_base64_data)  # 解码 Base64 获得二进制数据

                            # 使用正则表达式提取文件名
                            if list_index < len(decoded_attachment_file_header_list):
                                match = EmailPatterns.PAT_DECODED_ATTACHMENT_FILENAME.search(decoded_attachment_file_header_list[list_index])
                                if match:
                                    decoded_attachment_filename = match.group(1)
                                else:
                                    decoded_attachment_filename = f"attachment_{list_index}.bin"
                                list_index += 1  # 递增索引
                            else:
                                # 提供一个默认的文件名，以防解析不到
                                decoded_attachment_filename = f"attachment_{list_index}.bin"
                                print("Warning: list_index 超出了 decoded_attachment_file_header_list 的范围，使用默认文件名")

                            # 调用解码函数处理附件
                            EmailDecoder.decode_attachment_base64(attachment_bin_data, decoded_attachment_filename)
                            print(f"\nGet Attachment: {decoded_attachment_filename}")

                            collected_lines = []
                            start = False
                            break

                        collected_lines.append(email_content[j])

    # 获取邮件未解码内容，并存储至 Email Content.txt
    def get_content(self, email_index):
        """获取原邮件数据，写入文件"""
        email_content = self.read_email.retr(email_index)[1] # response, contents(list), octets
        print("\nEmail Content:")
        with open ("Email Content.txt", "wb") as email_file:
            email_file.write(b'\n'.join(email_content))

    # 获取邮件头信息（From、To、Date、Subject）
    def get_email_head_info(self,email_index) -> tuple:
        email_content = self.read_email.retr(email_index)[1] # response, contents(list), octets

        decoded_list = {
            "decoded_from": None,
            "decoded_to_list": [],
            "decoded_date": None,
            "decoded_subject": None
        }

        for line in email_content:
            if EmailPatterns.PAT_FROM.search(line):
                decoded_list["decoded_from"] = EmailDecoder.check_mime_format(EmailPatterns.PAT_FROM, line)

            if EmailPatterns.PAT_TO.search(line):
                decoded_to = EmailDecoder.check_mime_format(EmailPatterns.PAT_TO, line)
                decoded_list["decoded_to_list"].append(decoded_to)

            if EmailPatterns.PAT_DATE.search(line):
                decoded_list["decoded_date"] = EmailDecoder.check_mime_format(EmailPatterns.PAT_DATE, line)

            if EmailPatterns.PAT_SUBJECT.search(line):
                decoded_list["decoded_subject"] = EmailDecoder.check_mime_format(EmailPatterns.PAT_SUBJECT, line)

        return decoded_list

    # 获取邮件正文文本
    def get_text_content(self, email_index) -> str:
        email_content = self.read_email.retr(email_index)[1] # response, contents(list), octets

        start = False
        collected_lines = []
        list_index = 0
        final_content = ""

        for i, line in enumerate(email_content):
            if b"Content-Type: text/plain" in line:
                for j in range(i + 1, len(email_content)):
                    if b"charset" in email_content[j]:
                        charset = email_content[j].split(b"charset=")[1].strip(b'"').decode('utf-8')

                    next_line = email_content[j].strip()
                    if next_line == b"":  # 空行，代表 Base64 数据的开始
                        start = True
                        continue

                    # 开始收集 Base64 数据，直到遇到下一个分隔符
                    if start:
                        if b"------=" in email_content[j]:
                            # 拼接并解码 Base64 数据
                            content_text_base64 = b''.join(collected_lines).decode('utf-8')
                            final_content = EmailDecoder.decode_content_base64(content_text_base64,charset)
                            print(f"\nFinal Content:\n{final_content}")

                            collected_lines = []
                            start = False
                            break

                        collected_lines.append(email_content[j])
        return final_content

    # 列出邮箱内所有邮件
    def get_email_list(self):
        self.emails_num = self.read_email.stat()[0]  # 获取邮箱状态
        for i in range(1, self.emails_num + 1): # 邮件的编号是从 1 开始的
            decoded_list = EmailReceiver.get_email_head_info(self,i)
            print(f"Receive Email:{i}")
            print(f"Email {decoded_list["decoded_from"]}")
            print(f"Email {decoded_list["decoded_to_list"]}")
            print(f"Email {decoded_list["decoded_date"]}")
            print(f"Email {decoded_list["decoded_subject"]}")
            print(f"\n")

def receive_main(email_index):
    MyEmail = EmailReceiver(EMAIL_ADDRESS, PASSWORD, POP_SERVER)
    MyEmail.pop_connect()
    MyEmail.get_emailbox_state()
    MyEmail.get_email_list()
    MyEmail.get_content(email_index)
    MyEmail.get_email_head_info(email_index)
    MyEmail.get_attachment_content(email_index)
    MyEmail.get_text_content(email_index)

def send_main():
    ToSend = EmailSender()
    ToSend.stmp_send_text_email()

if __name__ == "__main__":
    EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
    PASSWORD = os.environ["PASSWORD"]
    SMTP_PASS = os.environ["SMTP_PASS"]
    SMTP_USER = os.environ["SMTP_USER"]

    SMTP_FROM = EmailDecoder.parse_email_tuple(os.environ["SMTP_FROM"])  # 解析成元组 # Tuple:(Real Name,Email Address)
    SMTP_TO = EmailDecoder.parse_email_tuple(os.environ["SMTP_TO"])  # 解析成元组 # Tuple:(Real Name,Email Address)

    POP_SERVER = "pop.qq.com"
    SMTP_HOST = "smtp.qq.com"

    receive_main(email_index = 12)