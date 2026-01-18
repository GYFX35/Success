# Tencent Cloud Static Website Deployment

This document provides instructions on how to deploy the static website in the `docs/` directory to Tencent Cloud Object Storage (COS).

## Prerequisites

1.  **Tencent Cloud Account:** You will need a Tencent Cloud account. If you don't have one, you can sign up on the [Tencent Cloud website](https://www.tencentcloud.com/).

2.  **AWS CLI:** The deployment script uses the AWS CLI, which is compatible with Tencent's S3-like API for COS. You can install it using pip:
    ```bash
    pip install awscli
    ```

3.  **API Credentials:** You need to create an API key (SecretId and SecretKey) in the Tencent Cloud console.
    -   Navigate to the [API Key Management page](https://console.cloud.tencent.com/cam/capi).
    -   Create a new key and save the SecretId and SecretKey securely.

4.  **Configure AWS CLI:** Configure the AWS CLI with your Tencent Cloud credentials. Run the following command and enter your credentials when prompted:
    ```bash
    aws configure
    ```
    -   **AWS Access Key ID:** Enter your Tencent Cloud SecretId.
    -   **AWS Secret Access Key:** Enter your Tencent Cloud SecretKey.
    -   **Default region name:** Enter a Tencent Cloud region, for example, `ap-guangzhou`.
    -   **Default output format:** You can leave this as `json`.

## Deployment

The `tencent_deploy.sh` script automates the process of creating a COS bucket, configuring it for static website hosting, and uploading the website files.

### Usage

1.  **Make the script executable:**
    ```bash
    chmod +x tencent_deploy.sh
    ```

2.  **Run the script:**
    ```bash
    ./tencent_deploy.sh <bucket-name> <region>
    ```
    -   `<bucket-name>`: A unique name for your COS bucket (e.g., `my-static-website-123`).
    -   `<region>`: The Tencent Cloud region where you want to create the bucket (e.g., `ap-guangzhou`).

    **Example:**
    ```bash
    ./tencent_deploy.sh my-awesome-static-site ap-singapore
    ```

3.  **Access your website:**
    After the script finishes, it will print the URL of your deployed website. You can open this URL in your browser to see your live website.
