#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com


from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib

smtp_server_gmail = 'smtp.gmail.com'
smtp_port_gmail = 587

smtp_server_qq = 'smtp.qq.com'
smtp_port_qq = 465

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def _get_suffix(file_path):
    temp = str(file_path).split(".")
    return temp[len(temp) - 1]


def _get_file_name(file_path):
    str_path = str(file_path).split(".")
    if len(str_path) < 2:
        raise AttributeError("file path error.")
    temp = str_path[len(str_path) - 2]
    i = len(temp) - 1
    while i >= 0:
        if temp[i] == "/":
            break
        elif temp[i] == "\\":
            break
        else:
            i = i - 1
    return temp[i + 1:]


def send_gmail(from_addr, password, to_addr, content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_gmail_html(from_addr, password, to_addr, html_content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_gmail_attach(from_addr, password, to_addr, content, subject, file_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(file_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in file_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('file', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        tag = tag + 1
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_gmail_images(from_addr, password, to_addr, content, subject, image_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(image_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in image_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('image', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
                            '<p><img src="cid:%s"></p>' +
                            '</body></html>' % str(tag), 'html', 'utf-8'))
        tag = tag + 1
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()



def send_qq(from_addr, password, to_addr, content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_qq_html(from_addr, password, to_addr, html_content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_qq_attach(from_addr, password, to_addr, content, subject, file_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(file_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in file_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('file', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        tag = tag + 1
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_qq_images(from_addr, password, to_addr, content, subject, image_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(image_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in image_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('image', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
                            '<p><img src="cid:%s"></p>' +
                            '</body></html>' % str(tag), 'html', 'utf-8'))
        tag = tag + 1
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

