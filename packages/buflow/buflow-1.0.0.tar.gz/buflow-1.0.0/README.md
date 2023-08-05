Official Buflow Bindings for Python
===================================

A Python library for Buflow's API.


Setup
-----

You can install this package by using the pip tool and installing:

    $ pip install Buflow
    
Or:

    $ easy_install Buflow
    

Setting up a Buflow Account
---------------------------

Sign up for Buflow at https://buflow.com

Using the Buflow API
--------------------

Documentation for the python bindings can be found alongside Buflow's other bindings here:

- https://buflow.com/docs

In the standard documentation, most of the reference pages will have examples in Buflow's official bindings (including Python). Just click on the Python tab to get the relevant documentation.


Example
-------

```python
import buflow
import os


buflow.api_key = os.environ.get("STRIPE_SECRET_KEY")

print("Creating task...")

task_params = {
  "questions": [
    "Is there a tree in this image?",
    "Is there a pedestrian in this image?",
  ],
}
resp = buflow.Task.create(
  task_type='binary_classification',
  task_params=task_params,
  content='http://cdn.lamag.com/wp-content/uploads/sites/9/2016/07/134002821-800x500.jpg',
  content_type='image',
  priority='medium',
  instructions='Answer questions asked.',
  callback_url='https://www.example.com/labels',
)

print("Success: %r" % resp)

task_id = resp["task_id"]

print("Fetching task...")
resp = buflow.Task.get(task_id)

print("Success: %r" % resp)
```
