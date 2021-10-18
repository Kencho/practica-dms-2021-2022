#!/bin/bash

SUCCESS=0

echo "[dms2122common]"
mypy --install-types --non-interactive components/dms2122common/dms2122common
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122auth]"
mypy --install-types --non-interactive components/dms2122common/dms2122common components/dms2122auth/dms2122auth
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122backend]"
mypy --install-types --non-interactive components/dms2122common/dms2122common components/dms2122backend/dms2122backend
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2122frontend]"
mypy --install-types --non-interactive components/dms2122common/dms2122common components/dms2122frontend/dms2122frontend
SUCCESS=$((${SUCCESS}+$?))

exit ${SUCCESS}
