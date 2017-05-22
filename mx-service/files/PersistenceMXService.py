#! /usr/bin/python

'''
(c) Copyright 2017 Hewlett Packard Enterprise Development LP
Created on Jan 17, 2017
version 0.1
@author: senthilt
'''

import sys
import subprocess
import json
import time

class MXPersistenceService(object):
    '''
    This module starts a MXOAS Service.
    command to inovke this module is
    ./ConfigureMXService <service name> <port no.> <start>
    '''
    def __init__(self, params):
        '''
        Constructor
        '''

        self.serviceName = params['service_name']
        self.servicePort = params['port_number']
        self.action = params['action']
        self.processName = params['process_name']
    
    def serve_request(self):                
        if self.action == "start":
            return self.__start_service();
        elif self.action == "stop": 
            return self.__stop_service();
        else:
            return self.__handle_error("Invalid value for action.")    
    
    def __start_service(self):
        #does the service exists ?
        command = "status $"+self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" not in  str(result):
            data = self.__handle_error("Service exists")
            return data                 
        
        #does the exe exists ?
        command = "fileinfo $system.zmxodbc.mxoas"
        result = self.__execute_in_tacl(command)
        if "No files match" in str(result):
            data = self.__handle_error("MXCS is not installed on system.")
            return data
            
        return self.__start_process()
    
    def __stop_service(self):
        #does the service exists ?
        command = "status $"+self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" in  str(result):
            data = self.__handle_error("Service doesn't exists")
            return data                 
        
        #does the exe exists ?
        commands = [
                     "abort #{} \n".format(self.processName),
                     "delete #{} \n".format(self.processName)                 
                 ]
        
        result = self.__execute_in_scf(commands)
        
        if "ERROR" in str(result):
            data = self.__handle_error("Error while configuring service.")
            return data        
        
        data = {
       'result' : 'success',
       'message':'MXCS process removed successfully',
       'service Name' : '{}'.format(self.serviceName)
        }
        return data 

    
    def __start_process(self):
        commandList = [
                    "add #{}, cpu firstof(01,00), AutoRestart 10,hometerm $zhome,name ${},startupmsg \"-pn {} \", StartMode application, program $system.zmxodbc.mxoas\n".format(self.processName,self.serviceName,self.servicePort),                       
                    "start #{} \n".format(self.processName),
                    "status #{} \n".format(self.processName)
               ]
        result = self.__execute_in_scf(commandList)
        if "ERROR" in str(result):
            return self.__handle_error("Error while configuring service.." + str(result))    
        
        data = {
       'result' : 'success',
       'message':'MXCS configured successfully',
       'service Name' : '{}'.format(self.serviceName),            
        }
        return data
    
    def __execute_in_tacl(self,command):        
        process = subprocess.Popen(["gtacl" ,"-c",command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.flush()
        result = process.stdout.readlines()        
        return result
    
    def __execute_in_scf(self,commands):
        process = subprocess.Popen(["gtacl" ,"-p","scf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)        
        process.stdin.write("assume process $zzkrn\n")    
        for command in commands:
            process.stdin.write(command)
            time.sleep(3)
    
        process.stdin.write("exit\n")
        result =  process.stdout.readlines()    
        return result

    def __handle_error(self, errorMsg):
        data = {
       'result' : 'Fail',
       'Reason' : 'Error while serving the request: {}'.format(errorMsg)       
        }    
#       json_str = json.dumps(data)
        return data
#         print "Error while serving the request.\n"+errorMsg
    
if __name__ == '__main__':
    MXPersistenceService(sys.argv[1])
