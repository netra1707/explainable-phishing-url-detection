# 🛡️ Explainable Phishing URL Detection

An Explainable Machine Learning System for Detecting Potentially Phishing URLs Using Random Forest and SHAP.

## 📌 Project Overview

Phishing attacks are a common cybersecurity threat in which attackers create deceptive URLs and websites to trick users into revealing sensitive information such as login credentials, financial details, and personal data.

This project implements a machine learning-based phishing URL detection system that analyzes URL characteristics and predicts whether a given URL is potentially phishing or likely legitimate.

The system uses a **Random Forest Classifier** for prediction and **SHAP (SHapley Additive exPlanations)** to provide insights into the features influencing each prediction.

A web interface built using **Streamlit** allows users to enter a URL, view the prediction, examine the estimated phishing probability, and explore feature-level explanations.

## 🎯 Objectives

- Develop a machine learning model for phishing URL classification.
- Extract meaningful characteristics directly from URL strings.
- Apply Random Forest for binary classification.
- Integrate SHAP to improve model interpretability.
- Build an interactive web application using Streamlit.
- Provide users with understandable prediction results.

## 🏗️ System Architecture

The application follows this workflow:

```text
       User Input
           |
           v
      Enter URL
           |
           v
   URL Feature Extraction
           |
           v
    Feature Preparation
           |
           v
   Trained Random Forest
           |
           v
    Classification
           |
       +---+---+
       |       |
       v       v
   Phishing  Legitimate
       |       |
       +---+---+
           |
           v
  Prediction Probability
           |
           v
    SHAP Explanation
           |
           v
   Streamlit Interface
```

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data handling and preprocessing |
| Scikit-learn | Machine learning and model evaluation |
| Random Forest | Classification algorithm |
| SHAP | Model explainability |
| Streamlit | Interactive web application |
| Joblib | Saving and loading the trained model |
| UCI Machine Learning Repository | Dataset source |

## 📊 Dataset

This project uses the **PhiUSIIL Phishing URL (Website) Dataset** from the UCI Machine Learning Repository.

**Dataset details:**

- Dataset ID: 967
- Total records: 235,795
- Legitimate URLs: 134,850
- Phishing URLs: 100,945
- Total original dataset features: 54

**Dataset authors:** Arvind Prasad and Shalini Chandra.

**Dataset source:**

https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+website+dataset

**Dataset license:** Creative Commons Attribution 4.0 International (CC BY 4.0).

### Data Preparation

The original dataset provides URL and webpage-related information. For this project, a URL-only feature extraction approach was implemented.

The target labels were converted as follows:

- `1` – Phishing
- `0` – Legitimate

The dataset was divided into training and testing sets using `GroupShuffleSplit`, grouping by domain to prevent domains from appearing in both sets.

| Dataset | Records |
|---|---:|
| Training | 189,074 |
| Testing | 46,721 |
| Total | 235,795 |

This domain-based splitting strategy helps reduce domain overlap between training and testing data.

## 🔍 URL Feature Extraction

The system extracts 18 numerical features directly from the submitted URL.

| Feature | Description |
|---|---|
| URLLength | Total length of the URL |
| DomainLength | Length of the domain |
| IsDomainIP | Indicates whether the domain is an IP address |
| TLDLength | Length of the top-level domain |
| NoOfSubDomain | Number of subdomains |
| HasObfuscation | Indicates URL obfuscation patterns |
| NoOfObfuscatedChar | Number of percent-encoded characters |
| ObfuscationRatio | Ratio of obfuscated characters |
| NoOfLettersInURL | Number of alphabetic characters |
| LetterRatioInURL | Ratio of alphabetic characters |
| NoOfDegitsInURL | Number of digits in the URL |
| DegitRatioInURL | Ratio of digits in the URL |
| NoOfEqualsInURL | Number of equals signs |
| NoOfQMarkInURL | Number of question marks |
| NoOfAmpersandInURL | Number of ampersands |
| NoOfOtherSpecialCharsInURL | Number of special characters |
| SpacialCharRatioInURL | Ratio of special characters |
| IsHTTPS | Indicates whether HTTPS is used |

These features are calculated using URL parsing and string-based analysis.

## 🤖 Machine Learning Model

A **Random Forest Classifier** was selected for the binary classification task.

