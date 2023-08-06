# Copyright 2019 Amazon.com, Inc. and its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the 'License').
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#   http://aws.amazon.com/asl/
#
# or in the 'license' file accompanying this file. This file is distributed
# on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from aws_cdk import (
    aws_lambda,
    aws_events as events,
    aws_iam as iam,
    core
)

from aws_emr_launch.constructs.lambdas import _lambda_path
from aws_emr_launch.constructs.iam_roles import emr_roles


class FailIfClusterRunningBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/fail_if_cluster_running'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('FailIfClusterRunning')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'FailIfClusterRunning',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer],
                initial_policy=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            'elasticmapreduce:ListClusters'
                        ],
                        resources=['*']
                    )
                ]
            )
        return lambda_function


class LoadClusterConfigurationBuilder:
    @staticmethod
    def build(scope: core.Construct, profile_namespace: str, profile_name: str,
              configuration_namespace: str, configuration_name: str) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/load_cluster_configuration'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = aws_lambda.Function(
            scope,
            'LoadClusterConfiguration',
            code=code,
            handler='lambda_source.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            timeout=core.Duration.minutes(1),
            layers=[layer],
            initial_policy=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=['ssm:GetParameter'],
                    resources=[
                        stack.format_arn(
                            partition=stack.partition,
                            service='ssm',
                            resource='parameter/emr_launch/cluster_configurations/'
                            f'{configuration_namespace}/{configuration_name}'
                        ),
                        stack.format_arn(
                            partition=stack.partition,
                            service='ssm',
                            resource='parameter/emr_launch/emr_profiles/'
                            f'{profile_namespace}/{profile_name}'
                        )
                    ]
                )
            ]
        )
        return lambda_function


class OverrideClusterConfigsBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/override_cluster_configs'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('OverrideClusterConfigs')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'OverrideClusterConfigs',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer]
            )
        return lambda_function


class UpdateClusterTagsBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/update_cluster_tags'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('UpdateClusterTags')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'UpdateClusterTags',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer]
            )
        return lambda_function


class ParseJsonStringBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/parse_json_string'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('ParseJsonString')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'ParseJsonString',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer]
            )
        return lambda_function


class OverrideStepArgsBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/override_step_args'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('OverrideStepArgs')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'OverrideStepArgs',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer]
            )
        return lambda_function


class RunJobFlowBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct, roles: emr_roles.EMRRoles, event_rule: events.Rule) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/run_job_flow'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('RunJobFlow')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'RunJobFlow',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer],
                initial_policy=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=['elasticmapreduce:RunJobFlow'],
                        resources=['*']
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=['iam:PassRole'],
                        resources=[
                            roles.service_role.role_arn,
                            roles.instance_role.role_arn,
                            roles.autoscaling_role.role_arn
                        ]
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=['states:SendTaskSuccess'],
                        resources=['*']
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=['events:EnableRule', 'events:PutTargets'],
                        resources=[event_rule.rule_arn]
                    )
                ]
            )
        return lambda_function


class CheckClusterStatusBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct, event_rule: events.Rule) -> aws_lambda.Function:
        code = aws_lambda.Code.from_asset(_lambda_path('emr_utilities/check_cluster_status'))
        stack = core.Stack.of(scope)

        layer = EMRConfigUtilsLayerBuilder.get_or_build(scope)

        lambda_function = stack.node.try_find_child('CheckClusterStatus')
        if lambda_function is None:
            lambda_function = aws_lambda.Function(
                stack,
                'CheckClusterStatus',
                code=code,
                handler='lambda_source.handler',
                runtime=aws_lambda.Runtime.PYTHON_3_7,
                timeout=core.Duration.minutes(1),
                layers=[layer],
                initial_policy=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            'states:SendTaskSuccess',
                            'states:SendTaskHeartbeat',
                            'states:SendTaskFailure'
                        ],
                        resources=['*']
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=['elasticmapreduce:DescribeCluster'],
                        resources=['*']
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            'events:ListTargetsByRule',
                            'events:DisableRule',
                            'events:RemoveTargets'],
                        resources=[event_rule.rule_arn]
                    )
                ]
            )
            lambda_function.add_permission(
                'EventRulePermission',
                principal=iam.ServicePrincipal('events.amazonaws.com'),
                action='lambda:InvokeFunction',
                source_arn=event_rule.rule_arn)

        return lambda_function


class EMRConfigUtilsLayerBuilder:
    @staticmethod
    def get_or_build(scope: core.Construct) -> aws_lambda.LayerVersion:
        code = aws_lambda.Code.from_asset(_lambda_path('layers/emr_config_utils'))
        stack = core.Stack.of(scope)

        layer = stack.node.try_find_child('EMRConfigUtilsLayer')
        if layer is None:
            layer = aws_lambda.LayerVersion(
                stack,
                'EMRConfigUtilsLayer',
                layer_version_name='EMRLaunch_EMRUtilities_EMRConfigUtilsLayer',
                code=code,
                compatible_runtimes=[
                    aws_lambda.Runtime.PYTHON_3_7
                ],
                description='EMR configuration utility functions'
            )
        return layer
