#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Envio de gráfico por WhatsApp, Telegram e Email através do ZABBIX (Send zabbix alerts graph WhatsApp, Telegram e Mail)
#
# Copyright (C) <2016>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contacts:
# Eracydes Carvalho (Sansão Simonton) - Monitoring Specialist - Telegram: @sansaoipb
# Thiago Paz - NOC Analyst - thiagopaz1986@gmail.com

import os
import re
import sys
import time
import json
import smtplib
from time import sleep

if len(sys.argv) == 1:
    sys.argv.append("-h")

elif len(sys.argv) == 3:
    if re.match("-\d+_\d+", sys.argv[2]):
        sys.argv[2] = sys.argv[2].replace("_", " ")

import urllib3
import requests
from pyrogram import Client
from pyrogram.raw.functions.channels import GetForumTopics
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, BadRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import argparse

import configparser

conf = configparser

from base64 import b64encode, b64decode
from urllib.parse import quote

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


class PropertiesReaderX:
    config = None

    def __init__(self, pathToProperties):
        PropertiesReaderX.config = conf.RawConfigParser()
        PropertiesReaderX.config.read(pathToProperties)

    def getValue(self, section, key):
        # type: (object, object) -> object
        return PropertiesReaderX.config.get(section, key)


path = "{0}".format("/".join(sys.argv[0].split("/")[:-1]))
if sys.platform.startswith('win32') or sys.platform.startswith('cygwin') or sys.platform.startswith(
        'darwin'):  # para debug quando estiver no WINDOWS ou no MAC
    path = path + "{0}"

else:
    path = path + "/{0}"

# '''
urlConfig = "https://raw.githubusercontent.com/sansaoipb/Graphical_notifications_Zabbix/main/configScripts.properties"
configDefault = requests.get(urlConfig).text.replace("\r", "")
arqConfig = path.format('configScripts.properties')
if not os.path.exists(arqConfig):
    contArq = configDefault

else:
    fileIn = f"{configDefault}".split("\n")

    with open(arqConfig, "r") as f:
        fileOut = f.read()

    contArq = ""
    for lineIn in fileIn:
        linhaIn = re.search(f"(^[a-z.]+) ?= ?(.*)", lineIn)
        if linhaIn:
            keyIn = linhaIn.group(1).rstrip()
            lineOut = re.search(f"\n({keyIn}) ?= ?(.*)", fileOut)
            if lineOut:
                keyOut = lineOut.group(1).split("=")[0].strip().rstrip()
                if keyIn == keyOut:
                    # lineOut = re.search(f"\n({keyIn}) ?= ?(.*)", fileOut).group().strip()
                    lineOut = lineOut.group().strip()
                    if " = " not in lineOut:
                        lineOut = lineOut.replace('=', ' = ')
                    contArq += f"{lineOut}\n"
                else:
                    valueIn = re.search(f"\n({keyIn}) ?= ?(.*)", fileOut).group(2).strip()
                    lineOut = lineOut.group().replace(keyOut, keyIn).strip()
                    if " = " not in lineOut:
                        lineOut = lineOut.replace('=', ' = ')

                    contArq += f"{lineOut}\n"

            else:
                contArq += f"{lineIn}\n"
            continue

        contArq += f"{lineIn}\n"

    contArq = contArq.rstrip()

with open(arqConfig, "w") as f:
    f.writelines(contArq)
# '''

# Zabbix settings | Dados do Zabbix ####################################################################################
zbx_server = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'url')
zbx_user = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'user')
zbx_pass = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'pass')

# Graph settings | Configuracao do Grafico #############################################################################
height = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection',
                                                                             'height')  # Graph height | Altura
width = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection',
                                                                            'width')  # Graph width  | Largura
graph_path = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram',
                                                                                 'path.graph')  # Path where graph file will be save temporarily

# Salutation | Saudação ################################################################################################
Salutation = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'salutation')
if re.search("(sim|s|yes|y)", str(Salutation).lower()):
    hora = int(time.strftime("%H"))

    if hora < 12:
        salutation = 'Bom dia'
    elif hora >= 18:
        salutation = 'Boa noite'
    else:
        salutation = 'Boa tarde'
else:
    salutation = ""

if zbx_server.endswith("/"):
    zbx_server = zbx_server[:-1]


def keepass(value=None):
    import random
    char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#-_=+,.;:?"
    passwd = ""
    if value:
        char1 = value
    else:
        char1 = len(char)

    while len(passwd) != char1:
        passwd += random.choice(char)
    return passwd


def encrypt(key, source, encode=True):
    source = source.encode("ISO-8859-1")
    key = SHA256.new(key.encode("ISO-8859-1")).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return b64encode(data).decode("ISO-8859-1") if encode else data


def decrypt(key, source, decode=True):
    if decode:
        source = b64decode(source.encode("ISO-8859-1"))
    key = SHA256.new(key.encode("ISO-8859-1")).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding].decode("ISO-8859-1")  # remove the padding


def load_json(File):
    with open(File, 'r') as f:
        return json.load(f)


def write_json(fileName, Json):
    with open(fileName, 'w') as f:
        json.dump(Json, f, ensure_ascii=False, indent=True)


# Diretórios
# Log path | Diretório do log
projeto = sys.argv[0].split("/")[-1:][0].split(".")[0]
logName = '{0}.log'.format(projeto)
pathLogs = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'path.logs')

if "default" == pathLogs.lower():
    pathLogs = path.format("log")

arqLog = "{0}".format(os.path.join(pathLogs, logName))

if not os.path.exists(pathLogs):
    os.makedirs(pathLogs)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
arqJson = ".env.json"
fileX = os.path.join(pathLogs, arqJson)
fileC = """{
    "code": false,
    "general": {
            "user": false,
            "pass": false
    },
    "email": {
            "smtp.server": false,
            "mail.user": false,
            "mail.pass": false
    },
    "telegram": {
            "api.id": false,
            "api.hash": false
    },
    "whatsapp": {
        "line": false,
        "acess.key": false,
        "port": false,
        "open.source.url": false,
        "open.source.token": false
    },
    "proxy": {
        "proxy.hostname": false,
        "proxy.port": false,
        "proxy.username": false,
        "proxy.password": false
    }
}"""

