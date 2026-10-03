# Lab 16 Submission Checklist

Use this checklist after Terraform deploys the CPU node successfully.

## Recommended Path

Use the CPU-only AWS path unless your instructor explicitly asks for GPU:

```bash
cd terraform
ssh-keygen -t rsa -b 4096 -f lab-key -N ""
terraform init
terraform apply
```

After `terraform apply`, record:

- `bastion_public_ip`
- `gpu_private_ip` (this is the CPU compute node in the default path)

## Run Benchmark On The Compute Node

SSH through the bastion:

```bash
ssh -i lab-key ubuntu@<BASTION_PUBLIC_IP>
ssh ubuntu@<CPU_PRIVATE_IP>
```

Prepare Kaggle credentials and dataset:

```bash
mkdir -p ~/.kaggle
cat > ~/.kaggle/kaggle.json << 'EOF'
{"username": "YOUR_KAGGLE_USERNAME", "key": "YOUR_KAGGLE_API_KEY"}
EOF
chmod 600 ~/.kaggle/kaggle.json

mkdir -p ~/ml-benchmark
kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/
```

Copy `benchmark.py` from this repo to the compute node, then run:

```bash
python3 benchmark.py
cat benchmark_result.json
```

## Evidence To Submit

- Screenshot of terminal running `python3 benchmark.py` with all printed metrics.
- File `benchmark_result.json`.
- Screenshot of resource usage on the compute node:

```bash
top
free -h
ip -s link
```

- Screenshot of AWS Billing or Cost Explorer for today's costs.
- The Terraform source folder you used: `terraform/`.
- Short report, 5-10 lines, covering training time, AUC-ROC, inference speed, resource usage, estimated cost, and cleanup.

## Suggested Short Report Template

```text
I deployed the Lab 16 CPU infrastructure on AWS using Terraform. The environment
created a VPC, public/private subnets, NAT Gateway, bastion host, Application
Load Balancer, and a private t3.medium compute node. I trained a LightGBM model
on the Credit Card Fraud Detection dataset with 284,807 transactions. The model
achieved AUC-ROC = <AUC>, Accuracy = <ACC>, F1 = <F1>, Precision = <PRECISION>,
and Recall = <RECALL>. Training took <TRAINING_TIME> seconds, and single-row
inference latency was <LATENCY> ms. The 1000-row inference throughput was
<THROUGHPUT> rows/second. CPU and memory usage were acceptable for a small CPU
instance. The main cost drivers were EC2, NAT Gateway, and ALB. After collecting
evidence, I destroyed the Terraform resources to avoid extra cost.
```

## Cleanup

Run this immediately after collecting screenshots and files:

```bash
cd terraform
terraform destroy
```
