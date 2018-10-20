import aws_cdk.aws_cognito.cloudformation as cognito_cloudformation
import aws_cdk.cdk as cdk


def CognitoChatRoomPool(parent: cdk.Construct, name: str):
    self = cdk.Construct(parent, name)

    # Create chat room user pool
    chatPool = cognito_cloudformation.UserPoolResource(
        self,
        "UserPool",
        {
            "adminCreateUserConfig": {"allowAdminCreateUserOnly": False},
            "policies": {
                "passwordPolicy": {"minimumLength": 6, "requireNumbers": True}
            },
            "schema": [
                {"attributeDataType": "String", "name": "email", "required": True}
            ],
            "autoVerifiedAttributes": ["email"],
        },
    )

    # Now for the client
    cognito_cloudformation.UserPoolClientResource(
        self,
        "UserPoolClient",
        {
            "clientName": "Chat-Room",
            "explicitAuthFlows": ["ADMIN_NO_SRP_AUTH"],
            "refreshTokenValidity": 30,
            "userPoolId": chatPool.ref,
        },
    )

    return self