if os.path.exists(fileX):
    with open(fileX, "r") as f:
        fileOutX = f.read()

    dictOutX = json.loads(fileOutX)
    updated_dict = {}
    if "general" not in fileOutX or "proxy" not in fileOutX:
        if "general" not in fileOutX:
            general = {"general": {"user": False, "pass": False}}
            for k, v in dictOutX.items():
                updated_dict[k] = v
                if k == "code":
                    updated_dict.update(general)

        if "proxy" not in fileOutX:
            updated_dict.update({
                "proxy": {
                    "proxy.hostname": False,
                    "proxy.port": False,
                    "proxy.username": False,
                    "proxy.password": False
                }
            })
    else:
        updated_dict = dictOutX

    write_json(fileX, updated_dict)

import logging.config

file = """{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s][%(levelname)s] - %(message)s"
        }
    },

    "handlers": {
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 5242880,
            "backupCount":5,
            "level": "INFO",
            "formatter": "simple",
            "filename": "python_logging.log",
            "encoding": "utf8"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["file_handler"]
    }
}
"""

arqConfig = "logging_configuration.json"
pathDefault = ""


class Log:
    @staticmethod
    def writelog(entry, pathfile, log_level):
        global pathDefault

        try:
            Log.log(entry, pathfile, log_level)
        except Exception:
            try:
                pathDefault = f"{pathLogs}/"
                # arquivo = open("{0}{1}".format(pathDefault, arqConfig), "w")
                # arquivo.writelines(file)
                # arquivo.close()

                with open(f"{pathDefault}{arqConfig}", "w") as f:
                    f.write(file.rstrip())

                Log.log(entry, pathfile, log_level)
            except Exception:
                pass

    @staticmethod
    def log(entry, pathfile, log_level):
        logging.getLogger('suds.client').setLevel(logging.CRITICAL)
        logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)
        with open("{0}{1}".format(pathDefault, arqConfig), 'r+') as logging_configuration_file:
            config_dict = json.load(logging_configuration_file)
            config_dict["handlers"]["file_handler"]['filename'] = pathfile
        logging.config.dictConfig(config_dict)
        logger = logging.getLogger(__name__)
        logging.getLogger("suds").setLevel(logging.CRITICAL)

        if log_level.upper() == "INFO":
            logger.info(str(entry))
        elif log_level.upper() == "WARNING":
            logger.warning(str(entry))
        elif log_level.upper() == "CRITICAL":
            logger.critical(str(entry))
        elif log_level.upper() == "ERROR":
            logger.error(str(entry))


log = Log

nograph = "--nograph"


def destinatarios(dests):
    destinatario = ["{0}".format(dest).strip().rstrip() for dest in dests.split(",")]
    return destinatario


def getProxy():
    Proxy = {}
    validaProxy = {0: 'hostname', 1: 'port', 2: 'username', 3: 'password'}

    proxyHostname = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionProxy',
                                                                                        'proxy.hostname')
    proxyPort = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionProxy', 'proxy.port')
    proxyUsername = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionProxy',
                                                                                        'proxy.username')
    proxyPassword = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionProxy',
                                                                                        'proxy.password')

    validaVars = [proxyHostname, proxyPort, proxyUsername, proxyPassword]
    for y in range(len(validaVars)):
        if not re.search("no", f"{validaVars[y]}"):
            valor = validaVars[y]
            if y == 1:
                valor = int(validaVars[y])

            Proxy[validaProxy[y]] = valor

    if not Proxy:
        Proxy = None

    return Proxy


def send_mail(dest, itemType, get_graph):
    # Mail settings | Configrações de e-mail ###########################################################################
    mail_from = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.from')
    smtp_server0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail',
                                                                                       'smtp.server')
    mail_user0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.user')
    mail_pass0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.pass')
    ####################################################################################################################

    try:
        smtp_server = decrypt(codeKey, smtp_server0)
    except:
        smtp_server = smtp_server0

    try:
        mail_user = decrypt(codeKey, mail_user0)
    except:
        mail_user = mail_user0

    try:
        mail_pass = decrypt(codeKey, mail_pass0)
    except:
        mail_pass = mail_pass0

    try:
        mail_from = email.utils.formataddr(tuple(mail_from.replace(">", "").split(" <")))
    except:
        mail_from = mail_from

    dests = ', '.join(dest)
    msg = body
    msg = msg.replace("\\n", "").replace("\n", "<br>")
    try:
        Subject = re.sub(r"(<(\/)?[a-z]>)", "", subject)
    except:
        Subject = subject

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = Subject
    msgRoot['From'] = mail_from
    msgRoot['To'] = dests

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    saudacao = salutation
    if saudacao:
        saudacao = "<p>{0},</p>".format(salutation)
    else:
        saudacao = ""

    text = '{0}<p>{1}</p>'.format(saudacao, msg)

    if re.search("(0|3)", itemType):
        URL = urlGraph.replace("width=900&height=200", "width=1400&height=300")
        text += f'<br><a href="{URL}"><img src="cid:image1"></a>'
        msgImage = MIMEImage(get_graph.content)
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

    msgText = MIMEText(text, 'html', _charset='utf-8')
    msgAlternative.attach(msgText)

    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.ehlo()

        try:
            smtp.starttls()
        except Exception:
            pass

        if "SeuEmail@gmail.com" != mail_user:
            try:
                smtp.login(mail_user, mail_pass)
            except smtplib.SMTPAuthenticationError as msg:
                print("Error: Unable to send email | Não foi possível enviar o e-mail - {0}".format(
                    msg.smtp_error.decode("utf-8").split(". ")[0]))
                log.writelog('Error: Unable to send email | Não foi possível enviar o e-mail - {0}'.format(
                    msg.smtp_error.decode("utf-8").split(". ")[0]), arqLog, "WARNING")
                smtp.quit()
                exit()
            except smtplib.SMTPException:
                pass

        try:
            smtp.sendmail(mail_from, dest, msgRoot.as_string())
        except Exception as msg:
            print("Error: Unable to send email | Não foi possível enviar o e-mail - {0}".format(
                msg.smtp_error.decode("utf-8").split(". ")[0]))
            log.writelog('Error: Unable to send email | Não foi possível enviar o e-mail - {0}'.format(
                msg.smtp_error.decode("utf-8").split(". ")[0]), arqLog,
                "WARNING")
            smtp.quit()
            exit()

        print("Email sent successfully | Email enviado com sucesso ({0})".format(dests))
        log.writelog('Email sent successfully | Email enviado com sucesso ({0})'.format(dests), arqLog, "INFO")
        smtp.quit()
    except smtplib.SMTPException as msg:
        print("Error: Unable to send email | Não foi possível enviar o e-mail ({0})".format(msg))
        log.writelog('Error: Unable to send email | Não foi possível enviar o e-mail ({0})'.format(msg), arqLog,
                     "WARNING")
        logout_api()
        smtp.quit()
        exit()


