#!/bin/bash

modes="  start-dev\n  stop-dev\n  interactive-dev\n  check-syntax\n  generate-data\n  run-tests\n"
mode=$1
project_name="parkomate"

if [ "$project_name" == "*****" ]; then
    echo "Please Update the Project Name in run.sh"
    exit 0;
fi

if [ "$mode" == "" ]; then
    echo -e $"Invalid mode \nPlease enter one of the following mode:\n${modes}"
elif [ "$mode" == "start-dev" ]; then
    docker-compose -p ${project_name}-dev -f docker-compose-dev.yml build
    docker-compose -p ${project_name}-dev -f docker-compose-dev.yml up -d
elif [ "$mode" == "stop-dev" ]; then
    docker-compose -p ${project_name}-dev -f docker-compose-dev.yml stop
elif [ "$mode" == "interactive-dev" ]; then
    docker exec -it --user root ${project_name}-backend bash
elif [ "$mode" == "check-syntax" ]; then
    docker exec -it --user root ${project_name}-backend flake8 .
elif [ "$mode" == "generate-data" ]; then
    docker exec -it --user root ${project_name}-backend bash -c "python manage.py generate_fake_users && python manage.py generate_fake_organizations && python manage.py generate_fake_gates && python manage.py generate_fake_parkings && python manage.py generate_fake_cctvs && python manage.py generate_fake_vehicles"
elif [ "$mode" == "run-tests" ]; then
    echo "Running DRF Backend Tests..."
    output=$(docker exec -it --user root ${project_name}-backend bash -c "python manage.py test -v 2 .")
    while IFS= read -r line; do
        if echo "$line" | grep -q -E "(... ok)"; then
            echo -e "\e[32m✔\e[0m ${line%%(*}"
        elif echo "$line" | grep -q -E "(FAIL)"; then
            echo -e "\e[31m✘\e[0m ${line%%(*}"
        fi
    done <<< "$output"
else
    echo -e $"Invalid mode \nPlease enter one of the following mode:\n${modes}"
fi
