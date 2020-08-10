# -*- coding : utf-8  -*-
import sys
import time
import logging
from ncclient import manager
from ncclient import operations
from kafka import KafkaClient, SimpleProducer, SimpleConsumer

log = logging.getLogger(__name__)

#kafka = KafkaClient("locakhost:9092")
#producer = SimpleProducer(kafaka)
#consumer = SimpleConsumer(kafka,"python",topic)

#yang push subscriptin condition 1:
subtreemixifuser = '''<ifm xmlns="http:/www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfaces>
       <interface>
         <ifName>GigabitEthernet0/0/0</ifName>
         <ifDynamicInfo/>
         <ifStatistics/>
       </interface>
    </interfaces>
   </ifm>
   <userif xmlns="http:/www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
   </userif>'''

subtreermfull = '''<rm xmlns="http:/www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <rmbase>
    <uniAfs>
    <uniAf>
    <topologys>
    <topology>
    <routes>
       <route>
         <protocoId>ISIS</protocoId>
         <ifNmae/>
         <prefix/>
         <nextHop/>
         <instance/>
       </route>
       <route>
         <protocoId>OSPF</protocoId>
         <ifNmae/>
         <prefix/>
         <nextHop/>
         <instance/>
       </route>
    </routes>
    </topology>
    </topologys>
    </uniAf>
    </uniAfs>
    </rmbase>
    </rm>'''

subtreermisis = '''<rm xmlns="http:/www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <rmbase>
    <uniAfs>
    <uniAf>
    <topologys>
    <topology>
    <routes>
       <route>
         <protocoId>ISIS</protocoId>
         <ifNmae/>
         <prefix/>
         <nextHop/>
         <instance/>
       </route>
      </routes>
    </topology>
    </topologys>
    </uniAf>
    </uniAfs>
    </rmbase>
    </rm>'''

class InterfacesTest():  
    def setUp(self):
        print("\r\nTry to create connection to remote lab ......")
        try:
            
            self.conn = manager.connect(host = "172.19.37.173",port = 22,
                                        username = "telnet", password = "Test2change",
                                        hostkey_verify =False,
                                        device_params = {'name','huawei'},
                                        allow_agent = False,
                                        look_for_keys = False)
            self.conn.raise_mode = operations.RaiseMode.NONE
            
            
        except:
            log.exception("Exception in connecting to %s" % host)

    def subscribe_yangpush_notification(self):
        """
        test <create-subscription> operation.
        :return:
        """

        print("\r\n")
        subscrib = input("Please select subscrib condition (1: interface dynamicinfo and user status; 2: routing table all; 3: ISIS routing table)\r\n")
        if (subscrib =='1'):
            filter = subtreemixifuser

        if (subscrib =='2'):
            filter = subtreermfull

        if (subscrib =='3'):
            filter = subtreermisis


        period = 500
        try:
            ret = self.conn.establish_subscription(user_callback,error_callback,filter,period)
            
            log.info(ret)
        except Exception:
            log.exception("Establish_subscription error")
        while(True):
            print("in while loop!\r\n")
            time.sleep(5)

def user_callback(raw):
    print(raw)
    kafka_producer("yang-push",raw)

def error_callback(raw):
    print(raw)
    print("=======error_info=======================")



def kafka_producer(topic,message):
    kafka = KafkaClient("locakhost:9092")
    producer = SimpleProducer(kafaka)

    producer.send_message(topic,message)

def kafka_consumer(topic):

    kafka = KafkaClient("locakhost:9092")
    consumer = SimpleConsumer(kafka,"python",topic)
    for msg in consumer:
        print(msg)
    

            
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    
    handle = InterfacesTest()
    handle.setUp()
    handle.subscribe_yangpush_notification()
    