def send_telegram(dest, itemType, get_graph, triggerid, valueProxy):
    # Telegram settings | Configuracao do Telegram #####################################################################
    api_id0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.id')
    api_hash0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.hash')
    ####################################################################################################################

    try:
        api_id = int(decrypt(codeKey, api_id0))
    except:
        api_id = api_id0

    try:
        api_hash = str(decrypt(codeKey, api_hash0))
    except:
        api_hash = api_hash0

    app = Client("SendGraph", api_id=api_id, api_hash=api_hash, proxy=valueProxy)

    saudacao = salutation
    if saudacao:
        # saudacao = salutation + " {0} \n\n"
        saudacao = salutation + " <b><u>{0}</u></b> \n\n"
    else:
        saudacao = ""

    dest = dest.lower()
    topic = None
    if re.match(r"-\d+ \d+", dest):
        dest, topic = dest.split(" ")
        topic = int(topic)

    elif re.search("user#|chat#|\'|\"", dest):
        if "#" in dest:
            dest = dest.split("#")[1]

        elif dest.startswith("\"") or dest.startswith("\'"):
            dest = dest.replace("\"", "").replace("\'", "")

    elif dest.startswith("@"):
        dest = dest[1:]

    with app:
        flag = True
        while flag:
            try:
                Contatos = app.get_contacts()
                for contato in Contatos:
                    Id = f"{contato.id}"
                    nome = f"{contato.first_name}"
                    if contato.last_name:
                        nome += f" {contato.last_name}"

                    username = contato.username.lower()
                    if username:
                        if username in dest or dest in Id or dest in nome.lower():
                            dest = nome
                            flag = False
                            break
                    else:
                        if dest in Id or dest in nome.lower():
                            dest = nome
                            flag = False
                            break
            except:
                pass

            try:
                if flag:
                    Dialogos = app.get_dialogs()
                    for dialogo in Dialogos:
                        Id = f"{dialogo.chat.id}"
                        if dialogo.chat.title:
                            nome = f"{dialogo.chat.title}"
                        else:
                            nome = f"{dialogo.chat.first_name}"
                            if dialogo.chat.last_name:
                                nome += f" {dialogo.chat.last_name}"

                        username = dialogo.chat.username
                        if username:
                            if username in dest or dest in Id or dest in nome.lower():
                                dest = nome
                                flag = False
                                break
                        else:
                            if dest in Id or dest in nome.lower():
                                dest = nome
                                flag = False
                                break
            except:
                flag = False
                try:
                    if re.match("^([0-9-]+)$", dest):
                        dest = int(dest)
                    chat = app.get_chat(dest)
                    Id = "{}".format(chat.id)

                    if chat.title:
                        dest = f"{chat.title}"
                    else:
                        dest = f"{chat.first_name}"
                        if chat.last_name:
                            dest += f" {chat.last_name}"

                except Exception as msg:
                    print(msg.args[0])
                    log.writelog(f'{msg.args[0]}', arqLog, "ERROR")
                    exit()

        Id = int(Id)
        sendMsg = """{}{}\n{}""".format(saudacao.format(dest), subject, body)
        if re.search("(0|3)", itemType):
            try:
                # graph = '{0}/{1}.png'.format(graph_path, triggerid)
                graph = os.path.join(os.getcwd() if os.name == "nt" else graph_path, f'{triggerid}.png')
                with open(graph, 'wb') as png:
                    png.write(get_graph.content)
            except BaseException as e:
                log.writelog(
                    '{1} >> An error occurred at save graph file in {0} | Ocorreu um erro ao salvar o grafico no diretório {0}'.format(
                        graph_path, str(e)), arqLog, "WARNING")
                logout_api()
                exit()

            try:
                app.send_photo(Id, graph, caption=sendMsg, reply_to_message_id=topic)
                print(
                    'Telegram sent photo message successfully | Telegram com gráfico enviado com sucesso ({0})'.format(
                        dest))
                log.writelog(
                    'Telegram sent photo message successfully | Telegram com gráfico enviado com sucesso ({0})'.format(
                        dest), arqLog, "INFO")
            except Exception as e:
                print(
                    'Telegram FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo telegram\n%s' % e)
                log.writelog(
                    '{0} >> Telegram FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo telegram ({1})'.format(
                        e, dest), arqLog, "ERROR")
                logout_api()
                exit()

            try:
                os.remove(graph)
            except Exception as e:
                print(e)
                log.writelog('{0}'.format(str(e)), arqLog, "ERROR")

        else:
            try:
                app.send_message(Id, sendMsg, reply_to_message_id=topic)
                print('Telegram sent successfully | Telegram enviado com sucesso ({0})'.format(dest))
                log.writelog('Telegram sent successfully | Telegram enviado com sucesso ({0})'.format(dest), arqLog,
                             "INFO")
            except Exception as e:
                print('Telegram FAIL at sending message | FALHA ao enviar mensagem pelo telegram\n%s' % e)
                log.writelog(
                    '{0} >> Telegram FAIL at sending message | FALHA ao enviar mensagem pelo telegram ({1})'.format(e,
                                                                                                                    dest),
                    arqLog, "ERROR")
                logout_api()
                exit()


