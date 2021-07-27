# Welcome to the Volkshop Project :wolf:

## Volkshop is an e-commerce platform with a fresh design using Django and SQL

This website implements a complete cart functionality for non registered users, built-in MercadoPago payment flow, On-Sale product system and an UI fully designed on Figma.

# Steps to run the project

1. Clone the repo
2. Install the dependencies using:
    ```
    pip install -r requirements.txt
    ```
3. In the root directory of the project run:
    ```
    python manage.py createsuperuser
    ```
    and complete the data to register an admin user

4. Then do:
    ```
    python manage.py runserver
    ```

5. Go to 127.0.0.1:8000/ to enter the website or 127.0.0.1:8000/admin to enter the admin panel

# TODOs:

- [x] Integrate payment methods (MercadoPago)
- [x] Complete user manage system (Login, Register, Forgot, Reset)
- [ ] Wrap into a RESTful API using DRF
- [ ] Make CRM
