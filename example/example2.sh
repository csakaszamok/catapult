#!/bin/bash
cd example_playbook
ansible-playbook -i inventories/dev1 site.yml --extra-vars "release_folder=../payloads/release_v0.0.2"
cd ..