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


class MXService(object):
    '''
    This module starts a MXOAS Service.
    '''
    def __init__(self,params):
        '''
        Constructor
        '''
                    
        self.serviceName = params['service_name']
        self.servicePort = params['port_number']
        self.action = params['action']
        self.mxoasLocation = params['mxoas_location']
        
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
            
        command = " run ${} /name ${}, nowait/ -pn {}".format("system.zmxodbc.mxoas",self.serviceName,self.servicePort)
        result = self.__execute_in_tacl(command)
        if "*ERROR*" in str(result):
            data = self.__handle_error("Error while starting the service")
            return data   
        
        data = {
       'result' : 'success',
       'service Name' : '{}'.format(self.serviceName),
       'service port' : '{}'.format(self.servicePort)
        }
        return data 
            
    def __stop_service(self):
        #does the service exists ?
        command = "status $"+self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" in  str(result):
            data = self.__handle_error("Service doesn't exists")
            return data                 
        
        #does the exe exists ?
        command = "stop $"+ self.serviceName
        result = self.__execute_in_tacl(command)
        if "(Process does not exist)" in str(result):
            data = self.__handle_error("Service doesn't exist.")
            return data
        
        data = {
       'result' : 'success',
       'service Name' : '{}'.format(self.serviceName)
        }
        return data
    
    def __execute_in_tacl(self,command):        
        process = subprocess.Popen(["gtacl" ,"-c",command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        process.stdin.flush()
        result = process.stdout.readlines()        
        return result
    
    def __handle_error(self, errorMsg):
        data = {
       'result' : 'Fail',
       'Reason' : 'Error while serving the request: {}'.format(errorMsg)       
        }
        return data
    
if __name__ == '__main__':
    MXService(sys.argv[1])