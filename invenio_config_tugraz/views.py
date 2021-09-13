# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
#
# invenio-config-tugraz is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for TUGRAZ config."""

from os import environ
from typing import Dict

from elasticsearch_dsl.utils import AttrDict
from flask import Blueprint, current_app, redirect, url_for
from flask_babelex import get_locale
from flask.helpers import send_from_directory


def ui_blueprint(app):
    """Blueprint for the routes and resources provided by invenio-config-tugraz."""
    routes = app.config.get("CONFIG_TUGRAZ_ROUTES")

    blueprint = Blueprint(
        "invenio_config_tugraz",
        __name__,
        template_folder="templates",
        static_folder="static",
    )


    blueprint.add_url_rule(routes["guide"], view_func=guide)
    blueprint.add_url_rule(routes["terms"], view_func=terms)
    blueprint.add_url_rule(routes["gdpr"], view_func=gdpr)
    blueprint.add_url_rule(f'{app.config.get("SSL_CERTIFICATE_ROUTE", "/ssl_certificate/")}90A3291E0CB60238D970ACCA2E2CF6A9.txt', view_func=ssl_certificate)

    @blueprint.before_app_first_request
    def rank_higher():
        """Rank this modules blueprint higher than blueprint of security module."""
        blueprints = current_app._blueprint_order
        our_index = None
        security_index = None

        for index, bp in enumerate(blueprints):
            if bp.name == "security":
                security_index = index
            if bp.name == "invenio_config_tugraz":
                our_index = index

        if (security_index is not None) and (our_index > security_index):
            temp = blueprints[security_index]
            blueprints[security_index] = blueprints[our_index]
            blueprints[our_index] = temp

    return blueprint

def ssl_certificate():
    """Verify ownership of server for SSL certificate."""
    return send_from_directory('static/documents', filename='90A3291E0CB60238D970ACCA2E2CF6A9.txt')


def guide():
    """TUGraz_Repository_Guide."""
    locale = get_locale()
    return redirect(url_for('static',
                            filename=f'documents/TUGraz_Repository_Guide_02_{locale}.pdf',
                            _external=True))


def terms():
    """Terms_And_Conditions."""
    locale = get_locale()
    return redirect(url_for('static',
                            filename=f'documents/TUGraz_Repository_Terms_And_Conditions_{locale}.pdf',
                            _external=True))


def gdpr():
    """General_Data_Protection_Rights."""
    locale = get_locale()
    return redirect(url_for('static',
                            filename=f'documents/TUGraz_Repository_General_Data_Protection_Rights_{locale}.pdf',
                            _external=True))
