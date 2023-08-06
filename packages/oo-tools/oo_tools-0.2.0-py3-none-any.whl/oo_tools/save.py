import os, pathlib, pickle

def check_octal(func):
    def wrapper(*args, **kwargs):
        try:
            defaults = func.__defaults__
            if len(defaults) > 0:
                octal = defaults[0]
                
            if len(args) > 1:
                octal = args[1]
            
            if 'permissions' in kwargs.keys():
                octal = kwargs['permissions']

            int(octal)
            
            if len(octal) > 4:
                raise AttributeError(f'Octal length must be <= 4, not = {octal}')
            
            return func(*args, **kwargs)
    
        except ValueError:
            raise AttributeError(f'Octal permissions must be numbers, not = {octal}')
    
    return wrapper

class Saver:
    
    """
    Save your object to a file location. Use this object as a base class for another.
    """

    
    @property
    def filepath(self):
        """Filepath of where you want to save the object.
        
        Returns:
            str -- filepath
        """
        try:
            return self._filepath
        except:
            raise FileNotFoundError('You didn\'t specify the filepath of the object to save!')
            
    @filepath.setter
    def filepath(self, filepath):
        """Set the filepath. For exmaple/var/lib/mytest.obj
        
        Arguments:
            filepath {str} -- filepath or location where you want to save the object with teh file name
        
        Raises:
            IOError: The directory doesn't exist
            AttributeError: No suffix supplied, like .obj
        """
        fp = pathlib.Path(filepath)
        
        if not os.path.exists(fp.parent):
            # check the directory
            raise IOError(f'Directory = {fp.parent} does not exist! Create it first')
        
        if not fp.suffix:
            # check that there's a suffix
            raise AttributeError(f'You must supply a suffix to the filepath. For example, "/this/path/test.obj", not {filepath}')
        
        self._filepath = filepath
    
    @check_octal
    def save(self, permissions='0644'):
        """save the object to the path specified with .filepath

        Args:
            permissions (str, optional): Change the permissions of the save file, e.g. permissions='775'. Defaults to '0644'.
        """
        with open(self.filepath, 'wb') as f:
            pickle.dump(self.__dict__, f, 2)
            f.close()
            
        if permissions != '0644':
            os.system(f'chmod {permissions} {self.filepath}')
    
    def load(self):
        """Load the object
        """
        with open(self.filepath, 'rb') as f:
            tmp_dict = pickle.load(f)
            self.__dict__.update(tmp_dict)

            f.close()