def send_whatsapp_pay(itemType, graph, acessKey, url_base, message, line, destiny):
    message = quote(b64encode(message.encode("utf-8")))
    if re.search("(0|3)", itemType):
        Graph = quote(graph)
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = 'app=NetiZap%20Consumers%201.0&key={key}&text={text}&type=PNG&stream={stream}&filename=grafico'.format(
                key=acessKey, text=message, stream=Graph)
            url = f"{url_base}/file_send?line={line}&destiny={destiny}"
            result = requests.post(url, auth=("user", "api"), headers=headers, data=payload)

            if result.status_code != 200:
                texto = 'WhatsApp FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo WhatsApp{}'
                error = json.loads(result.content.decode("utf-8"))['errors'][0]['message']
                log.writelog('{0}'.format(error), arqLog, "ERROR")
                print(texto.format(f"\n{error}"))

            else:
                texto = f'WhatsApp sent photo message successfully | WhatsApp com gráfico enviado com sucesso ({destiny})'
                try:
                    result_str = json.loads(result.text)["result"]
                except KeyError:
                    texto = 'WhatsApp FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo WhatsApp{}'
                    result_str = result.text

                log.writelog(texto, arqLog, "INFO")
                log.writelog('{0}'.format(result_str), arqLog, "INFO")
                print(texto.format(result_str))

        except Exception as e:
            log.writelog('{0}'.format(str(e)), arqLog, "ERROR")
            exit()
    else:
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = 'App=NetiZap%20Consumers%201.0&AccessKey={}'.format(acessKey)
            url = f"{url_base}/message_send?line={line}&destiny={destiny}&reference&text={message}"
            result = requests.post(url, auth=("user", "api"), headers=headers, data=payload)

            if result.status_code != 200:
                error = json.loads(result.content.decode("utf-8"))['errors'][0]['message']
                log.writelog('{0}'.format(error), arqLog, "ERROR")

            else:
                texto = f'WhatsApp sent successfully | WhatsApp enviado com sucesso ({destiny})'
                try:
                    result_str = json.loads(result.text)["result"]
                except KeyError:
                    texto = 'WhatsApp FAIL at sending message | FALHA ao enviar mensagem pelo WhatsApp{}'
                    result_str = result.text

                log.writelog(texto, arqLog, "INFO")
                log.writelog('{0}'.format(result_str), arqLog, "INFO")
                print(texto.format(result_str))

        except Exception as e:
            log.writelog('{0}'.format(str(e)), arqLog, "ERROR")
            exit()


def send_whatsapp_free(token_wa, itemType, graph, url_base, message, destiny, saudacao):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_wa}"
    }
    Get_WA = get_WhatsApp(headers, f'{url_base}/all-groups')
    status_Group = [group for group in Get_WA if destiny == group['id']['user']]

    isGroup = True
    if not status_Group:
        isGroup = False

    groupName = status_Group[0]['name']
    if saudacao:
        saudacao, _ = saudacao.split(".")
        message = message.replace(saudacao, f"{saudacao}, {groupName}")

    data = {
        "phone": destiny,
        "isGroup": isGroup,
        "message": message.replace("\\n", "\n"),
    }

    if re.search("(0|3)", itemType):
        data["caption"] = data.pop("message")
        data["base64"] = f'data:image/png;base64,{graph.decode()}'
        url = f'{url_base}/send-image'

    else:
        url = f'{url_base}/send-message'

    try:
        result = requests.post(url, json=data, headers=headers)
        if result.status_code != 201:
            texto = 'WhatsApp FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo WhatsApp\n{}'
            error = json.loads(result.content.decode("utf-8"))['error']['name']
            log.writelog('{0}'.format(error), arqLog, "ERROR")
            print(texto.format(error))

        else:
            texto = f'WhatsApp sent photo message successfully | WhatsApp com gráfico enviado com sucesso ({groupName})'
            log.writelog(texto, arqLog, "INFO")
            r = json.loads(result.text)
            log.writelog('{}: {}'.format(r["status"], r['response']), arqLog, "INFO")
            print(texto)

    except Exception as e:
        log.writelog('{0}'.format(str(e)), arqLog, "ERROR")
        exit()


def send_whatsapp(destiny, itemType, get_graph):
    # WhatsApp settings | Configuracao do WhatsApp #####################################################################
    line0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'line')
    acessKey0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'acess.key')
    port0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'port')

    # WhatsApp Open source | Codigo aberto WhatsApp ####################################################################
    wa_free = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'open.source')
    url_base_free0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                         'open.source.url')
    api_token0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                     'open.source.token')
    ####################################################################################################################

    try:
        line = decrypt(codeKey, line0)
    except:
        line = line0

    try:
        acessKey = decrypt(codeKey, acessKey0)
    except:
        acessKey = acessKey0

    try:
        port = decrypt(codeKey, port0)
    except:
        port = port0

    try:
        url_base_free = decrypt(codeKey, url_base_free0)
    except:
        url_base_free = url_base_free0

    try:
        api_token = decrypt(codeKey, api_token0)
    except:
        api_token = api_token0

    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                   'salutation.whatsapp')

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = salutation + ".\\n\\n"
    else:
        saudacao = ""

    msg0 = body.replace("\r", "").split('\n ')[0].replace("\n", "\\n")
    msg = "{}\\n{}".format(subject, msg0)
    message = "{}{}".format(saudacao, msg.replace(r"✅", r"\u2705"))

    formatter = [("b", "*"), ("i", "_"), ("u", "")]
    for f in formatter:
        old, new = f
        if re.search(r"(<(/)?{}>)".format(old), message):
            message = re.sub(r"(<(/)?{}>)".format(old), r"{}".format(new), message)

    graph = get_graph
    if get_graph:
        graph = b64encode(get_graph.content)

    if re.search("(sim|s|yes|y)", str(wa_free).lower()):
        url_base = url_base_free
        send_whatsapp_free(api_token, itemType, graph, url_base, message, destiny, saudacao)
    else:
        url_base = f"http://api.meuaplicativo.vip:{port}/services"
        send_whatsapp_pay(itemType, graph, acessKey, url_base, message, line, destiny)


