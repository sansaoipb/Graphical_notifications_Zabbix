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

if len(sys.argv) <= 2 or "--send" in sys.argv:
    dest0 = "||".join(sys.argv).split("--send")[1].replace("||", "")
    print(
        f"\nEste script é pra ser executado pelo ZABBIx e não manualmente.\nPara realização de teste use o script:\n\nsudo -u zabbix ./notificacoes-teste.py --send {dest0}\n")
    exit()

import urllib3
import requests
from pyrogram import Client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import configparser

conf = configparser

from base64 import b64encode, b64decode
from urllib.parse import quote


class PropertiesReaderX:
    config = None

    def __init__(self, pathToProperties):
        PropertiesReaderX.config = conf.RawConfigParser()
        PropertiesReaderX.config.read(pathToProperties)

    def getValue(self, section, key):
        # type: (object, object) -> object
        return PropertiesReaderX.config.get(section, key)


path = "{0}".format("/".join(sys.argv[0].split("/")[:-1]) + "/{0}")

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin') or sys.platform.startswith(
        'darwin'):  # para debug quando estiver no WINDOWS ou no MAC
    graph_path = os.getcwd()

else:
    graph_path = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram',
                                                                                     'path.graph')  # Path where graph file will be save temporarily

# Zabbix settings | Dados do Zabbix ####################################################################################
zbx_server = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'url')
zbx_user = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'user')
zbx_pass = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'pass')

# Graph settings | Configuracao do Grafico #############################################################################
height = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection',
                                                                             'height')  # Graph height | Altura
width = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection',
                                                                            'width')  # Graph width  | Largura

# Ack message | Ack da Mensagem ########################################################################################
Ack = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSection', 'ack')

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


def decrypt(key, source, decode=True):
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
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
                arquivo = open("{0}{1}".format(pathDefault, arqConfig), "w")
                arquivo.writelines(file)
                arquivo.close()
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

argvs = " || ".join(sys.argv[1:])

if nograph not in argvs:
    try:
        triggerid, eventid, color, period, body = ' '.join(sys.argv[3:]).split('#', 4)
        period = int(period)

    except ValueError as e:
        if "unpack" in str(e):
            log.writelog(
                '{0} >> at split (triggerid, eventid, color, period, body) | Quantidade de argumentos insuficientes no split (triggerid, eventid, color, period, body)'.format(
                    str(e)), arqLog, "ERROR")

        else:
            log.writelog('{0}'.format(str(e)), arqLog, "ERROR")
        exit()

else:
    body = "\n{0}".format(sys.argv[3])

body = re.sub(r'(\d{4})\.(\d{2})\.(\d{2})', r'\3/\2/\1', body).replace("--nograph", "").rstrip().strip()


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


def send_mail(dest, itemType, get_graph, key):
    # Mail settings | Configrações de e-mail ###########################################################################
    mail_from = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.from')
    smtp_server0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail',
                                                                                       'smtp.server')
    mail_user0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.user')
    mail_pass0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'mail.pass')
    messageE = f"{PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail', 'message.email')} ({{0}})"
    ####################################################################################################################

    try:
        smtp_server = decrypt(key, smtp_server0)
    except:
        smtp_server = smtp_server0

    try:
        mail_user = decrypt(key, mail_user0)
    except:
        mail_user = mail_user0

    try:
        mail_pass = decrypt(key, mail_pass0)
    except:
        mail_pass = mail_pass0

    try:
        mail_from = email.utils.formataddr(tuple(mail_from.replace(">", "").split(" <")))
    except:
        mail_from = mail_from

    dests = ', '.join(dest)
    msg = body.replace("\\n", "").replace("\n", "<br>")
    try:
        subject = re.sub(r"(<(/)?[a-z]>)", "", sys.argv[2])
    except:
        subject = sys.argv[2]

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = mail_from
    msgRoot['To'] = dests

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionEmail',
                                                                                   'salutation.email')

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = "<p>{0},</p>".format(salutation)
    else:
        saudacao = ""

    text = '{0}<p>{1}</p>'.format(saudacao, msg)

    if re.match("([03])", itemType):
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
                texto = 'Error: Unable to send email | Não foi possível enviar o e-mail - {0}'.format(msg.smtp_error.decode("utf-8").split(". ")[0])
                log.writelog(texto, arqLog, "WARNING")
                smtp.quit()
                exit()
            except smtplib.SMTPException:
                pass

        try:
            smtp.sendmail(mail_from, dest, msgRoot.as_string())
        except Exception as msg:
            texto = 'Error: Unable to send email | Não foi possível enviar o e-mail - {0}'.format(msg.smtp_error.decode("utf-8").split(". ")[0])
            log.writelog(texto, arqLog, "WARNING")
            smtp.quit()
            exit()

        if re.search("(sim|s|yes|y)", str(Ack).lower()):
            if nograph not in argvs:
                ack(dests, messageE)

        texto = 'Email sent successfully | Email enviado com sucesso ({0})'.format(dests)
        log.writelog(texto, arqLog, "INFO")
        smtp.quit()
    except smtplib.SMTPException as msg:
        texto = 'Error: Unable to send email | Não foi possível enviar o e-mail ({0})'.format(msg)
        log.writelog(texto, arqLog, "WARNING")
        logout_api(auth)
        smtp.quit()
        exit()

    return texto


