# iac-bootstrap

iac-bootstrap is Python package to automate deploiment of infrastructure. Writtent and compatible with python 3 .
to use iac-bootstrap you should follow infra-base (structure).

## Documentation

Documentation to infra-base
<br>
<https://iac-bootstrap.readthedocs.io/en/latest/>
</br>

## installation

Using pip, the Python package manager:

```

pip install --user iac_bootstrap==1.0.2

```

iac-bootstrap is developed for Linux , No windows version is available.

## Usage

iac-bootstrap automate terraform initialization and deploiment ,although generating necessary files for ansible and launch playbook.<br>
I will describe below simple usage.

- iac_bootstrap.infra_bootstrap:

```
python -m iac_bootstrap.infra_bootstrap --account <group>-<env>
```

- iac_bootstrap.infra_builder_terraform:

```
python -m iac_bootstrap.infra_builder_terraform --account <group>-<env>
```

- iac_bootstrap.install_nginx:

```
python -m iac_bootstrap.install_nginx --group <group>-<env>
```

## Features

Here are features for infra_builder_terraform script:

```
Builder Terraform Script:
optional arguments:
  -h, --help            show this help message and exit
  --account ACCOUNT     account <group>-<env>
  --action ACTION       plan apply or destroy
  --region REGION       eu-west-1 by default
  --layer LAYER         terraform layer
  --ignore              ignore layer
  --provider PROVIDER   cloud provider , by default aws
  --approve APPROVE     Auto-approve option ,set 'yes' to enable it
```

Here are features for infra_bootstrap script :

```
Boot Strap script

optional arguments:
  -h, --help           show this help message and exit
  --provider PROVIDER  provider aws
  --account ACCOUNT    account <group>-<env>
  --action ACTION      plan apply or destroy
  --region REGION      eu-west-1 by default
  --approve APPROVE    Auto-approve option ,set 'yes' to enable it
```

## license

[GNU GENERAL PUBLIC LICENSE](https://github.com/WeScale/iac-bootstrap/blob/master/LICENSE)
