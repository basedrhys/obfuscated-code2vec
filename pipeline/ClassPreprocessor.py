import subprocess

class ClassPreprocessor:
    def __init__(self, jar_path, args):
        self.jar_path = jar_path
        self.args = args

    def get_methods(self, file_path):
        command = ['java', '-jar', self.jar_path, "-s", file_path, self.args]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            return result.stdout.decode('utf-8').split("_METHOD_SPLIT_")
        except:
            print("ERROR DECODING METHODS IN FILE:", file_path)
            return []
