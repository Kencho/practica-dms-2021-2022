#!/bin/bash

SUCCESS=0

echo "[dms2122common]"
mypy components/dms2122common/dms2122common
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122auth]"
mypy components/dms2122common/dms2122common components/dms2122auth/dms2122auth
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122backend]"
mypy components/dms2122common/dms2122common components/dms2122backend/dms2122backend
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122frontend]"
mypy components/dms2122common/dms2122common components/dms2122frontend/dms2122frontend
SUCCESS=$((${SUCCESS}+$?))

exit ${SUCCESS}