def send_teams(webhook, itemType, get_graph):
    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTeams',
                                                                                   'salutation.teams')

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = salutation + ".\n\n"
    else:
        saudacao = ""

    msg0 = body.replace("\\n", "").replace("\n", "\n\n")
    message = "{}\n\n{}".format(saudacao, subject, msg0)

    formatter = [("b", "**"), ("i", "_"), ("u", "")]
    for f in formatter:
        old, new = f
        if re.search(r"(<(/)?{}>)".format(old), message):
            message = re.sub(fr"(<(/)?{old}>)", new, message)

    headers = {'Content-Type': 'application/json'}
    bodyMsg = [{"type": "TextBlock", "text": message, "weight": "bolder", "wrap": True}]

    if re.search("(0|3)", itemType):
        image = b64encode(get_graph.content).decode()
        responseOk = 'Teams sent photo message successfully | Teams com gráfico enviado com sucesso\n{0}'
        responsePro = 'Teams FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo Teams\n{0}'
        bodyMsg.append({"type": "Image", "url": f"data:image/png;base64,{image}", "msTeams": {"allowExpand": True}})

    else:
        responseOk = 'Teams sent successfully | Teams enviado com sucesso ({0})'
        responsePro = 'Teams FAIL at sending message | FALHA ao enviar a mensagem pelo Teams\n{0}'

    bodyMsg.append({"type": "TextBlock", "text": body, "wrap": True})

    payload = {
        "type": "message",
        'attachments': [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": bodyMsg
            }
        }]
    }

    try:
        response = requests.post(webhook, headers=headers, json=payload)
        response.raise_for_status()

        if response.reason == 'OK':
            print(responseOk.format(webhook))
            log.writelog(responseOk.format(webhook), arqLog, "INFO")

        else:
            error = response.content.decode("utf-8")
            print(responsePro.format(error))
            log.writelog(responsePro.format(error), arqLog, "ERROR")

    except Exception as e:
        print(e)
        log.writelog('{0}'.format(str(e)), arqLog, "ERROR")
        exit()


def zbx_token():
    global zbx_user, zbx_pass
    try:
        zbx_user = decrypt(codeKey, zbx_user)
    except:
        zbx_user = zbx_user

    try:
        zbx_pass = decrypt(codeKey, zbx_pass)
    except:
        zbx_pass = zbx_pass

    credentials = {"user": zbx_user, "password": zbx_pass}
    try:
        versao_zabbix = float(version_api()[:3])
    except json.decoder.JSONDecodeError:
        print("Erro ao verificar a versão do zabbix.\ncorrija a URL no \"configScripts.properties\"")
        exit()
    if versao_zabbix >= 6.4:
        credentials["username"] = credentials.pop("user")

    try:
        login_api = requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                                  verify=False, data=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": credentials,
                    "id": 1
                }
            )
                                  )

        login_api = json.loads(login_api.text.encode('utf-8'))

        if 'result' in login_api:
            auth = login_api["result"]
            return auth

        elif 'error' in login_api:
            print('Zabbix: %s' % login_api["error"]["data"])
            log.writelog('Zabbix: {0}'.format(login_api["error"]["data"]), arqLog, "ERROR")
            exit()
        else:
            print(login_api)
            log.writelog('{0}'.format(login_api), arqLog, "ERROR")
            exit()

    except ValueError as e:
        print(
            'Check declared zabbix URL/IP and try again | Valide a URL/IP do Zabbix declarada e tente novamente\nCurrent: %s' % zbx_server)
        log.writelog(
            'Check declared zabbix URL/IP and try again | Valide a URL/IP do Zabbix declarada e tente novamente. (Current: {0})'.format(
                zbx_server), arqLog, "WARNING")
        exit()
    except Exception as e:
        print(e)
        log.writelog('{0}'.format(str(e)), arqLog, "WARNING")
        exit()


def version_api():
    resultado = requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                              verify=False, data=json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "apiinfo.version",
                "params": [],
                "id": 5
            }
        )
                              )
    resultado = json.loads(resultado.content)
    if 'result' in resultado:
        resultado = resultado["result"]
    return resultado


def logout_api():
    requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                  verify=False, data=json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.logout",
                "params": [],
                "auth": auth,
                "id": 4
            }
        )
                  )


def getgraph(period):
    global urlGraph
    # Graph start time [3600 = 1 hour ago]  |  Hora inicial do grafico [3600 = 1 hora atras]
    stime = int(PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'stime'))
    dictCores = {
        'FF0000': [
            'FF0000',
            'C71585',
            'FFA500',
            'FF1493',
            'FFC0CB',
            'CD5C5C',
            '8B0000',
            'FFD700',
            '800080',
            'DA70D6',
            'FA8072',
            'FF69B4',
            'DB7093',
            'FFB6C1',
            'FF00FF',
            'EE82EE',
            'FF6347',
            'F08080',
            'B22222',
            'DC143C',
        ],
        '00C800': [
            '008000',
            '00FF00',
            '6B8E23',
            '0000FF',
            '00FFFF',
            '4169E1',
            '7FFFD4',
            '32CD32',
            '708090',
            '00FF7F',
            '66CDAA',
            '40E0D0',
            '008B8B',
            '00BFFF',
            '4682B4',
            'B0C4DE',
            '2E8B57',
            '9ACD32',
            '98FB98',
            '90EE90'
        ]
    }

    try:
        loginpage = requests.get(f'{zbx_server}/index.php', auth=(zbx_user, zbx_pass), verify=False).text
        enter = re.search('<button.*value=".*>(.*?)</button>', loginpage)
        s = requests.Session()

        try:
            enter = str(enter.group(1))
            s.post(f'{zbx_server}/index.php?login=1', params={'name': zbx_user, 'password': zbx_pass, 'enter': enter},
                   verify=False).text
        except:
            pass

        stime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() - stime))

        if 4.0 > float(version_api()[:3]):
            period = "period={0}".format(period)
            nome_tempo = f"{{}}"

        else:
            periodD = period // 86400
            segundos_rest = period % 86400
            periodH = segundos_rest // 3600
            segundos_rest = segundos_rest % 3600
            periodM = segundos_rest // 60
            periodS = segundos_rest % 60

            Nome = f"{quote(triggerName)} {{}}"
            if periodD > 0:
                period = "from=now-{0}d-{1}h-{2}m&to=now".format(periodD, periodH, periodM)
                nome_tempo = Nome.format(f"({periodD}d {periodH}h:{periodM}m)")

            elif periodD == 0 and periodH == 0:
                period = "from=now-{0}m&to=now".format(periodM)
                nome_tempo = Nome.format(f"({periodM}m)")

            elif periodD == 0 and period % 60 == 0:
                period = "from=now-{0}h&to=now".format(periodH)
                nome_tempo = Nome.format(f"({periodH}h)")

            else:
                period = "from=now-{0}h-{1}m&to=now".format(periodH, periodM)
                nome_tempo = Nome.format(f"({periodH}h:{periodM}m)")

        urlGraph = f"{zbx_server}/chart3.php?name={hostName}: {nome_tempo}&{period}&width={width}&height={height}&stime={stime}"

        j = 0
        for i in range(len(listaItemIds)):
            try:
                cor = dictCores[color][i]
            except:
                if j == len(dictCores['00C800']):
                    j = 0
                cor = dictCores[color][j]
                j += 1

            urlGraph += f"&items[{i}][itemid]={listaItemIds[i]}&items[{i}][drawtype]=5&items[{i}][color]={cor}"

        get_graph = s.get(urlGraph)
        sid = s.cookies.items()[0][1]
        s.post(f'{zbx_server}/index.php?reconnect=1&sid={sid}')

        return get_graph

    except BaseException:
        log.writelog(
            'Can\'t connect to {0}/index.php | Não foi possível conectar-se à {0}/index.php'.format(zbx_server), arqLog,
            "CRITICAL")
        logout_api()
        exit()


