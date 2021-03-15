import os, shutil

class RecipeTorsion:
    def __init__(self, save_dir) -> None:
        self.save_dir = save_dir
        self.tree = {
            'simulation': {},
            'str': {},
            'output': {
                'log_files',
                'pdb_files',
                'meta_files'
            },
            'ansys': {},
        }

    def _createDirsFromTree(self, parent_dir, tree):
        for key, value in list(tree.items()):
            os.mkdir(os.path.join(parent_dir, key))
            if isinstance(value, dict) and value != {}:
                self._createDirsFromTree(os.path.join(parent_dir, key), value)
            elif isinstance(value, set):
                for i in list(value):
                    os.mkdir(os.path.join(parent_dir, key, i))
                
            
    def createDirs(self):
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
        os.mkdir(self.save_dir)
        self._createDirsFromTree(self.save_dir, self.tree)