"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
from flask import Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
from werkzeug.security import check_password_hash
from src.auth import login_required
from src.db import get_db
from src.dnacAPI import *
from datetime import datetime
import json
import pandas
import urllib3


urllib3.disable_warnings()
bp = Blueprint('portal', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def home():
    """
    Home Page back-end functionality
    :return:
    """
    # Check for any initial errors
    error = None
    if 'dnac' not in session:
        error = "ERROR: No DNA-Center instance configured. Please configure on the Settings page."
        flash(error)
        return render_template('portal/home.html', session=session)

    if session['dnac']['token'] == "":
        session['dnac']['token'] = dnac_get_Authorization_Token(session['dnac'])
        session.modified = True
        if session['dnac']['token'] == "":
            error = "ERROR: No DNA-Center Token found. Please check configuration on the Settings page."
            flash(error)
            return render_template('portal/home.html', session=session)

    # Set default state of page
    db = get_db()
    template_list = dnac_get_Available_Templates(session['dnac'])
    session['dnac']['selectedTemplate'] = ""
    # Retrieve Page Data Set
    task_log = db.execute(
        'SELECT t.id, ts, type, description'
        ' FROM tasklog t'
        ' ORDER BY ts DESC'
    ).fetchall()

    # On User Action
    if request.method == 'POST':
        # If a User selected Refresh
        if request.form.get('refresh'):
            session['dnac']['token'] = dnac_get_Authorization_Token(session['dnac'])
            session.modified = True
            return redirect(url_for('portal.home'))
        # If a DNA-Center Template is selected to view
        if request.form.get('template'):
            session['dnac']['selectedTemplate'] = request.form.get('template')
            session.modified = True
            return redirect(url_for('portal.templateDetails'))

    return render_template('portal/home.html', session=session, template_list=template_list, task_log=task_log)


@bp.route('/details', methods=('GET', 'POST'))
@login_required
def templateDetails():
    """
    Back-End to view Template Details
    """
    error = None
    template_Details_Json = dnac_get_Template(session['dnac'])
    template_Details = template_Details_Json.items()
    return render_template('portal/templateDetails.html', session=session, template_Details=template_Details, template_name=template_Details_Json['name'])


@bp.route('/action', methods=('GET', 'POST'))
@login_required
def templateAction():
    """
    Back-End to start the Custom User Action
    """
    error = None
    project_list = dnac_get_Available_Projects(session['dnac'])
    template_list = dnac_get_Available_Templates(session['dnac'])
    device_list = dnac_get_DNAC_Network_Devices(session['dnac'])
    if request.method == 'POST':
        # Collect User Inputs
        session['dnac']['deviceSelections'] = request.form.getlist('selectedDevice')
        session['dnac']['selectedTemplate'] = request.form.get('templateSelection')
        session.modified = True
        return redirect(url_for('portal.templateSetAction'))
    return render_template('portal/templateAction.html', session=session,
                           project_list=project_list, template_list=template_list, device_list=device_list['response'])


@bp.route('/actionSettings', methods=('GET', 'POST'))
@login_required
def templateSetAction():
    """
    Back-End to allowing the User to set Template Params
    """
    error = None
    template_json = dnac_get_Template(session['dnac'])
    template_parameters = template_json['templateParams']
    template_name = template_json['name']

    if request.method == 'POST':
        # TODO: Check if user manually added parameters
        # IF THE USER UPLOADED A PARAM FILE
        site_Csv = request.files['file']
        if site_Csv.filename == '':
            print('No file uploaded...')
        elif site_Csv.filename.endswith('.csv'):
            site_DF = pandas.read_csv(site_Csv)
            site_Params = site_DF.to_json(orient="columns")
            session['templateParams'] = site_Params
            print(site_Params)
            session.modified = True
            return redirect(url_for('portal.templateDeployAction'))
        else:
            error = "ERROR: File must be in CSV format!"
            flash(error)

    return render_template('portal/templateSetAction.html', session=session, template_name=template_name,
                           template_parameters=template_parameters)


@bp.route('/actionDeployment', methods=('GET', 'POST'))
@login_required
def templateDeployAction():
    """
    Back-End to the Deployment of the Template to each selected device.
    # NOTE: THIS IS WHERE THE DEVELOPMENT ON THE PROJECT CURRENTLY IS...
    # An Update to this section will be pushed soon
    """
    error = None
    print("Deployment Starting...")
    for device in session['dnac']['deviceSelections']:
        print('Deploying to {}...'.format(device))
        dnac_deploy_Template(session['dnac'], device, session['dnac']['selectedTemplate'], session['templateParams'], False)
        print('Finished!')
    if request.method == 'POST':
        print()
    return render_template('portal/templateDeployAction.html', session=session)


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """
    Settings Page back-end functionality
    :return:
    """
    # Set default state of page
    error = None
    dnac = {}
    clearPass = {}

    if 'dnac' in session:
        dnac = session['dnac']
    if 'clearPass' in session:
        clearPass = session['clearPass']

    if request.method == 'POST':
        update_dnac = False
        update_clearPass = False
        # Check for any DNA-Center inputs
        if request.form.get('dnac_host') != "":
            dnac["dnac_host"] = request.form.get('dnac_host')
            update_dnac = True
        if request.form.get('dnac_username') != "":
            dnac["dnac_username"] = request.form.get('dnac_username')
            update_dnac = True
        if request.form.get('dnac_password') != "":
            dnac["dnac_password"] = request.form.get('dnac_password')
            update_dnac = True
        if update_dnac:
            session['dnac'] = dnac
            session['dnac']['token'] = ""
            session['dnac']['selectedTemplate'] = ""

        # Check for any DNA-Center inputs
        if request.form.get('corp_Dot1x_cluster') != "":
            clearPass["corp_Dot1x_cluster"] = request.form.get('corp_Dot1x_cluster')
            update_clearPass = True
        if request.form.get('guest_Cluster') != "":
            clearPass["guest_Cluster"] = request.form.get('guest_Cluster')
            update_clearPass = True
        if update_clearPass:
            session['clearPass'] = clearPass

        session.modified = True
        return redirect(url_for('portal.home'))
    return render_template('portal/settings.html', session=session)
