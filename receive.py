from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService
from pyairmore.services.device import DeviceService
from PIL.Image import  Image

ip = IPv4Address("192.168.137.30")
session = AirmoreSession(ip)
# deviceService = DeviceService(session)
service = MessagingService(session)
messages = service.fetch_message_history()
# device = deviceService.fetch_device_details()
# d = deviceService.take_screenshot()
# d.show()
service.f
chat = service.fetch_message_history()
with open('text.txt','w') as f:
    for i in chat:
        f.write("id :{}\nname: {} \nphone :{}\ncontent : {}\ntype : {}\nwas read : {}\ncount : {}\n***************************************************************\n".format(i.id,i.name,i.phone,i.content,i.type,i.was_read,i.count))
# for i in messages:
#     print("id : {} \nname : {} \ncontent : {}    \nphone : {}\ntype : {}    \ndate & time : {} \n**********************************************************".format(i.id,i.name,i.content,i.phone,i.type,i.datetime))
