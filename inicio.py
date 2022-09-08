from flask import Flask, render_template, request,redirect, session, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import *
from prueba import Nav
from prueba.elements import *
from dominate.tags import img
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from flask_paginate import Pagination, get_page_args
from bd import conn, sch
import pyodbc
import urllib.parse 
import sys
import os
# import win32api
# import win32security
from cryptography.fernet import Fernet
from functools import wraps
from passlib.hash import sha256_crypt
import json
import requests
from werkzeug.utils import secure_filename
import pandas as pd
from models.reportconfig import ReportConfig
from models.embedtoken import EmbedToken
from models.embedconfig import EmbedConfig
from models.embedtokenrequestbody import EmbedTokenRequestBody
from flask import current_app as abort
import msal
from sqlalchemy import create_engine
import re

def get_access_token (app,session):
        with conn.cursor() as cursor:
                result=cursor.execute("select User_PBI_Email, User_PBI_Password from dbo.USERS_POWERBI where User_PBI_ID_Users =?", session)
                data = cursor.fetchone()

                response = None
                try:
                    if app.config['AUTHENTICATION_MODE'].lower() == 'masteruser':

                        # Create a public client to authorize the app with the AAD app
                        clientapp = msal.PublicClientApplication(app.config['CLIENT_ID'], authority=app.config['AUTHORITY'])
                        accounts = clientapp.get_accounts(username=data[0])

                        if accounts:
                            # Retrieve Access token from user cache if available
                            response = clientapp.acquire_token_silent(app.config['SCOPE'], account=accounts[0])

                        if not response:
                            # Make a client call if Access token is not available in cache
                            response = clientapp.acquire_token_by_username_password(data[0], data[1], scopes=app.config['SCOPE'])     

                    try:
                        return response['access_token']
                    except KeyError:
                        raise Exception(response['error_description'])

                except Exception as ex:
                    raise Exception('Error retrieving Access token\n' + str(ex))    



def get_embed_params_for_single_report( app,session,workspace_id, report_id, additional_dataset_id=None):

        report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}'       
        api_response = requests.get(report_url, headers=get_request_header(app,session))

        if api_response.status_code != 200:
            abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        api_response = json.loads(api_response.text)
        report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
    
        dataset_ids = [api_response['datasetId']]
    
        if additional_dataset_id is not None:
            dataset_ids.append(additional_dataset_id)

        embed_token = get_embed_token_for_single_report_single_workspace(app,session,report_id, dataset_ids, workspace_id)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
        return json.dumps(embed_config.__dict__)

def get_embed_token_for_single_report_single_workspace( app,session,report_id, dataset_ids, target_workspace_id=None):

        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        request_body.reports.append({'id': report_id})

        if target_workspace_id is not None:
            request_body.targetWorkspaces.append({'id': target_workspace_id})

        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=get_request_header(app,session))

        if api_response.status_code != 200:
            abort(api_response.status_code, description=f'Error while retrieving Embed token\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        api_response = json.loads(api_response.text)
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token


def all_workshop(app,session):
        url='https://api.powerbi.com/v1.0/myorg/groups'
        api_response = requests.get(url, headers=get_request_header(app,session))
        if api_response.status_code != 200:
            abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        api_response = json.loads(api_response.text)
        api_response['value']
        
        return (api_response['value'])


def all_workshop2(session):
         print(session)
         with conn.cursor() as cursor:
                cursor.execute("SELECT PBI_ID_WORKSPACE, PBI_NAME_WORKSPACE, PBI_TYPE FROM "+sch+".META_CRUD_POWERBI where PBI_ID_USER = ? ", session)
                camps = cursor.fetchall()
                workspace=[]
                for i in camps:
                    dict1={'id':i[0], 'name':i[1], 'type':i[2]}
                    workspace.append(dict1)
                return(workspace)


def all_reports( app,session,workshop):
    reportes=[]
    print(session)
    print(workshop)
    
    for i in workshop:
        if i['type'] == 'Workspace':
    
            url=f"https://api.powerbi.com/v1.0/myorg/groups/{i['id']}/reports"
            api_response = requests.get(url, headers=get_request_header(app,session))
            if api_response.status_code != 200:
                abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

            api_response = json.loads(api_response.text)
            
            
            for a in api_response['value']:

                dic2={'id_workshop':i['id'],'id_report':a['id'], 'name_report':a['name'] }
                reportes.append(dic2)


    return (reportes)

def get_request_header(app,session):

    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token(app,session)}