### Model Configuration

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
```

### Why Random Forest?

- Handles nonlinear relationships between features.
- Combines predictions from multiple decision trees.
- Provides feature importance information.
- Supports probability-based predictions.
- Works effectively with numerical URL characteristics.

The trained model is saved using Joblib and loaded by the Streamlit application.

## 📈 Model Evaluation

The model was evaluated on the held-out test set.

### Test Performance

| Metric | Score |
|---|---:|
| Accuracy | 99.52% |
| Precision (Phishing) | 99.59% |
| Recall (Phishing) | 99.27% |
| F1-score (Phishing) | 99.43% |
| ROC-AUC | 0.9979 |

### Confusion Matrix

| | Predicted Legitimate | Predicted Phishing |
|---|---:|---:|
| Actual Legitimate | 26,843 | 80 |
| Actual Phishing | 145 | 19,653 |

**Important:** These results represent performance on the selected dataset split. They do not establish equivalent performance on previously unseen, real-world URLs. Independent external validation is required to assess generalization.

## 💡 Explainable AI Using SHAP

A key component of this project is model explainability.

Instead of presenting only a classification result, the application uses SHAP to identify which URL characteristics contributed most to the model's prediction.

### SHAP Integration

- Uses `shap.TreeExplainer` for the trained Random Forest model.
- Calculates feature-level SHAP contributions.
- Identifies the eight features with the largest absolute contributions.
- Displays a horizontal bar chart in the Streamlit interface.

### Explanation Interpretation

- Positive SHAP contributions generally push the prediction towards phishing.
- Negative SHAP contributions generally push the prediction towards legitimate.

SHAP explanations describe the behavior of the trained model. They do not independently establish whether a URL is malicious.

## 🖥️ Application Features

The Streamlit application provides:

- URL input field.
- URL validation.
- Automatic URL feature extraction.
- Phishing or likely legitimate classification.
- Estimated phishing probability.
- SHAP-based feature contribution visualization.
- Expandable extracted-feature table.
- User-friendly error handling.

## 📂 Project Structure

```text
explainable-phishing-url-detection/
│
├── app.py
│
├── url_phishing_model.joblib
│
├── url_feature_columns.json
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Streamlit application and URL feature extraction |
| `url_phishing_model.joblib` | Trained Random Forest model |
| `url_feature_columns.json` | Expected model feature configuration |
| `requirements.txt` | Required Python libraries |
| `.gitignore` | Files excluded from Git tracking |
| `README.md` | Project documentation |

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/netra1707/explainable-phishing-url-detection.git
```

### 2. Navigate to the Project Directory

```bash
cd explainable-phishing-url-detection
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Environment

**Windows (Command Prompt):**

```bash
.venv\Scripts\activate
```

**Windows (Git Bash):**

```bash
source .venv/Scripts/activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## ⚠️ Limitations and Future Improvements

### Current Limitations

- The application analyzes URL characteristics only.
- It does not fetch or inspect the live webpage.
- Model performance may vary on URLs from different sources and time periods.
- A high phishing probability is not proof that a website is malicious.
- A legitimate prediction does not guarantee that a website is safe.
- The model requires additional external validation before real-world deployment.

### Future Improvements

- Evaluate the model on independent and more recent phishing datasets.
- Explore additional machine learning and deep learning approaches.
- Improve URL feature extraction and validation.
- Add webpage-content analysis.
- Investigate model robustness against evolving phishing techniques.
- Improve the explainability interface and user experience.

## 🔐 Responsible Use

This project is developed for academic, educational, and research purposes.

It is intended as a preliminary phishing URL screening tool and should not be treated as a replacement for professional cybersecurity solutions, browser security mechanisms, or threat intelligence services.

Always verify suspicious links using trusted security tools.

## 📜 Dataset Attribution and License

This project uses the PhiUSIIL Phishing URL (Website) Dataset.

**Citation:**

Prasad, A., & Chandra, S. (2024). *PhiUSIIL Phishing URL (Website) [Dataset].* UCI Machine Learning Repository.

https://doi.org/10.1016/j.cose.2023.103545

The dataset is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

The original dataset authors retain attribution for their work. The trained model is a project artifact derived from features calculated using this dataset.

The repository's source code and model artifact should not be assumed to have a separate open-source license unless one is explicitly added.

## ⭐ Acknowledgements

- UCI Machine Learning Repository for providing the PhiUSIIL dataset.
- The original dataset authors, Arvind Prasad and Shalini Chandra.
- The open-source Python machine learning and explainability communities.

---

**Built with Python, Machine Learning, Explainable AI, and Streamlit.**