def send_telegram(Ldest, itemType, get_graph, key, valueProxy):
    # Telegram settings | Configuracao do Telegram #####################################################################
    api_id0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.id')
    api_hash0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'api.hash')
    messageT = f"{PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram', 'message.telegram')} ({{0}})"
    ####################################################################################################################

    try:
        api_id = int(decrypt(key, api_id0))
    except:
        api_id = api_id0

    try:
        api_hash = str(decrypt(key, api_hash0))
    except:
        api_hash = api_hash0

    app = Client("SendGraph", api_id=api_id, api_hash=api_hash, proxy=valueProxy)

    msg = body.replace("\\n", "")
    msg = re.sub(r"(<br( ?\/)?>)", r"\n", msg).replace("\n\r\n", "\n")

    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTelegram',
                                                                                   'salutation.telegram')

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = salutation + " {0} \n\n"
    else:
        saudacao = ""

    with app:
        for dest in Ldest:
            dest = dest.lower()
            topic = None
            if re.match(r"-\d+_\d+", dest):
                if len(dest.split("_")) == 2:
                    dest, topic = dest.split("_")
                    topic = int(topic)

            elif re.search("user#|chat#|\'|\"", dest):
                if "#" in dest:
                    dest = dest.split("#")[1]

                elif dest.startswith("\"") or dest.startswith("\'"):
                    dest = dest.replace("\"", "").replace("\'", "")

            elif dest.startswith("@"):
                dest = dest[1:]

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
                        log.writelog(f'{msg.args[0]}', arqLog, "ERROR")
                        exit()

            Id = int(Id)
            sendMsg = """{}{}\n{}""".format(saudacao.format(dest), sys.argv[2], msg)
            if re.match("([03])", itemType):
                import io
                graph = io.BytesIO(get_graph.content)
                # try:
                #     # graph = '{0}/{1}.png'.format(graph_path, triggerid)
                #     # with open(graph, 'wb') as png:
                #     #     png.write(get_graph.content)
                # except BaseException as err:
                #     log.writelog(
                #         '{1} >> An error occurred at save graph file in {0} | Ocorreu um erro ao salvar o grafico no diretório {0}'.format(
                #             graph_path, str(err)), arqLog, "WARNING")
                #     logout_api(auth)
                #     exit()

                try:
                    app.send_photo(Id, graph, caption=sendMsg, reply_to_message_id=topic)
                    texto = 'Telegram sent photo message successfully | Telegram com gráfico enviado com sucesso ({0})'.format(dest)
                    log.writelog(texto, arqLog, "INFO")
                except Exception as err:
                    texto = 'Telegram FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo telegram ({0})\n{1}'.format(dest, err)
                    log.writelog(texto, arqLog, "ERROR")
                    logout_api(auth)
                    exit()

                # try:
                #     os.remove(graph)
                # except Exception as err:
                #     log.writelog('{0}'.format(str(err)), arqLog, "ERROR")

            else:
                try:
                    app.send_message(Id, sendMsg, reply_to_message_id=topic)
                    texto = 'Telegram sent successfully | Telegram enviado com sucesso ({0})'.format(dest)
                    log.writelog(texto, arqLog, "INFO")
                except Exception as err:
                    texto = 'Telegram FAIL at sending message | FALHA ao enviar a mensagem pelo telegram ({1})\n{0}'.format(dest, err)
                    log.writelog(texto, arqLog, "ERROR")
                    logout_api(auth)
                    exit()

            if re.search("(sim|s|yes|y)", str(Ack).lower()):
                if nograph not in argvs:
                    ack(dest, messageT)

            return texto


