echo off
pushd  example_playbook
wsl ansible-playbook -i inventories/dev1 site.yml --extra-vars "release_folder=../payloads/release_v0.0.1"
popd