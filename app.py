from flask import Flask, render_template, request, redirect
import gspread, os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("RegistrationData").sheet1

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    email_address = request.form['email_address']
    num_participants = int(request.form['num_participants'])
    num_greater_than_13 = int(request.form['num_greater_than_13'])
    num_between_6_and_12 = int(request.form['num_between_6_and_12'])
    num_below_6 = int(request.form['num_below_6'])

    total_cost = 110 * num_greater_than_13 + 65 * num_between_6_and_12

    # Append data to Google Sheets
    sheet.append_row([first_name, last_name, phone_number, email_address, num_participants,
                      num_greater_than_13, num_between_6_and_12, num_below_6, total_cost])

    return f"Total Cost: ${total_cost}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

