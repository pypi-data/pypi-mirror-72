## AWS AppSync Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Usage Example

Given the following GraphQL schema file `schema.graphql`:

```graphql
type ServiceVersion {
    version: String!
}

type Customer {
    id: String!
    name: String!
}

input SaveCustomerInput {
    name: String!
}

type Order {
    customer: String!
    order: String!
}

type Query {
    getServiceVersion: ServiceVersion
    getCustomers: [Customer]
    getCustomer(id: String): Customer
}

input FirstOrderInput {
    product: String!
    quantity: Int!
}

type Mutation {
    addCustomer(customer: SaveCustomerInput!): Customer
    saveCustomer(id: String!, customer: SaveCustomerInput!): Customer
    removeCustomer(id: String!): Customer
    saveCustomerWithFirstOrder(customer: SaveCustomerInput!, order: FirstOrderInput!, referral: String): Order
    doPostOnAws: String!
}
```

the following CDK app snippet will create a complete CRUD AppSync API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class ApiStack(Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        user_pool = UserPool(self, "UserPool",
            user_pool_name="myPool"
        )

        api = GraphQLApi(self, "Api",
            name="demoapi",
            log_config={
                "field_log_level": FieldLogLevel.ALL
            },
            authorization_config={
                "default_authorization": {
                    "authorization_type": AuthorizationType.USER_POOL,
                    "user_pool_config": {
                        "user_pool": user_pool,
                        "default_action": UserPoolDefaultAction.ALLOW
                    }
                },
                "additional_authorization_modes": [{
                    "authorization_type": AuthorizationType.API_KEY
                }
                ]
            },
            schema_definition_file="./schema.graphql"
        )

        none_dS = api.add_none_data_source("None", "Dummy data source")

        none_dS.create_resolver(
            type_name="Query",
            field_name="getServiceVersion",
            request_mapping_template=MappingTemplate.from_string(JSON.stringify(
                version="2017-02-28"
            )),
            response_mapping_template=MappingTemplate.from_string(JSON.stringify(
                version="v1"
            ))
        )

        customer_table = Table(self, "CustomerTable",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            partition_key={
                "name": "id",
                "type": AttributeType.STRING
            }
        )
        customer_dS = api.add_dynamo_db_data_source("Customer", "The customer data source", customer_table)
        customer_dS.create_resolver(
            type_name="Query",
            field_name="getCustomers",
            request_mapping_template=MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=MappingTemplate.dynamo_db_result_list()
        )
        customer_dS.create_resolver(
            type_name="Query",
            field_name="getCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_get_item("id", "id"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="addCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_put_item(
                PrimaryKey.partition("id").auto(),
                Values.projecting("customer")),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="saveCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_put_item(
                PrimaryKey.partition("id").is("id"),
                Values.projecting("customer")),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="saveCustomerWithFirstOrder",
            request_mapping_template=MappingTemplate.dynamo_db_put_item(
                PrimaryKey.partition("order").auto().sort("customer").is("customer.id"),
                Values.projecting("order").attribute("referral").is("referral")),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="removeCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_delete_item("id", "id"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )

        http_dS = api.add_http_data_source("http", "The http data source", "https://aws.amazon.com/")

        http_dS.create_resolver(
            type_name="Mutation",
            field_name="doPostOnAws",
            request_mapping_template=MappingTemplate.from_string("{\n        \"version\": \"2018-05-29\",\n        \"method\": \"POST\",\n        # if full path is https://api.xxxxxxxxx.com/posts then resourcePath would be /posts\n        \"resourcePath\": \"/path/123\",\n        \"params\":{\n            \"body\": $util.toJson($ctx.args),\n            \"headers\":{\n                \"Content-Type\": \"application/json\",\n                \"Authorization\": \"$ctx.request.headers.Authorization\"\n            }\n        }\n      }"),
            response_mapping_template=MappingTemplate.from_string("\n        ## Raise a GraphQL field error in case of a datasource invocation error\n        #if($ctx.error)\n          $util.error($ctx.error.message, $ctx.error.type)\n        #end\n        ## if the response status code is not 200, then return an error. Else return the body **\n        #if($ctx.result.statusCode == 200)\n            ## If response is 200, return the body.\n            $ctx.result.body\n        #else\n            ## If response is not 200, append the response to error block.\n            $utils.appendError($ctx.result.body, \"$ctx.result.statusCode\")\n        #end\n      ")
        )
```
