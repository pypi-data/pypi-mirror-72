# [Microlancer](https://Microlancer.io/)

![Image](https://pbs.twimg.com/profile_images/1059927941394485248/LqUPllxS_400x400.png)

[Buy me a coffee ☕︎](https://paywall.link/to/donate)

Microlancer.io is a freelancer site that uses the Bitcoin lightnetwork as a way to
paidmaneto, this library was made so that you can interact with the platform API in an easy and simple way.

 - [x] Tasks
 - [x] Services
 - [x] Offer
 - [x] Current
 - [x] Withdraw

## Instalation

##### (Microlancer)  requires [ Python ](https://www.python.org) v3.8

```sh
$ pip install Microlancer
```

#### Login

```python
Python 3.8.3 (default, Jun 16 2020, 19:00:28)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import Microlancer
>>>
>>> # [ Microlancer Login ]
>>>
>>> Login = Microlancer.Login('E-Mail', 'Password') # Microlancer Login.
>>> Login.login(two2fa=52314) # If you have activated 2FA, pass the code in the flag two2fa=code
```

#### Tasks

```python
>>> Tasks = Microlancer.Tasks() # Microlancer Tasks.
>>>
>>> Tasks.list(first=1, lenght=50) # List Tasks.
{'sort': [822], 'tasks': {'822': {'id': 822, 'title': 'Try out Spendl App', 'titleWithBreaks': ...}
>>>
>>> Tasks.create('teste', 'teste', amount=1, repeatable=False, escrow=False) # Create task.
{'hasErrors': False, 'formErrorMessage': None, ...}
>>>
>>> Tasks.view(1, first=1, lenght=2) # View Tasks.
{'id': 1, 'calledExternally': False, 'title': '' ...}
>>>
>>> Tasks.comment(1, 'Hello Word') # Comment Task.
{'hasErrors': False, 'formErrorMessage': None, 'formErrors': '' ... }
>>>  
```

#### Offer

```python
>>> Offer = Microlancer.Offer() # Microlancer Offer.
>>>
>>> Offer.pitch(1, 'Hello Word', amount=1, pitch='I can do this task.') # Pitch Offer.
{'hasErrors': False, 'formErrorMessage': None, ...}
>>>
>>> Offer.reply(1, amount=1, pitch='I can do this task.') # Reply Offer.
{'hasErrors': False, 'formErrorMessage': '' ...}
>>>
>>> Offer.retract(2, message='I can not do.') # Retract Offer.
{'hasErrors': False, 'formErrorMessage': '' ...}
>>>
>>> Offer.proposed(2, 50, message='') # New proposal.
{'hasErrors': False, 'formErrorMessage': '' ...}
>>>
>>> Offer.view(1) # View Offer.
{'hasErrors': False, 'formErrorMessage': '' ...}
```

#### Notifications

```python
>>> Notifications = Microlancer.Notifications() # Microlancer Notifications.
>>>
>>> Notifications.dismiss([1]) # Notifications Dismiss.
{'hasErrors': False, 'formErrorMessage': None, ...}
>>>
>>> Notifications.list(first=5, lenght=50, dismissed=True) # Notifications List.
{'sort': [21333, ...] ...}
```

#### Current

```python
>>> Microlancer.Current() # Microlancer Current.
{'loggedIn': True, 'authState': 'loggedIn', 'username': '' ... }
```

#### Withdraw

```python
>>> Withdraw = Microlancer.Withdraw(lnbc10n1p00 ..., two2fa=352146) # If you have activated 2FA, pass the code in the flag two2fa=code.
{"hasErrors": False, "formErrorMessage": None, ...}
```

#### Services

```python
>>> Services = Microlancer.Services() # Microlancer Services.
>>>
>>> Services.view(53) # Services View.
{'id': 53, 'packages': [{'packageId': 92, ...} ...] ...}
>>>
>>> Services.list(first=1, lenght=50, status='any', minsats=1) # Services List.
{'sort': [52, 47, 30, 13 ... ]}
>>>
>>> Services.create(escrow=True, packages=[{'title' : 'test', 'description' : 'test', 'amount' : 1}]) # Create services.
{'hasErrors': False, 'formErrorMessage': None, ...}
>>>
```