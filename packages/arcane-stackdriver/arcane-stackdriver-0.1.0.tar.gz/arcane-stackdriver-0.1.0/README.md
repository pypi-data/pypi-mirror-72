# Arcane Stackdriver

This package is based on [google-cloud-error-reporting](https://pypi.org/project/google-cloud-error-reporting/).

## Get Started

```sh
pip install arcane-stackdriver
```

## Example Usage

```python
from arcane import stackdriver
client = stackdriver.Client()
```

or

```python
from arcane import stackdriver

# Import your configs
from configure import Config

client = stackdriver.Client.from_service_account_json(Config.KEY, project=Config.GCP_PROJECT)
```
