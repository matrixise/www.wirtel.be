#!/bin/bash
set -ex
pip install awscli
aws s3 cp --acl public-read StephaneWirtel.pdf s3://public-mgxio/wirtel.be/StephaneWirtel.pdf
