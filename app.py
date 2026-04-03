from flask import Flask, request, render_template, redirect, url_for, session
import smtplib
import random

app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # सुरक्षित ठेव

# Home Page - Form
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        otp = str(random.randint(100000, 999999))
        session["otp"] = otp

        # ईमेल पाठवण्यासाठी SMTP
        sender_email = "तुझा_ईमेल@gmail.com"
        sender_password = "तुझं_AppPassword"  # Gmail App Password वापर
        subject = "तुझा OTP"
        message = f"तुझा OTP आहे: {otp}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, f"Subject:{subject}\n\n{message}")
            server.quit()
        except Exception as e:
            return f"Error: {e}"

        return redirect(url_for("verify"))

    return render_template("form.html")

# OTP Verify Page
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form.get("otp")
        if user_otp == session.get("otp"):
            return "✅ OTP Verify झाला! फॉर्म सबमिट यशस्वी."
        else:
            return "❌ OTP चुकीचा आहे. पुन्हा प्रयत्न करा."

    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)
