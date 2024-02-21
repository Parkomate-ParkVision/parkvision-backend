#!/bin/bash
modes="  start-dev\n  stop-dev\n  interactive-dev\n  check-syntax\n  generate-data\n"
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
else
    echo -e $"Invalid mode \nPlease enter one of the following mode:\n${modes}"
fi
