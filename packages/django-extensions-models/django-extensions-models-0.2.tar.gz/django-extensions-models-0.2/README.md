# Django Model Extensions
- A Django library for model extensions

### Requirements
- Python (3.5, 3.6, 3.7, 3.8)
- Django (2.0, 3.0)

We highly recommend and only officially support the latest patch release of each Python and Django series.

### Installation
Install using ```pip```...

```
pip install django-extensions-models
```

### Example
Let's take a look at a quick example of using model extensions

```
from models_extensions.models import UUIDModel, TimeStampedModel, ActivatorModel

class YourModel(UUIDModel, TimeStampedModel, ActivatorModel):
    # ...

```

Don't forget ```makemigrations``` & ```migrate``` to apply models to your database.

