# How to create a new Streamlit app checklist
 
## 1. Naming Conventions

| Identification | Header                                        |
|----------------|-----------------------------------------------|
| faaus2008      | Fatal Aircraft Accidents in the US since 2008 |
| pdus2008       | Profiling Data for the US since 2008          |

## 2. Coding

Adherence to the following recommendations will ensure consistent usability across all of IO-Aero's Streamlit applications:

- Use the sidebar for task and filter related controls
- Position the task-related controls in the sidebar at the top and the global filter elements at the bottom
- Make the task-related control elements visible only after the associated task has been selected

```
choice_data_profile = st.sidebar.checkbox(
    help="Pandas profiling of the dataset.",
    label="**`Show data profile`**",
    value=False,
)

if choice_data_profile:
    choice_data_profile_type = st.sidebar.radio(
        help="explorative: thorough but also slow - minimal: minimal but faster.",
        index=1,
        label="Data profile type",
        options=(
            [
                "explorative",
                "minimal",
            ]
        ),
    )
    choice_data_profile_file = st.sidebar.checkbox(
        help="Export the Pandas profile into a file.",
        label="Export profile to file",
        value=False,
    )
```

- Separate the individual tasks and the filter elements with separator line

```
st.sidebar.markdown("""---""")
```

## 3. Documentation

see file directory **`docs`**

### 3.1 config_io_avstats.md

```
...
| streamlit_server_port_faaus2008         | 8501                                          | Streamlit port number for application faaus2008                          |
| streamlit_server_port_pdus2008          | 8502                                          | Streamlit port number for application pdus2008                           |
...
```

### 3.2 how_to_setup_aws_instance.md

```
...
## 2. Open port numbers

Each Streamlit application must be assigned its own port number so that they can run simultaneously.
Currently, the following Streamlit applications are supported:

| Port | Application                                               |
|------|-----------------------------------------------------------|
| 8501 | faaus2008 - Fatal Aircraft Accidents in the US since 2008 |
| 8502 | pdus2008  - Profiling Data for the US since 2008          |
...
```

### 3.3 how_to_update_avstats_on_aws.md

```
...
## 1. Docker images

Currently, the following Streamlit applications are supported:

| Application | Description                                    |
|-------------|------------------------------------------------|
| faaus2008   | Fatal Aircraft Accidents in the US since 2008  |
| pdus2008    | Profiling Data for the US since 2008           |
...
```

### 3.4 index.md

```
...
Currently, it includes the following applications:

- faaus2008 - Fatal Aircraft Accidents in the US since 2008
- pdus2008  - Profiling Data for the US since 2008
...
```

### 3.5 Operation.md

```
...
TODO
...
```

## 4. Parameterization

### 4.1 docker-compose.yml

```
...
  # ------------------------------------------------------------------------------
  # faaus2008 - Fatal Aircraft Accidents in the US since 2008.
  # ------------------------------------------------------------------------------
  app_faaus2008:
    container_name: faaus2008
    depends_on:
      - db
    image: ioaero/faaus2008:latest
    ports:
      - "${IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008}:${IO_AVSTATS_STREAMLIT_SERVER_PORT}"
    restart: always

  # ------------------------------------------------------------------------------
  # pdus2008 - Profiling Data for the US since 2008.
  # ------------------------------------------------------------------------------
  app_pdus2008:
    container_name: pdus2008
    depends_on:
      - db
    image: ioaero/pdus2008:latest
    ports:
      - "${IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008}:${IO_AVSTATS_STREAMLIT_SERVER_PORT}"
    restart: always
...
```

### 4.2 settings.io_avstats.toml / settings.io_avstats_4_dockerfile.toml

```
...
streamlit_server_port_faaus2008 = 8501
streamlit_server_port_pdus2008 = 8502
...
```

## 5. Scripts

### 5.1 run_io_avstats

**cmd**:

```
...
if ["%IO_AVSTATS_TASK%"] EQU ["r_s_a"] (
    if ["%2"] EQU [""] (
        echo =========================================================
		echo faaus2008 - Fatal Aircraft Accidents in the US since 2008
		echo pdus2008  - Profiling Data for the US since 2008
        echo ---------------------------------------------------------
        set /P IO_AVSTATS_APPLICATION="Enter the Streamlit application name "
    ) else (
        set IO_AVSTATS_APPLICATION=%2
    )
)
...
```

**bash**:

```
...
if [ "${IO_AVSTATS_TASK}" = "r_s_a" ]; then
    if [ -z "$2" ]; then
        echo "========================================================="
        echo "faaus2008 - Fatal Aircraft Accidents in the US since 2008"
        echo "pdus2008  - Profiling Data for the US since 2008"
        echo "---------------------------------------------------------"
        # shellcheck disable=SC2162
        read -p "Enter the Streamlit application name " IO_AVSTATS_APPLICATION
        export IO_AVSTATS_APPLICATION=${IO_AVSTATS_APPLICATION}
    else
        export IO_AVSTATS_APPLICATION=$2
    fi
fi
...
```


### 5.2 See file directory **`scripts`**


#### 5.2.1 scripts/run_create_image

**cmd**:

```
...
if ["%1"] EQU [""] (
    echo =========================================================
    echo faaus2008 - Fatal Aircraft Accidents in the US since 2008
    echo pdus2008  - Profiling Data for the US since 2008
    echo ---------------------------------------------------------
    set /P APPLICATION="Enter the desired application name [default: %APPLICATION_DEFAULT%] "

    if ["!APPLICATION!"] EQU [""] (
        set APPLICATION=%APPLICATION_DEFAULT%
    )
) else (
    set APPLICATION=%1
)
...
```

**bash**:

```
...
if [ -z "$1" ]; then
    echo "========================================================="
    echo "faaus2008 - Fatal Aircraft Accidents in the US since 2008"
    echo "pdus2008  - Profiling Data for the US since 2008"
    echo "---------------------------------------------------------"
    read -p "Enter the desired application name [default: ${APPLICATION_DEFAULT}] " APPLICATION
    export APPLICATION=${APPLICATION}

    if [ -z "${APPLICATION}" ]; then
        export APPLICATION=${APPLICATION_DEFAULT}
    fi
else
    export APPLICATION=$1
fi
...
```

#### 5.2.2 scripts/run_docker_compose

**cmd**:

```
...
set IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008=8501
set IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008=8502
...
echo STREAMLIT_SRRVER_PORT_faaus2008 : %IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008%
echo STREAMLIT_SERVER_PORT_pdus2008  : %IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008%
...
```

**bash**:

```
...
export IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008=8501
export IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008=8502
...
echo "STREAMLIT_SRRVER_PORT_faaus2008 : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_faaus2008}"
echo "STREAMLIT_SERVER_PORT_pdus2008  : ${IO_AVSTATS_STREAMLIT_SERVER_PORT_pdus2008}"
...
```