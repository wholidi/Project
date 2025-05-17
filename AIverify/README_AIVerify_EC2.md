
# ✅ AI Verify on AWS EC2 – Custom Plugin & Model Testing

This project deploys **[AI Verify](https://aiverify-foundation.github.io/aiverify/)** on an AWS EC2 instance using Docker to evaluate AI/ML models for fairness, explainability, robustness, and compliance. It includes multiple model pipelines, datasets, and test configurations for dynamic plugin execution.

---

## 🛠 Deployment Setup

### EC2 Environment
- Instance: Amazon Linux / Ubuntu
- Docker & Docker Compose installed
- Ports: 3000 (web), 6379 (Valkey), 8080 (API Gateway), etc.

### Running Containers
```bash
docker-compose up -d
```
Expected containers:
- `apigw` – API Gateway
- `portal` – Web UI
- `valkey` – Valkey Redis-compatible DB
- `test-engine-worker` – Executes plugins/tests

---

## 🧪 Use Case

The instance runs **custom and sample models** through AI Verify plugins with uploaded configuration files.

Examples include:
- Binary classification (`sample_bc_credit_sklearn_linear`)
- Multi-class classification (`sample_mc_toxic_sklearn_linear`)
- Regression (`sample_reg_donation_sklearn_linear`)
- PyTorch & Sklearn pipelines
- Tabular and image datasets (e.g., fashion MNIST)

---

## 📁 Directory Structure

```
user_defined_files/
├── model/                  # Pre-trained models (.pkl/.sav)
├── data/                   # Test datasets (CSV, images, etc.)
├── pipeline/               # Custom class wrappers & pipelines
├── veritas_data/           # Veritas-specific sample data
├── test_config.json        # Test configuration file
├── final_upload/           # Final package (model + config + data)
├── clean_upload/           # Clean testable bundle
```

---

## 🧪 How to Run a Test

### 1. Upload files via Web Portal or API:
- `model.sav` or `aiverify_model.pkl`
- `test_data.csv` or `.sav`
- `test_config.json`

### 2. Run via API or Portal interface
- Web UI: `http://<EC2-PUBLIC-IP>:3000`
- Or use `curl` to POST model, data, and config

### 3. View results
- Test results show metrics for:
  - **Fairness**
  - **Transparency**
  - **Robustness**
  - **Accountability**

---

## 📦 Example Models in Repository

| Model Type     | File / Path                                                             |
|----------------|--------------------------------------------------------------------------|
| Logistic Regression | `model/sample_bc_credit_sklearn_linear.LogisticRegression.sav`     |
| PyTorch Fashion MNIST | `pipeline/sample_fashion_mnist_pytorch/fashion_mnist_pytorch.pt` |
| Multi-Class Toxic    | `pipeline/mc_tabular_toxic/sample_mc_toxic_sklearn_linear.Pipeline.sav` |

---

## 📬 Attribution

- 🧪 AI Verify is developed by [AI Verify Foundation](https://aiverifyfoundation.sg/)
- 📊 This deployment is used to explore AI audit, fairness, and compliance testing
- 📚 Supports integration with EU AI Act, OECD, IMDA Veritas, etc.

---

## ✅ Tips

- 📁 Bundle clean packages under `/final_upload` or `/clean_upload`
- 🧪 Run isolated test sessions with distinct `test_config.json` files
- 🧠 Extend by writing your own plugin in `/pipeline/` structure
