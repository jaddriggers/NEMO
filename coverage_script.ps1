$ErrorActionPreference = "Stop"
coverage erase
coverage run NEMO/manage.py test tests --settings=tests.test_settings
coverage xml -i
docker run --net=Sonar --rm -e SONAR_HOST_URL="http://SonarQube:9000/" -v "$(pwd):/usr/src"  sonarsource/sonar-scanner-cli
#[system.Diagnostics.Process]::Start("chrome","localhost:9000")
