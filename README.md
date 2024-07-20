# IKEA Price Tracking

This repository contains a Python script that tracks the price of an IKEA product and sends an email notification when the price drops. The script runs every 2 hour using GitHub Actions and records the price changes in a JSON file.

## Features

- Tracks the price of an IKEA product.
- Sends an email notification when the price drops.
- Records price changes in a JSON file.
- Runs every 2 hour using GitHub Actions.

## Prerequisites

- Python 3.10 or later
- A Gmail account with an app-specific password for sending email notifications

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/hsayed21/IKEA-Price-Tracking.git
    cd IKEA-Price-Tracking
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up your Gmail account to allow sending emails using an app-specific password. [Follow these instructions to generate an app-specific password](https://support.google.com/accounts/answer/185833).

4. Add your email credentials and recipient email to GitHub Secrets:

- `FROM_ADDRESS`: Your Gmail address.
- `FROM_PASSWORD`: Your app-specific password from Google.
- `TO_ADDRESS`: The email address where you want to receive the notifications.

## Usage

1. To run the script manually, execute:

    ```sh
    python ikea_price.py
    ```

2. The script will check the price of the specified IKEA product and send an email notification if the price has dropped. It will also update the `ikea_price_changes.json` file with the current price and timestamp.

## GitHub Actions

The script is set to run every 2 hour using GitHub Actions. The workflow is defined in `.github/workflows/price_check.yml`.

