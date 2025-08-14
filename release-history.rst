.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2024-08-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Added ``BaseBotoSesEnum`` factory class for environment-aware boto session management
- Implemented automatic authentication method selection based on runtime detection  
- Added support for multiple AWS execution environments (local, Cloud9, EC2, Lambda, Batch, ECS, Glue)
- Implemented ``get_aws_account_id_in_ci()`` function with 12-digit validation
- Added workload role ARN generation for CI/CD environments
- Implemented lazy-loaded session management with ``cached_property``

**Miscellaneous**

- Initial release with core boto session factory functionality
