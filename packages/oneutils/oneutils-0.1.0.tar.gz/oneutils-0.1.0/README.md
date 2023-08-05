# oneutils
python3 utils 


# how to use
```
first intstall:
pip3 install oneutils
pip3 install oneutils==0.1.0

update:
pip3 install --upgrade oneutils

```
# user in your code
```
from oneutils import hello  
hello.say()
```

# pip
1. add .pypirc and `pip3 install twine`
2. cd your work folder and use `python3 setup.py sdist`
3. cd dist and `twine upload xxxx-x.x.x.tar.gz`