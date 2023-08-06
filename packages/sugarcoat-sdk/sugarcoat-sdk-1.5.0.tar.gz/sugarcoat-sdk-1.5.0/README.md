# Sugarcoat Python SDK
The Sugarcoat SDK for Python applications.

## Installation
Install from source:
```
$ git clone git@gitlab.com:sugarcoat/sugarcoat-python-sdk.git
$ cd sugarcoat-python-sdk
$ pip install -r requirements.txt
```

## Usage
Copy the config file and add relevant API key:
```
cp config.py.dist config.py
```

Create the Sugarcoat object
```
from sugarcoat.sugarcoat import Sugarcoat

sc = Sugarcoat()
```

You can now create a wrapper, for example:
```
product = sc.Product
```

And perform actions on that wrapper:
```
product.list()

#{
#	"count": 2,
#	"current_page": 1,
#	"last_page": 1,
#	"products": [
#		{
#			"id": 1,
#			"store_id": 1,
#			"parent_product_id": null,
#			"search_engine_data_id": null,
#			"product_type_id": null,
#			"thumbnail_id": null,
#			"slug": "jb-product",
```

## Quick Reference
```
sc = Sugarcoat()                    # Create new Sugarcoat instance
sc.Product                          # Create Product wrapper
Product.list()                      # List all products
Product.read(1)                     # Read product with id 1
Product.create(payload)             # Create product with passed payload
Product.update(1, payload)          # Update product id 1 with passed payload
Product.delete(1)                   # Delete product id 1
```