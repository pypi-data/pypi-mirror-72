# cselector (Console Selector)

## Description

Console selector for python.
This is inspired from https://pypi.org/project/pick/ and it wanted to more customize for image previewer in iTerm2(imgcat).


##### Single Selector
```
Title hoge hoge.
=>  ItemA
    ItemB
    ItemC
```

##### Multi Selector
```
Title hogehoge
[ ]  Item0
[ ]  Item1
[*]  Item2
[ ]  Item3
[ ]  Item4
[ ]  Item5
[ ]  Item6
[ ]  Item7
[*]  Item8
[ ]  Item9
1 2 3 4 5
```

##### Binary Selector
```
Do you do machine learning? (default: yes)[Y/n] > Yes
# True
```

<br>
<br>

### Features

- Single selector.
- Multi selector.
- Binary selector.
- No dependencies.
- No clear display.
- Page navigation.
- All selector.
- Image viewer (for private)



<br>


## Installation
```
pip3 install cselector
```

<br>
<br>

------


#### Single selector

- Move: 'Up', 'Down' key
- End: 'Return' key

```
from cselector import selector

selected = selector(options=["ItemA","ItemB","ItemC"],title="Title hoge hoge.")
print(selected) # (<Index>,<Option>)
```
```
Title hoge hoge.
=>  ItemA
    ItemB
    ItemC
```
------


####  Multi Selector

- Pagenation: 'Left', 'Right' key
- Move: 'Up', 'Down' key
- Select: 'Space' key
- End: 'Return' key
- Preview: '@' key


```
from cselector import multi_selector

options = []
for x in range(47):
    options.append("Item"+str(x))
selected_array = multi_selector(options=options,title="Title hogehoge")
print(selected_array) # [(<Index>,<Option>),(<Index>,<Option>),(<Index>,<Option>)....]
```
```
Title hogehoge
[ ]  Item0
[ ]  Item1
[*]  Item2
[ ]  Item3
[ ]  Item4
[ ]  Item5
[ ]  Item6
[ ]  Item7
[*]  Item8
[ ]  Item9
1 2 3 4 5
```


####  Multi Selector - With all selector
```
from cselector import multi_selector

options = []
for x in range(47):
    options.append("Item"+str(x))
selected_array = multi_selector(options=options,title="Title hogehoge",all="All item title")
print(selected_array) # [(<Index>,<Option>),(<Index>,<Option>),(<Index>,<Option>)....]
```
```
Title hogehoge
[*]  All item title
[*]  Item0
[*]  Item1
[*]  Item2
[*]  Item3
[*]  Item4
[*]  Item5
[*]  Item6
[*]  Item7
[*]  Item8
1 2 3 4 5
```


####  Multi Selector - Minimum selection
```
from cselector import multi_selector

options = []
for x in range(47):
    options.append("Item"+str(x))
selected_array = multi_selector(options=options,title="Title hogehoge",min_count=2)
print(selected_array) # [(<Index>,<Option>),(<Index>,<Option>),(<Index>,<Option>)....]
```


####  Multi Selector - Maximum item number of page


```
from cselector import multi_selector

options = []
for x in range(47):
    options.append("Item"+str(x))
selected_array = multi_selector(options=options,title="Title hogehoge",split=20)
print(selected_array) # [(<Index>,<Option>),(<Index>,<Option>),(<Index>,<Option>)....]
```

#### Multi Selector - With previewer (Required aimage library)

- Preview: '@' key


```
import aimage
import glob
import os
from cselector import multi_selector
options = []
preview = []
for f in glob.glob(os.path.expanduser("~/cg/*.jpg")):
    preview += [aimage.load(f)]
    options += [os.path.basename(f)]
print(options)
selected_array = multi_selector(options=options,title="Title hogehoge",preview=preview,preview_console=True)
print(selected_array) # [(<Index>,<Option>),(<Index>,<Option>),(<Index>,<Option>)....]
```


------


####  Binary selector - Yes or No
```
from cselector import yes_or_no
ret = yes_or_no(question="Do you do machine learning?",default="y")
print(ret) # True/False
```



------

<br>


#### Supported OS

|  OS  | Support  |
| ---- | ---- |
|  Unix  | X  |
|  Linux  | X  |
|  MacOSX  | X  |
|  Windows  |   |

#### Supported Python Version

|  Version  | Support  |
| ---- | ---- |
|  Python2.7  |   |
|  Python3.4  | X |
|  Python3.5  | X |
|  Python3.6  | X |
|  Python3.7  | X |
|  Python3.8  | X |


<br>
<br>

#### Python package dependencies

- No dependencies

|  Version  |  Library  | installation  |
| ---- | ---- | ---- |
| None |  None  | None  |


<br>


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
