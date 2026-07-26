# Failure Modes

| Failure | Expected Behavior | Detection |
|---|---|---|
| Missing index | Build from sample docs or fail startup in production | Runtime validation |
| Empty retrieval | Return grounded no-answer response | Empty result metric |
| Bedrock unavailable | Return retrieval context or graceful error | CloudWatch alarm |
| Bad secrets | Fail validation before deploy | Validation script |
| Low recall after chunking change | Evaluation regression fails | Eval script |

