from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .HardwareHandler import HardwareHandler
from .kerror import KERR
import shutil

class MeowbitHandler(HardwareHandler):
  def __init__(self, websocket, extensions, userPath):
    HardwareHandler.__init__(self, websocket, extensions, userPath)

  def list_file(self):
    dest = getDisk(self.ext['thumbdisk'], "2M")
    if dest:
        fileFilter = None
        if 'filter' in self.params:
            fileFilter = self.params['filter']
        files = os.listdir(dest)
        allFiles = []
        for f in files:
            fileExtension = os.path.splitext(f)[1]
            if fileFilter:
                if fileExtension in fileFilter:
                    allFiles.append(f)
            else:
                allFiles.append(f)
        self.sendResp(self.pid, {'files': allFiles})
    else:
        self.sendResp(self.pid, {'err':'no_disk'})

  def disk_info(self):
    dest = getDisk(self.ext['thumbdisk'], "2M")
    if dest:
        total, used, free = shutil.disk_usage(dest)
        self.sendResp(self.pid, {'total': total, 'used': used, 'free': free})

  def upload_file(self):
    dest = getDisk(self.ext['thumbdisk'], "2M")
    if not dest:
        self.sendResp(self.pid, None, {"error": 'no_device', "code": KERR.CANNOT_FIND_DISK})
        return
    fileName = self.params['fileName']
    destPath = os.path.join(dest, fileName)
    total, used, free = shutil.disk_usage(dest)
    if free < 100*1024:
        self.sendResp(self.pid, None, {"error": "not enough space", "code": 103, 'file': destPath})
        return
    try:
        with open(destPath, 'wb') as output:
            # logger.info("copy %s to %s" %(fileName, destPath))
            content = base64.b64decode(self.params['content'])
            output.write(content)
            output.flush()
            os.fsync(output) # fix for windows flush with a quantity delay
            self.sendResp(self.pid, {'status': 'ok', 'file': destPath})
    except Exception as e:
        # self.sendResp(self.pid, None, {"error": str(e), "code": 103, 'file': destPath})
        self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': destPath})

  def upload_image(self):
    dest = getDisk(self.ext['thumbdisk'], "2M")
    fileName = self.params['fileName']
    if not dest:
        self.sendResp(self.pid, None, {"error": 'no_device', "code": KERR.CANNOT_FIND_DISK})
        return
    destPath = os.path.join(dest, fileName)
    total, used, free = shutil.disk_usage(dest)
    if free < 100*1024:
        self.sendResp(self.pid, None, {"error": "not enough space", "code": 103, 'file': destPath})
        return
    try:
        width = None
        if 'width' in self.params:
            width = int(self.params['width'])
        destPath = os.path.splitext(destPath)[0]+'.bmp'
        saveToBmp(self.params['content'], destPath, width)
        self.sendResp(self.pid, {'status': 'ok', 'file': destPath})
    except Exception as e:
        self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': destPath})
  
  def delete_file(self):
    dest = getDisk(self.ext['thumbdisk'], "2M")
    ret = -1
    if dest:
        fileName = self.params['fileName']
        filePath = os.path.join(dest, fileName)
        if os.path.exists(filePath):
            os.remove(filePath)
            ret = 0
    self.sendReq("extension-method", {"extensionId": self.ext['id'], "func": "onDelDone", "msg": ret})   

  def upload_firmware(self):
    if self.ext["fwtype"] == "uf2":
        def onDone(msg, err):
            if err:
                self.sendResp(self.pid, None, {"error": msg, "code": KERR.UPLOAD_FIRM_FAIL})
            else:
                self.sendResp(self.pid, {'status': 'ok', 'msg': msg})
        uploadUf2(self.ext, self.params, self.sendReq, self.userPath, onDone)
    