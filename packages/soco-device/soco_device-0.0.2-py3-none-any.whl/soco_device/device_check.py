import os
import json
import GPUtil


class DeviceCheck(object):
    def __init__(self):
        """ Log model gpu usage, save into a file, and auto choose
            available device (gpu/cpu) for the next time.

        Example:
            dc = DeviceCheck()
            device_name = dc.get_device_by_model(model_name_or_path)
            device = torch.device(device_name)
            
            dc.log_start()
            # inference model for one time here
            dc.log_end()
            dc.save(model_name_or_path)
        
        """
        self.local_dir = 'resources'
        self.current_device = None
        self.current_device_id = None
        self.model_memory_map = dict()
        self.save_name = 'config.json'
        self.log_map = dict()

        
    def get_device(self, max_load=1, max_mem=1):
        """ Get first available gpu device
        """
        device_id = GPUtil.getAvailable(order='memory', limit=1, maxLoad=max_load, maxMemory=max_mem)
        return(self._check_and_return(device_id))


    def get_device_by_model(self, model_id):
        """ Get first available gpu with largest available memory by model name,
            if not found return first gpu with largest available memory by default
        """
        path = os.path.join(self.local_dir, model_id)
        model_name = os.path.join(path, self.save_name)
        if model_id not in self.model_memory_map:
            if os.path.exists(model_name):  
                data = json.load(open(model_name))
                if 'memory_needed' in data:
                    print('Load memory info from json')
                    self.model_memory_map[model_id] = data['memory_needed']
                else:
                    return self.get_device()
            else:
                return self.get_device()

        all_device = GPUtil.getGPUs()
        device_id = [(i.id, i.memoryUsed) for i in all_device if i.memoryFree >= self.model_memory_map[model_id]]
        device_id = [sorted(device_id, key=lambda x: x[1])[0][0]] if len(device_id) > 0 else device_id
        print('GPU: {} Memory needed: {} '.format(device_id, self.model_memory_map[model_id]))
        return(self._check_and_return(device_id))


    def log_start(self):
        if self.current_device != 'cuda':
            return
        all_device = GPUtil.getGPUs()
        id_to_mem_st_map = {i.id: i.memoryUsed for i in all_device}
        self.log_map['start'] = id_to_mem_st_map[self.current_device_id]
        

    def log_end(self):
        if 'start' not in self.log_map:
            print('Did not find a log_start')
            return
        if self.current_device != 'cuda':
            return
        all_device = GPUtil.getGPUs()
        id_to_mem_ed_map = {i.id: i.memoryUsed for i in all_device}
        self.log_map['end'] = id_to_mem_ed_map[self.current_device_id]


    def save(self, model_path, save_max=True):
        if 'start' not in self.log_map or 'end' not in self.log_map:
            print('Did not find a complete log')
            return
        if not os.path.exists(model_path):
            if '/' not in model_path:
                model_path = os.path.join(self.local_dir, model_path)
            os.makedirs(model_path, exist_ok=True)
        memory_needed = self.log_map['end'] - self.log_map['start']
        if memory_needed < 0:
            print('Warning: memory change is negative')
            memory_needed = 0
        model_name = os.path.join(model_path, self.save_name)
        
        if not os.path.exists(model_name):
            json.dump({'model':model_path, 'memory_needed':memory_needed}, open(model_name, 'w'))
        else:
            # only overwrite the config when the memory usage is higher than the record
            data = json.load(open(model_name))
            if 'memory_needed' not in data or not save_max or memory_needed > data['memory_needed']:
                data['memory_needed'] = memory_needed
                json.dump(data, open(model_name, 'w'))
            else:
                print('Did not update since {}mb (current) <= {}mb (recorded)'.format(memory_needed, data['memory_needed']))
                return

        print('{} needs {} mb gpu memory.'.format(model_path, memory_needed))
        print('Saved into {}'.format(model_name))


    def _check_and_return(self, device_id):
        # return string of device name: 'cpu'/'cuda:x' 
        if len(device_id) == 0:
            self.current_device = 'cpu'
            return 'cpu'
        else:
            self.current_device = 'cuda'
            self.current_device_id = device_id[0]
            return 'cuda:{}'.format(self.current_device_id)
