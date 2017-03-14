#!/bin/bash

python links.py reviews | tee reviews/README.org
python links.py writings | tee writings/README.org
