Django TokkoRPC
---

> _Django Tokko's microservices RPC interface_


__TOC__

+ [What it's DjangoTokkoRPC?](#about-django-tokkorpc)
+ [Installation](#install)
+ [Usage](#usage)
+ [Testing](#testing)


# About Django TokkoRPC
_ToDo_

# Install
```bash
# Virtual Environment
(venv) pip install django_tokko_rpc
# Main Python3 environment
sudo -H pip3 install django_tokko_rpc
```

# Usage
Add to {your-project}/settings.py
```python
INSTALLED_APPS = [
    "other-apps",
    "...",
    "django-tokko-rpc" # <- Django TokkoRPC Plugin
]
```

# Testing
```bash
python ./manage.py test django_tokko_rpc
```

---
[goBack](../../../README.md)
