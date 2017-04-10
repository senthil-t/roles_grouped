> CONFIGURE SQL/MX SERVICE

  To start or stop SQL/MX MXCS service with the specified service name and port number. Optionally, user can choose to provide the
  MXOAS guardian location.

Options (= is mandatory):

= action
        To determine whether to start or stop the service. (Choices: start, stop) [Default: start]

- mxoas_location
        Guardian location of the MXCS objects. [Default: $system.zmxodbc.mxoas.]

= port_number
        MXCS service will be started with this name.

= service_name
        MXCS Service will be started with this name.

Requirements:  Ansible must be installed, NonStop server with proper user credentials

EXAMPLES:
- name: start MX Service
  configure_mxservice:    
    service_name: "mxsv1"    
    port_number: "18650"
    action: "start"
  register: result

RETURN VALUES:
dest:
    description: starts/stops SQL/MX service.
    returned: success
    type: string
    sample: none


MAINTAINERS: senthilt
