[![](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)

## Overview
CloudEdge PIR is a custom integration for receive motion alarm notification from **CloudEdge** app<br/>
Tested on:
* ieGeek ZS-GX5 camera with pir motion detection

**ATTENTION!** it works only on CloudEdge app

## Installation
### *Manual*
**(1)** Place the `custom_components` folder in your configuration directory (or add its contents to an existing `custom_components` folder).
It should look similar to this:
```
<config directory>/
|-- custom_components/
|   |-- cloudedge_pir/
|       |-- __init__.py
|       |-- binary_sensor.py
|       |-- config_flow.py
|       |-- const.py
|       |-- etc...
```
**(1)** Restart Home Assistant and follow our configuration flow.

| Field           | Description                                                                     | Required  |
| ----------------| ------------------------------------------------------------------------------- | --------- |
| E-mail          | CloudEdge account e-mail. (**ATTENTION!** duplicate account with sharing device)| Yes       |
| Password        | CloudEdge account password.                                                     | Yes       |
| Phone code      | CloudEdge account phone code. [See all](https://countrycode.org/)               | Yes       |
| Country code    | CloudEdge account country code (2 DIGIT ISO).                                   | Yes       |
| Name            | Name of your home assistant device.                                             | Yes       |
| Time to wait    | Time to wait to reset state of motion sensor.                                   | Yes       |
