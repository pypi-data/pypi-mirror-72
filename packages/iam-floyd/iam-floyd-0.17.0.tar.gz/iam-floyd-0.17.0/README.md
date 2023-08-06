# IAM Floyd

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/iam-floyd)
[![GitHub](https://img.shields.io/github/license/udondan/iam-floyd)](https://github.com/udondan/iam-floyd/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-iam--floyd-orange)](https://awscdk.io/packages/iam-floyd@0.17.0)

[![npm package](https://img.shields.io/npm/v/iam-floyd?color=brightgreen)](https://www.npmjs.com/package/iam-floyd)
[![PyPI package](https://img.shields.io/pypi/v/iam-floyd?color=brightgreen)](https://pypi.org/project/iam-floyd/)
[![NuGet package](https://img.shields.io/nuget/v/IAM.Floyd?color=brightgreen)](https://www.nuget.org/packages/IAM.Floyd/)
[![Maven package](https://img.shields.io/badge/maven-v0.17.0-brightgreen)](https://github.com/udondan/iam-floyd/packages/258358)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/iam-floyd?label=npm&color=blueviolet)](https://www.npmjs.com/package/iam-floyd)
[![PyPI](https://img.shields.io/pypi/dm/iam-floyd?label=pypi&color=blueviolet)](https://pypi.org/project/iam-floyd/)
[![NuGet](https://img.shields.io/nuget/dt/IAM.Floyd?label=nuget&color=blueviolet)](https://www.nuget.org/packages/IAM.Floyd/)

**AWS [IAM policy statement](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_statement.html) generator.**

[![Auto completion demo](https://raw.githubusercontent.com/udondan/iam-floyd/master/docs/movie-preview.png)](https://www.youtube.com/watch?v=ivG6VnbwMB0)

> This is an early version of the package. The signature of methods will change while I implement new features. Therefore make sure you use an exact version in your `package.json` before it reaches 1.0.0.
>
> If you see something off, think something could be done better or have any other suggestion, speak up. :-)

<!-- vscode-markdown-toc -->

* [Usage](#Usage)
* [Examples](#Examples)
* [Methods](#Methods)

  * [allow](#allow)
  * [deny](#deny)
  * [allActions](#allActions)
  * [if*, if](#ifif)
  * [on*, on](#onon)
  * [not](#not)
* [But I don't use CDK. Can I still use this package?](#ButIdontuseCDK.CanIstillusethispackage)
* [Floyd?](#Floyd)
* [Similar projects](#Similarprojects)
* [Legal](#Legal)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config --><!-- /vscode-markdown-toc -->

While [method chaining](https://en.wikipedia.org/wiki/Method_chaining) is not seen a lot in CDK-land, this library's goal is to provide a way to generate policy statements in a single chain. Code completion FTW!

## <a name='Usage'></a>Usage

The package contains a statement provider for each AWS service, e.g. `Ec2`. A statement provider is an extension of the original `PolicyStatement` of the `@aws-cdk/aws-iam` package, so you can use it as drop-in replacement.

A statement provider has methods for every single action of a service. Calling such method will add the related action to the list of actions of the statement:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam
import iam_floyd as statement

statement.Ec2().start_instances()
```

Every method returns the statement provider, so you can chain method calls:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().start_instances().stop_instances()
```

The default effect of any statement is `Allow`. To add some linguistic sugar you can explicitly call the `allow()` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().stop_instances()
```

And of course `deny()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().deny().start_instances().stop_instances()
```

If you don't want to be verbose and add every single action manually to the statement, you discovered the reason why this package was created. You can work with [access levels](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_understand-policy-summary-access-level-summaries.html#access_policies_access-level)!

There are 5 access levels you can use: `LIST`, `READ`, `WRITE`, `PERMISSION_MANAGEMENT` and `TAGGING`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().all_actions(statement.AccessLevel.LIST, statement.AccessLevel.READ)
```

The `allActions()` method also accepts regular expressions which test against the action name:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().deny().all_actions(/vpn/i)
```

If no value is passed, all actions (`ec2:*`) will be added:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().all_actions()
```

For every available condition key, there are `if*()` methods available.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if_encrypted().if_instance_type(["t3.micro", "t3.nano"]).if_associate_public_ip_address(False).if_request_tag("Owner", "John")
```

If you want to add a condition not covered by the available methods, you can define just any condition yourself via `if()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if("aws:RequestTag/Owner", "John")
```

Most of the `if*()` methods allow an optional operator as last argument:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if_instance_type("*.nano", "StringLike").if("aws:RequestTag/Owner", "John*", "StringLike")
```

By default the statement applies to all resources. To limit to specific resources, add them via `on*()`.

For every resource type an `on*()` method exists:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().all_actions().on_bucket("some-bucket").on_object("some-bucket", "some/path/*")
```

If instead you have an ARN ready, use the `on()` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().all_actions().on("arn:aws:s3:::some-bucket", "arn:aws:s3:::another-bucket")
```

What about [notAction](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html)? Yes, simply add a `not()` to the chain. Though it is important that you add it **before** you add actions.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().not().delete_bucket().on_bucket("some-bucket")
```

## <a name='Examples'></a>Examples

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
iam.PolicyDocument(
    statements=[
        statement.Ec2().allow().start_instances().if_request_tag("Owner", "${aws:username}"),
        statement.Ec2().allow().stop_instances().if_resource_tag("Owner", "${aws:username}"),
        statement.Ec2().allow().all_actions(statement.AccessLevel.LIST, statement.AccessLevel.READ)
    ]
)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
iam.PolicyDocument(
    statements=[
        statement.Cloudformation().allow().all_actions(),
        statement.All().allow().all_actions().if_called_via("cloudformation.amazonaws.com"),
        statement.S3().allow().all_actions().on("arn:aws:s3:::cdktoolkit-stagingbucket-*"),
        statement.Account().deny().all_actions(statement.AccessLevel.PERMISSION_MANAGEMENT, statement.AccessLevel.WRITE),
        statement.Organizations().deny().all_actions(statement.AccessLevel.PERMISSION_MANAGEMENT, statement.AccessLevel.WRITE)
    ]
)
```

## <a name='Methods'></a>Methods

### <a name='allow'></a>allow

Sets the `Effect` of the statement to `Allow`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().stop_instances()
```

### <a name='deny'></a>deny

Sets the `Effect` of the statement to `Deny`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().deny().stop_instances()
```

### <a name='allActions'></a>allActions

This method allows you to add multiple actions at once. If called without parameters, it adds all actions of the service.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().all_actions()
```

The method can take regular expressions and [access levels](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_understand-policy-summary-access-level-summaries.html#access_policies_access-level) as options and will add only the matching actions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().all_actions(/vpn/i)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().all_actions(statement.AccessLevel.LIST, statement.AccessLevel.READ)
```

There exist 5 access levels:

* LIST
* READ
* WRITE
* PERMISSION_MANAGEMENT
* TAGGING

### <a name='ifif'></a>if*, if

For every available condition key, there are `if*()` methods available.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if_encrypted().if_instance_type(["t3.micro", "t3.nano"]).if_associate_public_ip_address(False).if_request_tag("Owner", "John")
```

Most of them allow an optional operator as last argument:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if_instance_type("*.nano", "StringLike")
```

If you want to add a condition not covered by the available methods, you can define just any condition yourself via `if()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().if("StringEquals",
    aws:_request_tag/_owner="${aws:username}"
)
```

### <a name='onon'></a>on*, on

Limit statement to specified resources.

For every resource type an `on*()` method exists:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().all_actions().on_bucket("some-bucket")
```

If instead you have an ARN ready, use the `on()` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().all_actions().on("arn:aws:s3:::some-bucket")
```

If no resources are applied to the statement, it defaults to all resources (`*`). You can also be verbose and set this yourself:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().all_actions().on("*")
```

### <a name='not'></a>not

Switches the policy provider to use [notAction](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html). Calling this method will change the behavior of all successive called action methods. It will not modify actions that have been added before the call.

**Correct:** `s3:DeleteBucket` will be added to the list of `NotAction`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().not().delete_bucket().on_bucket("some-bucket")
```

**Wrong:** `s3:DeleteBucket` will be added to the list of `Action`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.S3().allow().delete_bucket().not().on_bucket("some-bucket")
```

## <a name='ButIdontuseCDK.CanIstillusethispackage'></a>But I don't use CDK. Can I still use this package?

Yes. While the package is designed to be used within CDK you can also just use it to generate policy statements in JSON format:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
statement.Ec2().allow().start_instances().stop_instances().on("*").to_jSON()

iam.PolicyDocument(
    statements=[
        statement.Ec2().allow().start_instances().stop_instances().on("*")
    ]
).to_jSON()
```

## <a name='Floyd'></a>Floyd?

George Floyd has been murdered by racist police officers on May 25th, 2020.

This package is not named after him to just remind you of him and his death. I want this package to be of great help to you and I want you to use it on a daily base. Every time you use it, I want you to remember our society is ill and needs change. The riots will stop. The news will fade. The issue persists!

If this statement annoys you, this package is not for you.

## <a name='Similarprojects'></a>Similar projects

* [cdk-iam-actions](https://github.com/spacerat/cdk-iam-actions)
* [cdk-iam-generator](https://github.com/srihariph/cdk-iam-generator)
* [iam-policy-generator](https://github.com/aletheia/iam-policy-generator)

## <a name='Legal'></a>Legal

The code contained in the [lib](https://github.com/udondan/iam-floyd/tree/master/lib) folder is generated from the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html). The class- and function-names and their description therefore are property of AWS.

AWS and their services are trademarks, registered trademarks or trade dress of AWS in the U.S. and/or other countries.

This project is not affiliated, funded, or in any way associated with AWS.
