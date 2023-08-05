set -e

shopt -s nullglob

PULSAR_TARGET_POORT="${PULSAR_TARGET_POORT:-8913}"
PULSAR_INSTALL_TARGET="${PULSAR_INSTALL_TARGET:-pulsar-app}"
PLANEMO_INSTALL_TARGET="${PLANEMO_INSTALL_TARGET:-planemo==0.36.1}"

init_temp_dir() {
    TEMP_DIR=`mktemp -d`
    echo "Setting up test directory $TEMP_DIR"
    cd "$TEMP_DIR"
}

init_pulsar() {
    PULSAR_INSTALL_TARGET="${PULSAR_INSTALL_TARGET:-pulsar-app}"
    PROJECT_DIR="$SCRIPT_DIR/.."

    mkdir pulsar
    cd pulsar
    echo "Setting up virtualenv for Pulsar"
    virtualenv venv
    . venv/bin/activate # .venv\Scripts\activate if Windows
    echo "Installing Pulsar using 'pip install $PULSAR_INSTALL_TARGET'"
    pip install $PULSAR_INSTALL_TARGET

    cd ..
}

stop_pulsar() {
    cd pulsar
    . venv/bin/activate
    echo "Stopping Pulsar daemon."
    pulsar --stop-daemon
    echo "Ending tests."    
}


check_pulsar() {
    cd pulsar

    if curl -s "http://localhost:$PULSAR_TARGET_POORT"
    then
        echo "Port $PULSAR_TARGET_POORT already bound, Pulsar will fail to start."
        exit 1;
    fi

    echo "Starting Pulsar in daemon mode."
    pulsar --daemon
    echo "Waiting for Pulsar to start."
    while ! curl -s "http://localhost:$PULSAR_TARGET_POORT";
    do
        printf "."
        sleep 1;
    done
    sleep 2
    echo "Running a standalone Pulsar job."
    pulsar-check # runs a test job
    echo "Stopping Pulsar daemon."
    pulsar --stop-daemon
    echo "End Pulsar Checks"

    echo "Testing Pulsar-Galaxy Interaction"
    echo "Starting Pulsar in daemon mode."
    pulsar --daemon
    echo "Waiting for Pulsar to start."
    while ! curl -s "http://localhost:$PULSAR_TARGET_POORT";
    do
        printf "."
        sleep 1;
    done
    sleep 2
    cat paster.log

    cd ..    
}

init_planemo() {
    template="$1"

    echo "Creating a virtual environment for Planemo to drive a test job."
    virtualenv planemo-venv
    . planemo-venv/bin/activate
    echo "Installing Pulsar using 'pip install $PLANEMO_INSTALL_TARGET'"
    pip install --upgrade pip
    pip install "$PLANEMO_INSTALL_TARGET"
    echo "Setting up Planemo test tools."
    planemo project_init --template="$template" test_tools
}

run_planemo() {
    echo "Running tool tests with Planemo through Pulsar"
    : ${GALAXY_ROOT:=""}
    galaxy_root_args=""
    if [ -d "$GALAXY_ROOT" ];
    then
        galaxy_root_args="--galaxy_root $GALAXY_ROOT"
    fi
    planemo --verbose test $galaxy_root_args "$@"
    echo "Tests complete."
}
