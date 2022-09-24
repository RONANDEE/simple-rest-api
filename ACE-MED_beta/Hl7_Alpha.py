
import hl7
import time

from datetime import datetime
from hl7.client import MLLPClient

barcode = "1234"
temperature = "34"
sys = "120"
dia = "80"
pr = "72"

while True:
    str_date = datetime.now().strftime("%Y%m%d%H%M%S")
    msg = "MSH|^~\&|BMP3|AMMARIN MEDICAL|HIS|BMS-HOSxP|"+str_date+"||ORU^R01|2701|P|2.3\n"
    msg += "PID|1||"+barcode+"|\n"
    msg += "PV1|||||||||||||||||||\n"
    msg += "OBR|1|||||"+str_date+"||||||||"+str_date+"\n"
    msg += "OBX|1|ST|TEMP||"+temperature+"|"+temperature+"|||||F|||"+str_date+"\n"
    msg += "OBX|2|ST|SYSTOLIC||"+sys+".0|"+sys+".0|||||F|||"+str_date+"\n"
    msg += "OBX|3|ST|DIASTOLIC||"+dia+".0|"+dia+".0|||||F|||"+str_date+"\n"
    msg += "OBX|4|ST|PULSE||"+pr+".0|"+pr+".0|||||F|||"+str_date+"\n"
    h = hl7.parse(msg)
    
    localtime = time.localtime()
    result = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
    print(result)
    

    with MLLPClient('10.24.249.183',8888) as client:
        client.send_message(msg)

    time.sleep(1)
