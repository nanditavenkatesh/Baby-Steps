# Baby Steps

## Vision

**Baby Steps** is an educational application designed to help preschoolers learn how to write alphabets and numbers in an interactive and rewarding way. Our goal is to make learning accessible to all children by combining technology, personalized content, and interactive learning methods to foster independent learning. The app empowers children to become active self-learners, with a focus on making the learning process enjoyable.

## Features

- **User Registration & Login**: Parents or guardians can sign up as new users and login to the platform to manage their child's learning progress.
- **Practice Writing**: Kids can practice writing upper-case alphabets on a digital canvas, with the ability to check their answers using an AI-based verification system.
- **Watch Tutorial**: The app includes video tutorials on how to write each alphabet, making it easy for preschoolers to learn by watching.
- **Attempt Quiz**: Users can attempt a quiz to assess their skills by writing 5 uppercase alphabets, scoring up to 5 points.
- **Administrator Role**: Admin users can add training data to improve the AI model's accuracy.

## Actors and Use Cases

- **Parent/Guardian**: Registers or logs in to manage learning activities for their child.
- **Pre-schooler**: Can watch tutorial videos, practice writing, and take quizzes to test their knowledge.

## Technology Stack

- **Python**: Core programming language used for development.
- **Flask**: Framework for building web applications.
- **Jupyterlab**: Development environment for step-by-step illustration of the analysis process.
- **TensorFlow & Keras**: Libraries for machine learning tasks, used to train and test the handwriting model.
- **Scikit-learn**: For evaluating the accuracy of the handwriting classification using a confusion matrix.
- **NumPy**: For handling high-performance multidimensional array operations.
- **Matplotlib & Seaborn**: Libraries for data visualization.
- **MySQL Workspace**: For storing user account information.

## Project Architecture

- **User Interfaces**: Built using Flask for the backend, with simple HTML forms for login, registration, practice, and tutorial pages.
- **Backend Services**: Flask handles user authentication and interaction with the MySQL database, which stores user credentials and progress.
- **AI Model**: A convolutional neural network (CNN) built using TensorFlow and Keras, trained on user-submitted writing samples, and evaluated using Scikit-learn.

## Pages and Functionality

- **Registration and Login Page**: Users can register with an email, username, and password. They can later login to access the app.
- **Home Page**: Provides access to the following features: Practice, Watch Tutorial, and Attempt Quiz. Admins have access to an additional "Add Data" page.
- **Practice Page**: Allows preschoolers to practice writing uppercase alphabets, compare their writing against the model, and try again if needed.
- **Watch Tutorial Page**: A tutorial for each uppercase alphabet to help children learn how to write.
- **Attempt Quiz Page**: A quiz to evaluate writing skills, where users write 5 alphabets, and the system scores them.
- **Add Data (Admin Only)**: Admins can add new data points to improve the handwriting model.

## Installation and Setup

### Prerequisites
- **Python**: Version 3.x
- **Pycharm or any IDE**
- **JupyterLab**
- **MySQL Workbench**

### Steps to Execute Project
1. **Clone the repository**:
   ```
   git clone https://github.com/nanditavenkatesh/Baby-Steps
   ```
2. **Install required packages**:
   - Use pip to install dependencies:
3. **Setup MySQL Database**:
   - Create a MySQL database and update the credentials in the application code.
4. **Model Training**:
   - Navigate to the `scripts` folder.
   - Open `model_training.ipynb` in JupyterLab and run all cells to train the handwriting model.
5. **Run the Application**:
   - Run the `app.py` file to start the Flask server.
   - Open the link provided in the terminal to access the website.

## Project Demo
- **Demo Video**: [Baby Steps Demo Video](https://github.com/nanditavenkatesh/Baby-Steps/blob/master/BabyStepsVideo.mp4)
- **GitHub Repository**: [Baby Steps GitHub Repository](https://github.com/nanditavenkatesh/Baby-Steps)

## Contributors
- **Aditya Somani**
- **Aditya Kumar**
- **Nandita Venkatesh**
- **Niranchana Shiju**

## Contact
For any inquiries or contributions, please reach out to us via the GitHub repository.

---

We hope Baby Steps provides an engaging and enriching learning experience for preschoolers. Happy learning!
