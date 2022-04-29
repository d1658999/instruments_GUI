import pyvisa

class test(pyvisa.ResourceManager):
    def __init__(self):
        gpib = self.get_gpib()
        self.inst = super().open_resource(gpib)
        self.inst.timeout = 5000
        print(self.inst.timeout)

    def get_gpib(self):
        for resource in super().list_resources():
            if 'GPIB' in resource:
                return resource


def main():
    x = test()
    print(x)




main()




