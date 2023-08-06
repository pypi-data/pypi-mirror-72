# Hello Password

A very simple secure password management tool.

**Why?** Because I can't believe the current password management software. In addition, the fact that the data file cannot be exported bothers me.

## Quick Start

### Use `hpass -h` view detailed commands

```powershell
$ hpass -h
usage: hpass [-h] [-v] [-r PASSWORD_LENGTH] [-i] [-c]

Hello Password

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         View version information
  -r PASSWORD_LENGTH, --random_password PASSWORD_LENGTH
                        Randomly generate passwords containing uppercase and lowercase letters/numbers/symbols
  -i, --initialization  Create or specify a password storage file in the current directory
  -c, --cli             Start CLI Workbench
  -t, --transfer        Reset primary password (Change master password)
```

### Use `hpass -i` initialize password data file in specified directory

```powershell
$  hpass -i
Your primary password:
Enter your primary password again:
Find the password storage file in the current directory
Password storage file initialized successfully
```

### Use `hpass` enter Workbench

```powershell
$ hpass
Your primary password:
H-Pass>
```

#### Use `random` generate a secure random password

```powershell
H-Pass> random 16
hiSVJ@77AEYFaZhu
```

#### Use `add` to add a new account

```powershell
H-Pass> add
The following is the information required for the new password :
Website = https://www.yeah.net/
Notes = 163 Yeah Mail
Username = xxxxxxx@yeah.net
Email =
Phone =
Password = hiSVJ@77AEYFaZhu
The new password has been successfully added!
```

#### Use `search` search password data

```powershell
H-Pass> search yeah
+----+-----------------------+--------------+
| ID |        Website        |    Notes     |
+----+-----------------------+--------------+
| 18 | https://www.yeah.net/ | 163 Yeah Mail |
+----+-----------------------+--------------+
```

#### Use `get` view password data

```powershell
H-Pass> get 18
website = https://www.yeah.net/
notes = 163 Yeah Mail
username = xxxxxxx@yeah.net
email =
phone =
password = hiSVJ@77AEYFaZhu
```

#### Use `set` change password data

```powershell
H-Pass> set 18 notes
Original notes = 163 Yeah Mail
Now notes = Yeah Mail
Password value modified successfully!
```

#### Use `help` view cli help information

```powershell
H-Pass> help
filepath           - Print the absolute path of the password storage file
all                - View the basic information of all password data
add                - Enter a new password data
search <keyword>   - Find password data by keyword
random <length>    - Generate a secure password of specified length
get <id>           - View the password data of the specified id
del <id>           - Delete the password data of the specified id
set <id> <key>     - Modify the key value of the password data of specified id
```

## Installation

As usual, the easiest way is with pip:

```powershell
$ pip install hpass
```

Alternatively you can [download](https://pypi.org/project/hpass/#files) the `hpass-x.x.x.tar.gz` installation file:

```powershell
$ pip install hpass-x.x.x.tar.gz
```

Pip will install dependencies *([colorama](https://pypi.org/project/colorama/) and [PrettyTable](https://pypi.org/project/PrettyTable/))* for you. Alternatively you can clone the repository:

```powershell
$ git clone https://github.com/hekaiyou/hpass.git --recursive
$ cd hpass
$ python setup.py install
```

## Philosophy

`hpass` uses RC4 algorithm for data encryption storage.

### Use key to generate S box

> The key-scheduling algorithm (KSA)

```python
def rc4_init_s_box(key):
    s_box = list(range(256))
    j = 0
    for i in range(256):
        j_step_1 = j + s_box[i]
        j_step_2 = j_step_1 + ord(key[i % len(key)])
        j_step_3 = j_step_2 % 256
        j = j_step_3
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
```

### Use S box to generate key stream

> The pseudo-random generation algorithm (PRGA)

```python
def rc4_res_program(s_box, message):
    res = []
    i = j = 0
    for s in message:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        k = s_box[t]
        res.append(chr(ord(s) ^ k))
    return res
```

## License

`hpass` is free and open-source software licensed under the [MIT License](https://github.com/hekaiyou/hpass/blob/master/LICENSE).