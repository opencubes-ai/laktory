from laktory import models

with open("./stack.yaml", "r") as fp:
    stack = models.Stack.model_validate_yaml(fp)

empty_stack = stack.model_copy(deep=True, update={"resources": models.StackResources()})


def test_stack_model():
    data = stack.model_dump()
    print(data)
    assert data == {
        "variables": {},
        "name": "unit-testing",
        "config": {
            "databricks:host": "${var.DATABRICKS_HOST}",
            "databricks:token": "${var.DATABRICKS_TOKEN}",
        },
        "description": None,
        "resources": {
            "catalogs": [],
            "clusters": [],
            "groups": [],
            "jobs": [
                {
                    "access_controls": [],
                    "clusters": [
                        {
                            "apply_policy_default_values": None,
                            "autoscale": None,
                            "autotermination_minutes": None,
                            "cluster_id": None,
                            "custom_tags": None,
                            "data_security_mode": "USER_ISOLATION",
                            "driver_instance_pool_id": None,
                            "driver_node_type_id": None,
                            "enable_elastic_disk": None,
                            "enable_local_disk_encryption": None,
                            "idempotency_token": None,
                            "init_scripts": [],
                            "instance_pool_id": None,
                            "name": "main",
                            "node_type_id": "Standard_DS3_v2",
                            "num_workers": None,
                            "policy_id": None,
                            "runtime_engine": None,
                            "single_user_name": None,
                            "spark_conf": {},
                            "spark_env_vars": {},
                            "spark_version": "14.0.x-scala2.12",
                            "ssh_public_keys": [],
                        }
                    ],
                    "continuous": None,
                    "control_run_state": None,
                    "email_notifications": None,
                    "format": None,
                    "health": None,
                    "max_concurrent_runs": None,
                    "max_retries": None,
                    "min_retry_interval_millis": None,
                    "name": "job-stock-prices-ut-stack",
                    "notification_settings": None,
                    "parameters": [],
                    "retry_on_timeout": None,
                    "run_as": None,
                    "schedule": None,
                    "tags": {},
                    "tasks": [
                        {
                            "condition_task": None,
                            "depends_ons": None,
                            "description": None,
                            "email_notifications": None,
                            "existing_cluster_id": None,
                            "health": None,
                            "job_cluster_key": "main",
                            "libraries": [
                                {
                                    "cran": None,
                                    "egg": None,
                                    "jar": None,
                                    "maven": None,
                                    "pypi": {
                                        "package": "laktory==0.0.27",
                                        "repo": None,
                                    },
                                    "whl": None,
                                },
                                {
                                    "cran": None,
                                    "egg": None,
                                    "jar": None,
                                    "maven": None,
                                    "pypi": {"package": "yfinance", "repo": None},
                                    "whl": None,
                                },
                            ],
                            "max_retries": None,
                            "min_retry_interval_millis": None,
                            "notebook_task": {
                                "notebook_path": "/jobs/ingest_stock_metadata.py",
                                "base_parameters": None,
                                "source": None,
                            },
                            "notification_settings": None,
                            "pipeline_task": None,
                            "retry_on_timeout": None,
                            "run_if": None,
                            "run_job_task": None,
                            "sql_task": None,
                            "task_key": "ingest-metadata",
                            "timeout_seconds": None,
                        },
                        {
                            "condition_task": None,
                            "depends_ons": None,
                            "description": None,
                            "email_notifications": None,
                            "existing_cluster_id": None,
                            "health": None,
                            "job_cluster_key": None,
                            "libraries": None,
                            "max_retries": None,
                            "min_retry_interval_millis": None,
                            "notebook_task": None,
                            "notification_settings": None,
                            "pipeline_task": {
                                "pipeline_id": "${resources.pl-custom-name.id}",
                                "full_refresh": None,
                            },
                            "retry_on_timeout": None,
                            "run_if": None,
                            "run_job_task": None,
                            "sql_task": None,
                            "task_key": "run-pipeline",
                            "timeout_seconds": None,
                        },
                    ],
                    "timeout_seconds": None,
                    "trigger": None,
                    "webhook_notifications": None,
                }
            ],
            "notebooks": [],
            "pipelines": [
                {
                    "access_controls": [
                        {
                            "group_name": "account users",
                            "permission_level": "CAN_VIEW",
                            "service_principal_name": None,
                            "user_name": None,
                        },
                        {
                            "group_name": "role-engineers",
                            "permission_level": "CAN_RUN",
                            "service_principal_name": None,
                            "user_name": None,
                        },
                    ],
                    "allow_duplicate_names": None,
                    "catalog": None,
                    "channel": "PREVIEW",
                    "clusters": [],
                    "configuration": {},
                    "continuous": None,
                    "development": None,
                    "edition": None,
                    "libraries": [
                        {
                            "file": None,
                            "notebook": {"path": "/pipelines/dlt_brz_template.py"},
                        }
                    ],
                    "name": "pl-stock-prices-ut-stack",
                    "notifications": [],
                    "photon": None,
                    "serverless": None,
                    "storage": None,
                    "tables": [],
                    "target": None,
                    "udfs": [],
                }
            ],
            "schemas": [],
            "secrets": [],
            "secretscopes": [],
            "serviceprincipals": [],
            "sqlquerys": [],
            "tables": [],
            "providers": [
                {
                    "account_id": None,
                    "auth_type": None,
                    "azure_client_id": None,
                    "azure_client_secret": None,
                    "azure_environment": None,
                    "azure_login_app_id": None,
                    "azure_tenant_id": None,
                    "azure_use_msi": None,
                    "azure_workspace_resource_id": None,
                    "client_id": None,
                    "client_secret": None,
                    "cluster_id": None,
                    "config_file": None,
                    "databricks_cli_path": None,
                    "debug_headers": None,
                    "debug_truncate_bytes": None,
                    "google_credentials": None,
                    "google_service_account": None,
                    "host": "${var.DATABRICKS_HOST}",
                    "http_timeout_seconds": None,
                    "metadata_service_url": None,
                    "password": None,
                    "profile": None,
                    "rate_limit": None,
                    "retry_timeout_seconds": None,
                    "skip_verify": None,
                    "token": "${var.DATABRICKS_TOKEN}",
                    "username": None,
                    "warehouse_id": None,
                }
            ],
            "users": [],
            "volumes": [],
            "warehouses": [],
            "workspacefiles": [],
        },
        "environments": [],
        "pulumi_outputs": {},
    }

    return stack