def getTrigger(triggerId=None):
    try:
        limit = 8000
        triggerid = requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                                  verify=False, data=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                        "output": ["description"],
                        'triggerids': triggerId,
                        "limit": limit,
                        "selectItems": ['name', 'value_type', 'lastvalue'],
                        "selectHosts": ["name"],
                        "expandDescription": True,
                    },
                    "auth": auth,
                    "id": 3
                }
            )
                                  )

        if triggerid.status_code != 200:
            print(f"HTTPError {triggerid.status_code}: {triggerid.reason}")
            log.writelog(f'HTTPError {triggerid.status_code}: {triggerid.reason}', arqLog, "WARNING")
            logout_api()
            exit()

        resultTriggers = triggerid.content
        if not resultTriggers:
            print('User has no read permission on environment | Usuário sem permissão de leitura no ambiente')
            log.writelog('User has no read permission on environment | Usuário sem permissão de leitura no ambiente',
                         arqLog, "WARNING")
            logout_api()
            exit()

        triggerid = json.loads(resultTriggers)

        item_type = ""
        if 'result' in triggerid:

            resultado = triggerid["result"]
            if not resultado:
                print('Zabbix: Nenhuma trigger encontrada')
                log.writelog('Zabbix: Nenhum resultado encontrado', arqLog, "ERROR")
                exit()

            if triggerId:
                hostName = resultado[0]['hosts'][0]['name']
                triggerName = resultado[0]['description']
                triggerID = resultado[0]['triggerid']

                for i in range(0, len(resultado)):
                    listaItemIds = []
                    for items in resultado[i]['items']:
                        if items['lastvalue'] != '0' and items['lastvalue']:
                            if items['itemid'] not in listaItemIds:
                                listaItemIds.append(items['itemid'])

                            if not item_type:
                                item_type += items['value_type']

                    return (item_type, triggerName, triggerID, hostName, listaItemIds)

            else:
                for i in range(0, len(resultado)):
                    hostName = resultado[i]['hosts'][0]['name']
                    triggerName = resultado[i]['description']
                    triggerID = resultado[i]['triggerid']
                    listaItemIds = []
                    for items in resultado[i]['items']:
                        if items['lastvalue'] != '0' and re.match("(0|3)", items['value_type']):
                            listaItemIds.append(items['itemid'])

                            if not item_type:
                                item_type += items['value_type']

                    if listaItemIds:
                        return (item_type, triggerName, triggerID, hostName, listaItemIds)

        elif 'error' in triggerid:
            print('Zabbix: %s' % triggerid["error"]["data"])
            log.writelog('Zabbix: {0}'.format(triggerid["error"]["data"]), arqLog, "ERROR")
            exit()

        else:
            print(triggerid)
            log.writelog('{0}'.format(triggerid), arqLog, "ERROR")
            exit()

    except Exception as msg:
        print(msg)
        log.writelog('{0}'.format(msg), arqLog, "ERROR")
        exit()


def countdown(Time=3):
    print()
    message = "O processo encerrará em {:1d} {}"
    for remaining in range(Time, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(message.format(remaining, "segundos. " if remaining > 1 else "segundo. "))
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write(f"\rCompleto!{' ' * len(message)}\n")
    print()
    exit()


def get_WhatsApp(headers, url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        buscas = response.json()['response']
    except:
        buscas = None

    return buscas


def get_info_WhatsApp(name=None):
    url_base_free0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                         'open.source.url')
    api_token0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                     'open.source.token')
    ####################################################################################################################

    try:
        url_base_free = decrypt(codeKey, url_base_free0)
    except:
        url_base_free = url_base_free0

    try:
        api_token = decrypt(codeKey, api_token0)
    except:
        api_token = api_token0

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    url = f'{url_base_free}/all-contacts'
    ContA = 0
    infos = ""
    try:
        buscas = get_WhatsApp(headers, url)
        if not buscas:
            print("\nNão foi possivel conectar no WhatsApp, verifique as informações no \"configScripts.properties\"")
            exit()

        infos += ""
        if name:
            for busca in buscas:
                Id = f"Id: {busca['id']['user']}"
                try:
                    nome = f"Nome: {busca['name']}"
                except KeyError:
                    try:
                        nome = f"Nome: {busca['contact']['name']}"
                    except KeyError:
                        nome = f"Nome: {busca['formattedName']}"

                tipo = "Grupo"
                if busca['isUser']:
                    tipo = "Usuário"

                tipo = f'Tipo: {tipo}'
                if name.lower() in nome.lower() or name in Id:
                    if not infos:
                        infos += "\n####### Chats encontrados (ContA) ########################################\n\n"

                    infos += f"{tipo}\n{nome}\n{Id}\n\n"
                    ContA += 1

        else:
            infos += "\n####### Chats encontrados (ContA) ########################################\n\n"
            for busca in buscas:
                try:
                    name = busca['name']
                except KeyError:
                    try:
                        name = busca['contact']['name']
                    except KeyError:
                        name = busca['formattedName']

                tipo = "Grupo"
                if busca['isUser']:
                    tipo = "Usuário"

                nome = f"Nome: {name} ( {tipo} )"
                infos += "{}\n".format(nome)
                ContA += 1

        infos += "\n####### Chats encontrados (ContA) ########################################\n\n"
        if ContA == 1:
            infos = re.sub("Chats encontrados \(ContA\)", f"Único chat encontrado", infos)

        infos = re.sub("ContA", f"{ContA}", infos)

        if not ContA:
            infos = "\nNão há registros referente à \"{}\"\n".format(name)

        return infos
    except requests.exceptions.RequestException as msg:
        print("Erro na solicitação:\n", msg)
        log.writelog('{0}'.format(msg), arqLog, "ERROR")
        exit()


