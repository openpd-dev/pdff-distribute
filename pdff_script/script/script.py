import os

class Script:
    def __init__(self, save_dir: str, model_name: str, forcefield_file: str, cuda_id: int=0) -> None:
        self.save_dir = save_dir
        self.model_name = model_name
        self.forcefield_file = forcefield_file
        self.cuda_id = cuda_id

    def format_context(self):
        raise NotImplementedError('format_context has not been overloaded')

    def writeFile(self):
        self.format_context()
        f = open(os.path.join(self.save_dir, self.file_name), 'w')
        print(self.context, file=f)
        f.close()