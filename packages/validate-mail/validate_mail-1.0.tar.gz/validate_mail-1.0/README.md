# Validate E-mail ID

This project validates the e-mail ID passed.

## Installation

Run the following to install:

```python
pip install validate_mail
```

## Usage

```python
from validate_mail import validate_email

valid_mail = abc@gmail.com
invalid_mail = abc.@gmail.com

# validate your mail ID
print(validate_email(valid_mail)) # True

print(validate_email(invalid_mail)) # False

```