def get_WhatsApp(headers, url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        buscas = response.json()['response']
    except:
        buscas = None

    return buscas


def send_whatsapp_pay(itemType, graph, acessKey, url_base, message, line, destiny):
    message = quote(b64encode(message.encode("utf-8")))
    if re.match("([03])", itemType):
        Graph = quote(graph)
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = 'app=NetiZap%20Consumers%201.0&key={key}&text={text}&type=PNG&stream={stream}&filename=grafico'.format(
                key=acessKey, text=message, stream=Graph)
            url = f"{url_base}/file_send?line={line}&destiny={destiny}"
            result = requests.post(url, auth=("user", "api"), headers=headers, data=payload)

            if result.status_code != 200:
                error = json.loads(result.content.decode("utf-8"))['errors'][0]['message']
                log.writelog('{0}'.format(error), arqLog, "ERROR")
            else:
                texto = f'WhatsApp sent photo message successfully | WhatsApp com gráfico enviado com sucesso ({destiny})'
                try:
                    result_str = json.loads(result.text)["result"]
                except KeyError:
                    texto = 'WhatsApp FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo WhatsApp{}'
                    result_str = result.text

                log.writelog(texto, arqLog, "INFO")
                log.writelog('{0}'.format(result_str), arqLog, "INFO")
                return texto

        except Exception as err:
            log.writelog('{0}'.format(str(err)), arqLog, "ERROR")
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

        except Exception as err:
            log.writelog('{0}'.format(str(err)), arqLog, "ERROR")
            exit()


def send_whatsapp_free(token_wa, itemType, graph, url_base, message, destiny, saudacao):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_wa}"
    }
    Get_WA = get_WhatsApp(headers, f"{url_base}/all-groups")
    status_Group = [group for group in Get_WA if destiny == group['id']['user']]

    isGroup = True
    if not status_Group:
        isGroup = False

    try:
        groupName = status_Group[0]['name']
    except IndexError:
        Get_WA = get_WhatsApp(headers, f"{url_base}/all-contacts")
        status_Group = [group for group in Get_WA if destiny == group['id']['user']]
        groupName = status_Group[0]['name']

    if saudacao:
        saudacao, _ = saudacao.split(".")
        message = message.replace(saudacao, f"{saudacao}, {groupName}").replace(r"\u2705", r"✅")

    data = {
        "phone": destiny,
        "isGroup": isGroup,
        "message": message.replace("\\n", "\n"),
    }

    if re.match("([03])", itemType):
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

        else:
            texto = f'WhatsApp sent photo message successfully | WhatsApp com gráfico enviado com sucesso ({groupName})'
            log.writelog(texto, arqLog, "INFO")
            r = json.loads(result.text)
            log.writelog('{}: {}'.format(r["status"], r['response']), arqLog, "INFO")

        return [groupName, texto]
    except Exception as err:
        log.writelog('{0}'.format(str(err)), arqLog, "ERROR")
        exit()


def send_whatsapp(Ldestiny, itemType, get_graph, key):
    # WhatsApp settings | Configuracao do WhatsApp #####################################################################
    line0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'line')
    acessKey0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'acess.key')
    port0 = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'port')
    messageW = f"{PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'message.whatsapp')} ({{0}})"

    # WhatsApp Open source | Codigo aberto WhatsApp ####################################################################
    wa_free = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp', 'open.source')
    url_base_free = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                        'open.source.url')
    api_token = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                    'open.source.token')
    ####################################################################################################################

    try:
        line = decrypt(key, line0)
    except:
        line = line0

    try:
        acessKey = decrypt(key, acessKey0)
    except:
        acessKey = acessKey0

    try:
        port = decrypt(key, port0)
    except:
        port = port0

    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionWhatsApp',
                                                                                   'salutation.whatsapp')

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = salutation + ".\\n\\n"
    else:
        saudacao = ""

    msg0 = body.replace("\r", "").split('\n ')[0].replace("\n", "\\n")
    msg = "{}\\n{}".format(sys.argv[2], msg0)
    message = "{}{}".format(saudacao, msg.replace(r"✅", r"\u2705"))

    formatter = [("b", "*"), ("i", "_"), ("u", "")]
    for f in formatter:
        old, new = f
        if re.search(r"(<(/)?{}>)".format(old), message):
            message = re.sub(r"(<(/)?{}>)".format(old), r"{}".format(new), message)

    graph = get_graph
    if get_graph:
        graph = b64encode(get_graph.content)

    for destiny in Ldestiny:
        if re.search("(sim|s|yes|y)", str(wa_free).lower()):
            url_base = url_base_free
            destiny, resultado = send_whatsapp_free(api_token, itemType, graph, url_base, message, destiny, saudacao)
        else:
            url_base = f"http://api.meuaplicativo.vip:{port}/services"
            resultado = send_whatsapp_pay(itemType, graph, acessKey, url_base, message, line, destiny)

        if re.search("(sim|s|yes|y)", str(Ack).lower()):
            if nograph not in argvs:
                ack(destiny, messageW)

        return resultado


