import requests
import json

class pyRepRapComm:
    
    status_path = '/rr_status'
    file_info_path = '/rr_fileinfo'
    
        
    def __init__(self, duet_addr):
        self.base_url = f"http://{duet_addr}"
        
    def get_status_info(self, status_type=1):
        """ Gets the current status of the printer 
            Types:  1 - Default
                    2 - Enhanced
                    3 - Current Print Status
            Returns parsed JSON from the printer
        """
        status_url = self.base_url + self.status_path
        
        r = requests.get(status_url,params={'type':status_type})
        data = json.loads(r.text)
        return data
    
    def get_file_info(self):
        """ Gets the info about the currently printing file """
        print_status = self.get_status_info()
        if 'P' not in print_status['status']:   # If we're not printing, we return none
            return None
       
        file_url = self.base_url + self.file_info_path
        r = requests.get(file_url)
        data = json.loads(r.text)
        return data
    
    def get_printer_temps(self, status_data=None):
        """ Gets current printer temp information """
        
        degree_sign= u'\N{DEGREE SIGN}'
        temps = {'bed':dict(),'heads':list()}
        
        print_status = None
        if not status_data:
            print_status = self.get_status_info()
        else:  # Avoid repolling if we just did already
            print_status = status_data
        
        # Bed Temp
        temps['bed']['current'] = print_status['temps']['bed']['current']
        temps['bed']['target'] = print_status['temps']['bed']['active']
        temps['bed']['formatted'] = f"{temps['bed']['current']}{degree_sign} / {temps['bed']['target']}{degree_sign}"
        
        # Print Head Temps
        # Zip together the info about heads to support multiple tools
        # zip will give us a list of tuples where the values are (current, active, standby) for each nozzle
        combined_nozzles = list(zip(print_status['temps']['heads']['current'],
                                    print_status['temps']['heads']['active'],
                                    print_status['temps']['heads']['standby']))     
        
        counter = 0
        for nozzle in combined_nozzles:
            nozzle_formatted = f"{nozzle[0]}{degree_sign} / {nozzle[1]}{degree_sign}"
            temps['heads'].append({'head':counter,
                               'current':nozzle[0],
                               'target':nozzle[1],
                               'standby':nozzle[2],
                               'formatted': nozzle_formatted})
            counter+=1
              
        return temps
        
    def get_printer_status(self, status_data=None):
        print_status = None
        if not status_data:
            print_status = self.get_status_info()
        else:  # Avoid repolling if we just did already
            print_status = status_data
            
        status_values = {'F':'Flashing Firmware',
                         'O':'Off',
                         'H':'Halted',
                         'D':'Pausing',
                         'S':'Paused',
                         'R':'Resuming',
                         'P':'Printing',
                         'M':'Simulating',
                         'B':'Busy',
                         'T':'Changing Tool',
                         'I':'Idle'}
        
        
        return (print_status['status'], status_values[print_status['status']])
    
    def get_printer_position(self, status_data=None):
        """ Simple function to return the XYZ position of the printer """
        print_status = None
        if not status_data:
            print_status = self.get_status_info()
        else:  # Avoid repolling if we just did already
            print_status = status_data

        return print_status['coords']['xyz']
            
    def get_print_info(self):
        """ Gathers information about the current print job that is running 
            Returns None if there's nothing printing
            TODO: See if there are other status where we may get this info?
        """
        print_status = self.get_status_info(3)   # We need type 3 for print status info
        if 'P' not in print_status['status']:
            return None
        
        file_data = self.get_file_info()
        
        # Percentage Complete
        print_info = {'PercentComplete':dict(),
                      'layers':dict(),
                      'elapsed':dict(),
                      'remaining':dict()}
        
        print_info['PercentComplete']['value'] = print_status['fractionPrinted']
        print_info['PercentComplete']['formatted'] = f"{print_status['fractionPrinted']}%"

        # Layer Status
        current_layer = print_status['currentLayer']
    
        if file_data['firstLayerHeight'] > 0:
            total_layers = (file_data['height'] - print_status['firstLayerHeight']) / file_data['layerHeight'] + 1
        else:
            total_layers = file_data['height'] / file_data['layerHeight']
    
        print_info['layers']['total'] = int(total_layers)
        print_info['layers']['current'] = current_layer
        print_info['layers']['formatted'] = f"{current_layer} / {int(total_layers)}"
        
        # Elapsed Print Time
        elapsed = print_status['printDuration']
        hours = divmod(elapsed, 3600)
        minutes = divmod(hours[1], 60)
        
        print_info['elapsed']['totalSeconds'] = elapsed
        print_info['elapsed']['hours'] = hours[0]
        print_info['elapsed']['minutes'] = minutes[0]
        print_info['elapsed']['seconds'] = minutes[1]
        print_info['elapsed']['formatted'] = f"{hours[0]:02.0f}:{minutes[0]:02.0f}:{minutes[1]:02.0f}"
        print_info['remaining'] = print_status['timesLeft']
        
        return print_info
