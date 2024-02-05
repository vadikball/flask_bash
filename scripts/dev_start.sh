#!/usr/bin/env bash

set -ex

sh scripts/lint.sh && sh scripts/test.sh
