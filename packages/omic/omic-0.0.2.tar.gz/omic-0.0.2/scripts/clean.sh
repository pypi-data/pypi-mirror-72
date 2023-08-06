#!/bin/bash
rm -r $(find . -name '*.egg-info')
rm -r $(find . -name '.eggs')
rm -r $(find . -name '__pycache__')
rm -r $(find . -name '.pytest_cache')
rm -r build/
rm -r dist/