> CONFIGURE SQL/MX DATASOURCE

  This module helps to add/remove a datasource on NonStop with the specified MX service and the datasource name. If the action is Add
  then the datasource will be added and started with provided service name. "delete" stops the datasource abruptly and deletes the
  datasource.

Options (= is mandatory):

= action
        To determine whether to add or delete the datasource. (Choices: add, delete) [Default: add]

- all_stat
        is a flag to set for this DS, all seven individual statistics gathering flags. [Default: False]

- connection_info_stat
        is a flag to turn ON, for this DS, the statistics gathering of session statistics at the time a session is established.
        [Default: False]

- connection_timeout
        is a keyword or the number of minutes a client-server connection can remain idle before the server terminates the connection
        and becomes available. [Default: SYSTEM_DEFAULT]

- cpu_list
        is an SQL string literal (with multiple values enclosed in single quotes), containing the list of CPU numbers where the
        service can start servers for this DS. [Default: ALL]

= datasource_name
        The name of the datasource which needs to be configured.

- idle_server
        is the lower limit on the available idle servers that are operational for this service on this DS [Default: 0]

- idle_timeout
        is a keyword or the integer number of minutes a server waits in the available state for a connection before it stops itself
        when the count of servers exceeds the IdleServer count value for the DS. [Default: SYSTEM_DEFAULT]

- init_pri
        is the initial system priority used to start a new server on this DS. [Default: SYSTEM_DEFAULT]

- init_server
        is the suggested number of servers that each service starts when the DS first starts. [Default: 0]

- max_server
        is the upper limit on the servers that can be operational for this service on this DS. [Default: 1]

= service_name
        MXCS Service where the datasource being tied up with.

- session_info_stat
        is a flag to turn ON, for this DS, the statistics gathering of session statistics at the time a session is terminated.
        [Default: False]

- sql_exec_direct_stat
        is a flag to turn ON, for this DS, the statistics gathering of SQLExecDirect statistics at the time an EXECUTE statement is
        received. [Default: False]

- sql_execute_stat
        is a flag to turn ON, for this DS, the statistics gathering of SQLExecute statistics at the time an EXECUTE statement is
        received. [Default: False]

- sql_fetch_stat
        is a flag to turn ON, for this DS, the statistics gathering of SQLFetch statistics at the time a statement is closed.
        [Default: False]

- sql_prepare_stat
        is a flag to turn ON, for this DS, the statistics gathering of SQLPrepare statistics at the time a PREPARE statement is
        received. [Default: False]

- sql_stmt_stat
        is a flag to turn ON, for this DS, the statistics gathering of statement statistics at the time a PREPARE statement is
        received. [Default: False]

- start_automatic
        is a flag to request the automatic starting of this DS when its association server process start. (Choices: True, False)
        [Default: False]

- trace
        is a flag for activating the server trace facility in all servers using this DS and started by this service. The Trace flag
        is not a permanent setting, is not stored in the configuration database, and is not retained through a service shutdown.
        [Default: False]

Requirements:  Ansible must be installed, NonStop server with proper user credentials

EXAMPLES:
- name: configure MX datasource
  configure_datasource:    
    service_name: "mxsv1"    
    datasource_name: "dsname"
    action: "add"
  register: result
- name: configure MX datasource 
  configure_datasource:
    service_name: "mxsv1"    
    datasource_name: "dsname"
    action: "delete"
  register: result

RETURN VALUES:
dest:
    description: add/delete SQL/MX datasource.
    returned: success
    type: string
    sample: none


MAINTAINERS: senthilt
