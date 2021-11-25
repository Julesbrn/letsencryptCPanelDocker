# Cpanel Letsencrypt Docker
The purpose of this docker is to simplify creating and automating letsencrypt certificates via dns records.

This docker will work with any cpanel (version 96 and above). 

# How to use
In order to use this docker, you will need to create a json with some required information. See below.

Once a domain's information json has been created and placed in the correct folder, you can run either of the following commands.

To create certs for all available domains:
```bash
docker exec -it DOCKER_CONTAINER_NAME /dockerRoot/scripts/runAllDomains.sh
```

To create a cert for a specific domain:
```bash
docker exec -it DOCKER_CONTAINER_NAME /dockerRoot/scripts/runCertbot.sh example.com
```
You can automate this by setting a crontab on the host.

# Domain information jsons
There are two types of domains supported. Standard and delegated.

Standard
```json
{
    "username": "USERNAME",
    "apiKey": "CPANEL APIKEY",
    "cpanelUrl": "https://cpanel.example.com:2083"
}
```
Delegated
```json
{
    "username": "USERNAME",
    "apiKey": "CPANEL API KEY",
    "cpanelUrl": "https://cpanel.example.com:2083",
    "ALIAS__acme-challenge": "_acme-challenge.MYDOMAIN",
    "controllingDomain": "MYDOMAIN.TLD"
}
```
In the event a domain is controlled by a non-cpanel dns host or an incompatible version, you can use a cname to perform the dns verification instead.
## JSON Key definitions
username - This is the username you use to log into to cpanel

apiKey - This is the apikey you will generate in cpanel. See below for instructions

cpanelUrl - This is normally "https://cpanel.MYDOMAIN.TLD:2083". Sometimes your dns host will have a different url. When in doubt, contact support.

ALIAS_{ZONE} - When using a delegate domain, you will need to specify the zone to use instead. In this case, we are looking for ALIAS__acme-challenge (note the double underscore). This means instead of modifying _acme-challenge.example.com, it will be modifying _acme-challenge.MYDOMAIN.example.net. See below for further explanation.

controllingDomain - The domain that will actually contain the dns record.

## Using a delegate domain
For the following example. I will be referring to two different domains. good.com and bad.com. In this case, bad.com is either a non-cpanel controlled domain, or an incompatible version. good.com is controlled by a compatible cpanel host.

Normally certbot would give you a key and you would put this key in _acme-challenge.bad.com. In our case, we cannot do that because bad.com does not use a compatible cpanel version. 

Instead, we will create a cname _acme-challenge.bad.com to _acme-challenge.bad.good.com.

In this case, we would set "ALIAS__acme-challenge" to "_acme-challenge.bad" and "controllingDomain" to "good.com"

After that, we then need to define the apikey, cpanelUrl, and username.

## Username
This should be easy, this is what you would login with. If you login via another method, login to cpanel and look for "Current User" on the right side.

## Api Key
To create the api key, do the following.
1. Login to cpanel
2. Security > Manage API Tokens (You can also search api key)
3. Click create on the right side
4. Give the token a name
5. Click create

You can optionally specify an expiration date.

The generated key can then be used for our purposes.

# Container Folders
## /dockerRoot/certbot_tmp
This is the folder that certbot uses as it's temporary folder. If you need to debug certbot, you can expose this to the host.

## /dockerRoot/certs
This is the output folder where the generated certificates are output. (They will not be symbolic links)

## /dockerRoot/domains
This is where your jsons that contain the domain information will go. You can either mount this to the host, or copy files yourself.

## /dockerRoot/scripts
This is where the scripts are stored. Containing both the python file and a few bash files.

# Starting the docker container
Here is my recommended run command
```bash
docker run -dit --name letsencrypt_cpanel_dkr \
-v /mnt/letsencrypt_cpanel_dkr/certbot_tmp:/dockerRoot/certbot_tmp \
-v /mnt/letsencrypt_cpanel_dkr/domains:/dockerRoot/domains \
-v /mnt/letsencrypt_cpanel_dkr/certs:/dockerRoot/certs \
-e emailAddress="YOUR EMAIL ADDRESS HERE" \
--restart unless-stopped \
letsencrypt_cpanel 
```
The docker itself will not do anything automatically. There are no crontabs and the entry point only keeps the container running.

You will need to specify an email address for letsencrypt. Your ip address will also be logged as usual by letsencrypt.

# Getting the image
## Building it yourself
Clone the repo and cd to the root folder. Then run the following command:
```bash
docker build . --tag "letsencrypt_cpanel" --no-cache
```
## Pulling from DockerHub
```bash
docker pull julesbrn/letsencrypt-cpanel-docker:v1
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

Contact me for commercial use.
