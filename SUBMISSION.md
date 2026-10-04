# Lab 16 Submission - AWS Cloud AI CPU Benchmark

## Execution Environment

- Cloud provider: AWS
- Region: `us-east-1` / United States (N. Virginia)
- Infrastructure as Code: Terraform
- Bastion host: `t3.micro`
- Compute node: `t3.medium` CPU instance in a private subnet
- Dataset: Credit Card Fraud Detection (`mlg-ulb/creditcardfraud`)
- Dataset path on AWS node: `/home/ubuntu/ml-benchmark/creditcard.csv`
- Output file: `aws_benchmark_result.json`

The AWS infrastructure was deployed with Terraform, benchmarked on the private CPU compute node, and then destroyed successfully to avoid ongoing cost. The Terraform destroy completed with `Resources: 27 destroyed`.

## AWS Terraform Outputs

These were the outputs after `terraform apply`:

| Output | Value |
|---|---|
| `bastion_public_ip` | `3.235.51.109` |
| `gpu_private_ip` | `10.0.10.62` |
| `alb_dns_name` | `ai-inference-alb-eac03583-986875896.us-east-1.elb.amazonaws.com` |
| `endpoint_url` | `http://ai-inference-alb-eac03583-986875896.us-east-1.elb.amazonaws.com/v1/completions` |

`gpu_private_ip` is the shared output name from the Terraform template; in the required CPU path it refers to the private CPU LightGBM compute node.

## Benchmark Results

| Metric | Result |
|---|---:|
| Rows | 284,807 |
| Fraud rows | 492 |
| Fraud rate | 0.00172749 |
| Load data time | 2.470128 seconds |
| Training time | 2.050067 seconds |
| Best iteration | 1 |
| AUC-ROC | 0.922938 |
| Accuracy | 0.998122 |
| F1-score | 0.60223 |
| Precision | 0.473684 |
| Recall | 0.826531 |
| Inference latency, 1 row | 1.39045 ms |
| Inference throughput, 1000 rows | 555,555.556 rows/second |

## Resource Evidence

The AWS compute node reported:

| Resource | Value |
|---|---:|
| CPU count | 2 |
| Memory total | 3.7 GiB |
| Memory available | 3.2 GiB |
| Network RX bytes | 279,571,846 |
| Network TX bytes | 912,343 |

## Submitted Files

- `terraform/`: AWS Terraform infrastructure source.
- `benchmark.py`: standalone benchmark script for the CPU LightGBM workflow.
- `aws_node_run.sh`: helper script used to run the AWS benchmark on the private compute node.
- `aws_benchmark_result.json`: measured AWS benchmark output.
- `LAB16_AWS_REPORT.md`: short written AWS report.
- `kaggle_lab16_benchmark.ipynb`: fallback notebook retained for reproducibility if cloud account access is unavailable.

## Short Report

I deployed the Lab 16 CPU infrastructure on AWS using Terraform in `us-east-1`. Terraform created a VPC, public and private subnets, an Internet Gateway, NAT Gateway, bastion host, Application Load Balancer, and a private `t3.medium` compute node. I connected through the bastion host to the private compute node and trained a LightGBM binary classifier on the Credit Card Fraud Detection dataset with 284,807 transactions. The model achieved AUC-ROC = 0.922938, Accuracy = 0.998122, F1-score = 0.60223, Precision = 0.473684, and Recall = 0.826531. Training took 2.050067 seconds, single-row inference latency was 1.39045 ms, and 1000-row inference throughput was 555,555.556 rows/second. After collecting the benchmark result and resource evidence, I ran `terraform destroy`, and Terraform confirmed `Resources: 27 destroyed`.
