#!/usr/bin/env python

"""
An Ansible action plugin waiting by user input
csakaszamok@gmail.com
"""
import time
import datetime
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.utils.vars import isidentifier

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display  # pylint: disable=ungrouped-imports
    display = Display()

def printGrey(self, str):
    self._display.display(str, color='dark gray') 

def printWarning(self, str):
    # self._display.warning(str)
    self._display.display(str, color='magenta') 


class ActionModule(ActionBase):
     """     
     Example:
        - name: schedule_setting_process
          wait_for_time:
            catapult_start_time: "{{prompt_input.user_input|lower}}"
     """
     def run(self, tmp=None, task_vars=None):
        catapult_start_time = self._task.args.get('catapult_start_time', '')
        catapult_delta_time = self.getData()                                
        # printGrey(self,  self._task.get_path())        

        if self.error != "":            
            raise AnsibleError('"catapult_time_format_error": '+self.error)                 
            # return {
            #     'ansible_facts': {"catapult_time_format_error": self.error},
            #     'changed': False,
            # }   

        if catapult_delta_time != "0000":
            printGrey(self, 'user input      : ' + str(catapult_start_time) )         
            printGrey(self, 'remaining time  : ' + catapult_delta_time)
            printWarning(self,'launch datetime : ' + str(self.end_t))
            while self.end_t >= datetime.datetime.now():
                time.sleep(1)

        return {             
             'ansible_facts': {"catapult_time_format_error": ""},
             'changed': False,
        }

     def getData(self, tmp=None, task_vars=None):                 
        self.error = ''
        end = self._task.args.get('catapult_start_time', '')        
        if end == "":
            return "0000"
        
        catapult_delta_time = ""
                
        try:
            # start_t = datetime.time(hour=int(start[0:2]), minute=int(start[2:4]))
            start_t = datetime.datetime.now()
        except Exception as e:
            self.error = str(e)
            return                
            
        try:
            end_t = datetime.time(hour=int(end[0:2]), minute=int(end[2:4]))
            now = datetime.datetime.now().time() 
            if end_t > now:
                end_t = datetime.datetime.combine( datetime.datetime.now().date(), 
                          end_t)
            else:              
                end_t = datetime.datetime.combine( datetime.datetime.now().date() + datetime.timedelta(days=1), 
                          end_t)
            self.end_t = end_t
        except Exception as e:
            self.error = str(e)
            return                        
        try:            
            now = datetime.datetime.now()
            if end_t > now:            
                catapult_delta_time = end_t - now
            else:    
                catapult_delta_time = now - end_t

        except Exception as e:
            self.error = str(e)
            return                
        
        return str(catapult_delta_time)