def get_info_telegram(valueProxy, name=None):
    # Telegram settings | Configuracao do Telegram #########################################################################
    api_id0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.id')
    api_hash0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.hash')

    try:
        api_id = int(decrypt(codeKey, api_id0))
    except:
        api_id = api_id0

    try:
        api_hash = str(decrypt(codeKey, api_hash0))
    except:
        api_hash = api_hash0

    app = Client("SendGraph", api_id=api_id, api_hash=api_hash, proxy=valueProxy)
    ContA = 0
    with app:
        infos = ""
        try:
            dialogos = app.get_dialogs()
            infos += ""
            if name:
                for dialogo in dialogos:
                    Topics = ""
                    tipos = {"group": "Grupo", "supergroup": "Super Grupo", "bot": "BOT", "channel": "Canal",
                             "private": "Usuário"}
                    tipo = f"Tipo: {tipos[dialogo.chat.type.value]}"
                    Id = f"Id: {dialogo.chat.id}"
                    try:
                        getTopicsForum = GetForumTopics(channel=app.resolve_peer(dialogo.chat.id), offset_topic=0,
                                                        offset_date=0, offset_id=0, limit=0)
                        validaTopics = app.invoke(getTopicsForum)
                        if validaTopics.chats[0].forum:
                            Topics += "\nTópicos:"
                            topicslist = sorted(validaTopics.topics, key=lambda Id: Id.id)
                            for topics in topicslist:
                                Topics += f"\n   - {topics.title} ( {dialogo.chat.id}_{topics.id} )"

                    except (ChannelInvalid, BadRequest):
                        pass

                    if dialogo.chat.title or '777000' in Id:
                        nome = "Nome: {}".format(dialogo.chat.title or dialogo.chat.first_name)
                    else:
                        nome = f"Nome: {dialogo.chat.first_name} "
                        if dialogo.chat.last_name:
                            nome += "{}".format(dialogo.chat.last_name)

                        if dialogo.chat.username:
                            nome += f"\nNome de usuário: {dialogo.chat.username}"

                    if name.lower() in nome.lower() or name in Id:
                        if not infos:
                            infos += "\n####### Chats encontrados (ContA) ########################################\n\n"

                        infos += f"{tipo}\n{nome}\n{Id}{Topics}\n\n"
                        ContA += 1

            else:
                infos += "\n####### Chats encontrados (ContA) ########################################\n\n"
                for dialogo in dialogos:
                    infos += "{}\n".format(dialogo.chat.title or dialogo.chat.first_name)
                    ContA += 1

            infos += "\n####### Chats encontrados (ContA) ########################################\n\n"
            if ContA == 1:
                infos = re.sub("Chats encontrados \(ContA\)", f"Único chat encontrado", infos)

            infos = re.sub("ContA", f"{ContA}", infos)

            if not ContA:
                infos = "\nNão há registros referente à \"{}\"\n".format(name)

            return infos
        except Exception as msg:
            if "BOT_METHOD_INVALID" in msg.args[0]:
                print("\nEsta função não está disponível para consultas com BOT\n")
            else:
                print(msg.args[0])

            log.writelog('{0}'.format(msg.args[0]), arqLog, "ERROR")
            exit()


def menu(listaopcoes):
    os.system('cls' if os.name == "nt" else "clear")
    print("--- Escolha uma opção do menu ---\n")
    OPCOES = [f"{opcoes}\n" for opcoes in listaopcoes]
    print("".join(OPCOES))
    print("  0 - Sair\n")

    return menu_opcao(listaopcoes)


def menu_opcao(QtOpcs):
    numeros = re.findall("(\d+)", ", ".join(QtOpcs))
    opcao = input(f"Selecione uma opção [0-{len(QtOpcs)}]: ")
    if opcao == '0':
        countdown()
        exit()

    elif opcao not in numeros:
        print("\nOPÇÃO INVÁLIDA, escolha uma numeração da lista")
        sleep(3)
        menu(QtOpcs)

    print("\nOpção selecionada:\n", QtOpcs[int(opcao) - 1].split("- ")[1])

    if not re.search("(s|y|sim|yes)", input("\nEstá correto (s/n)? ").lower()):
        menu(QtOpcs)

    os.system('cls' if os.name == "nt" else "clear")
    return opcao


def menuPrincipal():
    listaOpcoes = [
        "  1 - Telegram",
        "  2 - WhatsApp",
    ]

    return menu(listaOpcoes)


def get_info(valueProxy, name=None):
    info_get = int(menuPrincipal())

    if info_get == 1:
        r = get_info_telegram(valueProxy, name)
    else:
        r = get_info_WhatsApp(name)

    return r


def create_file():
    # import ipdb; ipdb.set_trace()
    if not os.path.exists(fileX):
        JsonX = json.loads(fileC)
        for obj in JsonX:
            if "code" == obj:
                if not JsonX[obj]:
                    JsonX[obj] = keepass()
                break
        write_json(fileX, JsonX)

    else:
        # import ipdb; ipdb.set_trace()
        JsonV = load_json(fileX)
        JsonC = json.loads(fileC)
        for obj_pai in JsonC:
            if "code" != obj_pai:
                try:
                    JsonV[obj_pai]
                except KeyError:
                    JsonV[obj_pai] = JsonC[obj_pai]

                for obj_filho in JsonC[obj_pai]:
                    try:
                        JsonV[obj_pai][obj_filho]
                    except KeyError:
                        JsonV[obj_pai][obj_filho] = JsonC[obj_pai][obj_filho]

        write_json(fileX, JsonV)
        JsonX = JsonV

    return JsonX


def get_cripto(flag=False):
    JsonX = create_file()
    # import ipdb; ipdb.set_trace()
    textK0 = []
    for obj in JsonX:
        if "code" == obj:
            if codeKey:
                JsonX[obj] = codeKey
            else:
                JsonX[obj] = keepass()
            continue
        textK = ""
        for k in JsonX[obj]:
            if JsonX[obj][k] == flag:
                if not textK:
                    textK += f"{obj}: "
                textK += f"{k}, "
                textK0 += [k]

    write_json(fileX, JsonX)

    return textK0, JsonX


