from datetime import datetime
import gadgets

class GarmrResult(object):
    logger = None
    
    def __init__(self, id):
        self.id = id
        self.result = {}
        self.finished = False
        self.success = False
        self.starttime = datetime.now()
        if GarmrResult.logger:
            GarmrResult.logger.info("%s initialized" % self.id)
    
    def succeed(self, message):
        self.endtime = datetime.now()
        self.finished = True
        if GarmrResult.logger:
            GarmrResult.logger.info("PASS %s: %s" % (self.id, message))
    
    def incomplete(self, message):
        self.endtime = datetime.now()
        self.finished = False
        self.success = False
        if GarmrResult.logger:
            GarmrResult.logger.error("%s succeeded: %s" % (self.id, message))
        
    def fail(self, message):
        self.endtime = datetime.now()
        self.finished = True
        self.success = False
        if GarmrResult.logger:
            GarmrResult.logger.critical("FAIL %s: %s" % (self.id, message))
            
    def duration(self):
        if self.finished == False:
            raise Exception("duration called on running check")
        return gadgets.total_seconds(self.starttime, self.endtime)
    
    def append(self, id, object):
        self.result[id] = object
        
    def debug(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.debug(msg, args, kwargs)
            
    def info(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.info(msg, args, kwargs)
    
    def warning(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.warning(msg, args, kwargs)
            
    def error(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.error(msg, args, kwargs)
            
    def critical(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.critical(msg, args, kwargs)
            
    def log(self, msg, *args, **kwargs):
        if GarmrResult.logger:
            GarmrResult.logger.log(msg, args, kwargs)
            
    
        