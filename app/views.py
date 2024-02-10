import time

from flask import Blueprint, jsonify, request

from app import db

from . import utils as ut
from .models import Domain

main = Blueprint("main", __name__)


@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"status": "No matching route for request"}), 404


@main.route("/visited_domains", methods=["GET"])
def get_users():
    args = request.args.to_dict()

    arg_from = args.get("from", None)

    arg_to = args.get("to", None)

    if arg_from:
        if not arg_from.isdigit():
            return jsonify({"status": f"Parameter from is not digit: {arg_from}"}), 400

        arg_from = int(arg_from)
        if arg_from > ut.MAX_SQLITE_INT:
            arg_from = ut.MAX_SQLITE_INT

    if arg_to:
        if not arg_to.isdigit():
            return jsonify({"status": f"Parameter to is not digit: {arg_to}"}), 400

        arg_to = int(arg_to)
        if arg_to > ut.MAX_SQLITE_INT:
            arg_to = ut.MAX_SQLITE_INT

    if arg_from and arg_to and arg_to < arg_from:
        return (
            jsonify(
                {
                    "status": f"Parameter from cannot be greater than parameter to: {arg_from} > {arg_to}"
                }
            ),
            400,
        )

    result = {"domains": [], "status": "ok"}

    domains = (
        Domain.query.filter(
            Domain.datetime >= arg_from if arg_from else True,
            Domain.datetime <= arg_to if arg_to else True,
        )
        .order_by(Domain.datetime)
        .all()
    )

    for domain in domains:
        link = domain.link
        domain = ut.search_domain(link)
        if domain and domain not in result["domains"]:
            result["domains"].append(domain)

    return jsonify(result), 200


@main.route("/visited_links", methods=["POST"])
def create_user():
    current_time = int(time.time())

    data = request.get_json()

    if "links" not in data:
        return jsonify({"status": "The links parameter is not specified"}), 400

    visited_links = data["links"]

    if not isinstance(visited_links, list):
        return jsonify({"status": f"Parameter links is not list: {visited_links}"}), 400

    need_commit = False
    incorrect_links = []
    for link in visited_links:
        domain = ut.search_domain(link)
        if domain:
            db_domain = Domain(link=link, datetime=current_time)
            db.session.add(db_domain)
            need_commit = True
        else:
            incorrect_links.append(link)

    if need_commit:
        db.session.commit()

    if len(incorrect_links) > 0:
        return jsonify(
            {
                "status": f'Incorrect links were ignored in the request: {", ".join(incorrect_links)}'
            }
        ), (207 if need_commit else 400)
    else:
        return jsonify({"status": "ok"}), 200
