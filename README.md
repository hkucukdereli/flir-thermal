# flir-thermal

Python wrappers to read seq files from flir thermal cameras. These functions require FLIR Science File SDK to be installed including their python module.

## Quick Start

1. Download and install FLIR Science File SDK from https://www.flir.com/products/flir-science-file-sdk/?vertical=rd%20science&segment=solutions.
2. Locate your SDK installation folder and enter the folder containing the python package.
```
cd ~/FLIR Systems/sdks/file/python
```
3. Install the python module.
```
pip install setup.py
```
4. Clone this repo.
```
git clone https://github.com/hkucukdereli/flir-thermal.git
cd ~/flir-thermal
```
5. Install as an editable package to allow changes in the future.
```
pip install -e .
```
6. Look under ```./scripts``` for an example.
