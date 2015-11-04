#!/bin/bash

sphinx-apidoc -F -o www ../www/
sphinx-build -b html . _build/
