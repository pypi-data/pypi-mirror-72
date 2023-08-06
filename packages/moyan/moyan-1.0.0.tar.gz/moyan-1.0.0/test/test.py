import moyan
from moyan.tools import walkDir2List, cv_read

@moyan.decorator.time_cost
def hello():
    path = r'C:\Users\Moyan\Desktop\demo\demo.jpg'
    im = cv_read(path)
    print(im.shape)
    print("hello")



for i in range(20):
    print(hello())  