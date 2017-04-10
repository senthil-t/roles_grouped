#! /usr/bin/python

'''
(c) Copyright 2017 Hewlett Packard Enterprise Development LP
Created on Jan 19, 2017
version 0.1
@author: senthilt
'''
import sys
import subprocess
import time

class ConfigureDatasource(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        This module adds a datasource.
        command to invoke this module is
        ./ConfigureMXDatasource <service name> <ds name.>
        '''            
        self.serviceName    = params['service_name']
        self.datasourceName = params['datasource_name']
        self.action = params['action']
        self.dsattributes = params

    def serve_request(self):
        if self.action == "add":            
            return self.__add_datasource();
        elif self.action == "delete": 
            return self.__delete_datasource();
        else:
            return self.__handle_error("Invalid value for action.")    
        
    def __add_datasource(self):
        #does the service exists ?
        command = "status $"+self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" in  str(result):
            return self.__handle_error("mx service does not exists")
        
        maxserver = self.dsattributes['max_server']
        initserver = self.dsattributes['init_server']
        
        #add server datasource with default configuration.
        commandList = ["add ds ${}.{}, maxserver {},initserver {},idleserver 2, ConnTimeout NO_TIMEOUT, IdleTimeout NO_TIMEOUT;\n".format(self.serviceName,self.datasourceName,int(maxserver),int(initserver)),                       
                       "start ds ${}.{};\n".format(self.serviceName,self.datasourceName)
                       ]
        result = self.__execute_in_mxcs(commandList)
        if "*** ERROR" in str(result):
            return self.__handle_error("Error while configuring datasource." + str(result))    
        
        data = {
       'result' : 'success',
       'message':'Datasource added successfully',
       'service Name' : '{}'.format(self.serviceName),
       'datasource_name' : '{}'.format(self.datasourceName),
       'MaxServer' : '{}'.format(maxserver),
       'InitServer' : '{}'.format(initserver)
        }    
        
        return data
    
    def __delete_datasource(self):
        #stop and delete the ds.
        commandList = ["stop ds ${}.{},reason '{}',AFTER NOW;\n".format(self.serviceName,self.datasourceName,'deleting the datasource'),
                       "delete ds {};\n".format(self.datasourceName),
                       ]
            
        result = self.__execute_in_mxcs(commandList)
        if "*** ERROR" in str(result):
            return self.__handle_error("Error while deleting datasource." + str(result))    
        
        data = {
       'result' : 'success',
       'message':'Datasource removed successfully',
       'service Name' : '{}'.format(self.serviceName),
       'datasource_name' : '{}'.format(self.datasourceName),     
       'output' : result  
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
    ConfigureDatasource(sys.argv[1])
        