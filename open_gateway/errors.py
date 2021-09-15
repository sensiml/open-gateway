"""Application error handlers."""
from flask import Blueprint, jsonify

errors = Blueprint("errors", __name__)
import logging

logger = logging.getLogger(__name__)


@errors.app_errorhandler(Exception)
def handle_error(error):
    detail = [str(x) for x in error.args]
    status_code = 500
    success = False
    logger.error({"error": {"type": error.__class__.__name__, "detail": detail}})

    return jsonify(detail=detail), status_code
