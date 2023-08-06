## AWS Batch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Launch template support

### Usage

Simply define your Launch Template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_launch_template = ec2.CfnLaunchTemplate(self, "LaunchTemplate",
    launch_template_name="extra-storage-template",
    launch_template_data={
        "block_device_mappings": [{
            "device_name": "/dev/xvdcz",
            "ebs": {
                "encrypted": True,
                "volume_size": 100,
                "volume_type": "gp2"
            }
        }
        ]
    }
)
```

and use it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources={
        "launch_template": {
            "launch_template_name": my_launch_template.launch_template_name
        },
        "vpc": vpc
    },
    compute_environment_name="MyStorageCapableComputeEnvironment"
)
```
