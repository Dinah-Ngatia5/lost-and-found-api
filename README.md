# Lost and Found Application

This is a Flask-based web application for managing lost and found items.

## Features

- User authentication (login, registration, password reset)
- Reporting lost items
- Reporting found items
- Commenting on items
- Claiming items
- Offering and receiving rewards
- Admin dashboard for managing items and reports

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository (or download the ZIP file and extract it):

   ```bash
   git clone https://github.com/yourusername/lost-and-found-app.git
   cd lost-and-found-app
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up the environment variables:

   Create a `.env` file in the root directory of the project and add the necessary environment variables. For example:

   ```plaintext
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///site.db
   ```

6. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the Flask development server:

   ```bash
   flask run
   ```

3. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Usage

- Register a new account or login with existing credentials.
- Use the navigation menu to access different features:
  - Report a lost item
  - Report a found item
  - View lost and found reports
  - Claim items
  - Offer or receive rewards
  - Admins can access the admin dashboard for additional management options.

## Contributing

Contributions to the Lost and Found Application are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please contact [Your Name] at [your.email@example.com].
