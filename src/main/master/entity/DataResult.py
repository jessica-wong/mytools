#
class DataResult(object):

    def __init__(self):
        #return result status
        self.success=False
        #return result message
        self.message=""
        #return result err code
        self.statusCode=0

    def getSuccess(self):
        return self.success

    def setSuccess(self,success):
        self.success = success

    def getMessage(self):
        return self.message

    def setMessage(self,message):
        self.message = message

    def getStatusCode(self):
        return self.statusCode

    def setStatusCode(self,statusCode):
        self.statusCode = statusCode