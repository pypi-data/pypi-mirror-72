.. _api:

API Reference
=============

The StreamSets SDK for Python is broadly divided into abstractions for interacting with
StreamSet Data Collector and StreamSets Control Hub.

.. module:: streamsets.sdk

StreamSets Data Collector
-------------------------

Main interface
""""""""""""""
This is the main entry point used by users when interacting with SDC instances.

.. autoclass:: streamsets.sdk.DataCollector
    :members:

.. autoattribute:: sdc.DEFAULT_SDC_USERNAME
.. autoattribute:: sdc.DEFAULT_SDC_PASSWORD

Models
""""""
These models wrap and provide useful functionality for interacting with common SDC abstractions.

Alerts
^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Alert
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Alerts
    :members:

Data Rules
^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.DataDriftRule
    :members:
.. autoclass:: streamsets.sdk.sdc_models.DataRule
    :members:

History
^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.History
    :members:
.. autoclass:: streamsets.sdk.sdc_models.HistoryEntry
    :members:

Issues
^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Issue
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Issues
    :members:

Logs
^^^^
.. autoclass:: streamsets.sdk.sdc_models.Log
    :members:

Metrics
^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.MetricCounter
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricGauge
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricHistogram
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricTimer
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Metrics
    :members:

Pipelines
^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelineBuilder
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Pipeline
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Stage
    :members:

Pipeline ACLs
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelineAcl
    :members:

Pipeline Permissions
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelinePermission
    :members:
.. autoclass:: streamsets.sdk.sdc_models.PipelinePermissions
    :members:

Previews
^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Preview
    :members:

Snapshots
^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Batch
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Record
    :members:
.. autoclass:: streamsets.sdk.sdc_models.RecordHeader
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Snapshot
    :members:
.. autoclass:: streamsets.sdk.sdc_models.StageOutput
    :members:

Users
^^^^^
.. autoclass:: streamsets.sdk.sdc_models.User
    :members:


StreamSets Transformer
----------------------

Main interface
""""""""""""""
This is the main entry point used by users when interacting with Transformer instances.

.. autoclass:: streamsets.sdk.Transformer
    :members:

Models
""""""
These models wrap and provide useful functionality for interacting with common SCH abstractions.

Alerts
^^^^^^
.. autoclass:: streamsets.sdk.st_models.Alert
    :members:
.. autoclass:: streamsets.sdk.st_models.Alerts
    :members:

Data Rules
^^^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.DataDriftRule
    :members:
.. autoclass:: streamsets.sdk.st_models.DataRule
    :members:

History
^^^^^^^
.. autoclass:: streamsets.sdk.st_models.History
    :members:
.. autoclass:: streamsets.sdk.st_models.HistoryEntry
    :members:

Issues
^^^^^^
.. autoclass:: streamsets.sdk.st_models.Issue
    :members:
.. autoclass:: streamsets.sdk.st_models.Issues
    :members:

Logs
^^^^
.. autoclass:: streamsets.sdk.st_models.Log
    :members:

Metrics
^^^^^^^
.. autoclass:: streamsets.sdk.st_models.MetricCounter
    :members:
.. autoclass:: streamsets.sdk.st_models.MetricGauge
    :members:
.. autoclass:: streamsets.sdk.st_models.MetricHistogram
    :members:
.. autoclass:: streamsets.sdk.st_models.MetricTimer
    :members:
.. autoclass:: streamsets.sdk.st_models.Metrics
    :members:

Pipelines
^^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.PipelineBuilder
    :members:
.. autoclass:: streamsets.sdk.st_models.Pipeline
    :members:
.. autoclass:: streamsets.sdk.st_models.Stage
    :members:

Pipeline ACLs
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.PipelineAcl
    :members:

Pipeline Permissions
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.PipelinePermission
    :members:
.. autoclass:: streamsets.sdk.st_models.PipelinePermissions
    :members:

Previews
^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.Preview
    :members:

Snapshots
^^^^^^^^^
.. autoclass:: streamsets.sdk.st_models.Batch
    :members:
.. autoclass:: streamsets.sdk.st_models.Record
    :members:
.. autoclass:: streamsets.sdk.st_models.RecordHeader
    :members:
.. autoclass:: streamsets.sdk.st_models.Snapshot
    :members:
.. autoclass:: streamsets.sdk.st_models.StageOutput
    :members:

