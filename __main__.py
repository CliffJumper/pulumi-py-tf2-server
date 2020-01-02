import pulumi
# from pulumi_aws import kms, s3
import pulumi_aws as aws
from pulumi_aws import ec2

size = 't2.micro'

# Read local config settings
config = pulumi.Config()

# Get env so we can match infra
env = pulumi.get_stack()
infra = pulumi.StackReference(f"CliffJumper/tf2-infra/{env}")

# Get the latest amazon linux AMI
ami = aws.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name": "name", "values": ["amzn-ami-hvm-*"]}])

# Set the public key
key_pair = ec2.KeyPair('tf2-keypair',
                       key_name='tf2-instance-keypair',
                       public_key=config.require('publickey'))

docker_cmd = "sudo docker run -d --net=host --name=tf2-dedicated -e SRCDS_TOKEN={token} cm2network/tf2".format(token=config.require('steam_token'))

user_data = """
#!/bin/bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
{cmd_str}
""".format(cmd_str=docker_cmd)

instance = ec2.Instance('tf2-instance',
                        instance_type=size,
                        vpc_security_group_ids=[infra.get_output('tf2-sg-id')],
                        ami=ami.id,
                        associate_public_ip_address=True,
                        subnet_id=infra.get_output('tf2-public-subnet-id'),
                        key_name=key_pair.key_name,
                        root_block_device={
                            'volume_size': 30
                        },
                        user_data=user_data
                        )
# pulumi.export('tf2-vpc-id', vpc.id)
# pulumi.export('tf2-public-subnet-id', public_subnet.id)
pulumi.export('publicIp', instance.public_ip)
pulumi.export('publicHostName', instance.public_dns)
