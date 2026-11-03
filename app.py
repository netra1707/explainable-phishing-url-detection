import shap
import json
import ipaddress
from urllib.parse import urlparse

import joblib
import pandas as pd
import streamlit as st


# Load the trained model and its expected feature order
MODEL_PATH = "url_phishing_model.joblib"
FEATURES_PATH = "url_feature_columns.json"

model = joblib.load(MODEL_PATH)

with open(FEATURES_PATH, "r") as file:
    feature_columns = json.load(file)


def extract_url_features(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    if (
        not domain
        or "." not in domain
        or domain.startswith(".")
        or domain.endswith(".")
        or " " in domain
    ):
        raise ValueError("Please enter a valid URL with a domain, such as example.com.")
    
    parsed = urlparse(url)
    domain = parsed.hostname or ""

    if not domain:
        raise ValueError("Please enter a valid URL with a domain.")

    url_length = len(url)
    domain_length = len(domain)
    tld = domain.rsplit(".", 1)[-1] if "." in domain else ""

    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    letters = sum(c.isalpha() for c in url)
    digits = sum(c.isdigit() for c in url)
    special_chars = sum(not c.isalnum() for c in url)
    obfuscated_chars = url.count("%")

    domain_parts = domain.split(".")
    subdomain_count = (
        max(0, len(domain_parts) - 2) if not is_domain_ip else 0
    )

    return {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "TLDLength": len(tld),
        "NoOfSubDomain": subdomain_count,
        "HasObfuscation": int("%" in url or "@" in url),
        "NoOfObfuscatedChar": obfuscated_chars,
        "ObfuscationRatio": obfuscated_chars / url_length if url_length else 0,
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letters / url_length if url_length else 0,
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digits / url_length if url_length else 0,
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": special_chars,
        "SpacialCharRatioInURL": special_chars / url_length if url_length else 0,
        "IsHTTPS": int(parsed.scheme.lower() == "https"),
    }


st.set_page_config(
    page_title="Phishing URL Detection",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Phishing URL Detection")
st.write(
    "Analyze URL characteristics using a machine-learning model "
    "and view the prediction."
)
st.caption(
    "This is a URL-only screening tool. It cannot guarantee that a website is safe."
)

url_input = st.text_input(
    "Enter a website URL",
    placeholder="https://example.com/login"
)

if st.button("Analyze URL", type="primary"):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    else:
        try:
            features = extract_url_features(url_input)
            feature_frame = pd.DataFrame([features]).reindex(
                columns=feature_columns
            )

            if feature_frame.isna().any().any():
                st.error(
                    "The feature extractor does not match the saved model's "
                    "expected features. Please check the feature columns."
                )
            else:
                prediction = int(model.predict(feature_frame)[0])
                probabilities = model.predict_proba(feature_frame)[0]
                phishing_probability = float(probabilities[1])

                st.subheader("Analysis result")

                if prediction == 1:
                    st.error("Potential phishing URL")
                else:
                    st.success("Classified as likely legitimate")

                st.metric(
                    "Model phishing probability",
                    f"{phishing_probability:.2%}"
                )

                with st.expander("Why did the model make this prediction?"):
                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(feature_frame)

                    if isinstance(shap_values, list):
                        contributions = shap_values[1][0]
                    elif shap_values.ndim == 3:
                        contributions = shap_values[0, :, 1]
                    else:
                        contributions = shap_values[0]

                    explanation = pd.DataFrame({
                        "Feature": feature_frame.columns,
                        "Contribution": contributions
                    })

                    explanation["Absolute contribution"] = (
                        explanation["Contribution"].abs()
                    )

                    explanation = explanation.sort_values(
                        "Absolute contribution", ascending=False
                    ).head(8)

                    st.write(
                        "These are the eight URL features with the largest SHAP contributions."
                    )

                    st.bar_chart(
                        explanation.set_index("Feature")["Contribution"],
                        horizontal=True
                    )

                    st.caption(
                        "Positive contributions generally push toward the phishing class; "
                        "negative contributions push away from it. Interpret them in the "
                        "context of this model, not as proof that a website is malicious."
                    )

                st.caption(
                    "This probability reflects the model's estimate, "
                    "not a guarantee of risk or safety."
                )

                with st.expander("View extracted URL features"):
                    st.dataframe(feature_frame, use_container_width=True)

        except Exception as error:
            st.error(f"Could not analyze this URL: {error}")
