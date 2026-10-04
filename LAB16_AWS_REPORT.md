# Lab 16 AWS Report

I deployed the Lab 16 CPU infrastructure on AWS using Terraform in `us-east-1`. The deployment created a VPC, public and private subnets, Internet Gateway, NAT Gateway, bastion host, Application Load Balancer, and a private `t3.medium` CPU compute node. I connected through the bastion host to the private compute node and ran the LightGBM benchmark on the Credit Card Fraud Detection dataset.

The dataset contained 284,807 transactions, including 492 fraud rows, with a fraud rate of 0.00172749. Data loading took 2.470128 seconds and model training took 2.050067 seconds. The LightGBM model achieved AUC-ROC = 0.922938, Accuracy = 0.998122, F1-score = 0.60223, Precision = 0.473684, and Recall = 0.826531. Single-row inference latency was 1.39045 ms, and 1000-row inference throughput was 555,555.556 rows/second.

The compute node reported 2 CPU cores, 3.7 GiB total memory, and 3.2 GiB available memory after the benchmark. Network counters showed 279,571,846 RX bytes and 912,343 TX bytes on the main interface. After collecting results, I ran `terraform destroy`, and Terraform confirmed that all 27 created resources were destroyed to avoid ongoing AWS credit usage.
