import importlib.abc, importlib.util
import os, sys
import json


class CustomPathFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: str, target=None) -> importlib.util.spec_from_file_location:
        if not path:  # If path not setted set path to current working dir
            path = [os.getcwd()]

        if "." in fullname:  # Get ext. of file name
            fullname = fullname.split(".")[-1]
        
        for cat in path:  # Loop in curr. dir
            in_path: str = f"{os.path.join(cat, fullname)}.json"
            
            if os.path.exists(in_path):
                return importlib.util.spec_from_file_location(
                    name=f"{fullname}.json",
                    location=in_path,
                    loader=CustomDataLoader()
                )

class CustomDataLoader(importlib.abc.Loader):
    def repack(self, mod, data) -> None:
        if type(data) == dict:
            for key, value in data.items():
                if key.startswith("__") and key.endswith("__") or hasattr(mod, key):
                    continue
                setattr(mod, key, value)
        mod.raw_data = data

    def exec_module(self, mod) -> None:
        data = self.load_data(open(mod.__spec__.origin, "r").read())
        self.repack(mod, data)
    
    def load_data(self, data) -> dict:
        return json.loads(data)


sys.meta_path.append(CustomPathFinder())