def test_pulumi_stack():
    pstack = stack.to_pulumi_stack()
    stack.write_pulumi_stack()
    data = pstack.model_dump()
    data["config"]["databricks:token"] = "***"
    data["resources"]["databricks-provider"]["properties"]["token"] = "***"
    print(data)

    assert data == {
        "variables": {},
        "name": "unit-testing",
        "runtime": "yaml",
        "config": {
            "databricks:host": "https://adb-2211091707396001.1.azuredatabricks.net/",
            "databricks:token": "***",
        },
        "resources": {
            "job-stock-prices-ut-stack": {
                "type": "databricks:Job",
                "properties": {
                    "name": "job-stock-prices-ut-stack",
                    "parameters": [],
                    "tags": {},
                    "tasks": [
                        {
                            "libraries": [
                                {"pypi": {"package": "laktory==0.0.27"}},
                                {"pypi": {"package": "yfinance"}},
                            ],
                            "jobClusterKey": "main",
                            "notebookTask": {
                                "notebookPath": "/jobs/ingest_stock_metadata.py"
                            },
                            "taskKey": "ingest-metadata",
                        },
                        {
                            "pipelineTask": {"pipelineId": "${pl-custom-name.id}"},
                            "taskKey": "run-pipeline",
                        },
                    ],
                    "jobClusters": [
                        {
                            "jobClusterKey": "main",
                            "newCluster": {
                                "dataSecurityMode": "USER_ISOLATION",
                                "initScripts": [],
                                "nodeTypeId": "Standard_DS3_v2",
                                "sparkConf": {},
                                "sparkEnvVars": {},
                                "sparkVersion": "14.0.x-scala2.12",
                                "sshPublicKeys": [],
                            },
                        }
                    ],
                },
                "options": {"dependsOn": [], "deleteBeforeReplace": True},
            },
            "pl-custom-name": {
                "type": "databricks:Pipeline",
                "properties": {
                    "channel": "PREVIEW",
                    "clusters": [],
                    "configuration": {},
                    "libraries": [
                        {"notebook": {"path": "/pipelines/dlt_brz_template.py"}}
                    ],
                    "name": "pl-stock-prices-ut-stack",
                    "notifications": [],
                },
                "options": {
                    "provider": "${databricks-provider}",
                    "dependsOn": [],
                    "deleteBeforeReplace": True,
                },
            },
            "permissions-pl-custom-name": {
                "type": "databricks:Permissions",
                "properties": {
                    "accessControls": [
                        {"groupName": "account users", "permissionLevel": "CAN_VIEW"},
                        {"groupName": "role-engineers", "permissionLevel": "CAN_RUN"},
                    ],
                    "pipelineId": "${pl-custom-name.id}",
                },
                "options": {"dependsOn": [], "deleteBeforeReplace": True},
            },
            "workspace-file-laktory-pipelines-pl-stock-prices-ut-stack-json": {
                "type": "databricks:WorkspaceFile",
                "properties": {
                    "path": "/.laktory/pipelines/pl-stock-prices-ut-stack.json",
                    "source": "./tmp-pl-stock-prices-ut-stack.json",
                },
                "options": {"dependsOn": [], "deleteBeforeReplace": True},
            },
            "permissions-file-workspace-file-laktory-pipelines-pl-stock-prices-ut-stack-json": {
                "type": "databricks:Permissions",
                "properties": {
                    "accessControls": [
                        {"groupName": "account users", "permissionLevel": "CAN_READ"}
                    ],
                    "workspaceFilePath": "/.laktory/pipelines/pl-stock-prices-ut-stack.json",
                },
                "options": {
                    "dependsOn": [
                        "${workspace-file-laktory-pipelines-pl-stock-prices-ut-stack-json}"
                    ],
                    "deleteBeforeReplace": True,
                },
            },
            "databricks-provider": {
                "type": "pulumi:providers:databricks",
                "properties": {
                    "host": "https://adb-2211091707396001.1.azuredatabricks.net/",
                    "token": "***",
                },
                "options": {"dependsOn": [], "deleteBeforeReplace": True},
            },
        },
        "outputs": {},
    }


def test_pulumi_up():
    # Create resources
    stack.pulumi_up("okube/dev", flags=["--yes"])

    # Delete resources
    empty_stack.pulumi_up("okube/dev", flags=["--yes"])


if __name__ == "__main__":
    test_stack_model()
    test_pulumi_stack()
    test_pulumi_up()