def send_teams(Lwebhook, itemType, get_graph):
    saudacao = salutation
    Saudacao = PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTeams',
                                                                                   'salutation.teams')
    messageT = f"{PropertiesReaderX(path.format('configScripts.properties')).getValue('PathSectionTeams', 'message.teams')} ({{0}})"

    if re.search("(sim|s|yes|y)", str(Saudacao).lower()):
        if saudacao:
            saudacao = salutation + ".\n\n"
    else:
        saudacao = ""

    message = re.sub(r"(<br( ?\/)?>)", r"\n", body).replace("\n\r\n", "\n").replace("\n", "\n\n")
    subject = "{}\n{}".format(saudacao, sys.argv[2])

    formatter = [("b", "**"), ("i", "_"), ("u", "")]
    for f in formatter:
        old, new = f
        if re.search(r"(<(/)?{}>)".format(old), subject):
            subject = re.sub(fr"(<(/)?{old}>)", new, subject)

    headers = {'Content-Type': 'application/json'}
    bodyMsg = [{"type": "TextBlock", "text": subject, "weight": "bolder", "wrap": True}]

    if re.match("([03])", itemType):
        image = b64encode(get_graph.content).decode()
        responseOk = 'Teams sent photo message successfully | Teams com gráfico enviado com sucesso\n{0}'
        responsePro = 'Teams FAIL at sending photo message | FALHA ao enviar mensagem com gráfico pelo Teams\n{0}'
        bodyMsg.append({"type": "Image", "url": f"data:image/png;base64,{image}", "msTeams": {"allowExpand": True}})

    else:
        responseOk = 'Teams sent successfully | Teams enviado com sucesso ({0})'
        responsePro = 'Teams FAIL at sending message | FALHA ao enviar a mensagem pelo Teams\n{0}'

    bodyMsg.append({"type": "TextBlock", "text": message, "wrap": True})

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

    for webhook in Lwebhook:
        try:
            response = requests.post(webhook, headers=headers, json=payload)
            response.raise_for_status()

            if re.search("OK|Accepted", response.reason):
                resultado = responseOk.format(webhook)
                # print(resultado)
                log.writelog(resultado, arqLog, "INFO")

            else:
                error = response.content.decode("utf-8")
                resultado = responsePro.format(error)
                # print(resultado)
                log.writelog(resultado, arqLog, "ERROR")

        except Exception as err:
            print(err)
            log.writelog('{0}'.format(str(err)), arqLog, "ERROR")
            exit()

        if re.search("(sim|s|yes|y)", str(Ack).lower()):
            if nograph not in argvs:
                ack(webhook, messageT)

        return resultado


def zbx_token(key):
    global zbx_user, zbx_pass
    try:
        zbx_user = decrypt(key, zbx_user)
    except:
        zbx_user = zbx_user

    try:
        zbx_pass = decrypt(key, zbx_pass)
    except:
        zbx_pass = zbx_pass

    credentials = {"user": zbx_user, "password": zbx_pass}
    if float(version_api()[:3]) >= 6.4:
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
            log.writelog('Zabbix: {0}'.format(login_api["error"]["data"]), arqLog, "ERROR")
            exit()
        else:
            log.writelog('{0}'.format(login_api), arqLog, "ERROR")
            exit()

    except ValueError:
        log.writelog(
            'Check declared zabbix URL/IP and try again | Valide a URL/IP do Zabbix declarada e tente novamente. (Current: {0})'.format(
                zbx_server), arqLog, "WARNING")
        exit()
    except Exception as err:
        log.writelog('{0}'.format(str(err)), arqLog, "WARNING")
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


