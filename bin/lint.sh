#! /usr/bin/env bash
set -euo pipefail
shopt -s expand_aliases
export PROMPT_DIRTRIM=1

## SETUP ###############################################################################

SERVICE_NAME="mle-api"
readonly SERVICE_NAME

DIRNAME="$(dirname "$0")"
DIRNAME="$(realpath --relative-to=. "$DIRNAME")"

REPODIR="$DIRNAME/.."
REPODIR="$(realpath --relative-to=. "$REPODIR")"

ROOT="$REPODIR"
ROOT="$(realpath --relative-to=. "$ROOT")"
readonly ROOT

ENV_FILE="$REPODIR/.env"
ENV_FILE="$(realpath --relative-to=. "$ENV_FILE")"
readonly ENV_FILE

PYTHON_VENV_PATH="$REPODIR/.venv"
PYTHON_VENV_PATH="$(realpath --relative-to=. "$PYTHON_VENV_PATH")"
readonly PYTHON_VENV_PATH

BANDIT_CONFIG="./pyproject.toml"
BANDIT_CONFIG="$(realpath --relative-to=. "$BANDIT_CONFIG")"
readonly BANDIT_CONFIG

MYPY_CONFIG="$REPODIR/pyproject.toml"
MYPY_CONFIG="$(realpath --relative-to=. "$MYPY_CONFIG")"
readonly MYPY_CONFIG

USER_ID="$(id -u)"
readonly USER_ID

GROUP_ID="$(id -g)"
readonly GROUP_ID

HELP="Run linters.
Usage: $(basename "$0") [options] [LINTERS...] [FILENAMES|PATHS ...]
Options:
  -h, --help    Show this help text
  -l, --local   Run linters locally instead of in the '$SERVICE_NAME' service's container
  -c, --check   Run linters in check mode, which will NOT try to automatically fix the code if any error is found
Examples:
  $(basename "$0")                   # run all (fix) linters in a docker container
  $(basename "$0") -c                # run all (check-only) linters in a docker container
  $(basename "$0") -l                # run all (fix) linters locally (make sure to be using virtual environment)
  $(basename "$0") black             # run black linter in a docker container
  $(basename "$0") -l -c isort mypy  # run (check-only) isort and mypy linters locally (make sure to be using virtual environment)"
readonly HELP

## PRINTS ##############################################################################

RED='\033[1;31m'
readonly RED

GREEN='\033[1;32m'
readonly GREEN

YELLOW='\033[1;33m'
readonly YELLOW

NC='\033[0m'
readonly NC

function print_stderr() (
    MSG="$1"
    COLOR="${2:-$YELLOW}"
    echo -e "\n${COLOR}${MSG}${NC}" >&2
)

## METHODS #############################################################################

CONTAINER_NAME="${SERVICE_NAME}_linters"
readonly CONTAINER_NAME

# shellcheck disable=SC2139
alias build="docker-compose build -q --force-rm $SERVICE_NAME"
# shellcheck disable=SC2139
alias start="docker-compose run -d --no-deps --rm --user \"${USER_ID}:${GROUP_ID}\" --name $CONTAINER_NAME $SERVICE_NAME sleep infinity"
# shellcheck disable=SC2139
alias get_cid="docker ps -a -q -f \"name=$CONTAINER_NAME\""
alias remove="docker rm -f \"\$CID\""
# shellcheck disable=SC2016
machine_to_execute="docker exec --user "${USER_ID}:${GROUP_ID}" -ite "TERM=$TERM" \"\$CID\""

function define_local_context() {
    DIRNAME="$(dirname "$0")"
    REPODIR="$DIRNAME/.."
    alias build=
    alias start=
    alias get_cid=
    alias remove=
    machine_to_execute=
    alias run_linter_mypy='print_stderr MYPY && execute python -m mypy --config-file "$MYPY_CONFIG" $FILES && echo All done! ✨ 🍪 ✨'
    echo "Running locally..."
}

function define_check_linters() {
    alias run_linter_black='print_stderr BLACK && execute python -m black --diff --check $FILES'
    alias run_linter_isort='print_stderr ISORT && execute python -m isort --check $FILES && echo All done! ✨ 🍪 ✨'
    alias run_linter_autoflake='print_stderr AUTOFLAKE && execute python -m autoflake -r $FILES && echo All done! ✨ 🌯 ✨'
}

alias run_linter_autoflake='print_stderr AUTOFLAKE && execute python -m autoflake -r --in-place --remove-unused-variables $FILES && execute python -m autoflake -r --in-place --remove-all-unused-imports --exclude=__init__.py $FILES && echo All done! ✨ 🌯 ✨'
alias run_linter_bandit='print_stderr BANDIT && execute python -m bandit -c "$BANDIT_CONFIG" -r $FILES && echo All done! ✨ 🧁 ✨'
alias run_linter_black='print_stderr BLACK && execute python -m black $FILES'
alias run_linter_flake8='print_stderr FLAKE8 && execute python -m flake8 $FILES && echo All done! ✨ 🍩 ✨'
alias run_linter_isort='print_stderr ISORT && execute python -m isort $FILES && echo All done! ✨ 🍪 ✨'
alias run_linter_mypy='print_stderr MYPY && execute python -m mypy --config-file "$MYPY_CONFIG" --cache-dir ".mypy_cache/container" $FILES && echo All done! ✨ 🍪 ✨'

