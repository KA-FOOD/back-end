import os
from flask import Flask, request, render_template, redirect, url_for, session, Response
import pdfplumber
import re
import csv
import io
from flask import Blueprint, render_template

dashboard_blueprint = Blueprint("dashboard", __name__)

app = Flask(__name__)
app.secret_key = "13cfc1ebd3ba359fce7bb3ccf5dd37862938d149d53d44c7"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@dashboard_blueprint.route("/")
def reception():
    return render_template("dashboard.html")