def logout_api(auth_token):
    requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                  verify=False, data=json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.logout",
                "params": [],
                "auth": auth_token,
                "id": 4
            }
        )
                  )


def getgraph(triggerName, hostName, listaItemIds, period):
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
            # periodS = segundos_rest % 60

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
        logout_api(auth)
        exit()


def getTrigger(triggerid):
    try:
        triggerid = requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'},
                                  verify=False, data=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                        "output": ["description"],
                        'triggerids': triggerid,
                        "selectItems": ['name', 'value_type', 'lastvalue'],
                        "selectHosts": ["name"],
                        "expandDescription": True,
                    },
                    "auth": auth,
                    "id": 2
                }
            )
                                  )

        if triggerid.status_code != 200:
            log.writelog(f'HTTPError {triggerid.status_code}: {triggerid.reason}', arqLog, "WARNING")
            logout_api(auth)
            exit()

        triggerid = json.loads(triggerid.text.encode('utf-8'))

        listaItemIds = []
        item_type = ""
        if 'result' in triggerid:
            resultado = triggerid["result"]

            if not resultado:
                log.writelog('Zabbix: Nenhuma trigger encontrada', arqLog, "ERROR")
                exit()

            hostName = resultado[0]['hosts'][0]['name']
            triggerName = resultado[0]['description']
            for i in range(0, len(resultado)):
                for items in resultado[i]['items']:
                    if items['itemid'] not in listaItemIds:
                        listaItemIds.append(items['itemid'])

                    if not item_type:
                        item_type += items['value_type']

            return item_type, triggerName, hostName, listaItemIds

        elif 'error' in triggerid:
            log.writelog('Zabbix: {0}'.format(triggerid["error"]["data"]), arqLog, "ERROR")
            exit()

        else:
            # print(triggerid)
            log.writelog('{0}'.format(triggerid), arqLog, "ERROR")
            exit()

    except Exception as msg:
        log.writelog('{0}'.format(msg), arqLog, "ERROR")
        exit()


def get_cripto():
    with open(fileX, 'r') as f:
        return json.load(f)


def ack(dest, message):
    Json = {
        "jsonrpc": "2.0",
        "method": "event.acknowledge",
        "params": {
            "eventids": eventid,
            "message": message.format(dest)
        },
        "auth": auth,
        "id": 3
    }
    if 4.0 < float(version_api()[:3]):
        Json["params"]["action"] = 6

    requests.post(f'{zbx_server}/api_jsonrpc.php', headers={'Content-type': 'application/json'}, verify=False,
                  data=json.dumps(Json))


def main(codeKey):
    proxy = getProxy()

    if nograph not in argvs:
        item_type, triggerName, hostName, listaItemIds = getTrigger(triggerid)
        get_graph = getgraph(triggerName, hostName, listaItemIds, period)

    else:
        item_type = "1"
        get_graph = ""

    dest = sys.argv[1]
    destino = destinatarios(dest)

    emails = []
    telegrams = []
    whatsapps = []
    teams = []

    for x in destino:
        if re.match(r"^(\d+(-)?\d+(@g\.us)?|\d{12,25})$", x):
            whatsapps.append(x)

        elif re.search(r"^.*@[a-z0-9-]+\.[a-z]+(\.[a-z].*)?$", x.lower()):
            emails.append(x)

        elif re.search("webhook.office.com|workflows", x.lower()):
            teams.append(x)

        else:
            telegrams.append(x)

    listaStatus = []
    if whatsapps:
        status = send_whatsapp(whatsapps, item_type, get_graph, codeKey)
        listaStatus.append({"whatsapp": {"status": status}})

    if teams:
        status = send_teams(teams, item_type, get_graph)
        listaStatus.append({"teams": {"status": status}})

    if telegrams:
        status = send_telegram(telegrams, item_type, get_graph, codeKey, proxy)
        listaStatus.append({"telegram": {"status": status}})

    if emails:
        status = send_mail(emails, item_type, get_graph, codeKey)
        listaStatus.append({"email": {"status": status}})

    return listaStatus


if __name__ == '__main__':
    JSON = get_cripto()
    code_key = JSON['code']
    auth = zbx_token(code_key)
    main(code_key)
    logout_api(auth)
