> ## 🛠 Status: In Development
> Catapult is currently in development. This package is still being developed and is not yet production ready. There are things that haven't been finalized yet, so this repo might change before it's ready for production. Check out the list of Known Issues and TODOs for updates.
# Catapult
[![version](https://img.shields.io/badge/version-0.2.0-g.svg)](https://semver.org)  
<img src="csakaszamok-catapult_300x300.svg" width="100">
<p>
  <a href="https://github.com/csakaszamok/catapult/releases">Download</a> ·
  <a href="#install">Install</a>  ·
  <a href="#examples">Examples</a>  ·
  <a href="#todos">Todos</a>  ·
</p>

----

Catapult is an open source deployment tool and package format for ansible.  
You can easily separate your depoyment logic and your release packages.

# Install
It's easy, just install capatult role under your roles folder.
```bash
ansible-galaxy install csakaszamok-catapult
```

# Usage

Just call it from your ansible playbook
```yml
- include_role:
    name: csakaszamok.catapult
```
# Parameters

| Name                 | Type     | Required | Default | Description    |
| -------------------- | -------- | -------- | ------- | ---------------|
| `autostart`          | bool     | not      | false   | If it is false you have to confirm to start manually |
| `release_folder`     | string   | yes      |         | Current deployment folder path |
| `inventory_name`     | string   | yes      |         | It's reletad to a host gorup name in the inventories folder |

# Basic concept

When you often have to manage a lot of release then probably 
you want to prepare these future deployments in diffrerent packages. 
With catapult you can easily separete your deployment logic and your deployment packages.  

Catapult is just an ansible playbook that uses payloads for identifying deployment packages.  
Each deployment package (name is playload) is a simple folder layout that contains a collection of ansible rules where
every rules represent a host group in your inventory.  
So if you know ansible then you already know catapult palyload format.

In summary:

- catapult = an ansible playbook that uses csakaszamok-catpault role
- payload, projectile = a folder with host gorup specified roles  

Let's take a look for some examples.

# Examples
> Tip: You can find below examples under example folder
## Preparing
First of all create some containers for playing

```bash
docker run -it -d -p 1121:22 rastasheep/ubuntu-sshd
docker run -it -d -p 1122:22 rastasheep/ubuntu-sshd
docker run -it -d -p 1123:22 rastasheep/ubuntu-sshd
```
## Build up your own catapult powered playbook:  

<img src="csakaszamok-catapult-manual_300x300.svg" alt="k6" width="100"/>

/home/your-playbook/site.yml:
```yaml
---  
  - name: deploy
    hosts: all            
    gather_facts: false
    tasks:       
    - include_role:
        name: csakaszamok.catapult
      vars:
        - autostart: true        
      when: release_folder and inventory_name
```    
/home/your-playbook/inventories/dev1/hosts:
```yaml
[all:vars]
inventory_name=dev1

; --> ! payloads will use groupnames like this to identify foldernames under payloads !
[webserver] 
local1 ansible_host=127.0.0.1  ansible_user=root ansible_ssh_pass=root ansible_port=1121
local2 ansible_host=127.0.0.1  ansible_user=root ansible_ssh_pass=root ansible_port=1122

; --> ! payloads will use groupnames like this to identify foldernames under payloads !
[anotherservers] 
local3 ansible_host=127.0.0.1  ansible_user=root ansible_ssh_pass=root ansible_port=1123
```

and finally but not least don't forget to install catapult under roles folder:
```bash
ansible-galaxy install csakaszamok-catapult
```

Everything is ready, so now we can prepare some payloads for catapult.

## Payload example 1: copy file to host(s)

> Goal: we want to put a simple file to /home/document on target server  

Create a payload folder layout
```bash
release_v0.0.1
|
---- webserver --> ! this folder name relates to inventory hostnames !
     |
     ---- files
          |
          ---- home
               |
               ---- documents
                    |
                    ---- text1.txt   
```

Execute your script:
```bash
ansible-playbook -i inventories/dev1 site.yml --extra-vars "release_folder=/home/my-payloads/release_v0.0.1" 
```
## Payload example 2: events, manage services

Create another payload folder
```bash
release_v0.0.2
|
---- webserver --> ! this folder name relates to inventory hostnames !
     |
     ---- handlers
     |     |
     |     ---- main.yml
     |          
     ---- taksk
          | 
          ---- main.yml                              
```

handlers' main.yml:
```yml
---
- name: "{{ role_name|basename }}_on_before_copy_files"
  service:
      name: nginx
      state: stopped

- name: "{{ role_name|basename }}_on_after_copy_files"
  service:
      name: nginx
      state: started
```
Becuase all of the handlers are in global scope, handlers' name have to follow a specific name convention: current role name + suffix:  
`{{ role_name|basename }}_on_after_copy_files`

tasks' main.yml:
```yml
---
- name: ensure nginx is at the latest version
  apt: name=nginx state=latest
- name: basic start nginx
  service:
      name: nginx
      state: started
```
Execute your script:
```bash
ansible-playbook -i inventories/dev1 site.yml --extra-vars "release_folder=/home/my-payloads/release_v0.0.2" 
```

## TODOs 
- [ ] Precise shot
- [ ] Parallel launch
- [ ] Safe projectile
- [ ] Fire ball