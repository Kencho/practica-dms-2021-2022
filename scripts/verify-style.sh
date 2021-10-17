#!/bin/bash

pylint --fail-under=7.0 -f text components/dms2122common/dms2122common components/dms2122auth/dms2122auth components/dms2122backend/dms2122backend components/dms2122frontend/dms2122frontend
