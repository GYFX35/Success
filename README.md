# Environment Protection Initiative

This project is a web application designed to promote environmental protection and sustainable development. It provides resources for forest management, promotes sustainable agriculture, and offers a platform for community collaboration. The application also leverages an AI assistant to provide guidance and information on environmental topics.

## Features

*   **Forester Resources:** Access to information and tools for forest management and conservation.
*   **Sustainable Agriculture:** Information and resources to promote eco-friendly farming practices.
*   **Community Forums:** A platform for users to discuss and collaborate on environmental projects.
*   **Development Projects:** Tracking and managing sustainable development goals, with data from the World Bank API.
*   **AI Assistant:** A chat-based AI assistant to answer questions and provide guidance on environmental protection.

## World Bank API Integration

This application integrates with the World Bank API to fetch and display data on environmental indicators. Currently, it displays the forest area percentage for Brazil, Indonesia, and the Democratic Republic of Congo.

## Usage

To run this project locally, you will need to have Python and Flask installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Navigate to the backend directory:**
    ```bash
    cd eco_project/backend
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
5.  **Open the frontend:**
    Open the `eco_project/frontend/index.html` file in your web browser.

## Deployment

This project can be deployed to Google Cloud Run using the provided `deploy.sh` script.

### Prerequisites

*   Google Cloud SDK (`gcloud`) installed and authenticated.
*   A Google Cloud project with billing enabled.

### Steps

1.  **Make the deploy script executable:**
    ```bash
    chmod +x deploy.sh
    ```
2.  **Run the deploy script:**
    ```bash
    ./deploy.sh
    ```
    The script will prompt you for your Google Cloud project ID if it's not already set in your environment. It will then perform the following actions:
    *   Enable the necessary Google Cloud APIs.
    *   Build the frontend and backend Docker images using Google Cloud Build.
    *   Push the images to Google Container Registry.
    *   Deploy the backend service to Cloud Run.
    *   Deploy the frontend service to Cloud Run.
    *   Print the URL of the deployed frontend service.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
