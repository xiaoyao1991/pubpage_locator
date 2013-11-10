class MyClass(object):
    def __init__(self):
        super(MyClass, self).__init__()
        self.name = 'xiaoyao'
    

    def say_my_name(self):
        print self.name




class Caller(object):
    def __init__(self, cls):
        super(Caller, self).__init__()
        self.cls = cls

    def call(self):
        tmp_obj = self.cls()
        tmp_obj.say_my_name()



if __name__ == '__main__':
    # c = Caller(MyClass)
    # c.call()
    cls_lst = []
    cls_lst.append(MyClass)
    cls_lst.append(Caller)

    cls_lst[1](cls_lst[0]).call()
        
        