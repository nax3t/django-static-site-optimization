# Image Optimization Automation with Cloudinary

## Usage

Running an existing Django app locally involves similar steps across different operating systems but with some notable differences, especially when setting up the environment and dealing with system-specific commands. Below is a detailed guide.

### Prerequisites

1. **Python**: Ensure you have Python installed. Django supports Python 3.6 and above.
2. **pip**: This is Python's package installer. It usually comes with Python.
3. **Virtual Environment**: Highly recommended for Python projects to manage dependencies.

### Windows vs. Mac/Linux Differences

- **Command Line Interface**: Windows uses Command Prompt or PowerShell, while Mac/Linux uses Terminal.
- **Path Variables**: Sometimes, you may need to add Python or other executables to your system's PATH. The process differs between Windows and Mac/Linux.
- **Commands**: Some commands differ slightly, e.g., activating a virtual environment.

### Steps to Set up and Run the App Locally

#### 1. Clone the Repository
First, clone the repository containing the Django project to your local machine. Use Git for this purpose.

```bash
$ git clone https://github.com/nax3t/django-static-site-optimization.git
$ cd django-static-site-optimization
```

#### 2. Set up a Virtual Environment

- **Windows**

```bash
$ python -m venv myenv
$ myenv\Scripts\activate
```

- **Mac/Linux**

```bash
$ python3 -m venv myenv
$ source myenv/bin/activate
```

#### 3. Install Dependencies

Ensure you are in the project root (where `requirements.txt` is located) and run:

```bash
$ pip install -r requirements.txt
```

#### 4. Set environment variables

DEBUG should be True in development, False in production.
SECRET_KEY can be generated using the following command:
```bash
$ python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

You can rename the `example.env` file in the project root directory to be `.env` then set your environment variables there.

#### 5. Run Migrations

Apply the database migrations to set up your database schema:

```bash
$ python manage.py migrate
```

#### 6. Run the Development Server

Finally, run the development server:

```bash
python manage.py runserver
```

Your Django app should now be accessible from `http://127.0.0.1:8000/` or `http://localhost:8000/`.

#### 7. Sign up for Cloudinary
Visit [Cloudinary](https://cloudinary.com) and sign up for a free account. You can find your Cloudname, API Key, and API Secret in the Dashboard after logging in.

#### 8. Test the app

- [Watch a video walkthrough](https://www.youtube.com/watch?v=v3DcFhCxoX8)
- Get started by uploading a zip file of your static website. Be sure to include your [Cloudinary](https://www.cloudinary.com) credentials.

#### Tips and Troubleshooting:

- Ensure all the necessary environment variables are set
- Check the Django app settings for any specified host or port changes.
- Make sure your Python and pip are correctly installed and accessible via your terminal or command prompt.
- Always activate your virtual environment before working on your project to isolate dependencies.