get_pip_activate_file() (
    local PIP_ACTIVATE
    local pip_activate_possible_files
    local VIRTUALENV_PATH

    VIRTUALENV_PATH="$1"
    readonly VIRTUALENV_PATH

    pip_activate_possible_files=("bin/activate" "usr/local/bin/activate")

    for pip_activate_file in "${pip_activate_possible_files[@]}"; do
        # print_stderr "Trying to use activate candidate file: $pip_activate_file ..." "$NC" "\x0"
        PIP_ACTIVATE="$VIRTUALENV_PATH/$pip_activate_file"
        if [ ! -f "$PIP_ACTIVATE" ]; then
            PIP_ACTIVATE=
        else
            break
        fi
    done

    echo "$PIP_ACTIVATE"
)

# shellcheck disable=SC2120
enter_python_env() {
    local VIRTUALENV_PATH

    VIRTUALENV_PATH="$1"
    readonly VIRTUALENV_PATH

    PIP_ACTIVATE="$(get_pip_activate_file "$VIRTUALENV_PATH")"
    readonly PIP_ACTIVATE

    # shellcheck disable=SC1090
    source "$PIP_ACTIVATE"
}

function execute() (
    # shellcheck disable=SC2030
    ARGS="$*"
    if [ "$machine_to_execute" == "" ]; then
        CMD="$ARGS"
    else
        CID="$(get_cid)"
        export CID
        CMD="$machine_to_execute $ARGS"
    fi
    envsubst < <(echo "> $CMD")
    echo ""
    eval "$CMD"
)

## ARGS ################################################################################

read -r -a run_all_linters <<<"$(compgen -a | grep '^run_' | xargs)"
declare -a run_spec_linters

declare -a ARGS
declare -a FILES
while (($#)); do
    case "$1" in
    # -h or --help show help
    "-h" | "--help")
        echo "$HELP" >&2
        exit 0
        ;;
    # -l or --local argument to run on your local machine
    "-l" | "--local")
        define_local_context
        ;;
    # -c or --check argument to run in check mode
    "-c" | "--check")
        define_check_linters
        ;;
    *)
        if [ -f "$1" ] || [ -d "$1" ]; then
            # shellcheck disable=SC2031
            FILES+=("$1")
        else
            # shellcheck disable=SC2031
            ARGS+=("$1")
        fi
        ;;
    esac
    shift
done
set -- "${ARGS[@]+${ARGS[@]}}"

set +u
if [ "${FILES[*]}" == "" ]; then
    FILES=("$ROOT")
fi
set -u
# shellcheck disable=SC2178
FILES="$(printf "'%s' " "${FILES[@]}")"

while (($#)); do
    # argument as the name of the linter to run only that linter
    run_all_linters=()
    run_spec_linters+=("run_linter_$1")
    shift
done

run_linter_cmds=("${run_all_linters[@]+${run_all_linters[@]}}" "${run_spec_linters[@]+${run_spec_linters[@]}}")

function run_linters() {
    RC=0
    if [ -f "$ENV_FILE" ]; then
        # shellcheck disable=SC1090
        . "$ENV_FILE"
        # shellcheck disable=SC2046
        eval export $(grep -vE "^(#.*|\s*)$" "$ENV_FILE")
    fi
    EC=
    for run_linter_cmd in "${run_linter_cmds[@]}"; do
        # shellcheck disable=SC1083
        set +e
        eval "$run_linter_cmd"
        EC=$?
        set -e
        if [ $EC -ne 0 ]; then
            RC=$EC
            linter_name="${run_linter_cmd:11}"
            print_stderr "ERROR while running $linter_name linter!" "$RED"
        fi
    done
    if [ $RC -eq 0 ]; then
        print_stderr "DONE!" "$GREEN"
        echo "All linters run successfully."
    else
        print_stderr "ERROR in one or more linters. Check above for details." "$RED"
    fi
    exit $RC
}

## TRAP ################################################################################

remove_if_running() (
    CID="$(get_cid)"
    export CID
    if [[ -n "$CID" ]]; then
        remove >/dev/null
    fi
)
trap remove_if_running 0

## MAIN ################################################################################

(
    remove_if_running
    build
    cd "$REPODIR"
    start
    if [ "$machine_to_execute" == "" ]; then
        # shellcheck disable=SC2119
        enter_python_env "$PYTHON_VENV_PATH"
    fi
    run_linters
)
