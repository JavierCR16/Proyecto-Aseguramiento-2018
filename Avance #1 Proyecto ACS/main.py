from flask import Flask, render_template, request,session,redirect, url_for

app = Flask(__name__)
app.secret_key = "something-from-os.urandom(24)"

