#!/usr/bin/python


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

DOCUMENTATION = '''
---
module:            Alters existing SQL/MX Datasource.

short_description: Alters SQL/MX Datasource properties.

description:    This module helps to alter a existing datasource properties on NonStop. 
                if necessary, this module also restarts the datasource.

version_added:      "2.2"

author:            "senthilt"

requirements:
    - Ansible must be installed
    - NonStop server with proper user credentials
    
options:
    service_name:
        description: MXCS Service where the datasource being tied up with.
        required:    True
    
    datasource_name: 
        description: The name of the datasource which needs to be configured.
        required:    True
    
    max_server: 
        description: is the upper limit on the servers that can be operational for this service on this DS.
        required:    False
        default:     1
    
    idle_server: 
        description: is the lower limit on the available idle servers that are operational for this service
                     on this DS
        required:    False
        default:     0
    
    init_server: 
        description: is the suggested number of servers that each service starts when the DS first
                     starts.
        required:    False
        default:     0
    
    idle_timeout: 
        description:    is a keyword or the integer number of minutes a server waits in the available state
                        for a connection before it stops itself when the count of servers exceeds the
                        IdleServer count value for the DS.
        required:    False
        default:     SYSTEM_DEFAULT
    
    connection_timeout: 
        description: is a keyword or the number of minutes a client-server connection can remain idle
                     before the server terminates the connection and becomes available.
        required:    False
        default:     SYSTEM_DEFAULT
    
    start_automatic: 
        description: is a flag to request the automatic starting of this DS when its association server
                     process start.
        required:    False
        default:     OFF
        choices: 
            - ON 
            - OFF
    
    init_pri: 
        description: is the initial system priority used to start a new server on this DS.
        required:    False
        default:     SYSTEM_DEFAULT
    
    trace: 
        description:    is a flag for activating the server trace facility in all servers using this DS and
                        started by this service. The Trace flag is not a permanent setting, is not stored in
                        the configuration database, and is not retained through a service shutdown.
        required:    False
        default:     OFF
    
    cpu_list: 
        description: is an SQL string literal (with multiple values enclosed in single quotes), containing
                     the list of CPU numbers where the service can start servers for this DS.
        required:    False
        default:     ALL
    
    all_stat: 
        description: is a flag to set for this DS, all seven individual statistics gathering flags.
        required:    False
        default:     OFF
    
    sql_execute_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of SQLExecute statistics
                     at the time an EXECUTE statement is received.
        required:    False
        default:     OFF
    
    sql_exec_direct_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of SQLExecDirect statistics
                     at the time an EXECUTE statement is received.
        required:    False
        default:     OFF
    
    sql_stmt_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of statement statistics at
                     the time a PREPARE statement is received.
        required:    False
        default:     OFF 

    sql_fetch_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of SQLFetch statistics at
                     the time a statement is closed.
        required:    False
        default:     OFF
    
    sql_prepare_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of SQLPrepare statistics
                     at the time a PREPARE statement is received.
        required:    False
        default:     OFF

    session_info_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of session statistics at the
                     time a session is terminated.
        required:    False
        default:     OFF

    connection_info_stat: 
        description: is a flag to turn ON, for this DS, the statistics gathering of session statistics at the
                     time a session is established.
        required:    False
        default:     OFF
notes:
    - This module requires a datasource present on the NonStop.

'''

EXAMPLES = '''
- name: configure MX datasource
  alter_datasource:    
    service_name: "mxsv1"    
    datasource_name: "dsname"
    max_server:"20"
    idle_server:"5"
    init_server:"5"
  register: result
  
'''

RETURN = '''
dest:
    description: alters SQL/MX datasource.
    returned: success
    type: string
    sample: none
'''


from ansible.module_utils.basic import *
import sys
sys.path.append('/tmp')
from ModifyMXDatasource import ModifyDatasource

def main():

    fields = {        
        "service_name": {"required": True, "type": "str"},
        "datasource_name": {"required": True, "type": "str"},
        "max_server": {"required": False, "type": "str", "default": "1"},
        "idle_server": {"required": False, "type": "str", "default": "0"},
        "init_server": {"required": False, "type": "str", "default": "0"},
        "idle_timeout": {"required": False, "type": "str"},
        "connection_timeout": {"required": False, "type": "str"},
        "start_automatic": {"required": False, "type": "bool", "default": "OFF"},
        "init_pri": {"required": False, "type": "str"},
        "trace": {"required": False, "type": "bool", "default": "OFF"},
        "cpu_list": {"required": False, "type": "str"},
        "all_stat": {"required": False, "type": "bool", "default": "OFF"},
        "sql_execute_stat": {"required": False, "type": "bool", "default": "OFF"},
        "sql_exec_direct_stat": {"required": False, "type": "bool", "default": "OFF"},
        "sql_stmt_stat": {"required": False, "type": "bool", "default": "OFF"},
        "sql_fetch_stat": {"required": False, "type": "bool", "default": "OFF"},
        "sql_prepare_stat": {"required": False, "type": "bool", "default": "OFF"},
        "session_info_stat": {"required": False, "type": "bool", "default": "OFF"},
        "connection_info_stat": {"required": False, "type": "bool", "default": "OFF"},
    }

    module = AnsibleModule(argument_spec=fields)
    
    modifyDatasource = ModifyDatasource(module.params)
    result = modifyDatasource.serveRequest()
    
    #parse the output.
    has_changed = result['result'] == 'success'  
    is_error = result['result'] == 'fail'       
    
    json_str = json.dumps(result)

    meta = {"status": 100, 'response': json_str}
    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error while configuring mx datasource", meta=result)


if __name__ == '__main__':
    main()