# sumologic-apptestutils

CLI client for Partner App Developers



## Installation

`pip install sumologic-apptestutils`



## Usage
<pre>
Usage: sumoapputils [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  create-manifest     For creating manifest file
  enableautocomplete  To enable command autocompletion in shell
  init                For generating initial structure of app folder
  run-app-tests       For running app unit tests
  update-manifest     For updating manifest file

</pre>



# sumologic-appdevutils

CLI client for Apps Team Developers

## Installation

`pip install dist/sumologic_appdevutils-1.0.4-py3-none-any.whl`



## Usage
<pre>
Usage: sumoapputils [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  create-manifest     For creating manifest file
  deploy-app          For deploying app to appcatalog
  enableautocomplete  To enable command autocompletion in shell
  export-app          For exporting app to your sumologic org
  import-app          For importing app to your sumologic org
  init                For generating initial structure of app folder
  reset-app-config    For resetting app configuration
  review-app-query    For generating a minimalistic diff of changes in app...
  run-all-app-tests   For running unit tests for multiple apps using config...
  run-app-tests       For running app unit tests
  save-sumo-config    For saving sumo logic deployment configuration
  show-app-config     For showing app configuration
  show-sumo-config    For showing sumo logic deployment configuration
  undeploy-app        For removing app from appcatalog
  update-manifest     For updating manifest file
  generate-scr-file   For Generating SCR file for SCR
</pre>


For more details Refer wiki page https://wiki.kumoroku.com/confluence/display/MAIN/App+Development+CLI+Tool