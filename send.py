from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService,MessageRequestGSMError

ip = IPv4Address("192.168.137.69")
session = AirmoreSession(ip)
service = MessagingService(session)
try :
    service.send_message("+213662642821","hello from pytho,")
except MessageRequestGSMError:
    print(MessageRequestGSMError)