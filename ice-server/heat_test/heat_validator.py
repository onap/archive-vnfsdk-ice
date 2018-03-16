import logging
import os
import shutil
import sys
import tempfile
import zipfile
from io import StringIO

import pytest
from flask import (request, jsonify, abort, current_app)


class HeatValidator(object):
    """REST service for HEAT templates validation"""

    # Customize messages for pytest exit codes...
    msg = {0: 'OK',
           1: 'Tests failed',
           2: 'Interrupted',
           3: 'Internal error',
           4: 'Usage error',
           5: 'No tests collected'}

    def ping(self):
        return "pong"

    def validate(self):
        """validate the heat template contained in the uploaded zipfile
        by running the ice_validator scripts"""
        logging.info("validate")

        # check if the post request is valid
        if 'file' not in request.files:
            logging.error("invalid request: no file found")
            abort(422, {'status': 1, 'message': 'no file found'})

        try:
            # extract the uploaded archive
            zip_file = request.files['file']
            tmp_dir = tempfile.mkdtemp()
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(tmp_dir)
            zip_ref.close()
            debug = request.args.get('debug')

            # execute the validation scripts with pytest
            if debug == 'true':
                # Save the original stream output, the console basically
                original_output = sys.stdout
                # Assign StringIO so the output is not sent anymore to the console
                sys.stdout = StringIO()
            script_path = current_app.config['ICE_SCRIPT_PATH']
            exit_code = pytest.main([script_path,
                                     '--resultlog=' + tmp_dir + '/result.txt',
                                     '--template-dir', tmp_dir])
            with open(tmp_dir + '/result.txt', 'r') as result_file:
                result = result_file.read()
            if debug == 'true':
                output = sys.stdout.getvalue()
                # close the stream and reset stdout to the original value (console)
                sys.stdout.close()
                sys.stdout = original_output
        except zipfile.BadZipFile:
            logging.exception("invalid file")
            abort(422, {'status': 4, 'message': 'invalid file'})
        except Exception as e:
            logging.exception("server error on file")
            abort(500, {'status': 3, 'message': 'server error'})
        finally:
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)

        result = {'status': exit_code, 'message': self.msg[exit_code], 'result': result}
        if debug == 'true':
            result['debug'] = output

        return jsonify(result), 200 if (exit_code == 0) else 422


class_instance = HeatValidator()
