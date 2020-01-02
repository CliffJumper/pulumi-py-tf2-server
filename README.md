# pulumi-py-tf2-server
Pulumi IaC to launch a TF2 server in the infrastructure setup by pulumi-py-tf2-infra

Sets-up EC2 instance, user-data, etc for running TeamFortress 2 servers in AWS using:
https://github.com/CliffJumper/pulumi-py-tf2-infra. 

Based on info from: https://wiki.teamfortress.com/wiki/Linux_dedicated_server

Runs TF2 server as a Docker container in EC2

## Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
1. [Configure Pulumi for AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/)
1. [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)

## Deploying and running the program

1. Install dependencies (a `virtualenv` is recommended - see [Pulumi Python docs](https://www.pulumi.com/docs/intro/languages/python/)):

    ```
    $ pip install -r requirements.txt
    ```

1.  Create a new stack:

    ```
    $ pulumi stack init tf2-server
    ```

1.  Set the AWS region:

    ```
    $ pulumi config set aws:region us-east-2
    ```

1.  Update your config settings by editing Pulumi.<env>.yaml  The current settings in the file are invalid!!!

    ```
    $ cat Pulumi.dev.yaml
    config:
        aws:profile: <your aws profile name here>
        aws:region: us-east-2
        tf2-server:publickey: <put ssh public key here>
        tf2-server:steam_token: <your steam token here>
    ```

1.  Run `pulumi up` to preview and deploy changes:

    ```
    $ pulumi up
    Previewing stack 'tf2-server-dev'
    Previewing changes:
    ...
        
    Do you want to perform this update? yes
    Updating (dev):

            Type                 Name            Status      
        +   pulumi:pulumi:Stack  tf2-server-dev  created     
        +   ├─ aws:ec2:KeyPair   tf2-keypair     created     
        +   └─ aws:ec2:Instance  tf2-instance    created     
    
    Outputs:
        publicIp      : "<generated>"

    Resources:
        + 3 created

    Duration: 32s

    Permalink: https://app.pulumi.com/<your-pulumi-id>/tf2-server/dev/updates/1
    ```

1.  View the host name and IP address of the instance via `stack output`:

    ```
    $pulumi stack output 
    Current stack outputs (2):
        OUTPUT          VALUE
        publicHostName  
        publicIp        <ip for instance>
    ```    


## Clean up

To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.