#! /usr/bin/python

'''
(c) Copyright 2017 Hewlett Packard Enterprise Development LP
Created on Feb 21, 2017
version 0.1
@author: senthilt
'''
import sys
import subprocess
import time

class ModifyDatasource(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        This module alters a datasource.
        command to invoke this module is
        ./ModifyDatasource <service name> <ds name.>
        '''            
        
        self.serviceName    = params['service_name']
        self.datasourceName = params['datasource_name']        
        self.dsattributes = params
        
    def serve_request(self):    
        return self.__alter_datasource()

        
    def __alter_datasource(self):
        #does the service exists ?
        command = "status $"+self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" in  str(result):
            return self.__handle_error("mx service does not exists")
        
        maxserver = self.dsattributes['max_server']
        initserver = self.dsattributes['init_server']
        idleserver = self.dsattributes['idle_server']
        ConnTimeout = self.dsattributes['connection_info_stat']
        IdleTimeout = self.dsattributes['idle_timeout']
        
        #add server datasource with default configuration.
        commandList = [
                       "alter ds ${}.{}, maxserver {},initserver {},idleserver {}, ConnTimeout NO_TIMEOUT, IdleTimeout NO_TIMEOUT;\n"
                       .format(self.serviceName, self.datasourceName, int(maxserver), int(initserver), int(idleserver))
#                        ,"start ds ${}.{};\n".format(self.serviceName, self.datasourceName)
                       ]
        result = self.__execute_in_mxcs(commandList)
        if "*** ERROR" in str(result):
            return self.__handle_error("Error while configuring datasource." + str(result))    
        
        data = {
       'result' : 'success',
       'message':'Datasource altered successfully',
       'service Name' : '{}'.format(self.serviceName),
       'datasource_name' : '{}'.format(self.datasourceName),
       'MaxServer' : '{}'.format(maxserver),
       'InitServer' : '{}'.format(initserver)
        }    
        
        return data
     
    def __execute_in_tacl(self,command):        
        process = subprocess.Popen(["gtacl" ,"-c",command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.flush()
        result = process.stdout.readlines()        
        return result

    #Utility support for OSS
    def __execute_in_oss(self,command):        
        process = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.flush()
        result = process.stdout.readlines()        
        return result
    
    def __execute_in_mxcs(self,commands):
        process = subprocess.Popen(["mxci"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.write("mode mxcs;\n")
    
        for command in commands:
            process.stdin.write(command)
            time.sleep(3)
    
        process.stdin.write("exit;\n")
        result =  process.stdout.readlines()

    def __handle_error(self, errorMsg):
        data = {
       'result' : 'Fail',
       'Reason' : 'Error while serving the request: {}'.format(errorMsg)       
        }    
#       json_str = json.dumps(data)
        return data
    
if __name__ == '__main__':
    ModifyDatasource(sys.argv[1])
        
