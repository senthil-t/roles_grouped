#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

DOCUMENTATION = '''
---
module:            configure SQL/MX service

short_description: Manages SQL/MX services.

description:       To start or stop SQL/MX MXCS service with the specified
                   service name and port number. Optionally, user can choose to provide the MXOAS guardian location.

version_added:      "2.2"

author:            "senthilt"

requirements:
    - Ansible must be installed
    - NonStop server with proper user credentials
    
options:
    service_name: 
        description: MXCS Service will be started with this name.
        required:    True
    
    port_number: 
        description: MXCS service will be started with this name.
        required:    True    
    
    action: 
        description: To determine whether to start or stop the service.
        required: True
        default: start
        choices: [start,stop]
    
    mxoas_location: 
        description: Guardian location of the MXCS objects.
        required: False
        default: $system.zmxodbc.mxoas.    

'''

EXAMPLES = '''
- name: start MX Service
  configure_mxservice:    
    service_name: "mxsv1"    
    port_number: "18650"
    action: "start"
  register: result
'''

RETURN = '''
dest:
    description: starts/stops SQL/MX service.
    returned: success
    type: string
    sample: none
'''


from ansible.module_utils.basic import *
import sys
sys.path.append('/tmp')
from ConfigureMXService import MXService

def main():

    fields = {        
        "service_name": {"required": True, "type": "str"},
        "port_number": {"required": True, "type": "str"},
        "mxoas_location": {"required": False,"default": "$system.zmxodbc.mxoas", "type": "str"},
        "action": {
            "default": "start",
            "choices": ['start', 'stop'],
            "type": 'str'
        },
    }

    module = AnsibleModule(argument_spec=fields)
    mxservice = MXService(module.params)
    result =  mxservice.serveRequest()
    
    #parse the output.
    has_changed = result['result'] == 'success'  
    is_error = result['result'] == 'fail'       
        
    json_str = json.dumps(result)
    meta = {"status": 100, 'response': json_str}

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error while configuring MXService", meta=result)


if __name__ == '__main__':
    main()