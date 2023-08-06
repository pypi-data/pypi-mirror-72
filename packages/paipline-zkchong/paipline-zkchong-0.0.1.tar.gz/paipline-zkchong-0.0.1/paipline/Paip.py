class Paip():
    '''Simple paipline.'''
    def __init__(self, step_list:list) -> None:
        '''
        step_list: Adding the step list to paip. Please follow the guideline 
        on setting the step. 
        '''
        self.step_list = step_list

        self.output_dict = {}
        self.check_step_list(self.step_list)
    
    def check_step_list(self, step_list):
        '''Ensure the step list has the default values in place. '''
        for step in step_list:
            # Each step must has name
            assert('name' in step.keys())
            # Create default value if not exists
            self.set_default_key_value(step, 'output_list', [])
            self.set_default_key_value(step, 'obj_dict', {} )
            self.set_default_key_value(step, 'persist_obj', False )
            self.set_default_key_value(step, 'run_dict', {} )
    
    def set_default_key_value(self, step:dict, key:str, obj )-> None:
        '''Assign default key value to step.'''
        if key not in step:
            step[key] = obj
    
    def add_next_paip(self, paip):
        '''Adding a new paip at the end of this one. '''
        self.step_list += paip.step_list
    
    def run(self, run_mode:str, obj_dict:dict, debug = False):
        '''
        To run the paip.
        
        run_mode: Run all the code at run_dict->run_mode.
        obj_dict: The external objects what we want to bring into the paip.
        debug: True if we want to see each running step.
        '''
        # This dict will hold the output variables at each iteraction.
        # Initially, this will hold our input variables.
        self.output_dict = obj_dict
        
        for step in self.step_list:
            # Unpack the external variables to locals 
            _locals = locals()
            _locals.clear() 
            _locals.update(**step['obj_dict']) # Unpack those object per step
            _locals.update(**self.output_dict) # Unpack those from previous step

            # Run pre-exec
            for code in step['run_dict'][run_mode]:
                if debug:
                    print('name:%s\n    code=\'\'\'%s\'\'\' ' % (step['name'], code))
                exec(code, _locals)
            
            # Store the local object for next run.
            if step['persist_obj']:
                step['obj_dict'].update({k: v for k,v in locals().items()
                                            if k in step['obj_dict'].keys() } )
            
            # Keep those selected local variables as output or
            # the input for the next step. 
            self.output_dict = {key:value for key, value in locals().items() 
                                            if key in step['output_list']}