Users
^^^^^
.. autoclass:: streamsets.sdk.st_models.User
    :members:


StreamSets Control Hub
----------------------

Main interface
""""""""""""""
This is the main entry point used by users when interacting with SCH instances.

.. autoclass:: streamsets.sdk.ControlHub
    :members:

Models
""""""
These models wrap and provide useful functionality for interacting with common SCH abstractions.

ACLs
^^^^
.. autoclass:: streamsets.sdk.sch_models.ACL
    :members:
.. autoclass:: streamsets.sdk.sch_models.ACLPermissionBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.Permission
    :members:

Classifiers
^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Classifier
    :members:

Classification Rules
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ClassificationRule
    :members:
.. autoclass:: streamsets.sdk.sch_models.ClassificationRuleBuilder
    :members:

DataCollectors
^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.DataCollector
    :members:

Transformers
^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Transformer
    :members:

Group
^^^^^
.. autoclass:: streamsets.sdk.sch_models.Group
    :members:
.. autoclass:: streamsets.sdk.sch_models.Groups
    :members:
.. autoclass:: streamsets.sdk.sch_models.GroupBuilder
    :members:

Jobs
^^^^
.. autoclass:: streamsets.sdk.sch_models.Job
    :members:
.. autoclass:: streamsets.sdk.sch_models.Jobs
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobMetrics
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobOffset
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobRunEvent
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobStatus
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobTimeSeriesMetric
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobTimeSeriesMetrics
    :members:
.. autoclass:: streamsets.sdk.sch_models.RuntimeParameters
    :members:

Organizations
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Organization
    :members:
.. autoclass:: streamsets.sdk.sch_models.Organizations
    :members:
.. autoclass:: streamsets.sdk.sch_models.OrganizationBuilder
    :members:

Pipelines
^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Pipeline
    :members:
.. autoclass:: streamsets.sdk.sch_models.Pipelines
    :members:
.. autoclass:: streamsets.sdk.sch_models.PipelineBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.PipelineParameters
    :members:
.. autoclass:: streamsets.sdk.sch_models.StPipelineBuilder
    :members:

Protection Methods
^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ProtectionMethod
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionMethodBuilder
    :members:

Protection Policies
^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicy
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicies
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicyBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.PolicyProcedure
    :members:

ProvisioningAgents
^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Deployment
    :members:
.. autoclass:: streamsets.sdk.sch_models.Deployments
    :members:
.. autoclass:: streamsets.sdk.sch_models.DeploymentBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProvisioningAgent
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProvisioningAgents
    :members:

Reports
^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.GenerateReportCommand
    :members:
.. autoclass:: streamsets.sdk.sch_models.Report
    :members:
.. autoclass:: streamsets.sdk.sch_models.Reports
    :members:
.. autoclass:: streamsets.sdk.sch_models.ReportDefinition
    :members:
.. autoclass:: streamsets.sdk.sch_models.ReportDefinitions
    :members:
.. autoclass:: streamsets.sdk.sch_models.ReportDefinitionBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.ReportResource
    :members:
.. autoclass:: streamsets.sdk.sch_models.ReportResources
    :members:

Scheduler
^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ScheduledTask
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskAudit
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskBaseModel
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskRun
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTasks
    :members:

Subscriptions
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Subscription
    :members:
.. autoclass:: streamsets.sdk.sch_models.Subscriptions
    :members:
.. autoclass:: streamsets.sdk.sch_models.SubscriptionAction
    :members:
.. autoclass:: streamsets.sdk.sch_models.SubscriptionBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.SubscriptionEvent
    :members:

Topologies
^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Topology
    :members:
.. autoclass:: streamsets.sdk.sch_models.Topologies
    :members:
.. autoclass:: streamsets.sdk.sch_models.TopologyBuilder
    :members:

Users
^^^^^
.. autoclass:: streamsets.sdk.sch_models.User
    :members:
.. autoclass:: streamsets.sdk.sch_models.Users
    :members:
.. autoclass:: streamsets.sdk.sch_models.UserBuilder
    :members:

Common
------
Models used by StreamSets Data Collector and StreamSets Control Hub:

.. autoclass:: streamsets.sdk.models.Configuration
    :members:

Exceptions
----------

.. automodule:: streamsets.sdk.exceptions
    :members:
