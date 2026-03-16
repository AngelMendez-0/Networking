#!/bin/bash

echo "Test 1: Printing"
python3 lab4.py -p 80 http://httpforever.com/

echo "Test 2: Saving"
python3 lab4.py -f 80 http://httpforever.com/

echo "Test 3: Printing subpath"
python3 lab4.py -p 80 http://httpforever.com/