def create_cripto():
    textoKey, JsonX = get_cripto()
    if textoKey:
        config = path.format('configScripts.properties')

        with open(config, "r") as f:
            contArq = f.read()

        textoKey = ", ".join(textoKey)
        print(f"\nOs seguintes campos podem ser criptografados:\n{textoKey}")
        criptoK = [str(objs).strip().rstrip() for objs in input("\ninforme quais deseja: ").split(",")]
        if [''] == criptoK:
            exit()
        for crip in criptoK:
            for js in JsonX:
                if "code" != js:
                    for k in JsonX[js]:
                        if crip == k:
                            valueR = re.search(f"\n{crip} ?= ?(.*)\n", contArq).group(1)
                            valueC = encrypt(codeKey, valueR)
                            contArq = contArq.replace(f"{valueR}", f"{valueC}")
                            JsonX[js][k] = True

        with open(config, "w") as f:
            f.write(contArq.rstrip())

        write_json(fileX, JsonX)

    else:
        print(f"\nNão há campos para criptografar.\n")
        exit()


def update_crypto(tag):
    pre = f"{'re' if 're' == tag else 'des'}"
    textoKey, JsonX = get_cripto(flag=True)
    if not textoKey:
        print(f"\nNão há campos para {pre}criptografar.\n")
        exit()

    config = path.format('configScripts.properties')

    with open(config, "r") as f:
        contArq = f.read().replace("email_from", "mail.from").replace("smtp_server",
                                                                      "smtp.server").replace("mail_", "mail.")

    textoKey = ", ".join(textoKey)
    print(f"\nOs seguintes campos podem ser {pre}criptografados:\n{textoKey}")
    criptoK = [str(objs).strip().rstrip() for objs in input("\ninforme quais deseja: ").split(",")]
    if [''] == criptoK:
        exit()
    for crip in criptoK:
        for js in JsonX:
            if "code" != js:
                for k in JsonX[js]:
                    if crip == k:
                        valueR = re.search(f"\n{crip} ?= ?(.*)\n", contArq).group(1)
                        if 'de' == tag:
                            valor = valueR
                            valueC = decrypt(codeKey, valor)
                            JsonX[js][k] = False
                        else:
                            valor = input(f"\nAgora informe um valor para o campo '{crip}': ")
                            valueC = encrypt(codeKey, valor)

                        contArq = contArq.replace(f"{valueR}", f"{valueC}")

    with open(config, "w") as f:
        f.write(contArq.rstrip())

    write_json(fileX, JsonX)


def multi_input():
    try:
        while True:
            data = map(str, input("").split("\n"))
            if not data:
                break
            yield data
    except KeyboardInterrupt:
        return


def input_complete(input_list):
    if "--test" in input_list[-1]:
        return True
    else:
        return False


def get_input(prompt1, prompt2):
    L = list()
    prompt = prompt1
    while True:
        L.append(input(prompt))
        if input_complete(L):
            return "\n".join(L).replace("--test", "").strip()
        prompt = prompt2


def send(msg=False):
    global subject, body, listaItemIds, triggerName, hostName, period, color, item_type, triggerid
    try:

        if msg:
            subject = input("Digite o 'Assunto': ")
            message = get_input("\nDigite a 'Mensagem' terminando com '--test': ", " ")
            triggerid, eventid, color, period, body = message.split('#', 4)
            period = int(period)

            item_type, triggerName, triggerid, hostName, listaItemIds = getTrigger(triggerid)

        else:
            item_type, triggerName, triggerid, hostName, listaItemIds = getTrigger()
            subject = '<b>testando o envio com o item</b>:'
            color = '00C800'
            period = 3600
            body = '{0}'.format(triggerName)

    except Exception as msg:
        print(msg)
        log.writelog(''.format(msg), arqLog, "WARNING")

    return triggerid, item_type, period


def main2(proxy, test=None):
    inicio = time.time()
    triggerid, item_type, period = send(test)
    try:

        dest = sys.argv[2]
        destino = destinatarios(dest)

        if nograph in sys.argv:
            item_type = "1"
            get_graph = ""
        else:
            get_graph = getgraph(period)

        emails = []
        for x in destino:
            if re.match("^(\d+(-)?\d+(@g\.us)?|\d{12,25})$", x):
                send_whatsapp(x, item_type, get_graph)

            elif re.search("webhook.office.com", x.lower()):
                send_teams(x, item_type, get_graph)

            elif re.search("^.*@[a-z0-9-]+\.[a-z]+(\.[a-z].*)?$", x.lower()):
                emails.append(x)

            else:
                send_telegram(x, item_type, get_graph, triggerid, proxy)

        if emails:
            send_mail(emails, item_type, get_graph)

        fim = time.time()
        total = fim - inicio
        print("\nTempo de execução do script: {:.2f}{}\n".format(total if total > 1 else 1000 * total,
                                                                 's' if total > 1 else 'ms'))

    except Exception as msg:
        print(msg)
        log.writelog(''.format(msg), arqLog, "WARNING")


def main():
    global auth, codeKey
    JSON = create_file()
    codeKey = JSON['code']
    proxy = getProxy()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--infoAll', action="store_true", help="Consult all information")
    parser.add_argument('-e', '--encrypt', action="store_true", help="Encrypt information")
    parser.add_argument('-d', '--decrypt', action="store_true", help="Decrypt information")
    parser.add_argument('-r', '--reEncrypt', action="store_true", help="Re-encrypt information")
    parser.add_argument('-i', '--info', action="store", dest="contact", help="Consult specific user/chat information")
    parser.add_argument('-s', '--send', action="store", dest="destiny", help="Send test")
    parser.add_argument('-t', '--test', action="store", dest="argvs_Environment", help="Send test environment")

    nome = None
    try:
        args = parser.parse_args()
    except:
        print("\n")
        exit()

    if args.encrypt:
        create_cripto()
        exit()

    elif args.reEncrypt:
        update_crypto('re')
        exit()

    elif args.decrypt:
        update_crypto('de')
        exit()

    elif args.destiny:
        auth = zbx_token()
        main2(proxy)
        logout_api()
        exit()

    elif args.argvs_Environment:
        auth = zbx_token()
        main2(proxy, True)
        logout_api()
        exit()

    elif args.contact:
        nome = args.contact

    r = get_info(proxy, nome)
    print(r)
    exit()


if __name__ == '__main__':
    main()
